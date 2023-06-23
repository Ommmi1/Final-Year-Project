from flask import Flask, request, render_template, redirect ,url_for,abort
from datetime import datetime
import pytz
from flask import render_template, flash
import re
from flask_login import login_user
from flask_login import login_required
from flask_login import current_user
from flask_login import logout_user
from flask_login import UserMixin
from flask_login import LoginManager
from pymongo import MongoClient
from bson.objectid import ObjectId
from passlib.hash import bcrypt
from werkzeug.security import generate_password_hash,check_password_hash
# from pymongo import MongoClient

# # Connect to MongoDB
# client = MongoClient('mongodb://localhost:27017/')

# # Access the 'vehicle_tracking' database
# db = client['vehicle_tracking']

karachi_timezone = pytz.timezone('Asia/Karachi')
utc_time = datetime.utcnow()
karachi_time = utc_time.astimezone(karachi_timezone)

class User(UserMixin):
    def __init__(self, user_data):
        self.id = str(user_data['_id'])
        self.username = user_data['username']
        self.email = user_data['email']
        self.is_admin = user_data['is_admin']

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username

    def is_admin(self):
        return True

    @staticmethod
    def validate_login(password_hash, password):
        return check_password_hash(password_hash, password)


def is_admin():
    return True

app = Flask(__name__)
app.secret_key = '13565f86f10f02e43ee54f23cbfe77cb'
# app.secret_key = 'mysecretkey'
app.static_folder = 'static'
app.static_url_path = '/static'

app.config['MONGO_URI'] = 'mongodb://localhost:27017/vehicle_tracking'
mongo = MongoClient(app.config['MONGO_URI'])
db = mongo.get_database('vehicle_tracking')
users = db['users']
vehicles = db['vehicles']
registrations = db['registrations']
locations = db['locations']
login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    if request.method == 'POST':
        number_plate = request.form['number_plate']
        # retrieve the vehicle information from the database
        vehicle = vehicles.find_one({'number_plate': number_plate})
        if vehicle:
            # if the vehicle is found, retrieve its latest location from the database
            location = locations.find_one({'number_plate': number_plate}, sort=[('timestamp', -1)])
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
        # Retrieve the vehicle information from the database
        vehicle = vehicles.find_one({'number_plate': number_plate})
        if vehicle:
            # If the vehicle is found, retrieve its associated RFID from the database
            registration = registrations.find_one({'number_plate': number_plate})
            if registration:
                rfid = registration['rfid_tag']
                # Display the vehicle and RFID information
                return render_template('view_rfid.html', vehicle=vehicle, rfid=rfid)
            else:
                # If the registration is not found, display an error message
                return render_template('view_rfid.html', error='Registration not found')
        else:
            # If the vehicle is not found, display an error message
            return render_template('view_rfid.html', error='Vehicle not found')
    else:
        # If the request method is GET, display the search form
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

        # Check if the CNIC format is valid
        cnic_pattern = r'^\d{5}-\d{7}-\d{1}$'
        if not re.match(cnic_pattern, cnic):
            return render_template('register.html', error='Invalid CNIC format. Please use the format: *****-*******-*')

        # Check if the number plate format is valid
        number_plate_pattern = r'^[A-Z]{3}-\d{3}$'
        if not re.match(number_plate_pattern, number_plate):
            return render_template('register.html', error='Invalid number plate format. Please use the format: ABC-123')

        # Check if the number plate or RFID tag already exists in the database
        if vehicles.find_one({'number_plate': number_plate}) and registrations.find_one({'rfid_tag': rfid_tag}) and registrations.find_one({'cnic': cnic}):
            return render_template('register.html', error='Vehicle or RFID already exists')

        # Create new vehicle and registration documents
        vehicle = {
            'rfid_tag': rfid_tag,
            'number_plate': number_plate
        }
        registration = {
            'name': name,
            'cnic': cnic,
            'engine_number': engine_number,
            'number_plate': number_plate,
            'rfid_tag': rfid_tag
        }

        # Insert the new documents into the respective collections
        vehicles.insert_one(vehicle)
        registrations.insert_one(registration)
        flash('Vehicle registered successfully!')


        return render_template('register.html', success='Vehicle registered successfully')
    else:
        return render_template('register.html')

def create_admin():
    admin_username = 'admin'
    admin_password = 'admin'
    admin_email = 'admin@example.com'

    admin = users.find_one({'username': admin_username})
    if admin:
        print("Admin user already exists")
        return

    hashed_password = generate_password_hash(admin_password)

    admin_user = {
        'username': admin_username,
        'password': hashed_password,
        'email': admin_email,
        'is_admin': True
    }

    users.insert_one(admin_user)
    print("Admin user created successfully")
# create_admin()





@app.route('/search_user', methods=['GET', 'POST'])
@login_required
def search_user():
    if request.method == 'POST':
        cnic = request.form['cnic']

        # Check if the CNIC format is valid
        cnic_pattern = r'^\d{5}-\d{7}-\d{1}$'
        if not re.match(cnic_pattern, cnic):
            return render_template('search_user.html', error='Invalid CNIC format. Please use the format: *****-*******-*')

        # Retrieve the user information from the database
        registration = registrations.find_one({'cnic': cnic})
        if registration:
            # If the user is found, display their information
            return render_template('view_user.html', registration=registration)
        else:
            # If the user is not found, display an error message
            return render_template('search_user.html', error='User not found')
    else:
        # If the request method is GET, display the search form
        return render_template('search_user.html')



