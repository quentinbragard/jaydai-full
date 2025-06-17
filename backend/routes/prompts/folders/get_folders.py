# Updated routes/prompts/folders/get_folders.py

from typing import List, Optional, Dict, Any
from fastapi import Depends, HTTPException, Query
from models.common import APIResponse
from utils import supabase_helpers
from .helpers import supabase, router
from utils.prompts import process_folder_for_response, process_template_for_response
from utils.access_control import get_user_metadata

async def fetch_accessible_folders(
    supabase,
    user_id: str,
    folder_types: List[str],
    locale: str = "en"
) -> Dict[str, List[Dict]]:
    """
    Fetch all accessible folders by type with proper access control.
    """
    user_metadata = get_user_metadata(supabase, user_id)
    pinned_folder_ids = await get_user_pinned_folder_ids(supabase, user_id)
    
    folders_by_type = {}
    
    for folder_type in folder_types:
        folders = []
        
        if folder_type == "user":
            # Get all user folders (not filtered by pinned for user folders)
            response = supabase.table("prompt_folders").select("*").eq("user_id", user_id).eq("type", "user").execute()
            folders = response.data or []
            
        elif folder_type == "official":
            # Get pinned official folders and their necessary hierarchy
            if pinned_folder_ids:
                print(f"Debug: Looking for pinned folder IDs: {pinned_folder_ids}")
                
                # Get all official folders that are pinned
                all_official_folders = []
                
                # Global official folders
                global_response = supabase.table("prompt_folders").select("*") \
                    .eq("type", "official") \
                    .is_("user_id", "null") \
                    .is_("company_id", "null") \
                    .is_("organization_id", "null") \
                    .execute()
                print(f"Debug: Found {len(global_response.data or [])} global official folders")
                all_official_folders.extend(global_response.data or [])
                
                # Organization official folders
                org_ids = user_metadata.get("organization_ids", [])
                print(f"Debug: User organization IDs: {org_ids}")
                if org_ids:
                    for org_id in org_ids:
                        org_response = supabase.table("prompt_folders").select("*") \
                            .eq("type", "official") \
                            .eq("organization_id", org_id) \
                            .execute()
                        print(f"Debug: Found {len(org_response.data or [])} org folders for org {org_id}")
                        all_official_folders.extend(org_response.data or [])
                
                print(f"Debug: Total official folders found: {len(all_official_folders)}")
                print(f"Debug: Official folder IDs: {[f['id'] for f in all_official_folders]}")
                
                # Filter to only include pinned folders
                folders = [f for f in all_official_folders if f["id"] in pinned_folder_ids]
                print(f"Debug: Filtered to {len(folders)} pinned folders")
            else:
                print("Debug: No pinned folder IDs found")
                        
        elif folder_type == "company":
            # Get pinned company folders
            company_id = user_metadata.get("company_id")
            if company_id and pinned_folder_ids:
                response = supabase.table("prompt_folders").select("*") \
                    .eq("type", "company") \
                    .eq("company_id", company_id) \
                    .execute()
                # Filter to only pinned folders
                all_company_folders = response.data or []
                folders = [f for f in all_company_folders if f["id"] in pinned_folder_ids]
        
        elif folder_type == "mixed":
            # NEW: Handle mixed type - combination of official and organization folders
            if pinned_folder_ids:
                print(f"Debug: Fetching mixed folders for pinned IDs: {pinned_folder_ids}")
                
                all_mixed_folders = []
                
                # Global official folders
                global_response = supabase.table("prompt_folders").select("*") \
                    .eq("type", "official") \
                    .is_("user_id", "null") \
                    .is_("company_id", "null") \
                    .is_("organization_id", "null") \
                    .execute()
                all_mixed_folders.extend(global_response.data or [])
                
                # Organization official folders
                org_ids = user_metadata.get("organization_ids", [])
                if org_ids:
                    for org_id in org_ids:
                        org_response = supabase.table("prompt_folders").select("*") \
                            .eq("type", "official") \
                            .eq("organization_id", org_id) \
                            .execute()
                        all_mixed_folders.extend(org_response.data or [])
                
                # Company folders if user has company
                company_id = user_metadata.get("company_id")
                if company_id:
                    company_response = supabase.table("prompt_folders").select("*") \
                        .eq("type", "company") \
                        .eq("company_id", company_id) \
                        .execute()
                    all_mixed_folders.extend(company_response.data or [])
                
                # Filter to only pinned folders
                folders = [f for f in all_mixed_folders if f["id"] in pinned_folder_ids]
                print(f"Debug: Mixed folders filtered to {len(folders)} pinned folders")
            else:
                print("Debug: No pinned folder IDs found for mixed folders")
        
        # Process folders for response
        processed_folders = []
        for folder in folders:
            processed_folder = process_folder_for_response(folder, locale)
            processed_folders.append(processed_folder)
        
        folders_by_type[folder_type] = processed_folders
    
    return folders_by_type

