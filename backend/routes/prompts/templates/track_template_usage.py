from fastapi import Depends, HTTPException
from models.common import APIResponse
from utils import supabase_helpers
from . import router, supabase

@router.post("/use/{template_id}")
async def track_template_usage(
    template_id: str,
    user_id: str = Depends(supabase_helpers.get_user_from_session_token),
):
    """Track template usage."""
    try:
        template_response = supabase.table("prompt_templates").select("usage_count").eq("id", template_id).single().execute()

        if not template_response.data:
            raise HTTPException(status_code=404, detail="Template not found")

        current_count = template_response.data.get("usage_count", 0)

        update_data = {
            "usage_count": current_count + 1,
            "last_used_at": "now()"
        }

        supabase.table("prompt_templates").update(update_data).eq("id", template_id).execute()

        return APIResponse(success=True, data={
            "usage_count": current_count + 1
        })

    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"Error tracking template usage: {str(e)}")
