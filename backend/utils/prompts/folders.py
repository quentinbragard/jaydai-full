# Update to utils/prompts/folders.py

"""
Updated utility functions for folder operations with new pinned folder structure.
"""
from typing import Dict, List, Optional, Any
from supabase import Client
from utils.prompts.locales import extract_localized_field
from utils.access_control import apply_access_conditions

def determine_folder_type(folder: Dict) -> str:
    """
    Determine folder type based on user_id and organization_id fields.
    
    Args:
        folder: Folder record dict
        
    Returns:
        Folder type: "user", "company", or "official"
    """
    if folder.get("user_id"):
        return "user"
    elif folder.get("company_id"):
        return "company"
    else:
        return "official"

def process_folder_for_response(folder_data: dict, locale: str = "en") -> dict:
    """Process block data for API response with localized strings"""
    return {
        "id": folder_data.get("id"),
        "type": folder_data.get("type"),
        "title": extract_localized_field(folder_data.get("title", {}), locale),
        "description": extract_localized_field(folder_data.get("description", {}), locale),
        "created_at": folder_data.get("created_at"),
        "user_id": folder_data.get("user_id"),
        "organization_id": folder_data.get("organization_id"),
        "company_id": folder_data.get("company_id"),
        "parent_folder_id": folder_data.get("parent_folder_id"),
    }

async def get_user_pinned_folders(supabase: Client, user_id: str) -> List[int]:
    """
    Get user's pinned folder IDs from the updated schema.
    
    Args:
        supabase: Supabase client
        user_id: User ID
        
    Returns:
        List of pinned folder IDs
    """
    try:
        user_metadata = supabase.table("users_metadata").select("pinned_folder_ids").eq("user_id", user_id).single().execute()
        
        if not user_metadata.data:
            return []
        
        return user_metadata.data.get("pinned_folder_ids", [])
    except Exception as e:
        print(f"Error fetching pinned folders: {str(e)}")
        return []

async def update_user_pinned_folders(supabase: Client, user_id: str, folder_ids: List[int]) -> Dict:
    """
    Update user's pinned folder IDs in the new unified structure.
    
    Args:
        supabase: Supabase client
        user_id: User ID
        folder_ids: List of folder IDs to pin
        
    Returns:
        Success response with updated folder IDs
    """
    try:
        user_metadata = supabase.table("users_metadata").select("id").eq("user_id", user_id).single().execute()
        
        if not user_metadata.data:
            # Create new user metadata
            metadata = {
                "user_id": user_id,
                "pinned_folder_ids": folder_ids
            }
            response = supabase.table("users_metadata").insert(metadata).execute()
        else:
            # Update existing metadata
            response = supabase.table("users_metadata").update({
                "pinned_folder_ids": folder_ids
            }).eq("user_id", user_id).execute()
        
        return {"success": True, "updated_folder_ids": folder_ids}
    except Exception as e:
        print(f"Error updating pinned folders: {str(e)}")
        return {"success": False, "error": str(e)}

async def add_folder_to_pinned(supabase: Client, user_id: str, folder_id: int) -> Dict:
    """
    Add a single folder to user's pinned folders.
    
    Args:
        supabase: Supabase client
        user_id: User ID
        folder_id: Folder ID to pin
        
    Returns:
        Success response
    """
    try:
        current_pinned = await get_user_pinned_folders(supabase, user_id)
        
        if folder_id not in current_pinned:
            current_pinned.append(folder_id)
            return await update_user_pinned_folders(supabase, user_id, current_pinned)
        
        return {"success": True, "message": "Folder already pinned"}
    except Exception as e:
        print(f"Error adding folder to pinned: {str(e)}")
        return {"success": False, "error": str(e)}

