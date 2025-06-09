from typing import List
from fastapi import Depends, HTTPException
from models.common import APIResponse
from utils import supabase_helpers
from .helpers import router, supabase, get_user_pinned_folders, update_user_pinned_folders

@router.post("/unpin/{folder_id}")
async def unpin_folder(
    folder_id: int,
    folder_type: str = "official",
    user_id: str = Depends(supabase_helpers.get_user_from_session_token),
) -> APIResponse[List[int]]:
    """Unpin a folder for a user."""
    try:
        if folder_type not in ["official", "organization"]:
            raise HTTPException(status_code=400, detail="Invalid folder type")

        pinned_folders = await get_user_pinned_folders(supabase, user_id)

        if folder_id in pinned_folders[folder_type]:
            pinned_folders[folder_type].remove(folder_id)

        await update_user_pinned_folders(supabase, user_id, folder_type, pinned_folders[folder_type])

        return APIResponse(success=True, data=pinned_folders[folder_type])
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"Error unpinning folder: {str(e)}")
