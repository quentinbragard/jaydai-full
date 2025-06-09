from fastapi import Depends, HTTPException
from models.common import APIResponse
from utils import supabase_helpers
from .helpers import router, supabase

@router.delete("/{folder_id}")
async def delete_folder(
    folder_id: int,
    user_id: str = Depends(supabase_helpers.get_user_from_session_token),
) -> APIResponse[dict]:
    """Delete a user folder."""
    try:
        verify = supabase.table("prompt_folders").select("id").eq("id", folder_id).eq("user_id", user_id).execute()

        if not verify.data:
            raise HTTPException(status_code=404, detail="Folder not found or doesn't belong to user")

        supabase.table("prompt_folders").delete().eq("id", folder_id).execute()

        return APIResponse(success=True, message="Folder deleted")
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"Error deleting folder: {str(e)}")
