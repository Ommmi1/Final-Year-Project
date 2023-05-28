from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rfid_tag = db.Column(db.String(50), unique=True, nullable=False)
    number_plate = db.Column(db.String(50), unique=True, nullable=False)

    def __init__(self, rfid_tag, number_plate):
        self.rfid_tag = rfid_tag
        self.number_plate = number_plate



class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lat = db.Column(db.Float, nullable=False)
    lng = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    number_plate = db.Column(db.String(50), db.ForeignKey('vehicle.number_plate'))

    def __init__(self, lat, lng, timestamp, number_plate):
        self.lat = lat
        self.lng = lng
        self.timestamp = timestamp
        self.number_plate = number_plate


class Registration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    cnic = db.Column(db.String(50), unique=True, nullable=False)
    engine_number = db.Column(db.String(50), nullable=False)
    number_plate = db.Column(db.String(50), db.ForeignKey('vehicle.number_plate'))
    rfid_tag = db.Column(db.String(50), unique=True, nullable=False)

    def __init__(self, name, cnic, engine_number, number_plate, rfid_tag):
        self.name = name
        self.cnic = cnic
        self.engine_number = engine_number
        self.number_plate = number_plate
        self.rfid_tag = rfid_tag

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def __init__(self, username, password,email,is_admin):
        self.username = username
        self.password = password
        self.is_admin = is_admin
        self.email = email
    

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)


    def __repr__(self):
        return '<User %r>' % self.username

