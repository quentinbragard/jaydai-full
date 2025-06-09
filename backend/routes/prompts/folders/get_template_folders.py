from typing import Optional
from fastapi import Depends, HTTPException
from models.common import APIResponse
from utils import supabase_helpers
from .helpers import (
    router, supabase, PromptType, fetch_folders_by_type,
    fetch_templates_for_folders, organize_templates_by_folder,
    add_templates_to_folders
)

@router.get("/template-folders")
async def get_template_folders(
    type: PromptType,
    folder_ids: Optional[str] = None,
    empty: bool = False,
    locale: Optional[str] = None,
    user_id: str = Depends(supabase_helpers.get_user_from_session_token),
) -> APIResponse[dict]:
    """Get template folders by type with proper error handling."""
    try:
        if not locale:
            locale = "en"
        folder_id_list = []
        if folder_ids:
            try:
                folder_id_list = [int(id_str) for id_str in folder_ids.split(',') if id_str.strip()]
            except ValueError as e:
                raise HTTPException(status_code=400, detail=f"Invalid folder ID format: {str(e)}")
        folder_resp = await fetch_folders_by_type(
            supabase,
            folder_type=type.value,
            user_id=user_id if type == PromptType.user else None,
            folder_ids=folder_id_list if folder_id_list else None,
            locale=locale
        )
        if not folder_resp.success:
            raise HTTPException(status_code=400, detail=folder_resp.message or "Error fetching folders")
        folders = folder_resp.data or []
        if empty:
            return APIResponse(success=True, data=folders)
        folder_ids_for_templates = [f["id"] for f in folders]
        templates = await fetch_templates_for_folders(supabase, folder_ids_for_templates, type.value, locale)
        templates_by_folder = organize_templates_by_folder(templates)
        folders_with_templates = add_templates_to_folders(folders, templates_by_folder)
        return APIResponse(success=True, data=folders_with_templates)
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"Error retrieving template folders: {str(e)}")
