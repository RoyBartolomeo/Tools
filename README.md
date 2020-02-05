# Tools

A handful of command line tools that interact with various APIs that I've written.

## ssltest.py

This program interacts with the Qualys SSL-Labs API to perform SSL tests on endpoints. The program prompts the user for a site analyze, provides on-going status of the scan, and outputs each IP Address and Host for the website with their respective SSL test grade. The user then has to option to request a detailed report from the scan and the detailed report will be written to disk.

## playlist.py 

This program interacts with the YouTube V3 API to search videos and create a playlist on the authenticated user's account based on the search results. The user is presented a variety of options throughout the program, including what to search for, how many results are wanted, how long the videos should be, the name of the playlist to create and playlist details.

To get OAUTH credentials setup for the YouTube account, follow the instructions here https://developers.google.com/youtube/registering_an_application . The client secrets need to be exported in json format, renamed to client_secret.json and saved to the directory containing the program.

This requires an API key and OAUTH client credentials.

## discogs.py

This program calls the Discogs Search API to find Albums, Compilations, and Mixes for a particular artist. The results are displayed sorted by the year the music was released. This program runs continuously until the user enters 'quit'.

This requires an API key.

## movie_review.py

This program calls the New York Times Movie Review API and returns the NYT staff critics picks for a defined date range. The user provides either an invidual date to search from or a range of dates to search between. The output contains Title, Release Date, and Summary of the movie.

This requires an API key.

## daily_playlist.py

This program interacts with the YouTube V3 API earches youtube Channels for content posted in the past 24 hours and creates a playlist of the videos found on the authenticated users account. I schedule this to run every 24 hours on my host machine to create a daily feed of videos from sources I'm interested. The tool is currently coded to pull videos from news sources but can be configured with any Youtube Channel ID.

This requires an API key and OAUTH client credentials.
