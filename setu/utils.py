import random
import time

def set_random_seed(id):
    seed = int(int(time.time())) ^ id
    random.seed((seed))