from typing import Optional
from app.db.database import get_db_collection
from app.schemas.user_schemas import UserInDB, HistoryItem
from app.core.hashing import verify_password  # <-- CHANGE THIS LINE

class UserService:
    def __init__(self):
        self.collection = get_db_collection("users")

    def get_user_by_email(self, email: str) -> Optional[UserInDB]:
        """Fetches a user by their email address."""
        user_data = self.collection.find_one({"email": email})
        if user_data:
            return UserInDB(**user_data)
        return None

    def authenticate_user(self, email: str, password: str) -> Optional[UserInDB]:
        """Authenticates a user by checking their email and password."""
        user = self.get_user_by_email(email)
        if not user or not verify_password(password, user.hashed_password): # This line now works correctly
            return None
        return user

    def add_prediction_to_history(self, email: str, history_item: HistoryItem):
        """Adds a new prediction record to a user's history."""
        history_data = history_item.dict()
        self.collection.update_one(
            {"email": email},
            {"$push": {"history": history_data}}
        )

# Singleton instance
user_service = UserService()
