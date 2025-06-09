from typing import Optional, List
from fastapi import Depends, HTTPException
from models.prompts.templates import TemplateResponse
from models.common import APIResponse
from utils import supabase_helpers
from . import router, supabase
from utils.prompts import process_template_for_response, expand_template_blocks

@router.get("/unorganized", response_model=APIResponse[List[TemplateResponse]])
async def get_unorganized_templates_endpoint(
    locale: Optional[str] = "en",
    expand_blocks: bool = True,
    user_id: str = Depends(supabase_helpers.get_user_from_session_token),
):
    """Get all templates that are not organized in any folder."""
    try:
        # Get user templates without folder
        query = supabase.table("prompt_templates").select("*")
        query = query.eq("user_id", user_id).eq("type", "user").is_("folder_id", "null")
        response = query.execute()

        templates = []
        for template_data in (response.data or []):
            # Process template for response
            processed_template = process_template_for_response(template_data, locale)

            # Expand blocks if requested
            if expand_blocks:
                processed_template = await expand_template_blocks(processed_template, locale)

            templates.append(processed_template)

        return APIResponse(success=True, data=templates)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving unorganized templates: {str(e)}")
