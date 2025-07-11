# routes/prompts/folders/create_folder.py - REPLACE ENTIRE FUNCTION
from fastapi import Depends, HTTPException, Request
from models.common import APIResponse
from utils import supabase_helpers
from .helpers import router, supabase
from models.prompts.folders import FolderCreate
from utils.middleware.localization import extract_locale_from_request 
from utils.prompts.locales import ensure_localized_field
from utils.access_control import user_has_access_to_folder

@router.post("")
async def create_folder(
    folder: FolderCreate,
    request: Request,
    user_id: str = Depends(supabase_helpers.get_user_from_session_token),
) -> APIResponse[dict]:
    """Create a new user folder with access control validation."""
    try:
        locale = extract_locale_from_request(request)
        
        # Validate parent folder access if specified
        if folder.parent_folder_id:
            parent_access = user_has_access_to_folder(supabase, user_id, folder.parent_folder_id)
            if parent_access is None:
                raise HTTPException(status_code=404, detail="Parent folder not found")
            if not parent_access:
                raise HTTPException(status_code=403, detail="Access denied to parent folder")
        
        localized_title = ensure_localized_field(folder.title, locale) if folder.title else {}
        localized_description = ensure_localized_field(folder.description, locale) if folder.description else {}

        response = supabase.table("prompt_folders").insert({
            "user_id": user_id,
            "organization_id": None,
            "company_id": None,
            "type": "user",
            "parent_folder_id": folder.parent_folder_id,
            "title": localized_title,
            "description": localized_description,
        }).execute()

        if response.data and len(response.data) > 0:
            return APIResponse(success=True, data=response.data[0])
        else:
            return APIResponse(success=False, data=None)

    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"Error creating folder: {str(e)}")