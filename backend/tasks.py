from celery import Celery
from bayesian_network import *
from mongo import get_db
import pickle
from utils import prepare_bayesian_features, preference_score
from fastapi.responses import JSONResponse

db = get_db()
collection = db['my_collection']

# Load the Bayesian Network model
flat_model = joblib.load("bayesian_model_userpref.pkl")

inference = VariableElimination(flat_model)

# Create a Celery instance
celery = Celery(
    'tasks',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/1'
)

celery.conf.broker_url = 'redis://localhost:6379/0'
celery.conf.result_backend = 'redis://localhost:6379/1'

@celery.task(name='bayesian_search')
def bayesian_search_task(search_params):
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
        
        prob = inference.query(variables=['UserPref'], evidence=evidence)
        score = preference_score(prob.values)
        scored_flats.append((flat, score))
    
    top_flats = sorted(scored_flats, key=lambda x: x[1], reverse=True)

    result = [{"latitude": result[0]["latitude"], "longitude": result[0]["longitude"],
                    "price": result[0]["price"], "name": result[0]["name"],
                    "sqfts": result[0]["sqfts"], "rooms": result[0]["rooms"],
                    "quality": result[0]["quality"], "score": float(result[1])*100} for result in top_flats]
    return result

