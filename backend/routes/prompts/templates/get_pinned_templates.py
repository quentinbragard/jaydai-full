from typing import List
from fastapi import Depends, HTTPException, Request
from models.common import APIResponse
from utils import supabase_helpers
from .helpers import router, supabase, process_template_for_response
from utils.middleware.localization import extract_locale_from_request

@router.get("/pinned", response_model=APIResponse[List[dict]])
async def get_pinned_templates(
    request: Request,
    user_id: str = Depends(supabase_helpers.get_user_from_session_token),
) -> APIResponse[List[dict]]:
    """Get user's pinned templates."""
    try:
        locale = extract_locale_from_request(request)
        print(f"🌍 GET_PINNED_TEMPLATES - LOCALE DETECTED: {locale}")
        
        # Get user's pinned template IDs
        user_metadata = supabase.table("users_metadata").select("pinned_templates").eq("user_id", user_id).single().execute()
        pinned_template_ids = user_metadata.data.get("pinned_templates", []) if user_metadata.data else []
        
        if not pinned_template_ids:
            return APIResponse(success=True, data=[])
        
        # Get the actual templates
        templates_response = supabase.table("prompt_templates").select("*").in_("id", pinned_template_ids).execute()
        
        processed_templates = []
        for template_data in (templates_response.data or []):
            processed_template = process_template_for_response(template_data, locale)
            processed_template["is_pinned"] = True
            processed_templates.append(processed_template)
        
        print(f"📤 GET_PINNED_TEMPLATES - RETURNING {len(processed_templates)} templates in {locale}")
        
        return APIResponse(success=True, data=processed_templates)
        
    except Exception as e:
        print(f"❌ GET_PINNED_TEMPLATES ERROR: {str(e)}")
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"Error retrieving pinned templates: {str(e)}")