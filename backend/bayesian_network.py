from pgmpy.models import BayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination
import numpy as np
from pgmpy.models import BayesianNetwork
from utils import *
from pgmpy.estimators import MaximumLikelihoodEstimator 

def calculate_probability(search):
    prob = bayesian_calculations(search)
    # process
    return prob

def bayesian_calculations(df):
    # Define the structure
    # 1. Define the Bayesian Network and CPDs (from previous code)

    flat_model = BayesianNetwork([
        ('SearchRooms', 'UserPref'),
        ('SearchSqft', 'UserPref'),
        ('SearchQuality', 'UserPref'),
        ('SearchPrice', 'UserPref'),
        ('IndustryRooms', 'Rooms'),
        ('IndustrySqft', 'Sqft'),
        ('IndustryQuality', 'Quality'),
        ('IndustryPrice', 'Price'),
        ('Rooms', 'UserPref'),
        ('Sqft', 'UserPref'),
        ('Quality', 'UserPref'),
        ('Price', 'UserPref')
    ])
    
    mle = MaximumLikelihoodEstimator(flat_model, df)
    cpds = [mle.estimate_cpd(node) for node in flat_model.nodes()]
    flat_model.add_cpds(*cpds)
    assert flat_model.check_model()

    # Inference
    inference = VariableElimination(flat_model)

    # 2. Compute the probability of `UserPref` being 'like' for each flat

    # Sample user search parameters
    user_search = {
        'SearchRooms': 2,
        'SearchSqft': 'medium',
        'SearchQuality': 'high',
        'SearchPrice': 'medium'
    }

    # For each flat in your database, compute the probability
    probabilities = []
    for index, row in df.iterrows():
        evidence = {
            'Rooms': row['Rooms'],
            'Sqft': row['Sqft'],
            'Quality': row['Quality'],
            'Price': row['Price'],
            **user_search
        }
        prob = inference.query(variables=['UserPref'], evidence=evidence)
        probabilities.append(prob.values[0])  # Assuming 'like' is the first category

    # 3. Rank the flats
    df['like_probability'] = probabilities
    top_10_flats = df.nlargest(10, 'like_probability')
    
    return top_10_flats

