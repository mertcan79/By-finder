import pandas as pd
import numpy as np
from scipy.stats import norm
import joblib
from sklearn.preprocessing import QuantileTransformer
from utils import *

def preference_score(probabilities):
    # Exponential weights for each UserPref level from 1 to 7
    weights = [1, 2, 4, 8, 16, 32, 64]
    
    # Calculating score as a weighted average
    score = sum([prob * weight for prob, weight in zip(probabilities, weights)])
    
    return score

def prob_significant_change(search_data):
    # Define your prior beliefs
    prior_mean = 500
    prior_stddev = 100
    prior = norm(loc=prior_mean, scale=prior_stddev)

    # Compute the likelihood of the new search parameters
    new_search_price = search_data['Price']# Obtain the price from the new search parameters
    likelihood = prior.pdf(new_search_price)

    # Compute the posterior distribution
    posterior_mean = prior_mean * likelihood # Update the mean based on the likelihood
    posterior_stddev = prior_stddev * likelihood #Update the stddev based on the likelihood
    posterior = norm(loc=posterior_mean, scale=posterior_stddev)

    # Compute the probability of a significant change
    threshold = 20 # Define a threshold for significant changes
    prob_significant_change = 1 - posterior.cdf(prior_mean + threshold)

    return prob_significant_change


def process_data():
    df = pd.read_csv('analysis/data.csv')
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

def prepare_bayesian_features(key, value):
    if key in ["SearchRooms", "Rooms"]:
        if value == 1:
            return 1
        elif value == 2:
            return 2
        elif value == 3:
            return 3
        elif value == 4:
            return 4
        elif value == 5:
            return 5
        elif value == 6:
            return 6
        else:
            return 7

    elif key in ["SearchSqft", "Sqft"]:
        if value <= 500:
            return 1
        elif value <= 800:
            return 2
        elif value <= 1200:
            return 3
        elif value <= 1700:
            return 4
        elif value <= 2300:
            return 5
        elif value <= 3000:
            return 6
        else:
            return 7

    elif key in ["SearchQuality", "Quality"]:
        if value <= 1:
            return 1
        elif value <= 1.5:
            return 2
        elif value <= 2:
            return 3
        elif value <= 2.5:
            return 4
        elif value <= 3:
            return 5
        elif value <= 4:
            return 6
        else:
            return 7

    elif key in ["SearchPrice", "Price"]:
        if value <= 1000:
            return 1
        elif value <= 2000:
            return 2
        elif value <= 3000:
            return 3
        elif value <= 4000:
            return 4
        elif value <= 5500:
            return 5
        elif value <= 7000:
            return 6
        else:
            return 7
        
    return value


def filter_flats_based_on_search(df, search_params, range_percent = 0.30):
    """
    Filter the dataframe based on the search parameters.
    """
    
    # Filter for price
    min_price = search_params['SearchPrice'] * (1 - range_percent)
    max_price = search_params['SearchPrice'] * (1 + range_percent)
    df = df[(df['price'] >= min_price) & (df['price'] <= max_price)]

    # # Filter for rooms
    # min_rooms = max(1, search_params['SearchRooms'] * (1 - range_percent))  # Assuming min 1 room
    # max_rooms = search_params['SearchRooms'] * (1 + range_percent)
    # df = df[(df['rooms'] >= min_rooms) & (df['rooms'] <= max_rooms)]

    # Filter for sqfts
    min_sqfts = search_params['SearchSqft'] * (1 - range_percent)
    max_sqfts = search_params['SearchSqft'] * (1 + range_percent)
    df = df[(df['sqfts'] >= min_sqfts) & (df['sqfts'] <= max_sqfts)]

    # Filter for quality (assuming quality is a numerical value, adjust if it's categorical)
    min_quality = search_params['SearchQuality'] * (1 - range_percent)
    max_quality = search_params['SearchQuality'] * (1 + range_percent)
    df = df[(df['quality'] >= min_quality) & (df['quality'] <= max_quality)]

    return df