# app.py
from flask import Flask, render_template, request, redirect, url_for
from models import db, Ticket, User, Customer
from multiprocessing import Process
from AI_Integration import get_category

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tickets.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db.init_app(app)


def assign_user_to_ticket():
    # Finde den Benutzer mit den wenigsten Tickets
    user = (
        User.query.outerjoin(Ticket)
        .group_by(User.id)
        .order_by(db.func.count(Ticket.id))
        .first()
    )
    return user


def save_form_data_and_process(form):
    with app.app_context():
        complaint = form["beschwerde"]
        category = get_category(complaint=complaint)
        user = assign_user_to_ticket()
        newTicket = Ticket(complaint=complaint, category=category, user_id=user.id)
        db.session.add(newTicket)
        db.session.commit()


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
        process = Process(target=save_form_data_and_process, args=(request.form,))
        process.start()
        return redirect(url_for("index"))
    return render_template("ticket.html")


@app.route("/ticket/<int:id>", methods=["GET", "POST"])
def edit_ticket(id):
    ticket = Ticket.query.get(id)
    if request.method == "POST":
        ticket.status = request.form["status"]
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("ticket.html", ticket=ticket)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
