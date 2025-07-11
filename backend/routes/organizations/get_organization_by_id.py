# routes/organizations/get_organization_by_id.py
from typing import Optional
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
    data: Optional[OrganizationResponse] = None
    message: Optional[str] = None

async def get_organization_by_id(
    organization_id: str,
    user_id: str = Depends(supabase_helpers.get_user_from_session_token),
) -> APIResponse:
    """Get a specific organization by ID if user has access."""
    try:
        # Check if user has access to this organization
        user_metadata = get_user_metadata(supabase, user_id)
        organization_ids = user_metadata.get("organization_ids", [])
        
        if organization_id not in organization_ids:
            raise HTTPException(status_code=403, detail="Access denied to this organization")
        
        # Fetch organization data
        response = supabase.table("organizations").select("id, name, image_url, banner_url, created_at, website_url").eq("id", organization_id).single().execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Organization not found")
        
        org_data = response.data
        organization = OrganizationResponse(
            id=org_data["id"],
            name=org_data["name"],
            image_url=org_data.get("image_url"),
            banner_url=org_data.get("banner_url"),
            website_url=org_data.get("website_url"),
        )
        
        return APIResponse(success=True, data=organization)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving organization: {str(e)}")