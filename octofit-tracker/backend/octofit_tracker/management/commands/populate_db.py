from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from faker import Faker
import logging
import random
from datetime import timedelta

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/populate_db.log'),
        logging.StreamHandler()
    ]
)

class Command(BaseCommand):
    help = 'Populates database with comprehensive test data'

    def __init__(self):
        super().__init__()
        self.faker = Faker()
        self.activity_types = ['running', 'weightlifting', 'cycling', 'swimming', 'yoga']
        self.workout_categories = ['cardio', 'strength', 'flexibility', 'endurance']

    def handle(self, *args, **options):
        try:
            self._clear_existing_data()
            users = self._create_users(5)
            teams = self._create_teams(3)
            self._assign_users_to_teams(users, teams)
            self._create_activities(users, 20)
            self._create_workouts(10)
            self._update_leaderboards(teams)
            
            self.stdout.write(self.style.SUCCESS('✅ Successfully populated test data'))
        except Exception as e:
            logging.exception('Data population failed')
            self.stdout.write(self.style.ERROR(f'❌ Error: {str(e)}'))

    def _clear_existing_data(self):
        """Safely clear all existing data"""
        models = [Leaderboard, Activity, Workout, Team, User]
        for model in models:
            model.objects.all().delete()
        logging.info('Cleared all existing data')

    def _create_users(self, count):
        """Generate test users with secure passwords"""
        users = []
        for i in range(count):
            user = User.objects.create(
                email=self.faker.unique.email(),
                name=self.faker.name(),
                password=make_password('testpass123'),  # Proper password hashing
                last_login=self.faker.date_time_this_month(),
                is_active=True
            )
            users.append(user)
            logging.debug(f'Created user: {user.email}')
        return users

    def _create_teams(self, count):
        """Generate test teams with realistic names"""
        teams = []
        prefixes = ['Elite', 'Pro', 'Alpha', 'Omega', 'Extreme']
        suffixes = ['Squad', 'Team', 'Club', 'Unit', 'Force']
        
        for i in range(count):
            name = f"{random.choice(prefixes)} {random.choice(suffixes)}"
            # Remove created_at if not in your Team model
            try:
                team = Team.objects.create(
                    name=name,
                    created_at=timezone.now() - timedelta(days=random.randint(1, 30))
                )
            except TypeError:
                team = Team.objects.create(name=name)
            teams.append(team)
            logging.debug(f'Created team: {team.name}')
        return teams

    def _assign_users_to_teams(self, users, teams):
        """Randomly assign users to teams"""
        for user in users:
            num_teams = random.randint(1, 2)
            selected_teams = random.sample(teams, num_teams)
            for team in selected_teams:
                team.members.add(user)
            logging.debug(f'Assigned user {user.email} to {num_teams} teams')

    def _create_activities(self, users, count):
        """Generate realistic activity data"""
        for _ in range(count):
            user = random.choice(users)
            activity_type = random.choice(self.activity_types)
            
            # Generate realistic durations based on activity type
            if activity_type == 'running':
                duration = random.randint(15, 120)
            elif activity_type == 'weightlifting':
                duration = random.randint(30, 90)
            else:
                duration = random.randint(20, 60)
                
            Activity.objects.create(
                user=user,
                activity_type=activity_type,
                duration=duration,
                calories=random.randint(100, 800),
                date=self.faker.date_time_this_month(),
                notes=self.faker.sentence()
            )
            logging.debug(f'Created activity for {user.email}')

    def _create_workouts(self, count):
        """Generate diverse workout plans"""
        for _ in range(count):
            category = random.choice(self.workout_categories)
            difficulty = random.choice(['beginner', 'intermediate', 'advanced'])
            
            Workout.objects.create(
                name=f"{category.capitalize()} {difficulty} workout",
                description=self.faker.paragraph(),
                category=category,
                duration=random.randint(15, 90),
                difficulty=difficulty
            )
            logging.debug(f'Created workout: {category} {difficulty}')

    def _update_leaderboards(self, teams):
        """Generate realistic leaderboard data"""
        for team in teams:
            points = random.randint(50, 500)
            Leaderboard.objects.create(
                team=team,
                points=points,
                last_updated=timezone.now()
            )
            logging.debug(f'Updated leaderboard for {team.name}')