import os
import certifi
from pathlib import Path
from dotenv import load_dotenv
from pymongo import MongoClient

# This line finds the .env file exactly where this script is located
env_path = Path(__file__).resolve().parent / '.env'
load_dotenv(dotenv_path=env_path)

MONGO_URI = os.getenv("MONGO_URI")

def test_mongo():
    if not MONGO_URI:
        print(f"❌ Error: MONGO_URI not found! Looked at: {env_path}")
        return

    try:
        # Connect using the absolute path to the certs
        client = MongoClient(
            MONGO_URI, 
            tlsCAFile=certifi.where(), 
            serverSelectionTimeoutMS=5000
        )
        client.admin.command('ping')
        print("✅ Success! MongoDB is connected.")
        
    except Exception as e:
        print(f"❌ CONNECTION FAILED: {e}")

if __name__ == "__main__":
    test_mongo()