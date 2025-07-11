# routes/prompts/folders/create_folder.py - REPLACE ENTIRE FUNCTION
from fastapi import Depends, HTTPException
from models.common import APIResponse
from utils import supabase_helpers
from .helpers import router, supabase

from utils.access_control import user_has_access_to_folder


# routes/prompts/folders/delete_folder.py - REPLACE ENTIRE FUNCTION
@router.delete("/{folder_id}")
async def delete_folder(
    folder_id: int,
    user_id: str = Depends(supabase_helpers.get_user_from_session_token),
) -> APIResponse[dict]:
    """Delete a folder with access control validation."""
    try:
        # Validate folder access
        access = user_has_access_to_folder(supabase, user_id, folder_id)
        if access is None:
            raise HTTPException(status_code=404, detail="Folder not found")
        if not access:
            raise HTTPException(status_code=403, detail="Access denied to this folder")

        # Check if folder has child folders or templates
        child_folders = supabase.table("prompt_folders").select("id").eq("parent_folder_id", folder_id).execute()
        if child_folders.data:
            raise HTTPException(status_code=400, detail="Cannot delete folder that contains subfolders")
            
        folder_templates = supabase.table("prompt_templates").select("id").eq("folder_id", folder_id).execute()
        if folder_templates.data:
            raise HTTPException(status_code=400, detail="Cannot delete folder that contains templates")

        # Delete the folder
        supabase.table("prompt_folders").delete().eq("id", folder_id).execute()
        return APIResponse(success=True, message="Folder deleted")
        
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"Error deleting folder: {str(e)}")