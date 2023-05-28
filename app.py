from flask import Flask, request, render_template, redirect ,url_for,abort
from flask_sqlalchemy import SQLAlchemy
from models import db
from flask_migrate import Migrate
from datetime import datetime
import pytz
from flask import render_template, flash
from flask import Flask, render_template, redirect, url_for

from urllib.parse import urlparse
# from app import app, db
rfid_gps_data=[]
import flask_login
from flask_login import login_user
from flask_login import login_required
from flask_login import current_user
from flask_login import logout_user
from flask_login import UserMixin



from werkzeug.security import check_password_hash,generate_password_hash
login_manager = flask_login.LoginManager()






# timestamp_str = datetime.utcnow()
# # date_time=timestamp_str.strftime("%Y-%m-%d %H:%M:%S")
# utc_time = timezone('UTC').localize(timestamp_str)
karachi_timezone = pytz.timezone('Asia/Karachi')
utc_time = datetime.utcnow()
karachi_time = utc_time.astimezone(karachi_timezone)

app = Flask(__name__)
app.secret_key = '13565f86f10f02e43ee54f23cbfe77cb'
app.static_folder = 'static'
app.static_url_path = '/static'
login_manager.init_app(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vehicle_tracking.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)



class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

def is_authenticated(self):
    return True

def is_active(self):
    return True

def is_anonymous(self):
    return False
    
def is_admin(self):
    return True

def get_id(self):
    return str(self.id)


# admin = User(username='admin', password=admin_password, email='a@g.com', is_admin=True)

# db.session.add(admin)
# db.session.commit()

class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rfid_tag = db.Column(db.String(50), unique=True, nullable=False)
    number_plate = db.Column(db.String(50), unique=True, nullable=False)

class Registration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    cnic = db.Column(db.String(50), unique=True, nullable=False)
    engine_number = db.Column(db.String(50), nullable=False)
    number_plate = db.Column(db.String(50), db.ForeignKey('vehicle.number_plate'))
    rfid_tag = db.Column(db.String(50), unique=True, nullable=False)

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lat = db.Column(db.Float, nullable=False)
    lng = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False,default=karachi_time)
    number_plate = db.Column(db.String(50), db.ForeignKey('vehicle.number_plate'))




@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    if request.method == 'POST':
        number_plate = request.form['number_plate']
        # retrieve the vehicle information from the database
        vehicle = Vehicle.query.filter_by(number_plate=number_plate).first()
        if vehicle:
            # if the vehicle is found, retrieve its latest location from the database
            location = Location.query.filter_by(number_plate=number_plate).order_by(Location.timestamp.desc()).first()
            # display the vehicle and location information
            return render_template('view_rfid.html', vehicle=vehicle, location=location)
        else:
            # if the vehicle is not found, display an error message
            return render_template('search.html', error='Vehicle not found')
    else:
        # if the request method is GET, display the search form
        return render_template('search.html')
    

@app.route('/view_rfid', methods=['GET', 'POST'])
@login_required
def view_rfid():
    if request.method == 'POST':
        number_plate = request.form['number_plate']
        # retrieve the vehicle information from the database
        vehicle = Vehicle.query.filter_by(number_plate=number_plate).first()
        if vehicle:
            # if the vehicle is found, retrieve its associated RFID from the database
            rfid = Registration.query.filter_by(number_plate=number_plate).first().rfid_tag
            # display the vehicle and RFID information
            return render_template('view_rfid.html', vehicle=vehicle, rfid=rfid)
        else:
            # if the vehicle is not found, display an error message
            return render_template('view_rfid.html', error='Vehicle not found')
    else:
        # if the request method is GET, display the search form
        return render_template('view_rfid.html')



@app.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    if request.method == 'POST':
        name = request.form['name']
        cnic = request.form['cnic']
        engine_number = request.form['engine_number']
        number_plate = request.form['number_plate']
        rfid_tag = request.form['rfid_tag']
        
        # check if the number plate or rfid tag already exist in the database
        if db.session.query(Vehicle).filter_by(number_plate=number_plate).first() or db.session.query(Registration).filter_by(rfid_tag=rfid_tag).first():
            return render_template('register.html', error='Vehicle or RFID already exists')
        
        # create new vehicle and registration objects
        vehicle = Vehicle(rfid_tag=rfid_tag, number_plate=number_plate)
        registration = Registration(name=name, cnic=cnic, engine_number=engine_number, number_plate=number_plate, rfid_tag=rfid_tag)
        
        # add the new objects to the database
        db.session.add(vehicle)
        db.session.add(registration)
        db.session.commit()
        
        return render_template('register.html', success='Vehicle registered successfully')
    else:
        return render_template('register.html')


