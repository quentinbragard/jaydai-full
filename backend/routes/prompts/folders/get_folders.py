from typing import List, Optional
from fastapi import Depends, HTTPException
from models.common import APIResponse
from utils import supabase_helpers
from .helpers import (
    router, supabase, fetch_folders_by_type, fetch_templates_for_folders,
    organize_templates_by_folder, add_templates_to_folders,
    get_user_pinned_folders, add_pinned_status_to_folders
)

@router.get("")
async def get_folders(
    type: Optional[str] = None,
    folder_ids: Optional[str] = None,
    locale: Optional[str] = None,
    user_id: str = Depends(supabase_helpers.get_user_from_session_token),
) -> APIResponse[List[dict]]:
    """Get folders with optional filtering by type."""
    try:
        if type not in ["user", "official", "company", None]:
            raise HTTPException(status_code=400, detail="Invalid folder type")

        if not locale:
            locale = "en"

        folder_id_list = []
        if folder_ids:
            try:
                folder_id_list = [int(id_str) for id_str in folder_ids.split(',') if id_str.strip()]
            except ValueError as e:
                raise HTTPException(status_code=400, detail=f"Invalid folder ID format: {str(e)}")

        if type:
            folder_resp = await fetch_folders_by_type(
                supabase,
                folder_type=type,
                user_id=user_id,
                folder_ids=folder_id_list if folder_id_list else None,
                locale=locale
            )
            if not folder_resp.success:
                raise HTTPException(status_code=400, detail=folder_resp.message or "Error fetching folders")
            folders = folder_resp.data or []

            folder_ids_for_templates = [f["id"] for f in folders]
            templates = await fetch_templates_for_folders(supabase, folder_ids_for_templates, type, locale)
            templates_by_folder = organize_templates_by_folder(templates)
            folders_with_templates = add_templates_to_folders(folders, templates_by_folder)

            if type in ["official", "company"]:
                pinned_folders = await get_user_pinned_folders(supabase, user_id)
                add_pinned_status_to_folders(folders_with_templates, pinned_folders[type])

            return APIResponse(success=True, data=folders_with_templates)
        else:
            user_resp = await fetch_folders_by_type(supabase, "user", user_id=user_id, locale=locale)
            official_resp = await fetch_folders_by_type(supabase, "official", user_id=user_id, locale=locale)
            company_resp = await fetch_folders_by_type(supabase, "company", user_id=user_id, locale=locale)

            for resp in [user_resp, official_resp, company_resp]:
                if not resp.success:
                    raise HTTPException(status_code=400, detail=resp.message or "Error fetching folders")

            user_folders = user_resp.data or []
            official_folders = official_resp.data or []
            company_folders = company_resp.data or []

            for folder_type, folders in [("user", user_folders), ("official", official_folders), ("company", company_folders)]:
                folder_ids_for_templates = [f["id"] for f in folders]
                templates = await fetch_templates_for_folders(supabase, folder_ids_for_templates, folder_type, locale)
                templates_by_folder = organize_templates_by_folder(templates)
                add_templates_to_folders(folders, templates_by_folder)

            pinned_folders = await get_user_pinned_folders(supabase, user_id)
            add_pinned_status_to_folders(official_folders, pinned_folders["official"])
            add_pinned_status_to_folders(company_folders, pinned_folders["company"])

            return APIResponse(success=True, data={
                "userFolders": user_folders,
                "officialFolders": official_folders,
                "companyFolders": company_folders
            })
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"Error retrieving folders: {str(e)}")
