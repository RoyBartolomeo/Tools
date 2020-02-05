#!/usr/bin/python3

# Author: Roy B
# This builds a playlist on the authenticated user account based on search parameters
# provided by the user while running.

import os

import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage


# Google code for OAuth. This requires the client secrets file downloaded from the dev api console
    
CLIENT_SECRETS_FILE = 'client_secret.json'
DEVELOPER_KEY = 'YOUR DEVELOPER KEY'
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
    
# Authorize the request and store authorization credentials. If the credential file doesn't exist it will
# open a link to authorize the account. 
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

  