@app.route('/search_user', methods=['GET', 'POST'])
@login_required
def search_user():
    if request.method == 'POST':
        cnic = request.form['cnic']
        # retrieve the user information from the database
        registrations = db.session.query(Registration).filter_by(cnic=cnic).first()
        if registrations:
            # if the user is found, display their information
            return render_template('view_user.html', registrations=registrations)
        else:
            # if the user is not found, display an error message
            return render_template('search_user.html', error='User not found')
    else:
        # if the request method is GET, display the search form
        return render_template('search_user.html')


@app.route('/all_vehicles')
@login_required
def all_vehicles():
    vehicles = Registration.query.all()
    return render_template('vehicles.html', vehicles=vehicles)


@app.route('/vehicle_location', methods=['GET', 'POST'])
@login_required
def vehicle_location():
    if request.method == 'POST':
        number_plate = request.form['number_plate']
        vehicle = Vehicle.query.filter_by(number_plate=number_plate).first()
        if vehicle:
            locations = Location.query.filter_by(number_plate=number_plate).all()
            if locations:
                return render_template('vehicle_location.html', locations=locations)
            else:
                return render_template('vehicle_location.html', error='No locations found for this vehicle.')
        else:
            return render_template('search.html', error='Vehicle not found')
    else:
        return render_template('search.html')




# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         user = User.query.filter_by(username=username).first()
#         if user and user.password == password:
#             login_user(user)
#             return redirect(url_for('vehicle_location'))
#         else:
#             flash('Invalid username or password')
#     return render_template('login.html')
# --------------------------------------------------

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if current_user.is_authenticated:
#         return redirect(url_for('admin_dashboard'))

#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         user = User.query.filter_by(username=username).first()
#         if user is None or not user.password==password:
#             flash('Invalid username or password')
#             return redirect(url_for('login'))
#         login_user(user)
#         next_page = request.args.get('next')
#         if not next_page or urlparse(next_page).netloc != '':
#             next_page = url_for('vehicle_location')
#         return redirect(next_page)
    # return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        remember_me = bool(request.form.get('remember_me'))
        user = User.query.filter_by(username=username).first()
        if user is None or not user.password==password:
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=remember_me)
        if user.is_admin:
            return redirect(url_for('admin_dashboard'))
        else:
            return redirect(url_for('user_main'))
    return render_template('login.html', title='Sign In')




@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/admin_dashboard')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        abort(403)
    users = User.query.all()
    return render_template('admin_dashboard.html',users=users)



@app.route('/create_officer', methods=['GET', 'POST']) # type: ignore
@login_required
def create_officer():
    if not current_user.is_admin:
        abort(403)
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        is_admin = False
        
        # check if the number plate or rfid tag already exist in the database
        if db.session.query(User).filter_by(username=username).first() or db.session.query(User).filter_by(email=email).first():
            return render_template('create_officer.html', error='username or email already exists')
        
        # create new vehicle and registration objects
        user = User(username=username, password=password, email=email, is_admin=is_admin)

        
        # add the new objects to the database
        db.session.add(user)
        db.session.commit()
        flash('Officer created successfully!')
        return render_template('create_officer.html', success='Officer registered successfully')
    else:
        return render_template('create_officer.html')


 


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    if not current_user.is_admin:
        abort(403)
    user = User.query.get_or_404(id)
    if request.method == 'POST':
        user.username = request.form['username']
        user.password = request.form['password']
        user.email = request.form['email']
        user.is_admin = request.form.get('is_admin') == 'on'
        db.session.commit()
        return redirect(url_for('admin_dashboard'))
    return render_template('update.html', user=user)

 


@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    if not current_user.is_admin:
        abort(403)
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('admin_dashboard'))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about_us')
def about_us():
    return render_template('about_us.html')

@app.route('/user_main')
def user_main():
    return render_template('user_main.html')



@app.route('/data/', methods=['POST'])
def receive_data():
    rfid = request.form['uid']
    lat = request.form['lat']
    lng = request.form['lng']
    vehicle = Vehicle.query.filter_by(rfid_tag=rfid).first()
    if vehicle:
        number_plate = vehicle.number_plate
        location = Location(lat=lat, lng=lng, timestamp=karachi_time, number_plate=number_plate)
        db.session.add(location)
        db.session.commit()
        return 'Inserted'
    else:
        return 'Vehicle not found'


if __name__ == '__main__':
    # db.create_all()
    # app.run(debug=True)
    # app.run(debug=True, host='192.168.43.206',port=5000)
    app.run(debug=True)



