from app import app
from models import db, Bearbeiter, Customer, Ticket

# Create all the tables
with app.app_context():
    db.create_all()

    # Add example data
    bearbeiter1 = Bearbeiter(name="Max Mustermann")
    bearbeiter2 = Bearbeiter(name="Erika Mustermann")
    db.session.add(bearbeiter1)
    db.session.add(bearbeiter2)

    customer1 = Customer(name="John Doe")
    customer2 = Customer(name="Jane Doe")
    db.session.add(customer1)
    db.session.add(customer2)

    db.session.commit()

    print("Database initialized with example data.")
