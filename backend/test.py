from mongo import get_db, upload_data, clean_data
from pymongo import MongoClient
from models import Coordinate
import requests
import json
from utils import *

db = get_db()
collection = db['my_collection']

# clean_data()
# upload_data()
# # Specify the types you want to check
# for coll in db.list_collection_names():
#     print(coll)
# print(db.my_collection.count_documents({}))

# latest_result = db.my_collection.find().sort('_id', -1).limit(1)
# print(latest_result)
# flat_ids = latest_result[0] if latest_result else []

# # Define a query with the filter criteria
# query = {
# }

# # Add price and rooms filters if they are provided
# if price is not None:
#     query["price"] = {"$lte": price}
# if rooms is not None:
#     query["rooms"] = {"$gte": rooms}  # Comparing as a string

# # Fetch coordinates from MongoDB of the filtered flats
# try:
#     results = collection.find(query, {"_id": 0, "latitude": 1, "longitude": 1})

#     # Convert MongoDB cursor to list
#     coordinates = [{"latitude": result["latitude"], "longitude": result["longitude"]} for result in results]
#     print(coordinates[:5])

# except Exception as e:
#     # Return an error message if any exception is raised
#     print({"error": str(e)})

# Send a GET request to the /coordinates endpoint
# response = requests.get(f'http://localhost:8000/traditional_search?price={price}&rooms={rooms}')

# # If the request was successful, print the data
# if response.status_code == 200:
#     data = response.json()
#     print(json.dumps(data, indent=4))
# else:
#     print('Failed to fetch data:', response.status_code)

# price = 2900.0
# sqfts = 1200.0
# quality = 3.5
# rooms = 2.0

# query = {}
# if price is not None:
#     query["price"] = {"$lte": price}
# if rooms is not None:
#     query["rooms"] = {"$gte": rooms}
# if sqfts is not None:
#     query["sqfts"] = {"$gte": sqfts}
# if quality is not None:
#     query["quality"] = {"$gte": quality}
    
    
# traditional_table_fields = {"_id": 0, "latitude": 1, "longitude": 1, "price": 1, "name": 1, "sqfts": 1, "rooms": 1, "quality": 1}
# # Fetch coordinates from MongoDB of the filtered flats
# results = collection.find(query, traditional_table_fields)
# # Convert MongoDB cursor to list
# full_results = [{"latitude": result["latitude"], "longitude": result["longitude"],
#                 "price": result["price"], "name": result["name"],
#                 "sqfts": result["sqfts"], "rooms": result["rooms"],
#                 "quality": result["quality"]} for result in results]

# print(len(full_results))

# from mongo import get_db
# import pickle
# from bayesian_network import *
# from utils import prepare_bayesian_features

# db = get_db()
# collection = db['my_collection']

# # Load the Bayesian Network model
# flat_model = joblib.load("bayesian_model_userpref.pkl")

# inference = VariableElimination(flat_model)

# search_params = {"SearchRooms": 2.0, "SearchSqft": 1400.0, "SearchQuality": 3.0, "SearchPrice": 2900.0,}
# # Extract user search parameters from the request
#     # Extract user search parameters from the request
# user_search = {
#     'SearchRooms': search_params.get("SearchRooms"),
#     'SearchSqft': search_params.get("SearchSqft"),
#     'SearchQuality': search_params.get("SearchQuality"),
#     'SearchPrice': search_params.get("SearchPrice")
# }

# traditional_table_fields = {
#     "_id": 0, "latitude": 1, "longitude": 1, "price": 1, 
#     "name": 1, "sqfts": 1, "rooms": 1, "quality": 1
# }

# query = {}  # Define your query to filter flats if needed

# # Fetch coordinates from MongoDB of the filtered flats
# results = collection.find(query, traditional_table_fields)

# full_results = [{
#     "latitude": result["latitude"], "longitude": result["longitude"],
#     "price": result["price"], "name": result["name"],
#     "sqfts": result["sqfts"], "rooms": result["rooms"],
#     "quality": result["quality"]
# } for result in results]

# user_search = {
#     key: int(value) if value is not None else None
#     for key, value in user_search.items()
# }
# user_search_raw = user_search.copy()
# # Convert raw search params to states expected by Bayesian network
# user_search = {
#     key: prepare_bayesian_features(key, value)
#     for key, value in user_search.items()
# }
# full_results_df = pd.DataFrame(data=full_results, columns=["latitude", "longitude", "price", "name", 
#                                                         "sqfts", "rooms", "quality"])

# full_results = filter_flats_based_on_search(full_results_df, user_search_raw)

# # Process each flat's raw data to be compatible with Bayesian network
# processed_flats = []
# for index, flat in full_results.iterrows():
#     processed_flat = {
#         'Rooms': prepare_bayesian_features('Rooms', flat['rooms']),
#         'Sqft': prepare_bayesian_features('Sqft', flat['sqfts']),
#         'Quality': prepare_bayesian_features('Quality', flat['quality']),
#         'Price': prepare_bayesian_features('Price', flat['price'])
#     }
#     processed_flats.append({**flat, **processed_flat})
# # Score each flat based on user search and Bayesian model

