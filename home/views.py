from django.shortcuts import render
from django.http import HttpResponse
from search.spotify_service import SpotifyService
import logging

logger = logging.getLogger(__name__)

# Create your views here.
def home_start(request):
    # Get trending albums from Spotify
    spotify_service = SpotifyService()
    trending_albums = []
    
    try:
        trending_albums = spotify_service.get_trending_albums(limit=12)
        print(f"Successfully retrieved {len(trending_albums)} trending albums")
        if trending_albums:
            print(f"First album: {trending_albums[0]['title']} by {trending_albums[0]['artist']}")
    except Exception as e:
        logger.error(f"Error fetching trending albums: {e}")
        print(f"Error fetching trending albums: {e}")
        # Fallback to empty list if API fails
        trending_albums = []
    
    context = {
        'trending_albums': trending_albums
    }
    
    return render(request, 'index.html', context)