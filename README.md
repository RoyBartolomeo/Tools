# Tools

Python command line tools that interact with various APIs that I've written.

## daily_playlist.py

This program interacts with the YouTube V3 API to search YouTube Channels for content posted in the past 24 hours and creates a playlist of the videos found on the authenticated user account. I schedule this to run every 24 hours on my host machine to create a daily feed of videos from sources I'm interested in. The tool is currently coded to pull videos from various news sources but can be configured with any YouTube Channel IDs.

This requires an API key and OAUTH client credentials.

## discogs.py

This program calls the Discogs Search API to find Albums, Compilations, and Mixes of a specified artist. The results are displayed sorted by the year the music was released. This program runs continuously until the user enters 'quit'.

This requires an API key.

## movie_review.py

This program calls the New York Times Movie Review API and returns the NYT staff critics picks for a defined date range. The user provides either an invidual date to search from or a range of dates to search between. The output contains Title, Release Date, and Summary of the movie.

This requires an API key.

## playlist.py 

This program interacts with the YouTube V3 API to search videos and create a playlist on the authenticated user account based on the search results. The user specifies search terms including search query, number of results, video length, new playlist name and playlist details.

This requires an API key and OAUTH client credentials.

## ssltest.py

This program interacts with the Qualys SSL-Labs API to perform SSL tests on endpoints. The program prompts the user for a site to analyze, provides on-going status of the scan, and outputs each IP Address and Host for the website with their respective SSL test grade. The user then has to option to request a detailed report from the scan which will be written to disk.
