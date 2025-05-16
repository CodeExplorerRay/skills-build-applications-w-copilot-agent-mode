from django.core.management.base import BaseCommand
from django.utils import timezone
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
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
    help = 'Populate the octofit_db database with test data using Django ORM.'

    def handle(self, *args, **kwargs):
        try:
            logging.debug('Starting data population...')
            self.stdout.write('Clearing existing data...')

            # Clear existing data using Django ORM
            Leaderboard.objects.all().delete()  # Delete related models first
            Activity.objects.all().delete()
            Team.objects.all().delete()
            User.objects.all().delete()
            Workout.objects.all().delete()
            logging.debug('Cleared all collections')

            # Create test users
            alice = User.objects.create(
                email="alice@example.com",
                name="Alice Smith",
                password="password123"
            )
            bob = User.objects.create(
                email="bob@example.com",
                name="Bob Johnson",
                password="password123"
            )
            logging.debug('Created test users')

            # Create test teams
            speed_demons = Team.objects.create(name="Speed Demons")
            power_lifters = Team.objects.create(name="Power Lifters")
            
            # Add members to teams
            speed_demons.members.add(alice)
            power_lifters.members.add(bob)
            logging.debug('Created test teams')

            # Create test activities
            Activity.objects.create(
                user=alice,
                activity_type="running",
                duration=30,
                date=timezone.now()
            )
            Activity.objects.create(
                user=bob,
                activity_type="weightlifting",
                duration=45,
                date=timezone.now()
            )
            logging.debug('Created test activities')

            # Create test workouts
            Workout.objects.create(
                name="Morning Run",
                description="5km run at moderate pace"
            )
            Workout.objects.create(
                name="Strength Training",
                description="Full body workout with weights"
            )
            logging.debug('Created test workouts')

            # Create leaderboard entries
            Leaderboard.objects.create(
                team=speed_demons,
                points=100
            )
            Leaderboard.objects.create(
                team=power_lifters,
                points=85
            )
            logging.debug('Created leaderboard entries')

            self.stdout.write(self.style.SUCCESS('Successfully populated all test data'))
        
        except Exception as e:
            logging.error(f'Error during data population: {str(e)}')
            self.stdout.write(self.style.ERROR(f'Failed to populate data: {str(e)}'))
            raise
