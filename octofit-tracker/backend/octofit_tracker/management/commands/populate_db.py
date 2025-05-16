from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from django.utils import timezone

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data.'

    def handle(self, *args, **kwargs):
        # Clear existing data
        User.objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()

        # Users
        user1 = User.objects.create(email='alice@example.com', name='Alice', password='password1')
        user2 = User.objects.create(email='bob@example.com', name='Bob', password='password2')
        user3 = User.objects.create(email='carol@example.com', name='Carol', password='password3')

        # Teams
        team1 = Team.objects.create(name='Team Alpha')
        team2 = Team.objects.create(name='Team Beta')
        team1.members.add(user1, user2)
        team2.members.add(user3)

        # Workouts
        workout1 = Workout.objects.create(name='Pushups', description='Do 20 pushups')
        workout2 = Workout.objects.create(name='Running', description='Run 1 mile')

        # Activities
        Activity.objects.create(user=user1, activity_type='pushups', duration=10, date=timezone.now())
        Activity.objects.create(user=user2, activity_type='running', duration=20, date=timezone.now())
        Activity.objects.create(user=user3, activity_type='pushups', duration=15, date=timezone.now())

        # Leaderboard
        Leaderboard.objects.create(team=team1, points=30)
        Leaderboard.objects.create(team=team2, points=15)

        self.stdout.write(self.style.SUCCESS('Test data populated successfully.'))
