from typing import List
from fastapi import Depends, HTTPException
from models.common import APIResponse
from utils import supabase_helpers
from .helpers import router, supabase

@router.post("/unpin/{folder_id}")
async def unpin_folder(
    folder_id: int,
    user_id: str = Depends(supabase_helpers.get_user_from_session_token),
) -> APIResponse[List[int]]:
    """Unpin a folder for a user."""
    try:
        pinned_folder_ids = supabase.table("users_metadata").select("pinned_folder_ids").eq("user_id", user_id).single().execute()
        pinned_folder_ids = pinned_folder_ids.data.get("pinned_folder_ids", []) if pinned_folder_ids.data else []
        pinned_folder_ids = pinned_folder_ids if type(pinned_folder_ids) == list else []

        if folder_id in pinned_folder_ids:
            pinned_folder_ids.remove(folder_id)

        response = supabase.table("users_metadata").update({"pinned_folder_ids": pinned_folder_ids}).eq("user_id", user_id).execute()

        return APIResponse(success=True, data=pinned_folder_ids)
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"Error unpinning folder: {str(e)}")
