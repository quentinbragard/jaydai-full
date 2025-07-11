# routes/organizations/get_organizations.py
from typing import List, Optional
from fastapi import Depends, HTTPException
from pydantic import BaseModel
from utils import supabase_helpers
from utils.access_control import get_user_metadata
from supabase import create_client, Client
import os

# Initialize Supabase client
supabase: Client = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_SERVICE_ROLE_KEY"))

class OrganizationResponse(BaseModel):
    id: str
    name: str
    image_url: Optional[str] = None
    banner_url: Optional[str] = None
    created_at: Optional[str] = None
    website_url: Optional[str] = None
class APIResponse(BaseModel):
    success: bool
    data: Optional[List[OrganizationResponse]] = None
    message: Optional[str] = None

async def get_organizations(
    user_id: str = Depends(supabase_helpers.get_user_from_session_token),
) -> APIResponse:
    """Get organizations that the user has access to."""
    try:
        # Get user's organization IDs from metadata
        user_metadata = get_user_metadata(supabase, user_id)
        organization_ids = user_metadata.get("organization_ids", [])
        
        if not organization_ids:
            return APIResponse(success=True, data=[])
        
        # Fetch organizations data
        response = supabase.table("organizations").select("id, name, image_url, banner_url, website_url").in_("id", organization_ids).execute()
        
        organizations = []
        for org_data in (response.data or []):
            organization = OrganizationResponse(
                id=org_data["id"],
                name=org_data["name"],
                image_url=org_data.get("image_url"),
                banner_url=org_data.get("banner_url"),
                website_url=org_data.get("website_url"),
            )
            organizations.append(organization)
        
        return APIResponse(success=True, data=organizations)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving organizations: {str(e)}")