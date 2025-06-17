# Updated routes/prompts/folders/pin_folder.py

from fastapi import Depends, HTTPException
from models.common import APIResponse
from utils import supabase_helpers
from .helpers import router, supabase, determine_folder_type
from utils.prompts.folders import add_folder_to_pinned

@router.post("/pin/{folder_id}")
async def pin_folder(
    folder_id: int,
    user_id: str = Depends(supabase_helpers.get_user_from_session_token),
) -> APIResponse[dict]:
    """
    Pin a folder for a user (works with unified pinned_folder_ids).
    """
    try:
        # Verify folder exists and determine its type
        folder = supabase.table("prompt_folders").select("*").eq("id", folder_id).single().execute()
        if not folder.data:
            raise HTTPException(status_code=404, detail="Folder not found")
        
        folder_type = determine_folder_type(folder.data)
        
        # Only allow pinning of official and company folders
        if folder_type == "user":
            raise HTTPException(status_code=400, detail="Cannot pin user folders")
        
        # Verify user has access to this folder
        if folder_type == "company":
            # Check if user belongs to the same company
            user_metadata = supabase.table("users_metadata").select("company_id").eq("user_id", user_id).single().execute()
            if not user_metadata.data or user_metadata.data.get("company_id") != folder.data.get("company_id"):
                raise HTTPException(status_code=403, detail="Access denied to this company folder")
        
        elif folder_type == "official" and folder.data.get("organization_id"):
            # Check if user belongs to this organization
            user_metadata = supabase.table("users_metadata").select("organization_ids").eq("user_id", user_id).single().execute()
            if not user_metadata.data:
                raise HTTPException(status_code=403, detail="Access denied to this organization folder")
            
            org_ids = user_metadata.data.get("organization_ids", [])
            if folder.data.get("organization_id") not in org_ids:
                raise HTTPException(status_code=403, detail="Access denied to this organization folder")
        
        # Add folder to pinned list
        result = await add_folder_to_pinned(supabase, user_id, folder_id)
        
        if not result.get("success"):
            raise HTTPException(status_code=500, detail=result.get("error", "Failed to pin folder"))
        
        return APIResponse(success=True, data={
            "folder_id": folder_id,
            "pinned": True,
            "message": result.get("message", "Folder pinned successfully")
        })
        
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"Error pinning folder: {str(e)}")


# Updated routes/prompts/folders/unpin_folder.py

from fastapi import Depends, HTTPException
from models.common import APIResponse
from utils import supabase_helpers
from .helpers import router, supabase
from utils.prompts.folders import remove_folder_from_pinned

@router.post("/unpin/{folder_id}")
async def unpin_folder(
    folder_id: int,
    user_id: str = Depends(supabase_helpers.get_user_from_session_token),
) -> APIResponse[dict]:
    """
    Unpin a folder for a user (works with unified pinned_folder_ids).
    """
    try:
        # Remove folder from pinned list
        result = await remove_folder_from_pinned(supabase, user_id, folder_id)
        
        if not result.get("success"):
            raise HTTPException(status_code=500, detail=result.get("error", "Failed to unpin folder"))
        
        return APIResponse(success=True, data={
            "folder_id": folder_id,
            "pinned": False,
            "message": result.get("message", "Folder unpinned successfully")
        })
        
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"Error unpinning folder: {str(e)}")


# Updated routes/prompts/folders/update_pinned_folders_endpoint.py

from typing import List
from fastapi import Depends, HTTPException
from pydantic import BaseModel
from models.common import APIResponse
from utils import supabase_helpers
from .helpers import router, supabase
from utils.prompts.folders import update_user_pinned_folders

class UpdatePinnedFoldersRequest(BaseModel):
    folder_ids: List[int]

@router.post("/update-pinned")
async def update_pinned_folders_endpoint(
    request: UpdatePinnedFoldersRequest,
    user_id: str = Depends(supabase_helpers.get_user_from_session_token),
) -> APIResponse[dict]:
    """
    Update all pinned folders in one call (unified structure).
    """
    try:
        result = await update_user_pinned_folders(supabase, user_id, request.folder_ids)
        
        if not result.get("success"):
            raise HTTPException(status_code=500, detail=result.get("error", "Failed to update pinned folders"))
        
        return APIResponse(success=True, data={
            "pinned_folder_ids": request.folder_ids,
            "message": "Pinned folders updated successfully"
        })
        
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"Error updating pinned folders: {str(e)}")


# New endpoint to get pinned folders
@router.get("/pinned")
async def get_pinned_folders(
    user_id: str = Depends(supabase_helpers.get_user_from_session_token),
) -> APIResponse[List[int]]:
    """
    Get user's pinned folder IDs.
    """
    try:
        from utils.prompts.folders import get_user_pinned_folders
        
        pinned_ids = await get_user_pinned_folders(supabase, user_id)
        
        return APIResponse(success=True, data=pinned_ids)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving pinned folders: {str(e)}")