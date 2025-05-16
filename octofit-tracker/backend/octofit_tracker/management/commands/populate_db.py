from django.core.management.base import BaseCommand
from django.utils import timezone
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
import pymongo
import logging

# Update logging configuration to save logs to a file
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/workspaces/skills-build-applications-w-copilot-agent-mode/octofit-tracker/backend/logs/debug.log'),
        logging.StreamHandler()
    ]
)

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data.'

    def handle(self, *args, **kwargs):
        try:
            logging.debug('Starting data population...')
            # Clear existing data using MongoDB directly
            client = pymongo.MongoClient('mongodb://localhost:27017/')
            db = client['octofit_db']
            
            # Log database connection
            logging.debug(f'Connected to database: {db.name}')

            collections = ['users', 'teams', 'activity', 'leaderboard', 'workouts']
            # Log clearing collections
            for collection in collections:
                try:
                    db[collection].delete_many({})
                    self.stdout.write(self.style.SUCCESS(f'Cleared {collection} collection'))
                    logging.debug(f'Cleared collection: {collection}')
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f'Error clearing {collection}: {str(e)}'))
                    logging.error(f'Error clearing collection {collection}: {e}')

            # Create test users
            db['users'].insert_many([
                {"email": "alice@example.com", "name": "Alice Smith", "password": "password123"},
                {"email": "bob@example.com", "name": "Bob Johnson", "password": "password123"}
            ])
            logging.debug('Inserted test users directly into MongoDB.')

            # Create test teams
            db['teams'].insert_many([
                {"name": "Speed Demons", "members": ["alice@example.com"]},
                {"name": "Power Lifters", "members": ["bob@example.com"]}
            ])
            logging.debug('Inserted test teams directly into MongoDB.')

            # Create test activities
            db['activity'].insert_many([
                {"user": "alice@example.com", "activity_type": "running", "duration": 30, "date": timezone.now().isoformat()},
                {"user": "bob@example.com", "activity_type": "weightlifting", "duration": 45, "date": timezone.now().isoformat()}
            ])
            logging.debug('Inserted test activities directly into MongoDB.')

            # Create test workouts
            db['workouts'].insert_many([
                {"name": "Morning Run", "description": "5km run at moderate pace"},
                {"name": "Strength Training", "description": "Full body workout with weights"}
            ])
            logging.debug('Inserted test workouts directly into MongoDB.')

            # Create leaderboard entries
            db['leaderboard'].insert_many([
                {"team": "Speed Demons", "points": 100},
                {"team": "Power Lifters", "points": 85}
            ])
            logging.debug('Inserted leaderboard entries directly into MongoDB.')

            self.stdout.write(self.style.SUCCESS('Successfully populated all test data'))
        except Exception as e:
            logging.error(f'Error during data population: {e}')
            self.stdout.write(self.style.ERROR(f'Error populating data: {str(e)}'))
