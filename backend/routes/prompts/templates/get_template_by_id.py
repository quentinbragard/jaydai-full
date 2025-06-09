from typing import Optional
from fastapi import Depends, HTTPException
from models.prompts.templates import TemplateResponse
from models.common import APIResponse
from utils import supabase_helpers
from utils.prompts import process_template_for_response
from utils.access_control import get_user_metadata
from . import router, supabase

@router.get("/{template_id}", response_model=APIResponse[TemplateResponse])
async def get_template_by_id(
    template_id: str,
    locale: Optional[str] = "en",
    user_id: str = Depends(supabase_helpers.get_user_from_session_token),
):
    """Get a specific template by ID."""
    try:
        response = supabase.table("prompt_templates").select("*").eq("id", template_id).single().execute()

        if not response.data:
            raise HTTPException(status_code=404, detail="Template not found")

        template_data = response.data

        if template_data.get("type") == "user" and template_data.get("user_id") != user_id:
            raise HTTPException(status_code=403, detail="Access denied")
        elif template_data.get("type") == "organization":
            metadata = get_user_metadata(supabase, user_id)
            if template_data.get("organization_id") not in (metadata.get("organization_ids") or []):
                raise HTTPException(status_code=403, detail="Access denied")
        elif template_data.get("type") == "company":
            metadata = get_user_metadata(supabase, user_id)
            if template_data.get("company_id") != metadata.get("company_id"):
                raise HTTPException(status_code=403, detail="Access denied")

        processed_template = process_template_for_response(template_data, locale)

        return APIResponse(success=True, data=processed_template)

    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"Error retrieving template: {str(e)}")
