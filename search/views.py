from django.shortcuts import render
from django.http import JsonResponse
from .spotify_service import SpotifyService
import logging

logger = logging.getLogger(__name__)

# Create your views here.
def search_albums(request):
    """Main search page"""
    context = {}
    
    try:
        # Get trending albums for the search page
        spotify_service = SpotifyService()
        trending_albums = spotify_service.get_trending_albums(limit=12)
        context['trending_albums'] = trending_albums
    except Exception as e:
        logger.error(f"Error fetching trending albums for search page: {e}")
        # Provide fallback data if Spotify fails
        context['trending_albums'] = []
    
    return render(request, 'search/search.html', context)

def search_results(request):
    """Handle search results - both regular and AJAX requests"""
    query = request.GET.get('q', '')
    results = []
    
    if query:
        try:
            # Use Spotify API to search for albums
            spotify_service = SpotifyService()
            spotify_results = spotify_service.search_albums(query, limit=20)
            
            # Convert Spotify results to our format
            for album in spotify_results:
                results.append({
                    'id': album['id'],
                    'title': album['title'],
                    'artist': album['artist'],
                    'year': album['year'],
                    'cover': album['cover'],
                    'spotify_url': album['spotify_url'],
                    'total_tracks': album['total_tracks'],
                    'album_type': album['album_type'],
                    'genres': album['genres'],
                    'rating': 0,  # Default rating, can be customized later
                })
                
        except Exception as e:
            logger.error(f"Error searching albums: {e}")
            # Fallback to mock data if Spotify fails
            results = get_mock_results(query)
    
    # If it's an AJAX request, return JSON
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'results': results,
            'query': query,
            'count': len(results)
        })
    
    # Otherwise render the template
    context = {
        'results': results,
        'query': query,
        'result_count': len(results)
    }
    return render(request, 'search/results.html', context)

def get_mock_results(query):
    """Fallback mock data if Spotify API fails"""
    return [
        {
            'id': 'mock1',
            'title': f'Album containing "{query}" - 1',
            'artist': 'Artist Name 1',
            'year': '2023',
            'cover': 'https://via.placeholder.com/300x300/FF6B6B/FFFFFF?text=Album+1',
            'spotify_url': '#',
            'total_tracks': 12,
            'album_type': 'album',
            'genres': ['Rock', 'Alternative'],
            'rating': 4.5,
        },
        {
            'id': 'mock2',
            'title': f'Album containing "{query}" - 2',
            'artist': 'Artist Name 2',
            'year': '2022',
            'cover': 'https://via.placeholder.com/300x300/4ECDC4/FFFFFF?text=Album+2',
            'spotify_url': '#',
            'total_tracks': 10,
            'album_type': 'album',
            'genres': ['Pop', 'Electronic'],
            'rating': 4.0,
        },
        {
            'id': 'mock3',
            'title': f'Album containing "{query}" - 3',
            'artist': 'Artist Name 3',
            'year': '2024',
            'cover': 'https://via.placeholder.com/300x300/45B7D1/FFFFFF?text=Album+3',
            'spotify_url': '#',
            'total_tracks': 8,
            'album_type': 'album',
            'genres': ['Hip Hop', 'R&B'],
            'rating': 3.5,
        }
    ]