from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from supabase import create_client, Client
from utils import supabase_helpers
from utils.prompts import (
    get_all_folder_ids_by_type,
    process_folder_for_response,
    process_template_for_response
)
import dotenv
import os
from typing import List

dotenv.load_dotenv()

# Initialize Supabase client
supabase: Client = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_SERVICE_ROLE_KEY"))

router = APIRouter(prefix="/user", tags=["User"])

class UserMetadata(BaseModel):
    name: str | None = None
    additional_email: str | None = None
    phone_number: str | None = None
    additional_organization: str | None = None
    company_id: str | None = None
    pinned_official_folder_ids: list[int] | None = None
    pinned_organization_folder_ids: list[int] | None = None

@router.get("/metadata")
async def get_user_metadata(user_id: str = Depends(supabase_helpers.get_user_from_session_token)):
    """Get metadata for a specific user."""
    try:
        response = supabase.table("users_metadata") \
            .select("name, additional_email, phone_number, additional_organization, company_id, pinned_official_folder_ids, pinned_organization_folder_ids") \
            .eq("user_id", user_id) \
            .single() \
            .execute()
            
        if not response.data:
            return {
                "success": True,
                "data": {
                    "name": None,
                    "additional_email": None,
                    "phone_number": None,
                    "additional_organization": None,
                    "company_id": None,
                    "pinned_official_folder_ids": [],
                    "pinned_organization_folder_ids": []
                }
            }
            
        return {
            "success": True,
            "data": response.data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching user metadata: {str(e)}")

@router.put("/metadata")
async def update_user_metadata(metadata: UserMetadata, user_id: str = Depends(supabase_helpers.get_user_from_session_token)):
    """Update user metadata with organization folder auto-pinning."""
    try:
        # Check if user metadata exists
        existing_metadata = supabase.table("users_metadata") \
            .select("user_id") \
            .eq("user_id", user_id) \
            .single() \
            .execute()
        
        update_data = {}
        
        # Only include fields that are provided
        if metadata.name is not None:
            update_data["name"] = metadata.name
            
        if metadata.additional_email is not None:
            update_data["additional_email"] = metadata.additional_email
            
        if metadata.phone_number is not None:
            update_data["phone_number"] = metadata.phone_number
            
        if metadata.additional_organization is not None:
            update_data["additional_organization"] = metadata.additional_organization
        
        # Handle company_id update and auto-pin organization folders
        if metadata.company_id is not None:
            # If organization has changed or is being set for the first time
            current_org_id = existing_metadata.data.get("company_id") if existing_metadata.data else None
            if metadata.company_id != current_org_id:
                update_data["company_id"] = metadata.organization_id
                
                # Auto-pin all folders for this organization using utility
                organization_folder_ids = await get_all_folder_ids_by_type(
                    supabase, 
                    "organization", 
                    str(metadata.organization_id)
                )
                update_data["pinned_organization_folder_ids"] = organization_folder_ids
        
        # Handle explicit updates to pinned folder IDs (only if provided)
        if metadata.pinned_official_folder_ids is not None:
            update_data["pinned_official_folder_ids"] = metadata.pinned_official_folder_ids
            
        if metadata.pinned_organization_folder_ids is not None:
            update_data["pinned_organization_folder_ids"] = metadata.pinned_organization_folder_ids
        
        # Only proceed if there are changes to make
        if update_data:
            if existing_metadata.data:
                # Update existing record
                response = supabase.table("users_metadata") \
                    .update(update_data) \
                    .eq("user_id", user_id) \
                    .execute()
            else:
                # Create new record
                update_data["user_id"] = user_id
                response = supabase.table("users_metadata") \
                    .insert(update_data) \
                    .execute()
            
            return {
                "success": True,
                "data": response.data[0] if response.data else None
            }
        else:
            return {
                "success": True,
                "message": "No changes to update"
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating user metadata: {str(e)}")

@router.get("/folders-with-prompts")
async def get_folders_with_prompts(
    locale: str = "en",
    user_id: str = Depends(supabase_helpers.get_user_from_session_token)
):
    """Get all folders with their prompts, including pinned status."""
    try:
        # Get user metadata for pinned folders
        metadata = supabase.table("users_metadata") \
            .select("pinned_official_folder_ids, pinned_organization_folder_ids, company_id") \
            .eq("user_id", user_id) \
            .single() \
            .execute()
            
        pinned_official_folders = metadata.data.get('pinned_official_folder_ids', []) if metadata.data else []
        pinned_org_folders = metadata.data.get('pinned_organization_folder_ids', []) if metadata.data else []
        user_org_id = metadata.data.get('organization_id') if metadata.data else None

        # Get all prompts
        prompts = supabase.table("prompt_templates") \
            .select("*") \
            .execute()

        # Get folders from unified table
        # Official folders
        official_folders_response = supabase.table("prompt_folders") \
            .select("*") \
            .is_("user_id", "null") \
            .is_("company_id", "null") \
            .execute()
        
        # Organization folders (for user's organization)
        org_folders_response = None
        if user_org_id:
            org_folders_response = supabase.table("prompt_folders") \
                .select("*") \
                .eq("company_id", user_org_id) \
                .execute()
        
        # User folders
        user_folders_response = supabase.table("prompt_folders") \
            .select("*") \
            .eq("user_id", user_id) \
            .execute()

        # Organize prompts by folder and type
        organized_folders = {
            "official": [],
            "organization": [],
            "user": []
        }

        # Process official folders
        for folder in official_folders_response.data or []:
            processed_folder = process_folder_for_response(folder, locale)
            
            # Process prompts for this folder
            folder_prompts = []
            for p in prompts.data or []:
                if p.get("folder_id") == folder["id"] and p.get("type") == "official":
                    processed_prompt = process_template_for_response(p, locale)
                    folder_prompts.append(processed_prompt)
                    
            processed_folder["prompts"] = folder_prompts
            processed_folder["is_pinned"] = folder["id"] in pinned_official_folders
            organized_folders["official"].append(processed_folder)

        # Process organization folders
        if org_folders_response:
            for folder in org_folders_response.data or []:
                processed_folder = process_folder_for_response(folder, locale)
                
                # Process prompts for this folder
                folder_prompts = []
                for p in prompts.data or []:
                    if p.get("folder_id") == folder["id"] and p.get("type") == "organization":
                        processed_prompt = process_template_for_response(p, locale)
                        folder_prompts.append(processed_prompt)
                        
                processed_folder["prompts"] = folder_prompts
                processed_folder["is_pinned"] = folder["id"] in pinned_org_folders
                organized_folders["organization"].append(processed_folder)

        # Process user folders
        for folder in user_folders_response.data or []:
            processed_folder = process_folder_for_response(folder, locale)
            
            # Get prompts for this folder
            folder_prompts = []
            for p in prompts.data or []:
                if p.get("folder_id") == folder["id"] and p.get("type") == "user":
                    processed_prompt = process_template_for_response(p, locale)
                    folder_prompts.append(processed_prompt)
            
            processed_folder["prompts"] = folder_prompts
            organized_folders["user"].append(processed_folder)

        return {
            "success": True,
            "data": organized_folders
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching folders with prompts: {str(e)}")
    

@router.get("/onboarding/status")
async def get_onboarding_status(user_id: str = Depends(supabase_helpers.get_user_from_session_token)):
    try:
        # Get user metadata for pinned folders
        metadata = supabase.table("users_metadata") \
            .select("job_type, job_industry, job_seniority, interests, signup_source") \
            .eq("user_id", user_id) \
            .single() \
            .execute()

        # Debug logging
        print(f"Metadata response: {metadata.data}")

        # Check if metadata exists and has any of the required fields
        has_completed = False
        if metadata.data:
            job_type = metadata.data.get("job_type")
            job_industry = metadata.data.get("job_industry")
            job_seniority = metadata.data.get("job_seniority")
            interests = metadata.data.get("interests")
            signup_source = metadata.data.get("signup_source")
            
            has_completed = bool(job_type or job_industry or job_seniority or interests or signup_source)
            
            # Debug logging
            print(f"Fields found: job_type={job_type}, job_industry={job_industry}, "
                  f"job_seniority={job_seniority}, interests={interests}, "
                  f"signup_source={signup_source}")
            
            print(has_completed)

        return {
            "success": True,
            "data": {"has_completed_onboarding": has_completed}
        }
    except Exception as e:
        print(f"Error in onboarding status: {str(e)}")  # Debug logging
        raise HTTPException(status_code=500, detail=f"Error checking onboarding status: {str(e)}")

    
    