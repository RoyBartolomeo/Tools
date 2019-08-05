#!/usr/bin/env python3
import requests, json, sys, re

def getReleases():
    albums = []
    title = []
    results = []

    text = input("Artist to search: ")
    if text == 'quit':
        print('Done')
        sys.exit()

    url = 'https://api.discogs.com/database/search?artist={}&format=Album&per_page=100'.format(text)
    headers = {'User-Agent': '"MunsonDiscog/1.0"', 'Authorization':'Discogs token=YOUR TOKEN HERE'}
    response = requests.get(url, headers = headers)
    response.raise_for_status()

    albumData = json.loads(response.text)
    for i in range(len(albumData['results'])):
        try:
            if (albumData['results'][i]['title']) not in title and (albumData['results'][i]['master_id']) != 0:
                titles = re.sub('^.*?- ', '', (albumData['results'][i]['title']))
                albums.append((titles, albumData['results'][i]['year'], 'Album'))
                title.append((albumData['results'][i]['title']))
        except KeyError:
            continue

    url = 'https://api.discogs.com/database/search?artist={}&format=Mixed&per_page=100'.format(text)
    headers = {'User-Agent': '"MunsonDiscog/3.0"', 'Authorization':'Discogs token=YOUR TOKEN HERE'}
    response = requests.get(url, headers = headers)
    response.raise_for_status()
    mixData = json.loads(response.text)
    for i in range(len(mixData['results'])):
        try:
            if (mixData['results'][i]['title']) not in title:
                titles = re.sub('^.*?- ', '', (mixData['results'][i]['title']))
                albums.append((titles, mixData['results'][i]['year'], 'Mix'))
                title.append((mixData['results'][i]['title']))
        except KeyError:
            continue

    url = 'https://api.discogs.com/database/search?artist={}&format=Compilation&per_page=100'.format(text)
    headers = {'User-Agent': '"MunsonDiscog/3.0"', 'Authorization':'Discogs token=YOUR TOKEN HERE'}
    response = requests.get(url, headers = headers)
    response.raise_for_status()
    compData = json.loads(response.text)
    for i in range(len(compData['results'])):
        try:
            if (compData['results'][i]['title']) not in title:
                titles = re.sub('^.*?- ', '', (compData['results'][i]['title']))
                albums.append((titles, compData['results'][i]['year'], 'Comp'))
                title.append((compData['results'][i]['title']))
        except KeyError:
            continue

    master_list = list(set(albums))
    if not master_list:
        print('No Results Found')

    for x,y,z in master_list:
        output = 'Released: ' + y + ' | Title: ' + x + ' | ' + z
        results.append(output)

    results.sort(reverse = True)
    print(*results, sep = "\n")

if __name__ == "__main__":
    while True:
        getReleases()