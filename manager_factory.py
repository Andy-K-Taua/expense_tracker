# manager_factory.py

import os
from data_manager import DataManager

def get_data_manager():
    if os.getenv('DATABASE_TYPE') == 'mongo':
        from mongo_manager import MongoDataManager
        return MongoDataManager(uri=os.getenv('MONGO_URI'))
    
    return DataManager("expenses.json")

db = get_data_manager()