RFID Vehicle Tracking System using GMaps and Flask Application
This is a web application built using Flask, SQLAlchemy, and GMaps to track vehicles using RFID technology. The application allows users to view the location of vehicles in real-time on Google Maps.

Features
Vehicle tracking using RFID technology
Real-time location updates
Integration with Google Maps
User-friendly dashboard
Easy to deploy and use
Installation
Clone the repository to your local machine using the command:

bash
Copy code
git clone https://github.com/
Install the required packages using the command:

Copy code
pip install -r requirements.txt
Configure your database settings in the config.py file.

Run the migrations to create the necessary tables in the database using the command:

Copy code
flask db upgrade
Start the application using the command:

arduino
Copy code
flask run
Usage
Navigate to http://localhost in your web browser to access the home page.

Click on the "Login" button to login with your credentials.

Once logged in, you will be directed to the dashboard where you can view the location of your vehicles on Google Maps.

To add a new vehicle, click on the "Add Vehicle" button and fill in the details.

To view the location of a vehicle, click on the "View Location" button next to the vehicle.

Technology Stack
Python
Flask
SQLAlchemy
Google Maps API
Contributing
Contributions are welcome! Please feel free to submit a pull request.

License
This project is licensed under the MIT License - see the LICENSE file for details.




