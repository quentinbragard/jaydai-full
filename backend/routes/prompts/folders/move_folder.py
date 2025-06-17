# routes/prompts/folders/move_folder.py
from fastapi import Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from models.common import APIResponse
from utils import supabase_helpers
from .helpers import router, supabase

class MoveFolderRequest(BaseModel):
    parent_folder_id: Optional[int] = None  # None means move to root

@router.post("/{folder_id}/move")
async def move_folder(
    folder_id: int,
    request: MoveFolderRequest,
    user_id: str = Depends(supabase_helpers.get_user_from_session_token),
) -> APIResponse[dict]:
    """Move a folder to a different parent folder or to root level."""
    try:
        # First verify the user owns this folder
        verify_response = supabase.table("prompt_folders").select("id, parent_folder_id") \
            .eq("id", folder_id) \
            .eq("user_id", user_id) \
            .execute()
        
        if not verify_response.data:
            raise HTTPException(status_code=404, detail="Folder not found or access denied")
        
        current_parent_id = verify_response.data[0].get("parent_folder_id")
        
        # Prevent circular references
        if request.parent_folder_id == folder_id:
            raise HTTPException(status_code=400, detail="Cannot move folder into itself")
        
        # If destination parent is specified, verify user owns it and check for circular reference
        if request.parent_folder_id is not None:
            parent_verify = supabase.table("prompt_folders").select("id") \
                .eq("id", request.parent_folder_id) \
                .eq("user_id", user_id) \
                .execute()
            
            if not parent_verify.data:
                raise HTTPException(status_code=404, detail="Destination parent folder not found or access denied")
            
            # Check for circular reference by checking if the destination is a child of the current folder
            if await is_descendant_folder(supabase, request.parent_folder_id, folder_id, user_id):
                raise HTTPException(status_code=400, detail="Cannot move folder into its own descendant")
        
        # Update the folder's parent_folder_id
        update_response = supabase.table("prompt_folders").update({
            "parent_folder_id": request.parent_folder_id,
            "sort_order": 0  # Reset sort order in new location
        }).eq("id", folder_id).eq("user_id", user_id).execute()
        
        if not update_response.data:
            raise HTTPException(status_code=400, detail="Failed to move folder")
        
        return APIResponse(success=True, data={
            "folder_id": folder_id,
            "from_parent_id": current_parent_id,
            "to_parent_id": request.parent_folder_id,
            "message": f"Folder moved {'to root' if request.parent_folder_id is None else f'to folder {request.parent_folder_id}'}"
        })
        
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"Error moving folder: {str(e)}")

async def is_descendant_folder(supabase, potential_descendant_id: int, ancestor_id: int, user_id: str) -> bool:
    """Check if potential_descendant_id is a descendant of ancestor_id to prevent circular references."""
    # Get all folders for the user to build a tree
    folders_response = supabase.table("prompt_folders").select("id, parent_folder_id") \
        .eq("user_id", user_id) \
        .execute()
    
    if not folders_response.data:
        return False
    
    # Build a parent-child mapping
    children_map = {}
    for folder in folders_response.data:
        parent_id = folder.get("parent_folder_id")
        if parent_id:
            if parent_id not in children_map:
                children_map[parent_id] = []
            children_map[parent_id].append(folder["id"])
    
    # Recursively check if potential_descendant_id is in the descendants of ancestor_id
    def check_descendants(folder_id):
        if folder_id == potential_descendant_id:
            return True
        children = children_map.get(folder_id, [])
        return any(check_descendants(child_id) for child_id in children)
    
    return check_descendants(ancestor_id)

