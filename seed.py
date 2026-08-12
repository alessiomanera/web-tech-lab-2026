"""
seed.py
-------
Database seeding script.
Drops all existing tables and populates the database with initial Museum and Exhibition data.
"""
from app import create_app
from models import db, Museum, Exhibition
from datetime import datetime, timedelta

def seed_db():
    """
    Initializes the app context, wipes the database, and creates mock data 
    for Museums and Exhibitions.
    """
    app = create_app()
    with app.app_context():
        # Clear existing data and create tables
        db.drop_all()
        db.create_all()

        m1 = Museum(
            name="The National Gallery of Future Art",
            description="A premier institution showcasing the intersection of technology and human creativity, featuring digital installations and interactive exhibits.",
            location="London, UK",
            image_url="https://images.unsplash.com/photo-1518998053401-a4149019d8f7?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"
        )
        
        m2 = Museum(
            name="Museum of Ancient History",
            description="Dive into the past with our extensive collection of artifacts from Rome, Egypt, and Greece. Step back in time.",
            location="Rome, Italy",
            image_url="https://images.unsplash.com/photo-1544265434-633092eafe2c?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"
        )
        
        m3 = Museum(
            name="Modern Art Space",
            description="A minimalist gallery featuring contemporary works from emerging artists around the globe.",
            location="New York, USA",
            image_url="https://images.unsplash.com/photo-1566411123287-c5ab352427a1?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80"
        )

        db.session.add_all([m1, m2, m3])
        db.session.commit()

        # Add exhibitions
        e1 = Exhibition(
            museum_id=m1.id,
            title="Neon Horizons: The Digital Era",
            start_date=datetime.utcnow() - timedelta(days=10),
            end_date=datetime.utcnow() + timedelta(days=50)
        )
        
        e2 = Exhibition(
            museum_id=m2.id,
            title="Secrets of the Pharaohs",
            start_date=datetime.utcnow() + timedelta(days=5),
            end_date=datetime.utcnow() + timedelta(days=60)
        )

        db.session.add_all([e1, e2])
        db.session.commit()
        print("Database successfully seeded with museums and exhibitions!")

if __name__ == '__main__':
    seed_db()
