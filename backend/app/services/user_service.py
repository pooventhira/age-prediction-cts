from typing import Optional
from uuid import UUID
from app.db.database import get_db_collection
from app.schemas.user_schemas import UserInDB, HistoryItem
from app.core.hashing import verify_password

class UserService:
    def __init__(self):
        self.collection = get_db_collection("users")

    # ... (get_user_by_email and authenticate_user remain the same)
    def get_user_by_email(self, email: str) -> Optional[UserInDB]:
        user_data = self.collection.find_one({"email": email})
        if user_data:
            return UserInDB(**user_data)
        return None

    def authenticate_user(self, email: str, password: str) -> Optional[UserInDB]:
        user = self.get_user_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            return None
        return user
    
    def add_prediction_to_history(self, email: str, history_item: HistoryItem):
        history_data = history_item.dict()
        # Convert UUID to string for MongoDB storage
        history_data['id'] = str(history_data['id'])
        self.collection.update_one(
            {"email": email},
            {"$push": {"history": history_data}}
        )

    # --- New Delete Function ---
    def delete_history_item(self, email: str, item_id: UUID) -> bool:
        """
        Deletes a single history item for a user by its ID.
        Returns True if an item was deleted, False otherwise.
        """
        result = self.collection.update_one(
            {"email": email},
            {"$pull": {"history": {"id": str(item_id)}}}
        )
        return result.modified_count > 0

# Singleton instance
user_service = UserService()
