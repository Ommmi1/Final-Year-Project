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

from bson import json_util


@app.route('/api/excisesearch', methods=['POST'])
def excisesearch():
    # Get the JSON data from the POST request
    data = request.json

    # Extract the number_plate from the JSON data
    number_plate = data.get('NUMBER_PLATE')

    if not number_plate:
        return jsonify({"error": "Number plate not provided"}), 400

    # Search the MongoDB collection for the matching number plate
    result = collection.find_one({"NUMBER_PLATE": number_plate})

    if result:
        # Convert ObjectId to a string representation
        result['_id'] = str(result['_id'])

        # Extract all the fields from the MongoDB document
        attributes = ["SERIAL_NO", "NUMBER_PLATE", "MAKE", "REG_DATE", "TAX_PAYMENT",
                      "ENGINE_NO", "VEHICLE_MODEL", "BODY_TYPE", "OWNER_NAME", "MODEL_YEAR",
                      "SEATING_CAPACITY", "CPLC", "SAFE_CUSTODY", "HORSE_POWER", "CLASS_OF_VEHIVLE"]
        filtered_result = {attr: result.get(attr) for attr in attributes}

        return json_util.dumps(filtered_result) ,200, {'Content-Type': 'application/json'} # Serialize the result using bson.json_util.dumps
    else:
        return jsonify({"error": "Vehicle not found"}), 404
    

@app.route('/api/cplcsearch', methods=['POST'])
def cplcsearch():
    # Get the JSON data from the POST request
    data = request.json

    # Extract the number_plate from the JSON data
    number_plate = data.get('NUMBER_PLATE')

    if not number_plate:
        return jsonify({"error": "Number plate not provided"}), 400

    # Search the MongoDB collection for the matching number plate
    result = collection.find_one({"NUMBER_PLATE": number_plate})

    if result:
        # Convert ObjectId to a string representation
        result['_id'] = str(result['_id'])

        # Extract all the fields from the MongoDB document
        attributes = [ "CPLC"]
        filtered_result = {attr: result.get(attr) for attr in attributes}

        return json_util.dumps(filtered_result) ,200, {'Content-Type': 'application/json'} # Serialize the result using bson.json_util.dumps
    else:
        return jsonify({"error": "Vehicle not found"}), 404


# @app.route('/api/cplcsearch', methods=['GET'])
# def cplcsearch():
#     return jsonify({"message": "CPLC Search endpoint"})


# @app.route('/exciseandcplc', methods=['POST', 'GET'])
# def exciseandcplc():
#     if request.method == 'POST':
#         number_plate = request.form['number_plate']  # Use square brackets to access form data
#         vehicle_info = collection.find_one({"NUMBER_PLATE": number_plate})
        
#         if vehicle_info:
#             # vehicle_info.pop('_id', None)
#             message = "Vehicle information:"
#             return render_template('exciseandcplc.html', message=message, vehicle_info=vehicle_info)

#         else:
#             message = "Vehicle not found"
#             # Process and display the vehicle_info dictionary as needed

#         # return render_template('exciseandcplc.html', message=message, vehicle_info=vehicle_info)

#     return render_template('search_form.html')

# --------------------------------------------------------------------------------------------------

# @app.route('/exciseandcplc', methods=['POST', 'GET'])
# def exciseandcplc():
#     if request.method == 'POST':
#         number_plate = request.form['number_plate']  # Use square brackets to access form data
#         vehicle_info = collection.find_one({"NUMBER_PLATE": number_plate})
        
#         if vehicle_info:
#             # vehicle_info.pop('_id', None)
#             message = "Vehicle information:"
#             return render_template('exciseandcplc.html', message=message, vehicle_info=vehicle_info)

#         else:
#             message = "Vehicle not found"
#             # Process and display the vehicle_info dictionary as needed

#         return render_template('exciseandcplc.html', message=message, vehicle_info=vehicle_info)
    
#     return render_template('search_form.html')

# # -----------------------------------------------------------------------------------------------------

# @app.route('/cplc', methods=['POST', 'GET'])
# def cplc():
#     if request.method == 'POST':
#         number_plate = request.form['number_plate']  # Use square brackets to access form data
#         vehicle_info = collection.find_one({"NUMBER_PLATE": number_plate})
        
#         if vehicle_info:
#             # vehicle_info.pop('_id', None)
#             message = "Vehicle information:"
#             return render_template('cplcresult.html', message=message, vehicle_info=vehicle_info)

#         else:
#             message = "Vehicle not found"
#             # Process and display the vehicle_info dictionary as needed

#         return render_template('cplcresult.html', message=message, vehicle_info=vehicle_info)

#     return render_template('search_form2.html')

# # -----------------------------------------------------------------------------------------------------
# @app.route('/')
# def index():
#     return render_template('home.html')
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
    app.run(debug=True,host='127.0.0.2',port=5000)