async def remove_folder_from_pinned(supabase: Client, user_id: str, folder_id: int) -> Dict:
    """
    Remove a single folder from user's pinned folders.
    
    Args:
        supabase: Supabase client
        user_id: User ID
        folder_id: Folder ID to unpin
        
    Returns:
        Success response
    """
    try:
        current_pinned = await get_user_pinned_folders(supabase, user_id)
        
        if folder_id in current_pinned:
            current_pinned.remove(folder_id)
            return await update_user_pinned_folders(supabase, user_id, current_pinned)
        
        return {"success": True, "message": "Folder was not pinned"}
    except Exception as e:
        print(f"Error removing folder from pinned: {str(e)}")
        return {"success": False, "error": str(e)}

async def get_all_folder_ids_by_type(supabase: Client, folder_type: str, company_id: Optional[str] = None, organization_ids: Optional[List[str]] = None) -> List[int]:
    """
    Get all folder IDs of a specific type with updated access logic.
    
    Args:
        supabase: Supabase client
        folder_type: Type of folders ("official", "company", "user")
        company_id: Company ID for company folders
        organization_ids: Organization IDs for organization folders
        
    Returns:
        List of folder IDs
    """
    try:
        if folder_type == "official":
            # Global official folders
            response = supabase.table("prompt_folders").select("id") \
                .eq("type", "official") \
                .is_("user_id", "null") \
                .is_("company_id", "null") \
                .is_("organization_id", "null") \
                .execute()
            folder_ids = [folder['id'] for folder in (response.data or [])]
            
            # Add organization official folders
            if organization_ids:
                for org_id in organization_ids:
                    org_response = supabase.table("prompt_folders").select("id") \
                        .eq("type", "official") \
                        .eq("organization_id", org_id) \
                        .execute()
                    folder_ids.extend([folder['id'] for folder in (org_response.data or [])])
            
            return folder_ids
            
        elif folder_type == "company" and company_id:
            response = supabase.table("prompt_folders").select("id") \
                .eq("type", "company") \
                .eq("company_id", company_id) \
                .execute()
            return [folder['id'] for folder in (response.data or [])]
        else:
            return []
        
    except Exception as e:
        print(f"Error fetching {folder_type} folder IDs: {str(e)}")
        return []

def add_pinned_status_to_folders(folders: List[Dict], pinned_folder_ids: List[int]) -> List[Dict]:
    """
    Add is_pinned status to folders.
    
    Args:
        folders: List of folder dicts
        pinned_folder_ids: List of pinned folder IDs
        
    Returns:
        Folders with is_pinned status added
    """
    for folder in folders:
        folder["is_pinned"] = folder["id"] in pinned_folder_ids
    return folders

async def fetch_folders_with_hierarchy(
    supabase: Client,
    folder_type: str,
    user_id: Optional[str] = None,
    folder_ids: Optional[List[int]] = None,
    locale: str = "en"
) -> List[Dict]:
    """
    Fetch folders maintaining their hierarchical structure.
    
    Args:
        supabase: Supabase client
        folder_type: Type of folders to fetch
        user_id: User ID for access control
        folder_ids: Specific folder IDs to filter by
        locale: Locale for response processing
        
    Returns:
        List of processed folder dicts with hierarchy info
    """
    try:
        query = supabase.table("prompt_folders").select("*").eq("type", folder_type)
        
        if folder_ids:
            query = query.in_("id", folder_ids)
        
        if folder_type == "user" and user_id:
            query = query.eq("user_id", user_id)
        elif folder_type == "company" and user_id:
            # Get user's company
            user_metadata = supabase.table("users_metadata").select("company_id").eq("user_id", user_id).single().execute()
            if user_metadata.data and user_metadata.data.get("company_id"):
                query = query.eq("company_id", user_metadata.data["company_id"])
            else:
                return []
        
        response = query.execute()
        folders = response.data or []
        
        # Process folders for response
        processed_folders = []
        for folder in folders:
            processed_folder = process_folder_for_response(folder, locale)
            processed_folders.append(processed_folder)
        
        return processed_folders
        
    except Exception as e:
        print(f"Error fetching folders with hierarchy: {str(e)}")
        return []