# scored_flats = []
# for flat in processed_flats:
#     evidence = {
#     'Rooms': flat['Rooms'],
#     'Sqft': flat['Sqft'],
#     'Quality': flat['Quality'],
#     'Price': flat['Price'],
#     **user_search
#     }
            
#     prob = inference.query(variables=['UserPref'], evidence=evidence)
#     score = preference_score(prob.values)

#     scored_flats.append((flat, score))

# top_flats = sorted(scored_flats, key=lambda x: x[1], reverse=True)[:10]

# result = [{"latitude": result[0]["latitude"], "longitude": result[0]["longitude"],
#                 "price": result[0]["price"], "name": result[0]["name"],
#                 "sqfts": result[0]["sqfts"], "rooms": result[0]["rooms"],
#                 "quality": result[0]["quality"], "score": float(result[1])*100} for result in top_flats]

# from pymongo.mongo_client import MongoClient
# from pymongo.server_api import ServerApi
# uri = "mongodb+srv://mc-79123:TfGX6ETzfuQ67kZ6@cluster0.movaern.mongodb.net/?retryWrites=true&w=majority"
# # Create a new client and connect to the server
# client = MongoClient(uri, server_api=ServerApi('1'))

# feature = "SearchPrice"

# db = client.search_data
# collection = db.my_collection

# data = collection.find({feature: {"$exists": True}})
# result = {"data": list(data)}

# import seaborn as sns
# import matplotlib.pyplot as plt


# # Query data based on the feature
# data = collection.find({feature: {"$exists": True}}, {feature: 1, "_id": 0})

# # Convert cursor data to a list
# feature_data = [entry[feature] for entry in data]

# # Create a KDE plot using seaborn
# sns.set(style="whitegrid")
# plt.figure(figsize=(8, 6))
# sns.kdeplot(feature_data, shade=True)
# plt.xlabel(feature)
# plt.ylabel("Density")
# plt.title(f"Kernel Density Estimation for {feature}")
# plt.show()
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from pgmpy.inference import VariableElimination
# uri = "mongodb+srv://mc-79123:TfGX6ETzfuQ67kZ6@cluster0.movaern.mongodb.net/?retryWrites=true&w=majority"
# # Create a new client and connect to the server
# client = MongoClient(uri, server_api=ServerApi('1'))

# feature="Price"
# db = client.mydatabase
# collection = db.my_collection
# data = collection.find({f"{feature.lower()}": {"$exists": True}}, {f"{feature.lower()}": 1, "_id": 1})
# # Convert cursor data to a list
# for x in data:
#     print(x)
# feature_data = [entry[feature.lower()] for entry in data]

# Load the Bayesian Network model
flat_model = joblib.load("bayesian_model_userpref.pkl")

inference = VariableElimination(flat_model)

search_params = {"SearchRooms": 2.0, "SearchSqft": 1400.0, "SearchQuality": 3.0, "SearchPrice": 2900.0,}
# Extract user search parameters from the request
user_search = {
    'SearchRooms': search_params.get("SearchRooms"),
    'SearchSqft': search_params.get("SearchSqft"),
    'SearchQuality': search_params.get("SearchQuality"),
    'SearchPrice': search_params.get("SearchPrice")
}

traditional_table_fields = {
    "_id": 0, "latitude": 1, "longitude": 1, "price": 1, 
    "name": 1, "sqfts": 1, "rooms": 1, "quality": 1
}

query = {}  # Define your query to filter flats if needed

# Fetch coordinates from MongoDB of the filtered flats
results = collection.find(query, traditional_table_fields)

full_results = [{
    "latitude": result["latitude"], "longitude": result["longitude"],
    "price": result["price"], "name": result["name"],
    "sqfts": result["sqfts"], "rooms": result["rooms"],
    "quality": result["quality"]
} for result in results]

user_search = {
    key: int(value) if value is not None else None
    for key, value in user_search.items()
}
user_search_raw = user_search.copy()
# Convert raw search params to states expected by Bayesian network
user_search = {
    key: prepare_bayesian_features(key, value)
    for key, value in user_search.items()
}
full_results_df = pd.DataFrame(data=full_results, columns=["latitude", "longitude", "price", "name", 
                                                        "sqfts", "rooms", "quality"])

full_results = filter_flats_based_on_search(full_results_df, user_search_raw)

# Process each flat's raw data to be compatible with Bayesian network
processed_flats = []
for index, flat in full_results.iterrows():
    processed_flat = {
        'Rooms': prepare_bayesian_features('Rooms', flat['rooms']),
        'Sqft': prepare_bayesian_features('Sqft', flat['sqfts']),
        'Quality': prepare_bayesian_features('Quality', flat['quality']),
        'Price': prepare_bayesian_features('Price', flat['price'])
    }
    processed_flats.append({**flat, **processed_flat})
# Score each flat based on user search and Bayesian model

scored_flats = []
for flat in processed_flats:
    evidence = {
    'Rooms': flat['Rooms'],
    'Sqft': flat['Sqft'],
    'Quality': flat['Quality'],
    'Price': flat['Price'],
    **user_search
    }
    print(evidence)
    prob = inference.query(variables=['UserPref'], evidence=evidence)
    score = preference_score(prob.values)
    scored_flats.append((flat, score))

top_flats = sorted(scored_flats, key=lambda x: x[1], reverse=True)