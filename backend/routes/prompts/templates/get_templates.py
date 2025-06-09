from typing import Optional, List
from fastapi import Depends, HTTPException
from models.prompts.templates import TemplateResponse
from models.common import APIResponse
from utils import supabase_helpers
from . import router, get_user_templates, get_official_templates, get_company_templates, get_all_templates

@router.get("", response_model=APIResponse[List[TemplateResponse]])
async def get_templates(
    type: Optional[str] = None,
    locale: Optional[str] = "en",
    expand_blocks: bool = True,
    user_id: str = Depends(supabase_helpers.get_user_from_session_token),
):
    """Get templates with optional filtering by type."""
    try:
        if type == "user":
            return await get_user_templates(user_id, locale, expand_blocks)
        elif type == "official":
            return await get_official_templates(user_id, locale, expand_blocks)
        elif type == "company":
            return await get_company_templates(user_id, locale, expand_blocks)
        else:
            # Get all templates
            return await get_all_templates(user_id, locale, expand_blocks)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving templates: {str(e)}")
