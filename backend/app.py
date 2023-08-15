from fastapi import FastAPI, HTTPException, Depends
from celery import Celery
from models import SearchParams, Flat, Coordinate
from typing import List, Union, Any
from mongo import get_db, client
from utils import *
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from pgmpy.inference import VariableElimination
import pickle
from tasks import bayesian_search_task
from scipy.stats import gaussian_kde

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost:3000",
    "http://localhost:8000",
    "http://0.0.0.0:3000",
    "http://0.0.0.0:8000",
    "http://0.0.0.0:50301",
]

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

db = get_db()
collection = db['my_collection']

@app.get("/traditional_search")
async def traditional_search(search_params: SearchParams = Depends()):
    user_search = {
        'SearchRooms': search_params.rooms,
        'SearchSqft': search_params.sqfts,
        'SearchQuality': search_params.quality,
        'SearchPrice': search_params.price
    }
    price = user_search['SearchPrice']
    sqfts = user_search['SearchSqft']
    quality = user_search['SearchQuality']
    rooms = user_search['SearchRooms']
    
    query = {}
    if price is not None:
        query["price"] = {"$lte": float(price)}
    if rooms is not None:
        query["rooms"] = {"$gte": float(rooms)}
    if sqfts is not None:
        query["sqfts"] = {"$gte": float(sqfts)}
    if quality is not None:
        query["quality"] = {"$gte": float(quality)}
    traditional_table_fields = {"_id": 1, "latitude": 1, "longitude": 1, "price": 1, "name": 1, "sqfts": 1, "rooms": 1, "quality": 1}
    # Fetch coordinates from MongoDB of the filtered flats
    results = collection.find(query, traditional_table_fields)
    # Convert MongoDB cursor to list
    full_results = [{"latitude": result["latitude"], "longitude": result["longitude"],
                    "price": result["price"], "name": result["name"],
                    "sqfts": result["sqfts"], "rooms": result["rooms"],
                    "quality": result["quality"]} for result in results]

    return full_results

@app.get("/bayesian_search/")
async def bayesian_search(search_params: SearchParams = Depends()):
    user_search = {
        'SearchRooms': search_params.rooms,
        'SearchSqft': search_params.sqfts,
        'SearchQuality': search_params.quality,
        'SearchPrice': search_params.price
    }
    
    # Call the Celery task and wait for it to finish
    result = bayesian_search_task.apply_async((user_search,)).get()
    
    # Return the result to the client
    return result

@app.get("/get_data")
async def get_data(feature: str = "Price"):
    if feature in ["SearchRooms", "SearchSqft", "SearchQuality", "SearchPrice"]:
        db = client.search_data
        collection = db.my_collection
        # Query data based on the feature
        data = collection.find({f"{feature}": {"$exists": True}}, {f"{feature}": 1, "_id": 1})

        # Convert cursor data to a list
        feature_data = [entry[feature] for entry in data]
    elif feature in ["Rooms", "Sqft", "Quality", "Price"]:
        # Query data based on the feature
        db = client.mydatabase
        collection = db.my_collection
        data = collection.find({f"{feature.lower()}": {"$exists": True}}, {f"{feature.lower()}": 1, "_id": 1})
        # Convert cursor data to a list
        feature_data = [entry[feature.lower()] for entry in data]
    else:
        pass
    
    kde = gaussian_kde(feature_data)
    x_range = np.linspace(min(feature_data), max(feature_data), 1000)
    kde_values = kde.evaluate(x_range)
    
    return {
        "x": x_range.tolist(),
        "y": kde_values.tolist()
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
