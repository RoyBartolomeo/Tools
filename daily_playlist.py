#!/usr/bin/python3

# Author: Roy B
# This searches youtube Channels for content posted in the
# past 24 hours and creates a playlist of the videos found
# on the authenticated users account.

import os

from pathlib import Path
from datetime import datetime, timedelta
import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

#set the time to search for videos created in the last 24 hours
date = datetime.today() - timedelta(days = 1)

# Channel IDs for: WSJ, NYT, FT, Economist, Atlantic, Quartz
channels = ['UCK7tptUDHh-RYDsdxO1-5QQ', 'UCqnbDFdCpuN8CMEg0VuEBqA', 'UCoUxsWakJucWg46KW5RsvPw',
    'UC0p5jTq6Xx_DosDFxVXnWaQ', 'UCK0z0_5uL7mb9IjntOKi5XQ', 'UC9f78Z5hgtDt0n8JWyfBk8Q']

# Google code for OAuth. This requires the client secrets file downloaded from the dev api console    
CLIENT_SECRETS_FILE = Path('YOUR/PATH/client_secret.json')
DEVELOPER_KEY = 'YOUR DEVELOPER KEY'
SCOPES = ['https://www.googleapis.com/auth/youtube']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

videos = []

# Call the Search API and return a list of video IDs
def youtube_search():
  youtube = build(API_SERVICE_NAME, API_VERSION,
    developerKey=DEVELOPER_KEY)

  # Call the search.list method to retrieve results matching the specified
  # query term.
  search_response = youtube.search().list(
    part='id,snippet',
    channelId=channel,
    publishedAfter=str(date.isoformat('T') + 'Z'), #RFC 3339 format
    type='video',
    safeSearch='none'
  ).execute()

  # Append return values to the videos list
  for search_result in search_response.get('items', []):
    videos.append(search_result['id']['videoId'])

  return(videos)
    
# Authorize the request and store authorization credentials. If the credential file doesn't exist it will
# open a link to authorize the account. 
def get_authenticated_service():
  credential_path = Path('YOUR/PATH/credential_sample.json')
  store = Storage(credential_path)
  credentials = store.get()
  if not credentials or credentials.invalid:
    flow = client.flow_from_clientsecrets(CLIENT_SECRETS_FILE, SCOPES)
    credentials = tools.run_flow(flow, store)
  return build(API_SERVICE_NAME, API_VERSION, credentials=credentials)

# Add a new playlist to the user account and return the playlist ID
def add_playlist(youtube):
  body = dict(
    snippet=dict(
      title=date.strftime('%x'),
      description='Recent News'
    ),
    status=dict(
      privacyStatus='public'
    ) 
  ) 
    
  playlists_insert_response = youtube.playlists().insert(
    part='snippet,status',
    body=body
  ).execute()

  return(playlists_insert_response['id'])

# Add videos to the user playlist
def add_video(user):
    for i in range(len(videos)):
        request = user.playlistItems().insert(
            part="snippet",
            body={
            "snippet": {
                "playlistId": playlistId,
                "position": i,
                "resourceId": {
                "kind": "youtube#video",
                "videoId": videos[i]
                }
            }
            }
        )
        request.execute()

if __name__ == '__main__':  
    user = get_authenticated_service()

    try:
        for channel in channels:       
            videos = youtube_search()
        playlistId = add_playlist(user)    
        add_video(user)
        print('Playlist Created')

    except HttpError as error:
        print(error)

  