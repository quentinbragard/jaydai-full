# routes/prompts/folders/toggle_priority.py
from fastapi import Depends, HTTPException
from pydantic import BaseModel
from models.common import APIResponse
from utils import supabase_helpers
from .helpers import router, supabase

class TogglePriorityRequest(BaseModel):
    is_priority: bool

@router.post("/{folder_id}/priority")
async def toggle_folder_priority(
    folder_id: int,
    request: TogglePriorityRequest,
    user_id: str = Depends(supabase_helpers.get_user_from_session_token),
) -> APIResponse[dict]:
    """Toggle priority status for a user folder."""
    try:
        # Verify ownership
        verify_response = supabase.table("prompt_folders").select("id") \
            .eq("id", folder_id) \
            .eq("user_id", user_id) \
            .execute()
        
        if not verify_response.data:
            raise HTTPException(status_code=404, detail="Folder not found or access denied")
        
        # Update priority status
        update_response = supabase.table("prompt_folders").update({
            "is_priority": request.is_priority
        }).eq("id", folder_id).eq("user_id", user_id).execute()
        
        if not update_response.data:
            raise HTTPException(status_code=400, detail="Failed to update folder priority")
        
        return APIResponse(success=True, data={
            "folder_id": folder_id,
            "is_priority": request.is_priority
        })
        
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"Error updating folder priority: {str(e)}")

