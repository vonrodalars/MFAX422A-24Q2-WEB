from app import app
from models import db, User, Customer, Ticket

# Create all the tables
with app.app_context():
    db.create_all()

    # Add example data
    user1 = User(name="Max Mustermann")
    user2 = User(name="Erika Mustermann")
    db.session.add(user1)
    db.session.add(user2)

    customer1 = Customer(name="John Doe")
    customer2 = Customer(name="Jane Doe")
    db.session.add(customer1)
    db.session.add(customer2)

    db.session.commit()

    print("Database initialized with example data.")
