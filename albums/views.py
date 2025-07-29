from django.shortcuts import render
from search.spotify_service import SpotifyService
import logging

logger = logging.getLogger(__name__)

def album_detail(request, album_id):
    """Album detail page"""
    try:
        # Try to get album details from Spotify
        spotify_service = SpotifyService()
        album = spotify_service.get_album_details(album_id)
        
        if album:
            context = {
                'album': album,
                'tracks': album.get('tracks', []),
                'related_albums': spotify_service.get_related_albums(album_id, limit=6)
            }
            return render(request, 'albums/album_detail.html', context)
        else:
            # Album not found
            context = {'error': 'Album not found'}
            return render(request, 'albums/album_detail.html', context)
            
    except Exception as e:
        logger.error(f"Error fetching album details for {album_id}: {e}")
        # Fallback to mock data
        context = {
            'album': get_mock_album_detail(album_id),
            'tracks': get_mock_tracks(),
            'related_albums': []
        }
        return render(request, 'albums/album_detail.html', context)


def get_mock_album_detail(album_id):
    """Fallback mock album detail data"""
    return {
        'id': album_id,
        'title': 'Sample Album Title',
        'artist': 'Sample Artist',
        'year': '2024',
        'cover': 'https://via.placeholder.com/400x400/FF6B6B/FFFFFF?text=Album+Cover',
        'spotify_url': '#',
        'total_tracks': 12,
        'album_type': 'album',
        'genres': ['Rock', 'Alternative'],
        'duration': '45:30',
        'description': 'This is a sample album description. In a real implementation, this would contain detailed information about the album.',
        'release_date': '2024-01-15',
        'label': 'Sample Records',
        'popularity': 85,
    }


def get_mock_tracks():
    """Fallback mock track data"""
    return [
        {'name': 'Track 1', 'duration': '3:45', 'track_number': 1},
        {'name': 'Track 2', 'duration': '4:12', 'track_number': 2},
        {'name': 'Track 3', 'duration': '3:28', 'track_number': 3},
        {'name': 'Track 4', 'duration': '5:01', 'track_number': 4},
        {'name': 'Track 5', 'duration': '3:34', 'track_number': 5},
    ]
