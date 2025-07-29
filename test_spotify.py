#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'JukeBox.settings')
django.setup()

from search.spotify_service import SpotifyService

def test_spotify():
    print("Testing Spotify Service...")
    
    # Initialize the service
    spotify_service = SpotifyService()
    
    if not spotify_service.sp:
        print("ERROR: Spotify client not initialized!")
        return
    
    print("Spotify client initialized successfully!")
    
    # Test getting trending albums
    print("Fetching trending albums...")
    trending_albums = spotify_service.get_trending_albums(limit=3)
    
    if trending_albums:
        print(f"Found {len(trending_albums)} trending albums:")
        for i, album in enumerate(trending_albums):
            print(f"{i+1}. {album['title']} by {album['artist']} ({album['year']})")
            print(f"   Cover: {album['cover']}")
    else:
        print("No trending albums found or error occurred.")

if __name__ == "__main__":
    test_spotify()
