from pymongo import MongoClient
from app.core.config import settings

class MongoDB:
    def __init__(self):
        try:
            self.client = MongoClient(settings.MONGODB_URL)
            self.db = self.client[settings.DB_NAME]
            # Ping the server to confirm a successful connection
            self.client.admin.command('ping')
            print("✅ Successfully connected to MongoDB.")
        except Exception as e:
            print(f"❌ Failed to connect to MongoDB: {e}")
            self.client = None
            self.db = None

    def get_collection(self, collection_name: str):
        if self.db is not None: # <-- CHANGE THIS LINE
            return self.db[collection_name]
        return None

# Singleton instance of the database connection
mongodb = MongoDB()

def get_db_collection(collection_name: str):
    """Dependency to get a database collection."""
    return mongodb.get_collection(collection_name)
