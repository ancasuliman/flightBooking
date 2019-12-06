from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from typing import List, Dict
from sqlalchemy import select
import json
import requests
import sys
import rstr

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@db:3306/airplane_service'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Flight(db.Model):
    __tablename__ = 'Flight'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    source = db.Column(db.String(10), nullable=False)
    dest = db.Column(db.String(10), nullable=False)
    departureDay = db.Column(db.Integer, nullable=False)
    departureHour = db.Column(db.Integer, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    numberOfSeats = db.Column(db.Integer, nullable=False)
    flightID = db.Column(db.String(10), nullable=False, unique=True)
    reservedSeats = db.Column(db.Integer, default=0)

    def __init__(self, source=None, dest=None, departureDay=None, departureHour=None, duration=None, numberOfSeats=None, flightID=None, reservedSeats=None):
        self.source = source
        self.dest = dest
        self.departureDay = departureDay
        self.departureHour = departureHour
        self.duration = duration
        self.numberOfSeats = numberOfSeats
        self.flightID = flightID
        self.reservedSeats = reservedSeats
    
    @property
    def serialize(self):
        return {
            'id': self.id,
            'source': self.source,
            'dest': self.dest,
            'departureDay': self.departureDay,
            'departureHour': self.departureHour,
            'duration': self.duration,
            'numberOfSeats': self.numberOfSeats,
            'flightID': self.flightID,
            'reservedSeats': self.reservedSeats
        }

    def __repr__(self):
        return f"Flight('{self.id}', '{self.source}', '{self.dest}', '{self.departureDay}', '{self.departureHour}', '{self.duration}', '{self.numberOfSeats}', '{self.flightID}')"

def random_reservationID():
    rand = rstr.xeger(r'RID\d\d\d\d')
    
    return rand

class Reservation(db.Model):
    __tablename__ = 'Reservation'
    id = db.Column(db.Integer, primary_key=True)
    flightIDs = db.Column(db.String(300), nullable=False)
    reservationID = db.Column(db.String(10), nullable=False, unique=True)

    def __init__(self, reservationID=None, flightIDs=None):
        self.reservationID = reservationID
        self.flightIDs = flightIDs
    
    @property
    def serialize(self):
        return {
            'reservationID': self.reservationID,
            'flightIDs': self.flightIDs
        }

    def __repr__(self):
        return f"Reservation('{self.reservationID}', '{self.flightIDs}')"
    
class Ticket(db.Model):
    __tablename__ = 'Ticket'
    id = db.Column(db.Integer, primary_key=True)
    reservationID = db.Column(db.Integer, db.ForeignKey('Reservation.reservationID'), nullable=False, unique=True)

    def __init__(self, reservationID=None):
        self.reservationID = reservationID
    
    @property
    def serialize(self):
        return {
            'id': self.id,
            'reservationID': self.reservationID
        }

    def __repr__(self):
        return f"Ticket('{self.id}', '{self.reservationID}')"

@app.route("/")
def index():
    return "Welcome to flight reservation system!"

# routes for flights - GET, POST, DELETE
@app.route('/flights/', methods=["POST"])
def add_flight():
    content = request.json
    flight = Flight(
        source = content["source"],
        dest = content["dest"],
        departureDay = content["departureDay"],
        departureHour = content["departureHour"],
        duration = content["duration"],
        numberOfSeats = content["numberOfSeats"],
        flightID = content["flightID"],
        reservedSeats=0
    )
    db.session.add(flight)
    db.session.commit()

    return jsonify(flight.serialize)
    
@app.route("/flights/", methods=['GET'])
def get_flights():
    json_response = {}
    
    flights = Flight.query.all()
    for flight in flights:
        json_response[flight.id] = [
                                        flight.source, 
                                        flight.dest,
                                        flight.departureHour, 
                                        flight.departureDay,
                                        flight.duration, 
                                        flight.numberOfSeats,
                                        flight.flightID,
                                        flight.reservedSeats
                                    ]
    
    return json_response

@app.route("/flights/<flight_id>", methods=["DELETE"])
def delete_flight(flight_id):
    to_delete = Flight.query.filter_by(flightID=flight_id).first()
    db.session.delete(to_delete)
    db.session.commit()

    return jsonify(to_delete.serialize)

@app.route("/optimalRoute", methods=["GET"])
def get_optimal_route():
    resp = dict()
    resp['flights'] = []
    resp['flightIDs'] = []

    nodes = set()

    source = request.args.get('source')
    destination = request.args.get('destination')
    max_flights = int(request.args.get('maxFlights'))
    departure_day = int(request.args.get('departureDay'))

    sol = []

    flights_from_source = Flight.query.\
        filter_by(source=source, departureDay=departure_day)
    connections = db.session.query(Flight).filter(Flight.departureDay >= departure_day)

    for connection in connections:
        nodes.add(connection.source)
        nodes.add(connection.dest)
    
    for source_flight in flights_from_source:
        updated_distance = dict()
        distance = dict()
        parent = dict()

        for node in nodes:
            distance[node] = sys.maxsize
            updated_distance[node] = sys.maxsize
        
        distance[source_flight.source] = 0
        updated_distance[source_flight] = 0

        while max_flights > 0:
            for connection in connections:
                edge_start = connection.source
                edge_end = connection.dest
                cost = sys.maxsize

                if distance[edge_start] != sys.maxsize:
                    if connection.id == source_flight.id:
                        cost = connection.duration
                    elif connection.id != source_flight.id and connection.source != source_flight.source:
                        arrival_day = parent[edge_start].departureDay + parent[edge_start].departureDay / 24
                        arrival_hour = (parent[edge_start].departureHour + parent[edge_start].duration) % 24

                        if connection.departureDay == arrival_day and connection.departureHour > arrival_hour:
                            cost = connection.departureHour - arrival_hour
                        elif connection.departureDay > arrival_day:
                            cost = 24 - arrival_hour + (departure_day - arrival_day - 1) * 24 + connection.departureHour
                        
                        cost += connection.duration
                    
                    if distance[edge_start] + cost < distance[edge_end]:
                        parent[edge_end] = connection
                        updated_distance[edge_end] = distance[edge_start] + cost
        
            distance = updated_distance
            max_flights -= 1
        
        sol.append((distance, parent))
    
    if sol != []:
        dist_to_destination = [pair[0][destination] for pair in sol]
        index_best_route = dist_to_destination.index(min(dist_to_destination))

        if min(dist_to_destination) != sys.maxsize:
            query_flights = list(sol[index_best_route][1].values())
            resp['flights'] = [flight.serialize for flight in query_flights]
            resp['flightIDs'] = [flight.flightID for flight in query_flights]
        
    return jsonify(resp)

# routes for reservations - GET, POST
@app.route("/reservations/", methods=['GET'])
def get_reservations():
    json_response = {}

    reservations = Reservation.query.all()
    for reservation in reservations:
        json_response[reservation.id] = [
                                            reservation.flightIDs,
                                            reservation.reservationID
                                        ]
    
    return json_response

@app.route("/reservations/", methods=['POST'])
def add_reservation():
    content = request.json
    resp = {'reservationID': ''}

    query = db.session.query(Flight).filter(Flight.flightID.in_(content["flightIDs"]))
    flights = query.all()
    
    if len(flights) == len(content["flightIDs"]):
        reservations_possible = list(map(lambda flight: flight.reservedSeats < flight.numberOfSeats * 1.1, flights))
        
        # reservations still possible
        if all(reservations_possible):
            query.update({Flight.reservedSeats: Flight.reservedSeats + 1}, synchronize_session = False)
            db.session.commit()

            reservationID = random_reservationID()
            resp['reservationID'] = reservationID
            reservation = Reservation(reservationID=reservationID, flightIDs=",".join(content["flightIDs"]))

            db.session.add(reservation)
            db.session.commit()

    return jsonify(resp)

# routes for tickets - GET, POST
@app.route("/tickets/", methods=['POST'])
def add_ticket():
    content = request.json
    resp = {'boardingPass': ''}

    reservation_query = Reservation.query.filter_by(reservationID=content['reservationID'])

    if reservation_query != []:
        reservation = reservation_query.first()
        flightIDs = reservation.flightIDs.split(',')
        flights = db.session.query(Flight).filter(Flight.flightID.in_(flightIDs))

        ticket = Ticket(reservationID=reservation.reservationID)
        db.session.add(ticket)
        db.session.commit()

        resp['boardingPass'] = [flight.serialize for flight in flights]
    
    return jsonify(resp)

@app.route("/tickets/", methods=['GET'])
def get_tickets():
    json_response = {}

    tickets = Ticket.query.all()
    hostname: client
    for ticket in tickets:
        json_response[ticket.id] = [
                                        ticket.reservationID
                                    ]
    
    return json_response

if __name__ == '__main__':
    app.run(host='0.0.0.0')
