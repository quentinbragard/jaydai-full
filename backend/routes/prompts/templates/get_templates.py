from typing import Optional, List
from fastapi import Depends, HTTPException, Query
from models.prompts.templates import TemplateResponse
from models.common import APIResponse
from utils import supabase_helpers
from utils.prompts import process_template_for_response
from . import router, supabase

@router.get("", response_model=APIResponse[List[TemplateResponse]])
async def get_templates(
    type: Optional[str] = None,
    folder_ids: Optional[str] = None,
    locale: Optional[str] = "en",
    user_id: str = Depends(supabase_helpers.get_user_from_session_token),
):
    """Get templates filtered by type or folder IDs."""
    try:
        query = supabase.table("prompt_templates").select("*")

        if type:
            query = query.eq("type", type)

        if folder_ids:
            try:
                folder_id_list = [int(fid) for fid in folder_ids.split(',') if fid.strip()]
            except ValueError as e:
                raise HTTPException(status_code=400, detail=f"Invalid folder ID format: {str(e)}")
            if folder_id_list:
                query = query.in_("folder_id", folder_id_list)

        response = query.execute()
        templates = []
        for template_data in (response.data or []):
            processed = process_template_for_response(template_data, locale)
            templates.append(processed)
            
        return APIResponse(success=True, data=templates)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving templates: {str(e)}")
