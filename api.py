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



from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
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

@app.route('/api/excisesearch', methods=['GET'])
def excisesearch():
    data = request.json
    number_plate = data.form.get('number_plate')

    if not number_plate:
        return jsonify({"error": "Number plate not provided"}), 400

    # Search the MongoDB collection for the matching number plate
    result = collection.find_one({"NUMBER_PLATE": number_plate})

    if result:
        # Remove the MongoDB _id field from the result
        result.pop('_id', None)
        return jsonify(result)
    else:
        return jsonify({"error": "Vehicle not found"}), 404

@app.route('/api/cplcsearch', methods=['GET'])
def cplcsearch():
    return jsonify({"message": "CPLC Search endpoint"})

if __name__ == '__main__':
    app.run(debug=True)

