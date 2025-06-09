"""
Utility functions for folder operations in the prompts system.
"""
from typing import Dict, List, Optional, Any
from supabase import Client
from .locales import extract_localized_field
from utils.access_control import apply_access_conditions

def determine_folder_type(folder: Dict) -> str:
    """
    Determine folder type based on user_id and organization_id fields.
    
    Args:
        folder: Folder record dict
        
    Returns:
        Folder type: "user", "organization", or "official"
    """
    if folder.get("user_id"):
        return "user"
    elif folder.get("company_id"):
        return "organization"
    else:
        return "official"

def process_folder_for_response(folder: Dict, locale: str = "en") -> Dict:
    """
    Process a folder record for API response with localization.
    
    Args:
        folder: Raw folder record from database
        locale: Requested locale
        
    Returns:
        Processed folder dict ready for API response
    """
    processed = folder.copy()
    
    # Determine if this is user content
    folder_type = determine_folder_type(folder)
    is_user_content = folder_type == "user"
    
    # Extract localized fields
    if "title" in folder:
        processed["name"] = extract_localized_field(folder["title"], locale, is_user_content)
    
    if "description" in folder:
        processed["description"] = extract_localized_field(folder["description"], locale, is_user_content)
    
    # Add folder type for backward compatibility
    processed["type"] = folder_type
    
    # Remove JSON fields to avoid confusion in response
    processed.pop("title", None)
    
    return processed

async def fetch_folders_by_type(
    supabase: Client,
    folder_type: Optional[str] = None,
    user_id: Optional[str] = None,
    company_id: Optional[str] = None,
    folder_ids: Optional[List[int]] = None,
    locale: str = "en"
) -> List[Dict]:
    """
    Fetch folders from unified prompt_folders table based on type and filters.
    
    Args:
        supabase: Supabase client
        folder_type: Type of folders to fetch ("user", "organization", "official")
        user_id: User ID for user folders
        company_id: Organization ID for org folders
        folder_ids: Specific folder IDs to filter by
        locale: Locale for response processing
        
    Returns:
        List of processed folder dicts
    """
    query = supabase.table("prompt_folders").select("*")

    if folder_type:
        query = query.eq("type", folder_type)

    if folder_ids:
        query = query.in_("id", folder_ids)

    if user_id:
        query = apply_access_conditions(query, supabase, user_id)
    
    response = query.execute()
    folders = response.data or []
    # Process folders for response
    return [process_folder_for_response(folder, locale) for folder in folders]

async def get_user_pinned_folders(supabase: Client, user_id: str) -> Dict[str, List[int]]:
    """
    Get user's pinned folder IDs.
    
    Args:
        supabase: Supabase client
        user_id: User ID
        
    Returns:
        Dict with "official" and "organization" pinned folder ID lists
    """
    user_metadata = supabase.table("users_metadata").select("*").eq("user_id", user_id).single().execute()
    
    if not user_metadata.data:
        return {"official": [], "organization": []}
    
    return {
        "official": user_metadata.data.get("pinned_official_folder_ids", []),
        "organization": user_metadata.data.get("pinned_organization_folder_ids", [])
    }

async def update_user_pinned_folders(supabase: Client, user_id: str, folder_type: str, folder_ids: List[int]) -> Dict:
    """
    Update user's pinned folder IDs.
    
    Args:
        supabase: Supabase client
        user_id: User ID
        folder_type: Type of folders ("official" or "organization")
        folder_ids: List of folder IDs to pin
        
    Returns:
        Success response with updated folder IDs
    """
    user_metadata = supabase.table("users_metadata").select("*").eq("user_id", user_id).single().execute()
    
    field_name = f"pinned_{folder_type}_folder_ids"
    
    if not user_metadata.data:
        # Create new user metadata
        metadata = {"user_id": user_id}
        metadata[field_name] = folder_ids
        response = supabase.table("users_metadata").insert(metadata).execute()
    else:
        # Update existing metadata
        response = supabase.table("users_metadata").update({
            field_name: folder_ids
        }).eq("user_id", user_id).execute()
    
    return {"success": True, "updated_folder_ids": folder_ids}

async def get_all_folder_ids_by_type(supabase: Client, folder_type: str, company_id: Optional[str] = None) -> List[int]:
    """
    Get all folder IDs of a specific type.
    
    Args:
        supabase: Supabase client
        folder_type: Type of folders ("official", "organization")
        company_id: Organization ID for org folders
        
    Returns:
        List of folder IDs
    """
    try:
        if folder_type == "official":
            response = supabase.table("prompt_folders").select("id").is_("user_id", "null").is_("company_id", "null").execute()
        elif folder_type == "organization" and company_id:
            response = supabase.table("prompt_folders").select("id").eq("company_id", organization_id).execute()
        else:
            return []
        
        return [folder['id'] for folder in (response.data or [])]
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