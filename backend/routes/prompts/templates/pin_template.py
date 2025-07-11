# routes/prompts/templates/create_template.py - REPLACE ENTIRE FUNCTION
from fastapi import Depends, HTTPException
from models.common import APIResponse
from utils import supabase_helpers
from utils.access_control import user_has_access_to_template
from . import router, supabase

# routes/prompts/templates/pin_template.py - REPLACE ENTIRE FUNCTION
@router.post("/pin/{template_id}")
async def pin_template(
    template_id: int,
    user_id: str = Depends(supabase_helpers.get_user_from_session_token),
) -> APIResponse[dict]:
    """Pin a template with access control validation."""
    try:
        # Validate template access
        access = user_has_access_to_template(supabase, user_id, template_id)
        if access is None:
            raise HTTPException(status_code=404, detail="Template not found")
        if not access:
            raise HTTPException(status_code=403, detail="Access denied to this template")

        # Get current pinned template ids
        user_meta_resp = (
            supabase.table("users_metadata")
            .select("pinned_template_ids")
            .eq("user_id", user_id)
            .single()
            .execute()
        )
        current_ids = user_meta_resp.data.get("pinned_template_ids", []) if user_meta_resp.data else []
        current_ids = current_ids if isinstance(current_ids, list) else []

        if template_id not in current_ids:
            new_ids = current_ids + [template_id]
            if user_meta_resp.data:
                supabase.table("users_metadata").update({"pinned_template_ids": new_ids}).eq("user_id", user_id).execute()
            else:
                supabase.table("users_metadata").insert({"user_id": user_id, "pinned_template_ids": new_ids}).execute()

        return APIResponse(success=True, data={"template_id": template_id, "pinned": True})

    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"Error pinning template: {str(e)}")