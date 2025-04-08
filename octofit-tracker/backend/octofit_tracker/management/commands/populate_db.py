import logging
from django.core.management.base import BaseCommand
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
from django.conf import settings

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class Command(BaseCommand):
    help = 'Populate the database with test data for users, teams, activities, leaderboard, and workouts'

    def handle(self, *args, **kwargs):
        logging.debug('Starting database population...')

        # Connect to MongoDB
        client = MongoClient(settings.DATABASES['default']['HOST'], settings.DATABASES['default']['PORT'])
        db = client[settings.DATABASES['default']['NAME']]

        # Drop existing collections
        db.users.drop()
        db.teams.drop()
        db.activity.drop()
        db.leaderboard.drop()
        db.workouts.drop()
        logging.debug('Dropped existing collections.')

        # Insert users
        users = [
            {"_id": ObjectId(), "email": "thundergod@mhigh.edu", "name": "Thunder God", "created_at": datetime.utcnow()},
            {"_id": ObjectId(), "email": "metalgeek@mhigh.edu", "name": "Metal Geek", "created_at": datetime.utcnow()},
            {"_id": ObjectId(), "email": "zerocool@mhigh.edu", "name": "Zero Cool", "created_at": datetime.utcnow()},
            {"_id": ObjectId(), "email": "crashoverride@hmhigh.edu", "name": "Crash Override", "created_at": datetime.utcnow()},
            {"_id": ObjectId(), "email": "sleeptoken@mhigh.edu", "name": "Sleep Token", "created_at": datetime.utcnow()}
        ]
        db.users.insert_many(users)
        logging.debug(f'Inserted users: {users}')

        # Insert teams
        teams = [
            {"_id": ObjectId(), "name": "Blue Team", "members": [users[0], users[1]]},
            {"_id": ObjectId(), "name": "Gold Team", "members": [users[2], users[3], users[4]]}
        ]
        db.teams.insert_many(teams)
        logging.debug(f'Inserted teams: {teams}')

        # Insert activities
        activities = [
            {"_id": ObjectId(), "user": users[0], "type": "Cycling", "duration": 60, "date": "2025-04-08"},
            {"_id": ObjectId(), "user": users[1], "type": "Crossfit", "duration": 120, "date": "2025-04-07"},
            {"_id": ObjectId(), "user": users[2], "type": "Running", "duration": 90, "date": "2025-04-06"},
            {"_id": ObjectId(), "user": users[3], "type": "Strength", "duration": 30, "date": "2025-04-05"},
            {"_id": ObjectId(), "user": users[4], "type": "Swimming", "duration": 75, "date": "2025-04-04"}
        ]
        db.activity.insert_many(activities)
        logging.debug(f'Inserted activities: {activities}')

        # Insert leaderboard entries
        leaderboard = [
            {"_id": ObjectId(), "team": teams[0], "score": 100},
            {"_id": ObjectId(), "team": teams[1], "score": 90}
        ]
        db.leaderboard.insert_many(leaderboard)
        logging.debug(f'Inserted leaderboard entries: {leaderboard}')

        # Insert workouts
        workouts = [
            {"_id": ObjectId(), "name": "Cycling Training", "description": "Training for a road cycling event"},
            {"_id": ObjectId(), "name": "Crossfit", "description": "Training for a crossfit competition"},
            {"_id": ObjectId(), "name": "Running Training", "description": "Training for a marathon"},
            {"_id": ObjectId(), "name": "Strength Training", "description": "Training for strength"},
            {"_id": ObjectId(), "name": "Swimming Training", "description": "Training for a swimming competition"}
        ]
        db.workouts.insert_many(workouts)
        logging.debug(f'Inserted workouts: {workouts}')

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with test data using pymongo.'))