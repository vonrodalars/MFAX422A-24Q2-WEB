from app import app
from models import db, User, Customer, FAQ

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

    faq1 = FAQ(
        stichwort="Drucker",
        antwort="Bitte überprüfen Sie die Verbindung zum Drucker und starten Sie ihn neu.",
    )
    faq2 = FAQ(
        stichwort="Passwort",
        antwort="Sie können Ihr Passwort über das Selbstbedienungsportal zurücksetzen.",
    )
    faq3 = FAQ(
        stichwort="Internet",
        antwort="Stellen Sie sicher, dass Ihr Router eingeschaltet ist und eine Verbindung zum Internet besteht.",
    )
    db.session.add(faq1)
    db.session.add(faq2)
    db.session.add(faq3)

    db.session.commit()

    print("Database initialized with example data.")
