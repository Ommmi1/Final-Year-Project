# from flask import Flask, render_template,request,jsonify
# import pymongo

# app = Flask(__name__)
# # MongoDB connection setup
# MONGO_URI = "mongodb://localhost:27017"  # Update with your MongoDB connection string
# mongo_client = pymongo.MongoClient(MONGO_URI)
# db = mongo_client["vehicle_info"]  # Replace "your_database_name" with the actual name of your MongoDB database
# collection = db["VehicleOwnerInfo"]

# @app.route('/api')
# def home():
#     return render_template('home.html')

# @app.route('/api/excisesearch',methods=['GET', 'POST'])
# def excisesearch():
#     if request.method == 'POST':
#         number_plate = request.form.get('number_plate')
#         result = collection.find_one({"NUMBER_PLATE": number_plate})
#         if result:
#             return render_template('excisesearch.html', result=result)
#         else:
#             return jsonify({"error": "Vehicle not found"}), 404

#     return render_template('excisesearch.html')

# @app.route('/api/cplcsearch')
# def cplcsearch():
#     return render_template('cplcsearch.html')

# if __name__ == '__main__':
#     app.run(debug=True)



from flask import Flask, request, jsonify, render_template
import requests
import json
from pymongo import MongoClient
app = Flask(__name__)
app.secret_key = 'mysecretkey'

app.config['MONGO_URI'] = 'mongodb+srv://omersidd93:Omer1234@cluster0.vvhwsll.mongodb.net/'
mongo = MongoClient(app.config['MONGO_URI'])
db = mongo.get_database('vehicle_info')
collection = db["VehicleOwnerInfo"]
# MongoDB connection setup
# MONGO_URI = "mongodb://localhost:27017/vehicle_info"  # Update with your MongoDB connection string
# mongo_client = pymongo.MongoClient(MONGO_URI)
# db = mongo_client["vehicle_info"]  # Replace "your_database_name" with the actual name of your MongoDB database
# collection = db["VehicleOwnerInfo"]

# @app.route('/api/excisesearch', methods=['POST'])
# def excisesearch():
#     # Get the JSON data from the POST request
#     data = request.json

#     # Extract the number_plate from the JSON data
#     number_plate = data.get('number_plate')

#     if not number_plate:
#         return jsonify({"error": "Number plate not provided"}), 400

#     # Search the MongoDB collection for the matching number plate
#     result = collection.find_one({"NUMBER_PLATE": number_plate})

#     if result:
#         # Remove the MongoDB _id field from the result
#         result.pop('_id', None)
#         return jsonify(result)
#     else:
#         return jsonify({"error": "Vehicle not found"}), 404

# @app.route('/api/cplcsearch', methods=['GET'])
# def cplcsearch():
#     return jsonify({"message": "CPLC Search endpoint"})

# @app.route('/exciseandcplc', methods=['POST', 'GET'])
# def exciseandcplc():
#     if request.method == 'POST':
#         data = request.json
#         number_plate = data.get('NUMBER_PLATE')
#         vehicle_info = search_vehicle_info(number_plate)

#         if vehicle_info:
#             message = "Vehicle information:"
#         else:
#             message = "Vehicle not found"
#             # Process and display the vehicle_info dictionary as needed

#         return render_template('exciseandcplc.html', message=message, vehicle_info=vehicle_info)

#     return render_template('search_form.html')  # Display the search form for GET requests

# def search_vehicle_info(number_plate):
#     # API endpoint URL
#     url = "https://web-production-39b9.up.railway.app/api/excisesearch"
#     headers = {"Content-Type": "application/json"}
#     # JSON payload containing the number_plate
#     payload = {"NUMBER_PLATE": number_plate}  # Ensure 'number_plate' key matches the API's expected key

#     try:
#         # Make the POST request with JSON data and set the 'Content-Type' header to 'application/json'
#         response = requests.post(url, data=json.dumps(payload), headers=headers)
#         response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes

#         try:
#             # Attempt to parse the JSON data from the response
#             response_data = response.json()
#         except ValueError:
#             # Failed to parse JSON, return None indicating an error
#             print("Invalid JSON data received from the API.")
#             return None

#         # Check if the response contains vehicle information or an error message
#         if "error" in response_data:
#             # Vehicle not found
#             return None
#         else:
#             # Vehicle information found
#             return response_data

#     except requests.exceptions.RequestException as e:
#         # Handle any exceptions that occurred during the request
#         print(f"An error occurred: {e}")
#         return None
@app.route('/exciseandcplc', methods=['POST', 'GET'])
def exciseandcplc():
    if request.method == 'POST':
        number_plate = request.form['number_plate']  # Use square brackets to access form data
        vehicle_info = collection.find_one({"NUMBER_PLATE": number_plate})
        
        if vehicle_info:
            # vehicle_info.pop('_id', None)
            message = "Vehicle information:"
        else:
            message = "Vehicle not found"
            # Process and display the vehicle_info dictionary as needed

        return render_template('exciseandcplc.html', message=message, vehicle_info=vehicle_info)

    return render_template('search_form.html')


# def get_vehicle_info(number_plate):
#     # Search the MongoDB collection for the matching number plate
#     result = collection.find_one({"NUMBER_PLATE": number_plate})

#     if result:
#         # Remove the MongoDB _id field from the result
#         result.pop('_id', None)
#         return result
#     else:
#         return None
if __name__ == '__main__':
    app.run(debug=True)