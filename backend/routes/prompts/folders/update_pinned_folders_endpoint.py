from typing import List
from fastapi import Depends, HTTPException
from models.common import APIResponse
from utils import supabase_helpers
from .helpers import router, supabase, update_user_pinned_folders

@router.post("/update-pinned")
async def update_pinned_folders_endpoint(
    official_folder_ids: List[int],
    company_folder_ids: List[int],
    user_id: str = Depends(supabase_helpers.get_user_from_session_token),
) -> APIResponse[dict]:
    """Update all pinned folders in one call."""
    try:
        await update_user_pinned_folders(supabase, user_id, "official", official_folder_ids)
        await update_user_pinned_folders(supabase, user_id, "company", company_folder_ids)
        return APIResponse(success=True, data={
            "pinnedOfficialFolderIds": official_folder_ids,
            "pinnedCompanyFolderIds": company_folder_ids
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating pinned folders: {str(e)}")
