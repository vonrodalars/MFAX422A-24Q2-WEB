from app import app
from models import db, User, Customer, FAQ

# Create all the tables
with app.app_context():
    db.create_all()

    # Beispiel-User hinzufügen
    user1 = User(name="Max Mustermann")
    user2 = User(name="Erika Mustermann")
    user3 = User(name="Hans Müller")
    user4 = User(name="Petra Schmidt")
    user5 = User(name="Claudia Klein")
    user6 = User(name="Sebastian Kurz")
    user7 = User(name="Lena Lange")
    user8 = User(name="Oliver Braun")
    user9 = User(name="Nicole Weiß")
    user10 = User(name="Tobias Schwarz")

    db.session.add_all(
        [user1, user2, user3, user4, user5, user6, user7, user8, user9, user10]
    )

    # Beispiel-Kunden hinzufügen
    customer1 = Customer(name="John Doe")
    customer2 = Customer(name="Jane Doe")
    customer3 = Customer(name="Alice Johnson")
    customer4 = Customer(name="Bob Smith")
    customer5 = Customer(name="Charlie Brown")
    customer6 = Customer(name="Diana Prince")
    customer7 = Customer(name="Edward Norton")
    customer8 = Customer(name="Fiona Gallagher")
    customer9 = Customer(name="George Clooney")
    customer10 = Customer(name="Helen Mirren")

    db.session.add_all(
        [
            customer1,
            customer2,
            customer3,
            customer4,
            customer5,
            customer6,
            customer7,
            customer8,
            customer9,
            customer10,
        ]
    )

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
