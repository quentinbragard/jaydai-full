# routes/prompts/templates/get_available_folders.py
from fastapi import Depends, HTTPException
from typing import List
from models.common import APIResponse
from utils import supabase_helpers
from utils.prompts import process_folder_for_response
from ..folders.helpers import router, supabase

@router.get("/available-folders")
async def get_available_folders(
    user_id: str = Depends(supabase_helpers.get_user_from_session_token),
) -> APIResponse[List[dict]]:
    """Get all available folders where a template can be moved."""
    try:
        # Get all user folders
        response = supabase.table("prompt_folders").select("*") \
            .eq("user_id", user_id) \
            .eq("type", "user") \
            .order("parent_folder_id", nulls_first=True) \
            .order("sort_order") \
            .execute()
        
        folders = response.data or []
        
        # Process folders for response
        processed_folders = []
        for folder in folders:
            processed_folder = process_folder_for_response(folder, "en")
            processed_folders.append(processed_folder)
        
        # Add a virtual "Root" option
        root_option = {
            "id": None,
            "name": "📁 Root (No Folder)",
            "description": "Move to root level (no folder)",
            "type": "user",
            "path": "/"
        }
        
        return APIResponse(success=True, data=[root_option] + processed_folders)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving available folders: {str(e)}")

