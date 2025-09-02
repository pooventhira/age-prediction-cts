from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from uuid import UUID
from app.schemas.user_schemas import UserInDB, HistoryItem
from app.core.security import get_current_active_user
from app.services.user_service import user_service

router = APIRouter()

@router.get("", response_model=List[HistoryItem], summary="Get User Prediction History")
async def get_user_history(current_user: UserInDB = Depends(get_current_active_user)):
    """
    Retrieves the prediction history for the currently authenticated user.
    """
    return current_user.history

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a History Item")
async def delete_history_item(
    item_id: UUID,
    current_user: UserInDB = Depends(get_current_active_user)
):
    """
    Deletes a specific prediction from the user's history by its unique ID.
    """
    success = user_service.delete_history_item(current_user.email, item_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="History item not found or you do not have permission to delete it."
        )
    return None # Return None for 204 No Content response
