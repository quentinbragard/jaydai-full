from fastapi import Depends, HTTPException
from models.common import APIResponse
from utils import supabase_helpers
from .helpers import (
    router, supabase, determine_folder_type,
    get_user_pinned_folders, update_user_pinned_folders
)

@router.post("/pin/{folder_id}")
async def pin_folder(
    folder_id: int,
    folder_type: str = "official",
    user_id: str = Depends(supabase_helpers.get_user_from_session_token),
) -> APIResponse[dict]:
    """Pin a folder for a user."""
    try:

        if folder_type not in ["official", "organization"]:
            raise HTTPException(status_code=400, detail="Invalid folder type")

        folder = supabase.table("prompt_folders").select("*").eq("id", folder_id).single().execute()
        if not folder.data:
            raise HTTPException(status_code=404, detail="Folder not found")

        actual_type = determine_folder_type(folder.data)
        if actual_type != folder_type:
            raise HTTPException(status_code=400, detail=f"Folder is not of type {folder_type}")
        
        pinned_folders = await get_user_pinned_folders(supabase, user_id)

        if folder_id not in pinned_folders:
            pinned_folders[folder_type].append(folder_id)

        await update_user_pinned_folders(supabase, user_id, folder_type, pinned_folders[folder_type])

        return APIResponse(success=True, data=pinned_folders)
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"Error pinning folder: {str(e)}")
