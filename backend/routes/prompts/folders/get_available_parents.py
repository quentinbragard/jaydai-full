# routes/prompts/folders/get_available_parents.py
from fastapi import Depends, HTTPException
from typing import List
from models.common import APIResponse
from utils import supabase_helpers
from utils.prompts import process_folder_for_response
from .helpers import router, supabase

@router.get("/{folder_id}/available-parents")
async def get_available_parent_folders(
    folder_id: int,
    user_id: str = Depends(supabase_helpers.get_user_from_session_token),
) -> APIResponse[List[dict]]:
    """Get all available parent folders where a folder can be moved (excluding itself and its descendants)."""
    try:
        # First verify the user owns this folder
        verify_response = supabase.table("prompt_folders").select("id") \
            .eq("id", folder_id) \
            .eq("user_id", user_id) \
            .execute()
        
        if not verify_response.data:
            raise HTTPException(status_code=404, detail="Folder not found or access denied")
        
        # Get all user folders
        response = supabase.table("prompt_folders").select("*") \
            .eq("user_id", user_id) \
            .eq("type", "user") \
            .order("parent_folder_id", nulls_first=True) \
            .order("sort_order") \
            .execute()
        
        all_folders = response.data or []
        
        # Build descendants set to exclude them
        descendants = set()
        descendants.add(folder_id)  # Exclude the folder itself
        
        # Find all descendants
        def find_descendants(parent_id):
            for folder in all_folders:
                if folder.get("parent_folder_id") == parent_id:
                    child_id = folder["id"]
                    if child_id not in descendants:
                        descendants.add(child_id)
                        find_descendants(child_id)
        
        find_descendants(folder_id)
        
        # Filter out the folder itself and its descendants
        available_folders = [f for f in all_folders if f["id"] not in descendants]
        
        # Process folders for response
        processed_folders = []
        for folder in available_folders:
            processed_folder = process_folder_for_response(folder, "en")
            processed_folders.append(processed_folder)
        
        # Add a virtual "Root" option
        root_option = {
            "id": None,
            "name": "📁 Root (No Parent)",
            "description": "Move to root level (no parent folder)",
            "type": "user",
            "path": "/"
        }
        
        return APIResponse(success=True, data=[root_option] + processed_folders)
        
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"Error retrieving available parent folders: {str(e)}")