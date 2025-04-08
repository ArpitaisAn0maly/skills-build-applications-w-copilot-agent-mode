from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from django.conf import settings
from pymongo import MongoClient
from datetime import timedelta
from bson import ObjectId

class Command(BaseCommand):
    help = 'Populate the database with test data for users, teams, activities, leaderboard, and workouts'

    def handle(self, *args, **kwargs):
        # Connect to MongoDB
        client = MongoClient(settings.DATABASES['default']['HOST'], settings.DATABASES['default']['PORT'])
        db = client[settings.DATABASES['default']['NAME']]

        # Drop existing collections
        db.users.drop()
        db.teams.drop()
        db.activity.drop()
        db.leaderboard.drop()
        db.workouts.drop()

        # Create users
        users = [
            User(_id=ObjectId(), email='thundergod@mhigh.edu', name='Thunder God'),
            User(_id=ObjectId(), email='metalgeek@mhigh.edu', name='Metal Geek'),
            User(_id=ObjectId(), email='zerocool@mhigh.edu', name='Zero Cool'),
            User(_id=ObjectId(), email='crashoverride@mhigh.edu', name='Crash Override'),
            User(_id=ObjectId(), email='sleeptoken@mhigh.edu', name='Sleep Token'),
        ]
        User.objects.bulk_create(users)

        # Create teams
        teams = [
            Team(_id=ObjectId(), name='Blue Team'),
            Team(_id=ObjectId(), name='Gold Team'),
        ]
        Team.objects.bulk_create(teams)

        # Assign members to teams as dictionaries
        teams[0].members = [{"_id": str(users[0]._id), "email": users[0].email, "name": users[0].name},
                            {"_id": str(users[1]._id), "email": users[1].email, "name": users[1].name}]
        teams[1].members = [{"_id": str(users[2]._id), "email": users[2].email, "name": users[2].name},
                            {"_id": str(users[3]._id), "email": users[3].email, "name": users[3].name},
                            {"_id": str(users[4]._id), "email": users[4].email, "name": users[4].name}]
        teams[0].save()
        teams[1].save()

        # Create activities
        activities = [
            Activity(_id=ObjectId(), user=users[0], type='Cycling', duration=60),  # 1 hour in minutes
            Activity(_id=ObjectId(), user=users[1], type='Crossfit', duration=120),  # 2 hours in minutes
            Activity(_id=ObjectId(), user=users[2], type='Running', duration=90),  # 1.5 hours in minutes
            Activity(_id=ObjectId(), user=users[3], type='Strength', duration=30),  # 30 minutes
            Activity(_id=ObjectId(), user=users[4], type='Swimming', duration=75),  # 1 hour 15 minutes
        ]
        Activity.objects.bulk_create(activities)

        # Create leaderboard entries
        leaderboard_entries = [
            Leaderboard(_id=ObjectId(), team=teams[0], score=100),
            Leaderboard(_id=ObjectId(), team=teams[1], score=90),
        ]
        Leaderboard.objects.bulk_create(leaderboard_entries)

        # Create workouts
        workouts = [
            Workout(_id=ObjectId(), name='Cycling Training', description='Training for a road cycling event'),
            Workout(_id=ObjectId(), name='Crossfit', description='Training for a crossfit competition'),
            Workout(_id=ObjectId(), name='Running Training', description='Training for a marathon'),
            Workout(_id=ObjectId(), name='Strength Training', description='Training for strength'),
            Workout(_id=ObjectId(), name='Swimming Training', description='Training for a swimming competition'),
        ]
        Workout.objects.bulk_create(workouts)

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with test data.'))