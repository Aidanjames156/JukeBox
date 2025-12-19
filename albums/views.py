
from django.shortcuts import render, redirect
from search.spotify_service import SpotifyService
import logging
from .forms import RatingForm
from .models import Rating
from django.contrib import messages
from django.contrib.auth.decorators import login_required

logger = logging.getLogger(__name__)

def album_detail(request, album_id):
    """Album detail page with rating/review support"""
    try:
        spotify_service = SpotifyService()
        album = spotify_service.get_album_details(album_id)

        # Get all reviews for this album
        reviews = Rating.objects.filter(album_id=album_id).select_related('user').order_by('-created_at')

        # Handle rating form
        if request.user.is_authenticated:
            try:
                user_rating = Rating.objects.get(user=request.user, album_id=album_id)
            except Rating.DoesNotExist:
                user_rating = None
        else:
            user_rating = None

        if request.method == 'POST' and request.user.is_authenticated:
            form = RatingForm(request.POST, instance=user_rating)
            if form.is_valid():
                rating_obj = form.save(commit=False)
                rating_obj.user = request.user
                rating_obj.album_id = album_id
                rating_obj.save()
                messages.success(request, 'Your rating and review have been saved!')
                return redirect('album_detail', album_id=album_id)
        else:
            form = RatingForm(instance=user_rating)

        if album:
            context = {
                'album': album,
                'tracks': album.get('tracks', []),
                'related_albums': spotify_service.get_related_albums(album_id, limit=6),
                'form': form,
                'reviews': reviews,
                'user_rating': user_rating,
            }
            return render(request, 'albums/album_detail.html', context)
        else:
            context = {'error': 'Album not found'}
            return render(request, 'albums/album_detail.html', context)

    except Exception as e:
        logger.error(f"Error fetching album details for {album_id}: {e}")
        context = {
            'album': get_mock_album_detail(album_id),
            'tracks': get_mock_tracks(),
            'related_albums': [],
            'form': None,
            'reviews': [],
            'user_rating': None,
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
