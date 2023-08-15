from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import pandas as pd
import numpy as np
from sklearn.preprocessing import QuantileTransformer

uri = "mongodb+srv://mc-79123:TfGX6ETzfuQ67kZ6@cluster0.movaern.mongodb.net/?retryWrites=true&w=majority"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

def get_db():
    db = client["mydatabase"]
    return db

def clean_data():
    get_db().my_collection.delete_many({})

def process_data():
    df = pd.read_csv('data.csv')
    # Process the data
    df['sqfts'] = pd.to_numeric(df['sqfts'].str.rstrip('ft2'))
    df['price'] = df['price'].str.replace(',', '').str.replace('$', '').astype(float)
    for col in df.columns:
        if df[col].mode()[0] == np.NaN:
            df[col] = df[col].fillna(df[col].mode()[1])
        else:
            df[col] = df[col].fillna(df[col].mode()[0])
    for col in ['price', 'sqfts']:
        P = np.percentile(df[col], [10, 90])
        df[col] = df[(df[col] > P[0]) & (df[col] < P[1])][col]
    df.bedrooms = df.bedrooms.astype('category')
    df = df.rename(columns={"bedrooms": "rooms"})
    # Set the maximum cap values for 'Price' and 'sqfts' columns
    max_price_cap = 5000
    max_sqfts_cap = 1700

    # Clip the values in the 'Price' column to the maximum cap
    df['price'] = df['price'].clip(upper=max_price_cap)

    # Clip the values in the 'sqfts' column to the maximum cap
    df['sqfts'] = df['sqfts'].clip(upper=max_sqfts_cap)

    df['mean_price'] = df.groupby('locality')['price'].transform('mean')
    # Create a QuantileTransformer object with output distribution as 'uniform'
    transformer = QuantileTransformer(output_distribution='uniform')

    # Perform Quantile Transformation on the 'quality' column
    df['transformed_quality'] = transformer.fit_transform(df[['mean_price']])

    # Rescale the transformed values to the desired range (e.g., [0, 5])
    new_min_scale = 0
    new_max_scale = 5
    df['scaled_quality'] = (df['transformed_quality'] - df['transformed_quality'].min()) * (new_max_scale - new_min_scale) / (df['transformed_quality'].max() - df['transformed_quality'].min()) + new_min_scale

    # Optional: If you want to round the scaled values to a specific number of decimal places
    decimal_places = 2
    df['quality'] = df['scaled_quality'].round(decimal_places)

    # Drop the intermediate columns if not needed
    df.drop(columns=['transformed_quality', 'scaled_quality'], inplace=True)

    df = df.dropna()
    return df

def upload_data():
    # Load data into a pandas DataFrame
    df = process_data()
    # Convert the DataFrame to a list of dictionaries and insert into MongoDB
    records = df.to_dict('records')

    get_db().my_collection.insert_many(records)
    print("Uploaded Data.")