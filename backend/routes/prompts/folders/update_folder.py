# routes/prompts/folders/create_folder.py - REPLACE ENTIRE FUNCTION
from fastapi import Depends, HTTPException, Request
from models.common import APIResponse
from utils import supabase_helpers
from .helpers import router, supabase
from models.prompts.folders import FolderUpdate
from utils.middleware.localization import extract_locale_from_request 
from utils.prompts.locales import ensure_localized_field
from utils.access_control import user_has_access_to_folder


# routes/prompts/folders/update_folder.py - REPLACE ENTIRE FUNCTION
@router.put("/{folder_id}")
async def update_folder(
    folder_id: int,
    folder: FolderUpdate,
    request: Request,
    user_id: str = Depends(supabase_helpers.get_user_from_session_token),
) -> APIResponse[dict]:
    """Update an existing folder with access control validation."""
    try:
        locale = extract_locale_from_request(request)
        
        # Validate folder access
        access = user_has_access_to_folder(supabase, user_id, folder_id)
        if access is None:
            raise HTTPException(status_code=404, detail="Folder not found")
        if not access:
            raise HTTPException(status_code=403, detail="Access denied to this folder")
        
        # Validate parent folder access if being changed
        if folder.parent_folder_id is not None and folder.parent_folder_id != 0:
            parent_access = user_has_access_to_folder(supabase, user_id, folder.parent_folder_id)
            if parent_access is None:
                raise HTTPException(status_code=404, detail="Parent folder not found")
            if not parent_access:
                raise HTTPException(status_code=403, detail="Access denied to parent folder")

        # Build update data
        update_data = {}
        
        if folder.title:
            update_data["title"] = ensure_localized_field(folder.title, locale)
        if folder.description is not None:
            update_data["description"] = ensure_localized_field(folder.description, locale)
        if folder.parent_folder_id is not None:
            update_data["parent_folder_id"] = folder.parent_folder_id if folder.parent_folder_id != 0 else None

        if not update_data:
            raise HTTPException(status_code=400, detail="No valid fields to update")

        response = supabase.table("prompt_folders").update(update_data).eq("id", folder_id).execute()

        if response.data:
            from utils.prompts.folders import process_folder_for_response
            processed_folder = process_folder_for_response(response.data[0], locale)
            return APIResponse(success=True, data=processed_folder)
        else:
            raise HTTPException(status_code=400, detail="Failed to update folder")
            
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"Error updating folder: {str(e)}")