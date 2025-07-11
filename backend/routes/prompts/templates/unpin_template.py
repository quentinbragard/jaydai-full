from typing import List
from fastapi import Depends, HTTPException
from models.common import APIResponse
from utils import supabase_helpers
from .helpers import router, supabase

@router.post("/unpin/{template_id}")
async def unpin_template(
    template_id: int,
    user_id: str = Depends(supabase_helpers.get_user_from_session_token),
) -> APIResponse[List[int]]:
    """Unpin a template for a user."""
    try:
        pinned_template_ids = supabase.table("users_metadata").select("pinned_template_ids").eq("user_id", user_id).single().execute()
        pinned_template_ids = pinned_template_ids.data.get("pinned_template_ids", []) if pinned_template_ids.data else []
        pinned_template_ids = pinned_template_ids if type(pinned_template_ids) == list else []

        if template_id in pinned_template_ids:
            pinned_template_ids.remove(template_id)

        response = supabase.table("users_metadata").update({"pinned_template_ids": pinned_template_ids}).eq("user_id", user_id).execute()

        return APIResponse(success=True, data=pinned_template_ids)
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"Error unpinning template: {str(e)}")
