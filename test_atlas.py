import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

mongo_uri = os.getenv("MONGO_URI")

try:
    client = MongoClient(mongo_uri, tls=True, tlsAllowInvalidCertificates=True)
    # Ping the Atlas deployment
    client.admin.command("ping")
    print(" Successfully connected to MongoDB Atlas Cloud!")

    db = client["review_analyzer"]
    collection = db["reviews"]
    print(
        f" Current review count in Atlas: {collection.count_documents({})}"
    )

except Exception as e:
    print(f" Connection failed: {e}")