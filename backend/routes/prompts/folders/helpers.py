from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from supabase import create_client, Client
from utils import supabase_helpers
from utils.prompts import (
    fetch_templates_for_folders,
    organize_templates_by_folder,
    add_templates_to_folders,
    get_user_pinned_folders,
    update_user_pinned_folders,
    add_pinned_status_to_folders,
    create_localized_field,
    determine_folder_type
)
import dotenv
import os
from typing import List, Optional
from enum import Enum
from models.common import APIResponse


dotenv.load_dotenv()

# Initialize Supabase client
supabase: Client = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_SERVICE_ROLE_KEY"))

router = APIRouter(tags=["Folders"])

class FolderBase(BaseModel):
    name: str
    path: str
    description: Optional[str] = None

class FolderCreate(FolderBase):
    parent_id: Optional[int] = None

class FolderUpdate(FolderBase):
    pass

class PromptType(str, Enum):
    official = "official"
    user = "user"
    company = "company"

# ---------------------- HELPER FUNCTIONS ----------------------

async def get_user_organizations(user_id: str) -> APIResponse[List[str]]:
    """Get all organization IDs a user belongs to"""
    try:
        user_metadata = supabase.table("users_metadata").select("organization_ids").eq("user_id", user_id).single().execute()
        if user_metadata.data and user_metadata.data.get("organization_ids"):
            return APIResponse(success=True, data=user_metadata.data.get("organization_ids", []))
        return APIResponse(success=True, data=[])
    except Exception as e:
        print(f"Error fetching user organizations: {str(e)}")
        return APIResponse(success=False, message="Error fetching user organizations")

async def get_user_company(user_id: str) -> APIResponse[Optional[str]]:
    """Get company ID a user belongs to"""
    try:
        user_metadata = supabase.table("users_metadata").select("company_id").eq("user_id", user_id).single().execute()
        if user_metadata.data:
            return APIResponse(success=True, data=user_metadata.data.get("company_id"))
        return APIResponse(success=True, data=None)
    except Exception as e:
        print(f"Error fetching user company: {str(e)}")
        return APIResponse(success=False, message="Error fetching user company")

async def fetch_folders_by_type(
    supabase: Client,
    folder_type: str,
    user_id: Optional[str] = None,
    folder_ids: Optional[List[int]] = None,
    locale: str = "en"
) -> APIResponse[List[dict]]:
    """Fetch folders by type with updated access logic"""
    try:
        # Start with base query
        query = supabase.table("prompt_folders").select("*").eq("type", folder_type)
        
        if folder_type == "user" and user_id:
            # User folders: owned by the user
            query = query.eq("user_id", user_id)
        elif folder_type == "company" and user_id:
            # Company folders: from user's company
            company_resp = await get_user_company(user_id)
            if not company_resp.success:
                return company_resp
            company_id = company_resp.data
            if company_id:
                query = query.eq("company_id", company_id)
            else:
                return APIResponse(success=False, message="No company, no folders")
        elif folder_type == "official" and user_id:
            # We'll need multiple queries for official folders
            folders = []
            
            # 1. Global official folders (no IDs)
            global_query = supabase.table("prompt_folders").select("*") \
                .eq("type", folder_type) \
                .is_("user_id", "null") \
                .is_("company_id", "null") \
                .is_("organization_id", "null")
                
            if folder_ids:
                global_query = global_query.in_("id", folder_ids)
                
            global_response = global_query.execute()
            if global_response.data:
                folders.extend(global_response.data)
            
            # 2. User's organization folders
            org_resp = await get_user_organizations(user_id)
            if not org_resp.success:
                return org_resp
            for org_id in org_resp.data:
                org_query = supabase.table("prompt_folders").select("*") \
                    .eq("type", folder_type) \
                    .eq("organization_id", org_id)
                    
                if folder_ids:
                    org_query = org_query.in_("id", folder_ids)
                    
                org_response = org_query.execute()
                if org_response.data:
                    folders.extend(org_response.data)
            
            # Process folders for response
            processed_folders = []
            for folder_data in folders:
                from utils.prompts.folders import process_folder_for_response
                processed_folder = process_folder_for_response(folder_data, locale)
                processed_folders.append(processed_folder)
            
            return APIResponse(success=True, data=processed_folders)
        
        # For user and company folders, continue with the original query
        
        # Filter by specific folder IDs if provided
        if folder_ids:
            query = query.in_("id", folder_ids)
        
        # Execute query
        response = query.execute()
        
        # Process folders for response
        folders = []
        for folder_data in (response.data or []):
            from utils.prompts.folders import process_folder_for_response
            processed_folder = process_folder_for_response(folder_data, locale)
            folders.append(processed_folder)
        
        return APIResponse(success=True, data=folders)
    
    except Exception as e:
        print(f"Error fetching folders: {str(e)}")
        return APIResponse(success=False, message="Error fetching folders")
    

# ---------------------- ROUTE HANDLERS ----------------------

