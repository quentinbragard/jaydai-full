# routes/prompts/templates/move_template.py
from fastapi import Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from models.common import APIResponse
from utils import supabase_helpers
from .helpers import router, supabase

class MoveTemplateRequest(BaseModel):
    folder_id: Optional[int] = None  # None means move to root

@router.post("/{template_id}/move")
async def move_template(
    template_id: int,
    request: MoveTemplateRequest,
    user_id: str = Depends(supabase_helpers.get_user_from_session_token),
) -> APIResponse[dict]:
    """Move a template to a different folder or to root level."""
    try:
        # First verify the user owns this template
        verify_response = supabase.table("prompt_templates").select("id, folder_id") \
            .eq("id", template_id) \
            .eq("user_id", user_id) \
            .execute()
        
        if not verify_response.data:
            raise HTTPException(status_code=404, detail="Template not found or access denied")
        
        current_folder_id = verify_response.data[0].get("folder_id")
        
        # If destination folder is specified, verify user owns it
        if request.folder_id is not None:
            folder_verify = supabase.table("prompt_folders").select("id") \
                .eq("id", request.folder_id) \
                .eq("user_id", user_id) \
                .execute()
            
            if not folder_verify.data:
                raise HTTPException(status_code=404, detail="Destination folder not found or access denied")
        
        # Update the template's folder_id
        update_response = supabase.table("prompt_templates").update({
            "folder_id": request.folder_id,
            "sort_order": 0  # Reset sort order in new location
        }).eq("id", template_id).eq("user_id", user_id).execute()
        
        if not update_response.data:
            raise HTTPException(status_code=400, detail="Failed to move template")
        
        return APIResponse(success=True, data={
            "template_id": template_id,
            "from_folder_id": current_folder_id,
            "to_folder_id": request.folder_id,
            "message": f"Template moved {'to root' if request.folder_id is None else f'to folder {request.folder_id}'}"
        })
        
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"Error moving template: {str(e)}")

