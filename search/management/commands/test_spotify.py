from django.core.management.base import BaseCommand
from search.spotify_service import SpotifyService

class Command(BaseCommand):
    help = 'Test Spotify API connection'

    def add_arguments(self, parser):
        parser.add_argument(
            '--query',
            type=str,
            default='The Beatles',
            help='Search query to test'
        )

    def handle(self, *args, **options):
        query = options['query']
        
        self.stdout.write(
            self.style.SUCCESS(f'Testing Spotify API with query: "{query}"')
        )
        
        try:
            spotify_service = SpotifyService()
            
            # Test album search
            albums = spotify_service.search_albums(query, limit=5)
            
            if albums:
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Found {len(albums)} albums!')
                )
                
                for i, album in enumerate(albums[:3], 1):
                    self.stdout.write(f"{i}. {album['title']} by {album['artist']} ({album['year']})")
                    
            else:
                self.stdout.write(
                    self.style.WARNING('⚠️  No albums found. Check your API credentials.')
                )
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Error: {e}')
            )
            self.stdout.write(
                self.style.ERROR('Make sure your SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET are set in the .env file')
            )
