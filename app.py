# app.py
from flask import Flask, render_template, request, redirect, url_for
from models import db, Ticket, User, Customer, FAQ
from multiprocessing import Process, Queue
from AI_Integration import get_category
from datetime import datetime, timedelta
from threading import Thread
import time

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db.init_app(app)


def assign_user_to_ticket(ticket):
    user = (
        User.query.outerjoin(Ticket)
        .group_by(User.id)
        .order_by(db.func.count(Ticket.id))
        .first()
    )
    ticket.user_id = user.id
    ticket.last_assigned = datetime.now()
    db.session.commit()


def reassign_tickets():
    now = datetime.now()
    three_days_ago = now = timedelta(days=3)
    tickets = Ticket.query.filter(
        Ticket.status == "offen", Ticket.last_assigned < three_days_ago
    ).all()
    for ticket in tickets:
        assign_user_to_ticket(ticket)


def save_form_data_and_process(form, result_queue):
    with app.app_context():
        complaint = form["beschwerde"]

        faqs = FAQ.query.all()
        for faq in faqs:
            if faq.stichwort.lower() in complaint.lower():
                result_queue.put({"faq_antwort": faq.antwort})
                return

        category = get_category(complaint=complaint)
        customer_id = form["customer_id"]
        newTicket = Ticket(
            complaint=complaint, category=category, customer_id=customer_id
        )
        db.session.add(newTicket)
        db.session.commit()
        assign_user_to_ticket(newTicket)
        result_queue.put({"ticket_erzeugt": True, "kategorie": category})


@app.route("/")
def index():
    tickets = Ticket.query.all()
    customers = Customer.query.all()
    user = User.query.all()
    return render_template(
        "index.html", tickets=tickets, customers=customers, user=user
    )


@app.route("/ticket/erstellen", methods=["GET", "POST"])
@app.route("/ticket/create", methods=["GET", "POST"])
def create_ticket():
    if request.method == "POST":
        result_queue = Queue()
        process = Process(
            target=save_form_data_and_process, args=(request.form, result_queue)
        )
        process.start()
        process.join()

        result = result_queue.get()
        if "faq_antwort" in result:
            return render_template("ticket.html", faq_antwort=result["faq_antwort"])
        return redirect(url_for("index"))
    customers = Customer.query.all()
    return render_template("ticket.html", customers=customers)


@app.route("/ticket/<int:id>", methods=["GET", "POST"])
def edit_ticket(id):
    ticket = Ticket.query.get(id)
    if request.method == "POST":
        ticket.status = request.form["status"]
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("ticket.html", ticket=ticket)


@app.route("/faq")
def faq():
    faqs = FAQ.query.all()
    return render_template("faq.html", faqs=faqs)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
