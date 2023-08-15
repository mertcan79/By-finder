from celery import Celery
from bayesian_network import *

celery = Celery('tasks', broker='pyamqp://guest@localhost//')

@celery.task(name='run_model')
def compute_probabilities(search):
    # infer = bayesian_calculations(data)
    # flat_evidence = get_evidence(data)
    # prob = infer.query(variables=['UserPref'], 
    #                     evidence=flat_evidence)
    prob = calculate_probability(search)
    return prob