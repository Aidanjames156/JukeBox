import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class SpotifyService:
    def __init__(self):
        """Initialize Spotify client with app credentials"""
        try:
            client_credentials_manager = SpotifyClientCredentials(
                client_id=settings.SPOTIFY_CLIENT_ID,
                client_secret=settings.SPOTIFY_CLIENT_SECRET
            )
            self.sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        except Exception as e:
            logger.error(f"Failed to initialize Spotify client: {e}")
            self.sp = None

    def search_albums(self, query, limit=20):
        """
        Search for albums using Spotify API
        
        Args:
            query (str): Search query
            limit (int): Number of results to return (max 50)
            
        Returns:
            list: List of album dictionaries
        """
        if not self.sp:
            logger.error("Spotify client not initialized")
            return []
            
        try:
            # Search for albums
            results = self.sp.search(q=query, type='album', limit=limit)
            albums = []
            
            for album in results['albums']['items']:
                # Get album details
                album_data = {
                    'id': album['id'],
                    'title': album['name'],
                    'artist': ', '.join([artist['name'] for artist in album['artists']]),
                    'year': album['release_date'][:4] if album['release_date'] else 'Unknown',
                    'cover': album['images'][0]['url'] if album['images'] else None,
                    'spotify_url': album['external_urls']['spotify'],
                    'total_tracks': album['total_tracks'],
                    'album_type': album['album_type'],
                    'genres': [],  # Genres are not available in album search, need separate call
                    'rating': 0,  # We'll handle ratings in our own system
                }
                
                # Try to get additional album details for genres
                try:
                    album_details = self.sp.album(album['id'])
                    album_data['genres'] = album_details.get('genres', [])
                except:
                    pass
                    
                albums.append(album_data)
                
            return albums
            
        except Exception as e:
            logger.error(f"Error searching albums: {e}")
            return []

    def get_album_details(self, album_id):
        """
        Get detailed information about a specific album
        
        Args:
            album_id (str): Spotify album ID
            
        Returns:
            dict: Album details
        """
        if not self.sp:
            return None
            
        try:
            album = self.sp.album(album_id)
            tracks = self.sp.album_tracks(album_id)
            
            album_data = {
                'id': album['id'],
                'title': album['name'],
                'artist': ', '.join([artist['name'] for artist in album['artists']]),
                'year': album['release_date'][:4] if album['release_date'] else 'Unknown',
                'release_date': album['release_date'],
                'cover': album['images'][0]['url'] if album['images'] else None,
                'spotify_url': album['external_urls']['spotify'],
                'total_tracks': album['total_tracks'],
                'album_type': album['album_type'],
                'genres': album.get('genres', []),
                'popularity': album.get('popularity', 0),
                'label': album.get('label', ''),
                'tracks': [
                    {
                        'name': track['name'],
                        'duration_ms': track['duration_ms'],
                        'track_number': track['track_number'],
                        'spotify_url': track['external_urls']['spotify']
                    }
                    for track in tracks['items']
                ]
            }
            
            return album_data
            
        except Exception as e:
            logger.error(f"Error getting album details: {e}")
            return None

    def search_artists(self, query, limit=20):
        """
        Search for artists using Spotify API
        
        Args:
            query (str): Search query
            limit (int): Number of results to return
            
        Returns:
            list: List of artist dictionaries
        """
        if not self.sp:
            return []
            
        try:
            results = self.sp.search(q=query, type='artist', limit=limit)
            artists = []
            
            for artist in results['artists']['items']:
                artist_data = {
                    'id': artist['id'],
                    'name': artist['name'],
                    'followers': artist['followers']['total'],
                    'genres': artist['genres'],
                    'popularity': artist['popularity'],
                    'image': artist['images'][0]['url'] if artist['images'] else None,
                    'spotify_url': artist['external_urls']['spotify']
                }
                artists.append(artist_data)
                
            return artists
            
        except Exception as e:
            logger.error(f"Error searching artists: {e}")
            return []

    def get_artist_albums(self, artist_id, limit=20):
        """
        Get albums by a specific artist
        
        Args:
            artist_id (str): Spotify artist ID
            limit (int): Number of albums to return
            
        Returns:
            list: List of album dictionaries
        """
        if not self.sp:
            return []
            
        try:
            albums = self.sp.artist_albums(artist_id, album_type='album', limit=limit)
            return [
                {
                    'id': album['id'],
                    'title': album['name'],
                    'artist': ', '.join([artist['name'] for artist in album['artists']]),
                    'year': album['release_date'][:4] if album['release_date'] else 'Unknown',
                    'cover': album['images'][0]['url'] if album['images'] else None,
                    'spotify_url': album['external_urls']['spotify'],
                    'total_tracks': album['total_tracks'],
                    'album_type': album['album_type']
                }
                for album in albums['items']
            ]
            
        except Exception as e:
            logger.error(f"Error getting artist albums: {e}")
            return []
