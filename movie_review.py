#!/usr/bin/env python3
import requests, json, sys

results = []

def getReviews():
    date = input("Enter date range or individual date to search from (YYYY-MM-DD;YYYY-MM-DD): ")

    offset = 0
    url = 'https://api.nytimes.com/svc/movies/v2/reviews/search.json?api-key=YOURKEYHERE&critics-pick=Y&opening-date={}&offset={}'.format(date, offset) 
    response = requests.get(url)
    response.raise_for_status()  
    data = json.loads(response.text)
    for i in range(len(data['results'])):
        text = 'Title: ' + str(data['results'][i]['display_title']) + '\nRelease Date: ' + str(data['results'][i]['opening_date']) + '\nSummary: ' + str(data['results'][i]['summary_short']) + '\n\n'
        results.append(text)

    while True:
        if data['has_more'] == True:
            offset += 20
            url = 'https://api.nytimes.com/svc/movies/v2/reviews/search.json?api-key=YOURKEYHERE&critics-pick=Y&opening-date={}&offset={}'.format(date, offset)   
            response = requests.get(url)
            response.raise_for_status()  
            data = json.loads(response.text)
            for i in range(len(data['results'])):
                text = 'Title: ' + str(data['results'][i]['display_title']) + '\nRelease Date: ' + str(data['results'][i]['opening_date']) + '\nSummary: ' + str(data['results'][i]['summary_short']) + '\n\n'
                results.append(text)
            
        else:
            break

    print('\nTotal Movies: ' + str(len(results)) + '\n')
    print(*results, sep = "\n")

if __name__ == "__main__":
    getReviews()