@router.get("", response_model=APIResponse[Dict])
async def get_folders(
    type: Optional[str] = Query(None, description="Folder type filter (user, official, company, mixed)"),
    withSubfolders: bool = Query(False, description="Include nested subfolders"),
    withTemplates: bool = Query(False, description="Include templates for each folder"),
    locale: Optional[str] = Query("en", description="Locale for localized content"),
    user_id: str = Depends(supabase_helpers.get_user_from_session_token),
) -> APIResponse[Dict]:
    """
    Get folders with optional nested structure and templates.
    """
    try:
        # Determine which folder types to fetch
        if type:
            if type not in ["user", "official", "company", "mixed"]:
                raise HTTPException(status_code=400, detail="Invalid folder type")
            folder_types = [type]
        else:
            folder_types = ["user", "official", "company"]
        
        # Fetch all accessible folders by type (includes descendants for pinned folders)
        folders_by_type = await fetch_accessible_folders(supabase, user_id, folder_types, locale)
        
        # Prepare result structure
        result = {"folders": {}}
        
        # Process each folder type
        for folder_type in folder_types:
            folders = folders_by_type.get(folder_type, [])
            
            print(f"Debug: Processing {folder_type} folders: {[f['id'] for f in folders] if folders else 'none'}")
            
            # Get all folder IDs for template fetching
            all_folder_ids = [f["id"] for f in folders] if folders else []
            
            # Fetch templates if requested
            templates_by_folder = {}
            if withTemplates and all_folder_ids:
                templates_by_folder = await fetch_templates_for_all_folders(
                    supabase, all_folder_ids, locale
                )
            
            # Handle special case for user folders with root templates
            if folder_type == "user" and withTemplates:
                print(f"Debug: Fetching root templates for user_id: {user_id}")
                root_templates_response = supabase.table("prompt_templates").select("*") \
                    .eq("user_id", user_id) \
                    .is_("folder_id", "null") \
                    .execute()
                
                root_templates = root_templates_response.data or []
                print(f"Debug: Found {len(root_templates)} root templates for user")
                
                if root_templates:
                    # Process root templates
                    processed_root_templates = []
                    for template in root_templates:
                        processed_template = process_template_for_response(template, locale)
                        processed_root_templates.append(processed_template)
                    
                    # Add root templates to folder_id = 0
                    templates_by_folder[0] = processed_root_templates
                    
                    # Create virtual root folder
                    virtual_root_folder = {
                        "id": 0,
                        "created_at": None,
                        "user_id": user_id,
                        "organization_id": None,
                        "parent_folder_id": None,
                        "content": {
                            "en": "Root Templates",
                            "fr": "Modèles Racine"
                        },
                        "description": "Templates not assigned to any folder",
                        "company_id": None,
                        "type": "user",
                        "name": "Root Templates"
                    }
                    
                    # Add the virtual folder to the beginning of folders list
                    folders = [virtual_root_folder] + folders
            
            if not folders:
                result["folders"][folder_type] = []
                continue
            
            if withSubfolders:
                # Build nested structure starting from root folders
                nested_folders = await build_nested_folder_structure(
                    folders, templates_by_folder, None, withTemplates
                )
                print(f"Debug: Built nested structure for {folder_type}: {[f.get('id') for f in nested_folders]}")
                result["folders"][folder_type] = nested_folders
            else:
                # Flat structure - show all folders at the same level
                display_folders = folders
                
                if withTemplates:
                    # Add templates to each folder
                    for folder in display_folders:
                        folder_templates = templates_by_folder.get(folder["id"], [])
                        if folder_templates:
                            folder["templates"] = folder_templates
                
                result["folders"][folder_type] = display_folders
        
        return APIResponse(success=True, data=result)
        
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"Error retrieving folders: {str(e)}")