@app.route('/all_vehicles')
@login_required
def all_vehicles():
    vehicles = registrations.find()
    return render_template('vehicles.html', vehicles=vehicles)



@app.route('/vehicle_location', methods=['GET', 'POST'])
@login_required
def vehicle_location():
    if request.method == 'POST':
        number_plate = request.form['number_plate']
        vehicle = vehicles.find_one({'number_plate': number_plate})
        number_plate_pattern = r'^[A-Z]{3}-\d{3}$'
        if not re.match(number_plate_pattern, number_plate):
            return render_template('vehicle_location.html', error='Invalid number plate format. Please use the format: ABC-123')
        if vehicle:
            location_data = locations.find({'number_plate': number_plate})
            # location_count = len(list(location_data))
            if location_data:
                location_list = []
                for loc in location_data:
                    location_list.append({
                        'lat': loc['lat'],
                        'lng': loc['lng'],
                        'timestamp': loc['timestamp']
                    })
                return render_template('vehicle_location.html', location=location_list)
            else:
                return render_template('vehicle_location.html', error='No locations found for this vehicle.')
        else:
            return render_template('search.html', error='Vehicle not found')
    else:
        return render_template('search.html')







@login_manager.user_loader
def load_user(user_id):
    user_data = users.find_one({'username': user_id})
    if user_data:
        return User(user_data)
    return None



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # remember_me = bool(request.form.get('remember_me'))
        user_data = users.find_one({'username': username})
        if user_data is None or not check_password_hash(user_data['password'], password):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        user = User(user_data)
        login_user(user)
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
    if current_user is None or not current_user.is_admin:
        abort(403)
    users_list = list(users.find())
    return render_template('admin_dashboard.html', users=users_list)



@app.route('/create_officer', methods=['GET', 'POST'])
@login_required
def create_officer():
    if not current_user.is_admin:
        abort(403)
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        is_admin = bool(request.form.get('is_admin'))

        # Check if the username or email already exist in the database
        if users.find_one({'username': username}) and users.find_one({'email': email}):
            flash('Officer Already exists!')
            return render_template('create_officer.html', error='Username or email already exists')

        # Check if the email is in the correct format
        if not email.endswith('.com'):
            return render_template('create_officer.html', error='Invalid email format')

        # Generate the password hash
        password_hash = generate_password_hash(password)

        # Create a new user object
        user = {
            'username': username,
            'password': password_hash,
            'email': email,
            'is_admin': is_admin
        }

        # Add the new user to the database
        users.insert_one(user)

        flash('Officer created successfully!')
        return render_template('create_officer.html', success='Officer registered successfully')
    else:
        return render_template('create_officer.html')



 


@app.route('/update/<string:id>', methods=['GET', 'POST'])
@login_required
def update(id):
    if not current_user.is_admin:
        abort(403)
    user = users.find_one({'_id': ObjectId(str(id))})
    if not user:
        abort(404)
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        is_admin = request.form.get('is_admin') == 'on'
        
        # Check if the updated username or email already exists in the database
        existing_user = users.find_one({'$or': [{'username': username}, {'email': email}], '_id': {'$ne': ObjectId(str(id))}})
        if existing_user:
            return render_template('update.html', user=user, error='Username or email already exists')
        
        # Hash the password before updating
        hashed_password = bcrypt.hash(password)
        
        # Update the user's information
        update_data = {
            'username': username,
            'password': hashed_password,
            'email': email,
            'is_admin': is_admin
        }
        
        # Update the user in the database
        users.update_one({'_id': ObjectId(str(id))}, {'$set': update_data})
        
        flash('User updated successfully!')
        return redirect(url_for('admin_dashboard'))
    
    return render_template('update.html', user=user)


@app.route('/delete/<string:id>', methods=['POST'])
@login_required
def delete(id):
    if not current_user.is_admin:
        abort(403)
    user = users.find_one({'_id': ObjectId(str(id))})
    if user:
        users.delete_one({'_id': ObjectId(str(id))})
        flash('User deleted successfully!')
    return redirect(url_for('admin_dashboard'))




    


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about_us')
def about_us():
    return render_template('about_us.html')

@login_required
@app.route('/user_main')
def user_main():
    return render_template('user_main.html')


@app.route('/data/', methods=['POST'])
def receive_data():
    uid = request.form.get('uid')
    lat = request.form.get('lat')
    lng = request.form.get('lng')
    print("UID:", uid)
    print("Latitude:", lat)
    print("Longitude:", lng)
    try:
        vehicle = vehicles.find_one({'rfid_tag': uid})
        if vehicle:
            number_plate = vehicle['number_plate']
            location = {
                        'lat': lat,
                        'lng': lng,
                        'timestamp': karachi_time,
                        'number_plate': number_plate
                    }
            locations.insert_one(location)
            return 'Inserted'
        else:
            return 'Vehicle not found'
    except Exception as e:
        print("Database error:", str(e))
        return 'Error accessing database'
    






if __name__ == '__main__':
    # db.create_all()
    # app.run(debug=True)
    # app.run(debug=True, host='192.168.43.202',port=5000)
    app.run(debug=True)






