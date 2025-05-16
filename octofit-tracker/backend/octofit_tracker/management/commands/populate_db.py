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
            user1 = User.objects.create(
                email='alice@example.com',
                name='Alice Smith',
                password='password123'
            )
            
            user2 = User.objects.create(
                email='bob@example.com',
                name='Bob Johnson',
                password='password123'
            )
            logging.debug(f'Created users: {user1}, {user2}')

            # Log user creation
            logging.debug(f'Creating user: {user1.email}')
            logging.debug(f'Creating user: {user2.email}')

            # Create test teams
            team1 = Team.objects.create(name='Speed Demons')
            team1.members.add(user1)
            
            team2 = Team.objects.create(name='Power Lifters')
            team2.members.add(user2)
            logging.debug(f'Created teams: {team1}, {team2}')

            # Log team creation
            logging.debug(f'Creating team: {team1.name}')
            logging.debug(f'Creating team: {team2.name}')

            # Create test activities
            Activity.objects.create(
                user=user1,
                activity_type='running',
                duration=30,
                date=timezone.now()
            )
            
            Activity.objects.create(
                user=user2,
                activity_type='weightlifting',
                duration=45,
                date=timezone.now()
            )
            logging.debug('Created activities.')

            # Log activity creation
            logging.debug('Creating activities...')

            # Create test workouts
            Workout.objects.create(
                name='Morning Run',
                description='5km run at moderate pace'
            )
            
            Workout.objects.create(
                name='Strength Training',
                description='Full body workout with weights'
            )
            logging.debug('Created workouts.')

            # Log workout creation
            logging.debug('Creating workouts...')

            # Create leaderboard entries
            Leaderboard.objects.create(team=team1, points=100)
            Leaderboard.objects.create(team=team2, points=85)
            logging.debug('Created leaderboard entries.')

            # Log leaderboard entries
            logging.debug('Creating leaderboard entries...')

            self.stdout.write(self.style.SUCCESS('Successfully populated all test data'))
        except Exception as e:
            logging.error(f'Error during data population: {e}')
            self.stdout.write(self.style.ERROR(f'Error populating data: {str(e)}'))
