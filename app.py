# app.py
from flask import Flask, render_template, request, redirect, url_for
from models import db, Ticket, Bearbeiter
from multiprocessing import Process
from AI_Integration import get_category

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tickets.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db.init_app(app)


def save_form_data_and_process(form):
    with app.app_context():
        complain = form['beschwerde']
        category = get_category(complain=complain)
        newTicket = Ticket(complain=complain, category=category)
        db.session.add(newTicket)
        db.session.commit()


@app.route('/')
def index():
    tickets = Ticket.query.all()
    print(tickets)
    return render_template('index.html', tickets=tickets)

@app.route('/ticket/erstellen', methods=['GET', 'POST'])
@app.route('/ticket/create', methods=['GET', 'POST'])
def ticket_erstellen():
    if request.method == 'POST':
        process = Process(target=save_form_data_and_process, args=(request.form,))
        process.start()
        return redirect(url_for('index'))
    return render_template('ticket.html')

@app.route('/ticket/<int:id>', methods=['GET', 'POST'])
def ticket_bearbeiten(id):
    ticket = Ticket.query.get(id)
    if request.method == 'POST':
        ticket.status = request.form['status']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('ticket.html', ticket=ticket)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
