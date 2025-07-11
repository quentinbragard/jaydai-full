# routes/prompts/folders/create_folder.py - REPLACE ENTIRE FUNCTION
from fastapi import Depends, HTTPException
from models.common import APIResponse
from utils import supabase_helpers
from .helpers import router, supabase

from utils.access_control import user_has_access_to_folder


# routes/prompts/folders/pin_folder.py - REPLACE THE pin_folder FUNCTION
@router.post("/pin/{folder_id}")
async def pin_folder(
    folder_id: int,
    user_id: str = Depends(supabase_helpers.get_user_from_session_token),
) -> APIResponse[dict]:
    """Pin a folder with access control validation."""
    try:
        # Validate folder access
        access = user_has_access_to_folder(supabase, user_id, folder_id)
        if access is None:
            raise HTTPException(status_code=404, detail="Folder not found")
        if not access:
            raise HTTPException(status_code=403, detail="Access denied to this folder")
        
        # Get current pinned folder ids
        user_meta_resp = (
            supabase.table("users_metadata")
            .select("pinned_folder_ids")
            .eq("user_id", user_id)
            .single()
            .execute()
        )
        current_ids = user_meta_resp.data.get("pinned_folder_ids", []) if user_meta_resp.data else []
        current_ids = current_ids if isinstance(current_ids, list) else []

        if folder_id not in current_ids:
            new_ids = current_ids + [folder_id]
            if user_meta_resp.data:
                supabase.table("users_metadata").update({"pinned_folder_ids": new_ids}).eq("user_id", user_id).execute()
            else:
                supabase.table("users_metadata").insert({"user_id": user_id, "pinned_folder_ids": new_ids}).execute()
        
        return APIResponse(success=True, data={
            "folder_id": folder_id,
            "pinned": True,
            "message": "Folder pinned successfully"
        })
        
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"Error pinning folder: {str(e)}")