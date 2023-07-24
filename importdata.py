import pandas as pd
import pymongo

# MongoDB connection setup
MONGO_URI = "mongodb+srv://omersidd93:Omer1234@cluster0.vvhwsll.mongodb.net/"  # Update with your MongoDB connection string
mongo_client = pymongo.MongoClient(MONGO_URI)
db = mongo_client["vehicle_info"]  # Replace "your_database_name" with the actual name of your MongoDB database
collection = db["VehicleOwnerInfo"]  # Replace "vehicle_info" with the name of your MongoDB collection

# Path to the CSV file
csv_file_path = r"C:\Users\Omer\Desktop\Fypexciseapi\output1.csv"  # Update with the actual path to your CSV file

# Read the CSV data into a DataFrame
df = pd.read_csv(csv_file_path)

# Convert the DataFrame to a list of dictionaries (one dictionary per row)
data_list = df.to_dict(orient='records')

# Insert the data into the MongoDB collection
collection.insert_many(data_list)

print("Data imported successfully!")




# import csv

# input_file = 'DATAfyp.txt'
# output_file = 'output.csv'

# with open(input_file, 'r', newline='') as f_in:
#     reader = csv.reader(f_in)
#     header = next(reader)  # Read the header row

#     # Replace spaces with no spaces for each row
#     modified_rows = [[value.replace(' ', '') for value in row] for row in reader]

# with open(output_file, 'w', newline='') as f_out:
#     writer = csv.writer(f_out)
#     writer.writerow(header)  # Write the header row
#     writer.writerows(modified_rows)  # Write the modified rows

# print("Spaces replaced and saved to output.csv!")





# def is_valid_csv_line(line):
#     # Function to check if a line is a valid CSV line
#     # Here, we are simply checking if the line contains a comma ',' as it is a basic CSV format
#     return ',' in line

# def filter_extra_lines(input_file, output_file):
#     # Read the input text file and filter out extra lines
#     with open(input_file, 'r') as f:
#         lines = f.readlines()

#     # Filter out lines that are not valid CSV lines
#     valid_lines = [line for line in lines if is_valid_csv_line(line)]

#     # Write the filtered lines to a new CSV file
#     with open(output_file, 'w') as f:
#         f.writelines(valid_lines)

#     print("Extra lines removed successfully!")

# if __name__ == "__main__":
#     input_file = "output.csv"  # Replace with the path to your input text file in CSV format
#     output_file = "output1.csv"  # Replace with the desired output CSV file name

#     filter_extra_lines(input_file, output_file)
