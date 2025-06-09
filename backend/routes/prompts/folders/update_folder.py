from fastapi import Depends, HTTPException
from models.common import APIResponse
from utils import supabase_helpers
from .helpers import router, supabase, FolderUpdate, create_localized_field

@router.put("/{folder_id}")
async def update_folder(
    folder_id: int,
    folder: FolderUpdate,
    user_id: str = Depends(supabase_helpers.get_user_from_session_token),
) -> APIResponse[dict]:
    """Update an existing user folder."""
    try:
        verify = supabase.table("prompt_folders").select("id").eq("id", folder_id).eq("user_id", user_id).execute()

        if not verify.data:
            raise HTTPException(status_code=404, detail="Folder not found or doesn't belong to user")

        title_json = create_localized_field(folder.name)
        description_json = create_localized_field(folder.description) if folder.description else {}

        response = supabase.table("prompt_folders").update({
            "title": title_json,
            "content": title_json,
            "description": description_json
        }).eq("id", folder_id).execute()

        processed_folder = None
        if response.data:
            from utils.prompts.folders import process_folder_for_response
            processed_folder = process_folder_for_response(response.data[0])
            processed_folder["path"] = folder.path

        return APIResponse(success=True, data=processed_folder)
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"Error updating folder: {str(e)}")
