# seed.py
from app import app
from db import db
from models import Episode, Guest, Appearance
from faker import Faker
import random

# Create a Faker instance
fake = Faker()

# Number of records to create
NUM_GUESTS = 10
NUM_EPISODES = 5
NUM_APPEARANCES = 20

def seed_database():
    with app.app_context():
        # Drop all existing tables and create new ones
        db.drop_all()
        db.create_all()

        # Create Guests
        guests = []
        for _ in range(NUM_GUESTS):
            guest = Guest(name=fake.name(), occupation=fake.job())
            guests.append(guest)

        db.session.add_all(guests)
        db.session.commit()
        print(f"Created {len(guests)} guests.")

        # Create Episodes
        episodes = []
        for _ in range(NUM_EPISODES):
            episode = Episode(date=fake.date(), number=_ + 1)
            episodes.append(episode)

        db.session.add_all(episodes)
        db.session.commit()
        print(f"Created {len(episodes)} episodes.")

        # Create Appearances
        appearances = []
        for _ in range(NUM_APPEARANCES):
            appearance = Appearance(
                rating=random.randint(1, 5),
                episode_id=random.choice(episodes).id,
                guest_id=random.choice(guests).id
            )
            appearances.append(appearance)

        db.session.add_all(appearances)
        db.session.commit()
        print(f"Created {len(appearances)} appearances.")

if __name__ == "__main__":
    seed_database()
