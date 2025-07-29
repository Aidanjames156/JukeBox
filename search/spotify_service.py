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

    def get_trending_albums(self, limit=10):
        """
        Get trending/popular albums by searching for popular tracks and extracting albums
        
        Args:
            limit (int): Number of albums to return
            
        Returns:
            list: List of trending album dictionaries
        """
        if not self.sp:
            return []
            
        try:
            trending_albums = []
            seen_albums = set()
            
            # Method 1: Search for popular tracks from various genres to get trending albums
            popular_genres = ['pop', 'hip-hop', 'rock', 'electronic', 'indie', 'r&b']
            
            for genre in popular_genres:
                if len(trending_albums) >= limit:
                    break
                    
                try:
                    # Search for popular tracks in each genre
                    results = self.sp.search(q=f'genre:{genre}', type='track', limit=20, market='US')
                    
                    for track in results['tracks']['items']:
                        if track['album'] and track['album']['id'] not in seen_albums:
                            if len(trending_albums) >= limit:
                                break
                                
                            album = track['album']
                            seen_albums.add(album['id'])
                            
                            album_data = {
                                'id': album['id'],
                                'title': album['name'],
                                'artist': ', '.join([artist['name'] for artist in album['artists']]),
                                'year': album['release_date'][:4] if album['release_date'] else 'Unknown',
                                'cover': album['images'][0]['url'] if album['images'] else None,
                                'spotify_url': album['external_urls']['spotify'],
                                'total_tracks': album['total_tracks'],
                                'album_type': album['album_type'],
                                'rating': 0
                            }
                            trending_albums.append(album_data)
                            
                except Exception as e:
                    logger.error(f"Error searching genre {genre}: {e}")
                    continue
            
            # Method 2: If we still need more albums, search for trending artists' albums
            if len(trending_albums) < limit:
                try:
                    trending_artists = ['Taylor Swift', 'Drake', 'Bad Bunny', 'The Weeknd', 'Ariana Grande', 'Billie Eilish', 'Dua Lipa', 'Post Malone']
                    
                    for artist_name in trending_artists:
                        if len(trending_albums) >= limit:
                            break
                        
                        try:
                            artist_results = self.sp.search(q=artist_name, type='artist', limit=1)
                            if artist_results['artists']['items']:
                                artist_id = artist_results['artists']['items'][0]['id']
                                albums = self.sp.artist_albums(artist_id, album_type='album', limit=5)
                                
                                for album in albums['items']:
                                    if album['id'] not in seen_albums and len(trending_albums) < limit:
                                        seen_albums.add(album['id'])
                                        album_data = {
                                            'id': album['id'],
                                            'title': album['name'],
                                            'artist': ', '.join([artist['name'] for artist in album['artists']]),
                                            'year': album['release_date'][:4] if album['release_date'] else 'Unknown',
                                            'cover': album['images'][0]['url'] if album['images'] else None,
                                            'spotify_url': album['external_urls']['spotify'],
                                            'total_tracks': album['total_tracks'],
                                            'album_type': album['album_type'],
                                            'rating': 0
                                        }
                                        trending_albums.append(album_data)
                        except Exception as e:
                            logger.error(f"Error getting albums for artist {artist_name}: {e}")
                            continue
                    
                except Exception as e:
                    logger.error(f"Error getting trending artist albums: {e}")
            
            # Method 3: If we still need more, search for popular terms
            if len(trending_albums) < limit:
                try:
                    popular_terms = ['hits', 'popular', 'trending', 'viral', 'chart']
                    
                    for term in popular_terms:
                        if len(trending_albums) >= limit:
                            break
                            
                        try:
                            results = self.sp.search(q=term, type='album', limit=10, market='US')
                            
                            for album in results['albums']['items']:
                                if album['id'] not in seen_albums and len(trending_albums) < limit:
                                    seen_albums.add(album['id'])
                                    album_data = {
                                        'id': album['id'],
                                        'title': album['name'],
                                        'artist': ', '.join([artist['name'] for artist in album['artists']]),
                                        'year': album['release_date'][:4] if album['release_date'] else 'Unknown',
                                        'cover': album['images'][0]['url'] if album['images'] else None,
                                        'spotify_url': album['external_urls']['spotify'],
                                        'total_tracks': album['total_tracks'],
                                        'album_type': album['album_type'],
                                        'rating': 0
                                    }
                                    trending_albums.append(album_data)
                        except Exception as e:
                            logger.error(f"Error searching term {term}: {e}")
                            continue
                        
                except Exception as e:
                    logger.error(f"Error getting popular term albums: {e}")
                    
            return trending_albums[:limit]
            
        except Exception as e:
            logger.error(f"Error getting trending albums: {e}")
            return []

    def get_related_albums(self, album_id, limit=6):
        """
        Get related albums based on the artist and similar genres
        
        Args:
            album_id (str): Spotify album ID
            limit (int): Number of related albums to return
            
        Returns:
            list: List of related album dictionaries
        """
        if not self.sp:
            logger.error("Spotify client not initialized")
            return []
            
        try:
            # First get the album details to find the artist
            album = self.sp.album(album_id)
            if not album or not album['artists']:
                return []
                
            # Get the main artist
            main_artist = album['artists'][0]
            artist_id = main_artist['id']
            
            # Get other albums by the same artist
            artist_albums = self.sp.artist_albums(artist_id, album_type='album', limit=limit*2)
            
            related_albums = []
            for album_item in artist_albums['items']:
                # Skip the current album
                if album_item['id'] == album_id:
                    continue
                    
                album_data = {
                    'id': album_item['id'],
                    'title': album_item['name'],
                    'artist': ', '.join([artist['name'] for artist in album_item['artists']]),
                    'year': album_item['release_date'][:4] if album_item['release_date'] else 'Unknown',
                    'cover': album_item['images'][0]['url'] if album_item['images'] else None,
                    'spotify_url': album_item['external_urls']['spotify'],
                    'total_tracks': album_item['total_tracks'],
                    'album_type': album_item['album_type'],
                    'rating': 0
                }
                related_albums.append(album_data)
                
                if len(related_albums) >= limit:
                    break
                    
            return related_albums
            
        except Exception as e:
            logger.error(f"Error getting related albums for {album_id}: {e}")
            return []
