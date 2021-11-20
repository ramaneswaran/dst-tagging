import os
import pickle
from typing import List



def save_as_pkl(path: str, data):
    with open(path, 'wb') as f:
        pickle.dump(data, f)

def read_pkl_data(path: str):
    with open(path, 'rb') as f:
        data = pickle.load(f)
    
    return data

def load_data(dir: str):
    
    items = []
    for _file in os.listdir(dir):
        path = os.path.join(dir, _file)
        item = read_pkl_data(path)
        items.append(item)
    

    data = {}

    for item in items:
        data[item['id']] = item

    return data