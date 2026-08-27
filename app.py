import json
from flask import Flask, render_template, request, redirect, url_for, session, make_response, Response

app = Flask(__name__)
app.secret_key = "secretkey"

DATA_FILE = 'buses.json'

class Bus:
    def __init__(self, bus_no, source, destination, seats, booked_seats=None, waiting_list=None):
        self.bus_no = bus_no
        self.source = source.lower()
        self.destination = destination.lower()
        self.seats = seats
        self.booked_seats = booked_seats or {}
        self.waiting_list = waiting_list or []

    def available_seats(self):
        return [i for i in range(1, self.seats + 1) if str(i) not in self.booked_seats]

    def book_ticket(self, name, seat_no):
        seat_no_str = str(seat_no)
        if seat_no_str in self.booked_seats:
            return "❌ Seat already booked!"
        elif len(self.booked_seats) < self.seats:
            self.booked_seats[seat_no_str] = name
            save_buses()
            return f"✅ Seat {seat_no} booked for {name}"
        else:
            self.waiting_list.append(name)
            save_buses()
            return f"🕒 Bus full. {name} added to waiting list. Wait for availability."

    def cancel_ticket(self, seat_no):
        seat_no_str = str(seat_no)
        if seat_no_str in self.booked_seats:
            removed = self.booked_seats.pop(seat_no_str)
            message = f"❌ Cancelled seat {seat_no} booked by {removed}"
            if self.waiting_list:
                next_person = self.waiting_list.pop(0)
                self.booked_seats[seat_no_str] = next_person
                save_buses()
                message += f" ➕ {next_person} moved from waiting list to seat {seat_no}"
            return message
        return "❌ Invalid seat number"

    def to_dict(self):
        return {
            "bus_no": self.bus_no,
            "source": self.source,
            "destination": self.destination,
            "seats": self.seats,
            "booked_seats": self.booked_seats,
            "waiting_list": self.waiting_list
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            bus_no=data["bus_no"],
            source=data["source"],
            destination=data["destination"],
            seats=data["seats"],
            booked_seats=data.get("booked_seats", {}),
            waiting_list=data.get("waiting_list", [])
        )

buses = []

def load_buses():
    global buses
    try:
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
            buses = [Bus.from_dict(b) for b in data]
    except (FileNotFoundError, json.JSONDecodeError):
        buses = []

def save_buses():
    with open(DATA_FILE, 'w') as f:
        json.dump([b.to_dict() for b in buses], f, indent=4)

load_buses()

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

def calculate_fare(source, destination):
    route = f"{source.lower()}-{destination.lower()}"
    fares = {
        "citya-cityb": 150,
        "citya-cityc": 200,
        "cityb-cityc": 180,
        "citya-cityd": 250,
    }
    return fares.get(route, 100)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/passenger', methods=['GET', 'POST'])
def passenger():
    message = ""
    matched = []
    if request.method == 'POST':
        action = request.form['action']
        bus_no = int(request.form['bus_no'])
        source = request.form['source'].lower()
        destination = request.form['destination'].lower()

        bus = next((b for b in buses if b.bus_no == bus_no and b.source == source and b.destination == destination), None)
        if not bus:
            bus = Bus(bus_no, source, destination, 5)
            buses.append(bus)
            save_buses()

        if action == 'Book':
            name = request.form['name']
            seat_no = int(request.form['seat_no'])
            if len(bus.booked_seats) < bus.seats:
                amount = calculate_fare(source, destination)
                return render_template("payment.html",
                    bus_no=bus_no,
                    source=source,
                    destination=destination,
                    name=name,
                    seat_no=seat_no,
                    amount=amount
                )
            else:
                bus.waiting_list.append(name)
                save_buses()
                message = f"🕒 Bus full. {name} added to waiting list."

        elif action == 'Cancel':
            seat_no = int(request.form['seat_no'])
            message = bus.cancel_ticket(seat_no)

        elif action == 'Search':
            matched = [b for b in buses if b.source == source and b.destination == destination]

    return render_template("passenger.html", buses=buses, message=message, results=matched)

@app.route('/payment', methods=['POST'])
def payment():
    bus_no = int(request.form['bus_no'])
    source = request.form['source']
    destination = request.form['destination']
    name = request.form['name']
    seat_no = int(request.form['seat_no'])
    amount = int(request.form['amount'])

    bus = next((b for b in buses if b.bus_no == bus_no and b.source == source and b.destination == destination), None)
    if not bus:
        return "❌ Bus not found", 404

    message = bus.book_ticket(name, seat_no)
    if "✅" in message:
        download_link = url_for('download_ticket', bus_no=bus_no, seat_no=seat_no)
        return render_template(
            "payment_success.html",
            message=message,
            amount=amount,
            download_link=download_link
        )
    else:
        return message

@app.route('/download_ticket/<int:bus_no>/<int:seat_no>')
def download_ticket(bus_no, seat_no):
    load_buses()
    bus = next((b for b in buses if b.bus_no == bus_no), None)
    seat_no_str = str(seat_no)
    if not bus:
        return "❌ Bus not found!", 404

    if seat_no_str not in bus.booked_seats:
        return "❌ Ticket not found!", 404

    name = bus.booked_seats[seat_no_str]
    ticket_text = (
        f"Bus Ticket\n"
        f"------------------\n"
        f"Bus Number: {bus.bus_no}\n"
        f"From: {bus.source.capitalize()}\n"
        f"To: {bus.destination.capitalize()}\n"
        f"Passenger Name: {name}\n"
        f"Seat Number: {seat_no}\n"
        f"Status: Confirmed\n\n"
        f"Thank you for booking with us!"
    )

    response = make_response(ticket_text)
    response.headers['Content-Type'] = 'text/plain'
    response.headers['Content-Disposition'] = f'attachment; filename=ticket_bus{bus_no}_seat{seat_no}.txt'
    return response

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = ""
    if request.method == 'POST':
        if request.form['username'] == ADMIN_USERNAME and request.form['password'] == ADMIN_PASSWORD:
            session['admin'] = True
            return redirect(url_for('admin'))
        else:
            error = "❌ Invalid credentials"
    return render_template("login.html", error=error)

@app.route('/admin')
def admin():
    if not session.get('admin'):
        return redirect(url_for('login'))
    return render_template("admin.html", buses=buses)

@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect(url_for('index'))

@app.route('/export')
def export():
    if not session.get('admin'):
        return redirect(url_for('login'))

    csv_data = "Bus Number,Source,Destination,Total Seats,Booked Seats,Waiting List\n"
    for bus in buses:
        csv_data += f"{bus.bus_no},{bus.source},{bus.destination},{bus.seats},{len(bus.booked_seats)},{len(bus.waiting_list)}\n"

    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=buses_report.csv"}
    )

if __name__ == '__main__':
    app.run(debug=True)
