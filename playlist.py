#!/usr/bin/python3

# This code sample creates a private playlist in the authorizing user's
# YouTube channel.
# Usage:
#   python playlist_updates.py

import os
import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret. You can acquire an OAuth 2.0 client ID and client secret from
# the {{ Google Cloud Console }} at
# {{ https://cloud.google.com/console }}.
# Please ensure that you have enabled the YouTube Data API for your project.
# For more information about using OAuth2 to access the YouTube Data API, see:
#   https://developers.google.com/youtube/v3/guides/authentication
# For more information about the client_secrets.json file format, see:
#   https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
    
CLIENT_SECRETS_FILE = 'client_secret.json'
DEVELOPER_KEY = 'YOUR KEY HERE'

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account.
SCOPES = ['https://www.googleapis.com/auth/youtube']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

def youtube_search():
  youtube = build(API_SERVICE_NAME, API_VERSION,
    developerKey=DEVELOPER_KEY)

  # Call the search.list method to retrieve results matching the specified
  # query term.
  search_response = youtube.search().list(
    q=input('Search: '),
    part='id,snippet',
    maxResults=input('Max Results: '),
    type='video',
    safeSearch='none',
    videoDuration=input('Length - any|long|medium|short: ')
  ).execute()

  videos = []

  # Add each result to the appropriate list, and then display the lists of
  # matching videos, channels, and playlists.
  for search_result in search_response.get('items', []):
    videos.append(search_result['id']['videoId'])

  return(videos)
    
# Authorize the request and store authorization credentials.
def get_authenticated_service():
  credential_path = os.path.join('./', 'credential_sample.json')
  store = Storage(credential_path)
  credentials = store.get()
  if not credentials or credentials.invalid:
    flow = client.flow_from_clientsecrets(CLIENT_SECRETS_FILE, SCOPES)
    credentials = tools.run_flow(flow, store)
  return build(API_SERVICE_NAME, API_VERSION, credentials=credentials)

def add_playlist(youtube):
  
  body = dict(
    snippet=dict(
      title=input('Playlist Name: '),
      description=input('Playlist Description: ')
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

def add_video(youtube):

    for i in range(len(videos)):
        request = youtube.playlistItems().insert(
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

  youtube = get_authenticated_service()

  try:       
    videos = youtube_search()
    playlistId = add_playlist(youtube)    
    add_video(youtube)
    print('Playlist Created')

  except HttpError as error:
    print(error)

  