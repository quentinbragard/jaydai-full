from fastapi import Depends, HTTPException
from models.common import APIResponse
from utils import supabase_helpers
from .helpers import router, supabase, FolderCreate, create_localized_field

@router.post("")
async def create_folder(
    folder: FolderCreate,
    user_id: str = Depends(supabase_helpers.get_user_from_session_token),
) -> APIResponse[dict]:
    """Create a new user folder."""
    try:
        title_json = create_localized_field(folder.name)
        description_json = create_localized_field(folder.description) if folder.description else {}

        response = supabase.table("prompt_folders").insert({
            "user_id": user_id,
            "organization_id": None,
            "company_id": None,
            "type": "user",
            "parent_folder_id": folder.parent_id,
            "title": title_json,
            "content": title_json,
            "description": description_json,
        }).execute()

        if response.data:
            from utils.prompts.folders import process_folder_for_response
            processed_folder = process_folder_for_response(response.data[0])

        return APIResponse(success=True, data=processed_folder)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating folder: {str(e)}")
