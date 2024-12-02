from flask import Flask, render_template, redirect, url_for, request, flash
from models import db
from utils.generate_invoice import generate_invoice

# Importing `init_db` instead of importing `Client` directly
from models.client import init_db
from models.order import Order
from models.appointment import Appointment

app = Flask(__name__)
app.config.from_object('config.Config')

# Initialize the database
db.init_app(app)

# Initialize the Client model after db is ready
Client = init_db()

@app.route('/')
def home():
    return render_template('layout.html')

@app.route('/clients')
def view_clients():
    clients = Client.query.all()
    return render_template('view_clients.html', clients=clients)

@app.route('/add_client', methods=['GET', 'POST'])
def add_client():
    from forms import ClientForm  # Import here to avoid circular import
    form = ClientForm()
    if form.validate_on_submit():  # This validates the form on submit
        client = Client(name=form.name.data, email=form.email.data, phone=form.phone.data)
        db.session.add(client)  # Add client to the database
        db.session.commit()  # Commit the changes
        flash('Client added successfully!', 'success')
        return redirect(url_for('view_clients'))  # Redirect to the view_clients page
    return render_template('add_client.html', form=form)

@app.route('/add_order', methods=['GET', 'POST'])
def add_order():
    from forms import OrderForm  # Import here to avoid circular import
    form = OrderForm()

    # Query all clients to pass their names and IDs to the form
    clients = Client.query.all()
    form.client_id.choices = [(client.id, client.name) for client in clients]

    if form.validate_on_submit():
        order = Order(client_id=form.client_id.data, total_price=form.total_price.data)
        db.session.add(order)
        db.session.commit()
        flash('Order added successfully!', 'success')
        return redirect(url_for('view_orders'))
    return render_template('add_order.html', form=form)

@app.route('/appointments')
def view_appointments():
    appointments = Appointment.query.all()
    return render_template('view_appointments.html', appointments=appointments)

@app.route('/generate_invoice/<int:order_id>')
def generate_invoice_route(order_id):
    order = Order.query.get_or_404(order_id)
    invoice_path = generate_invoice(order.client, order)
    return redirect(invoice_path)

if __name__ == '__main__':
    app.run(debug=True)