async def get_user_pinned_folder_ids(supabase, user_id: str) -> List[int]:
    """Get user's pinned folder IDs from the updated schema."""
    try:
        user_metadata = supabase.table("users_metadata").select("pinned_folder_ids").eq("user_id", user_id).single().execute()
        
        if not user_metadata.data:
            print(f"Debug: No user metadata found for user {user_id}")
            return []
        
        pinned_ids = user_metadata.data.get("pinned_folder_ids", [])
        print(f"Debug: Found pinned folder IDs for user {user_id}: {pinned_ids}")
        return pinned_ids
    except Exception as e:
        print(f"Debug: Error fetching pinned folders for user {user_id}: {str(e)}")
        return []

async def fetch_templates_for_all_folders(
    supabase,
    folder_ids: List[int],
    locale: str = "en"
) -> Dict[int, List[Dict]]:
    """
    Fetch all templates for the given folder IDs.
    """
    if not folder_ids:
        return {}
    
    # Get all templates for these folders
    response = supabase.table("prompt_templates").select("*").in_("folder_id", folder_ids).execute()
    templates = response.data or []
    
    # Group templates by folder_id
    templates_by_folder = {}
    for template in templates:
        folder_id = template.get("folder_id")
        if folder_id:
            if folder_id not in templates_by_folder:
                templates_by_folder[folder_id] = []
            
            processed_template = process_template_for_response(template, locale)
            templates_by_folder[folder_id].append(processed_template)
    
    return templates_by_folder

async def build_nested_folder_structure(
    folders: List[Dict],
    templates_by_folder: Dict[int, List[Dict]],
    parent_id: Optional[int] = None,
    with_templates: bool = False,
    processed_ids: Optional[set] = None
) -> List[Dict]:
    """
    Recursively build nested folder structure with circular reference protection.
    """
    if processed_ids is None:
        processed_ids = set()
    
    result = []
    
    # Find folders with the specified parent_id
    child_folders = []
    for f in folders:
        folder_parent_id = f.get("parent_folder_id")
        folder_id = f.get("id")
        
        # Skip circular references (folder cannot be its own parent)
        if folder_id == folder_parent_id:
            print(f"Debug: Skipping circular reference for folder {folder_id}")
            continue
            
        # Skip if this folder was already processed (prevents infinite loops)
        if folder_id in processed_ids:
            continue
            
        if folder_parent_id == parent_id:
            child_folders.append(f)
    
    for folder in child_folders:
        folder_id = folder["id"]
        
        # Mark this folder as processed
        processed_ids.add(folder_id)
        
        folder_data = folder.copy()
        
        # Get child folders recursively
        children = await build_nested_folder_structure(
            folders, templates_by_folder, folder_id, with_templates, processed_ids
        )
        
        if children:
            folder_data["subfolders"] = children
        
        # Add templates if requested
        if with_templates:
            folder_templates = templates_by_folder.get(folder_id, [])
            if folder_templates:
                folder_data["templates"] = folder_templates
        
        result.append(folder_data)
    
    return result