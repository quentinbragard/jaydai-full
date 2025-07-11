# routes/prompts/templates/get_unorganized_templates.py 
# OPTIONAL REWRITE (middleware already handles this automatically)

from typing import Optional, List
from fastapi import Depends, HTTPException, Request
from models.prompts.templates import TemplateResponse
from models.common import APIResponse
from utils import supabase_helpers
from . import router, supabase
from utils.prompts import process_template_for_response
from utils.access_control import apply_access_conditions
from utils.middleware.localization import extract_locale_from_request

@router.get("/unorganized", response_model=APIResponse[List[TemplateResponse]])
async def get_unorganized_templates_endpoint(
    request: Request,
    locale: Optional[str] = None,
    user_id: str = Depends(supabase_helpers.get_user_from_session_token),
):
    """Get all templates that are not organized in any folder with access control."""
    try:
        # Extract locale from request if not provided
        if not locale:
            locale = extract_locale_from_request(request)
        
        # Get all accessible templates without folder (not just user templates)
        query = supabase.table("prompt_templates").select("*")
        query = apply_access_conditions(query, supabase, user_id)  # This handles user/company/org access
        query = query.is_("folder_id", "null")
        response = query.execute()
    

        templates = []
        for template_data in (response.data or []):
            processed_template = process_template_for_response(template_data, locale)
            templates.append(processed_template)

        return APIResponse(success=True, data=templates)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving unorganized templates: {str(e)}")

# Key changes:
# 1. Added Request parameter and locale extraction
# 2. Used apply_access_conditions() instead of just user_id filter
# 3. Now includes company/organization templates user has access to