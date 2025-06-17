# routes/prompts/templates/reorder_templates.py
from fastapi import Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from models.common import APIResponse
from utils import supabase_helpers
from .helpers import router, supabase

class ReorderItem(BaseModel):
    id: int
    sort_order: int
    is_priority: Optional[bool] = False

class ReorderTemplatesRequest(BaseModel):
    items: List[ReorderItem]
    folder_id: Optional[int] = None

@router.post("/reorder")
async def reorder_templates(
    request: ReorderTemplatesRequest,
    user_id: str = Depends(supabase_helpers.get_user_from_session_token),
) -> APIResponse[dict]:
    """Reorder templates within a folder or at root level."""
    try:
        # Verify ownership and update sort orders
        for item in request.items:
            # First verify the user owns this template
            verify_response = supabase.table("prompt_templates").select("id") \
                .eq("id", item.id) \
                .eq("user_id", user_id) \
                .execute()
            
            if not verify_response.data:
                raise HTTPException(status_code=404, detail=f"Template {item.id} not found or access denied")
            
            # Update the sort order
            update_data = {
                "sort_order": item.sort_order,
                "is_priority": item.is_priority
            }
            
            supabase.table("prompt_templates").update(update_data) \
                .eq("id", item.id) \
                .eq("user_id", user_id) \
                .execute()
        
        return APIResponse(success=True, data={"reordered_count": len(request.items)})
        
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"Error reordering templates: {str(e)}")
