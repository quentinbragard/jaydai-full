# routes/prompts/templates.py
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional, List, Union, Dict
from supabase import create_client, Client
import os
from utils import supabase_helpers
from utils.prompts import (
    process_template_for_response,
    expand_template_blocks,
    validate_block_access,
    normalize_localized_field
)
from utils.access_control import get_user_metadata
import dotenv
from models.prompts.templates import TemplateCreate, TemplateUpdate, TemplateResponse, TemplateMetadata
from models.common import APIResponse
dotenv.load_dotenv()

# Initialize Supabase client
supabase: Client = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_SERVICE_ROLE_KEY"))


router = APIRouter(tags=["Templates"])

# ---------------------- HELPER FUNCTIONS ----------------------

async def get_user_organizations(user_id: str) -> List[str]:
    """Get all organization IDs a user belongs to"""
    try:
        user_metadata = supabase.table("users_metadata").select("organization_ids").eq("user_id", user_id).single().execute()
        if user_metadata.data and user_metadata.data.get("organization_ids"):
            return user_metadata.data.get("organization_ids", [])
        return []
    except Exception as e:
        print(f"Error fetching user organizations: {str(e)}")
        return []

async def get_user_company(user_id: str) -> Optional[str]:
    """Get company ID a user belongs to"""
    try:
        user_metadata = supabase.table("users_metadata").select("company_id").eq("user_id", user_id).single().execute()
        if user_metadata.data:
            return user_metadata.data.get("company_id")
        return None
    except Exception as e:
        print(f"Error fetching user company: {str(e)}")
        return None
    

async def get_user_templates(user_id: str, locale: str = "en", expand_blocks: bool = True):
    """Get user's personal templates."""
    try:
        # Get user templates
        response = supabase.table("prompt_templates").select("*").eq("user_id", user_id).eq("type", "user").execute()
        
        templates = []
        for template_data in (response.data or []):
            # Process template for response
            processed_template = process_template_for_response(template_data, locale)
            
            # Expand blocks if requested
            if expand_blocks:
                processed_template = await expand_template_blocks(processed_template, locale)
            
            templates.append(processed_template)
        
        return templates
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving user templates: {str(e)}")

async def get_official_templates(user_id: Optional[str] = None, locale: str = "en", expand_blocks: bool = True):
    """
    Get official prompt templates.
    Official templates now include:
    1. Templates with no user_id, company_id, or organization_id
    2. Templates belonging to organizations the user is a member of
    """
    try:
        # Get user's organizations
        org_ids = await get_user_organizations(user_id) if user_id else []
        
        # Start with a base query
        query = supabase.table("prompt_templates").select("*").eq("type", "official")
        
        # Use proper PostgREST filter syntax
        # First, get templates that have no IDs (truly official)
        no_ids_query = query.is_("user_id", "null").is_("company_id", "null").is_("organization_id", "null")
        response = no_ids_query.execute()
        templates = response.data or []
        
        # Then, if user has organizations, get templates from those orgs
        if org_ids:
            for org_id in org_ids:
                org_query = supabase.table("prompt_templates").select("*") \
                    .eq("type", "official") \
                    .eq("organization_id", org_id)
                org_response = org_query.execute()
                if org_response.data:
                    templates.extend(org_response.data)
        
        # Process templates
        processed_templates = []
        for template_data in templates:
            # Process template for response
            processed_template = process_template_for_response(template_data, locale)
            
            # Expand blocks if requested
            if expand_blocks:
                processed_template = await expand_template_blocks(processed_template, locale)
            
            processed_templates.append(processed_template)
        
        return processed_templates
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving official templates: {str(e)}")
    
    
async def get_company_templates(user_id: Optional[str] = None, locale: str = "en", expand_blocks: bool = True):
    """Get company templates for the user's company."""
    try:
        company_id = None
        
        if user_id:
            # Get user's company_id
            company_id = await get_user_company(user_id)
        
        if not company_id:
            return []
        
        # Get company templates
        response = supabase.table("prompt_templates").select("*").eq("type", "company").eq("company_id", company_id).execute()
        
        templates = []
        for template_data in (response.data or []):
            # Process template for response
            processed_template = process_template_for_response(template_data, locale)
            
            # Expand blocks if requested
            if expand_blocks:
                processed_template = await expand_template_blocks(processed_template, locale)
            
            templates.append(processed_template)
        
        return templates
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving company templates: {str(e)}")

async def get_all_templates(user_id: str, locale: str = "en", expand_blocks: bool = True):
    """Get templates organized by type (official, company, and user)."""
    #try:
    # Get all template types
    user_templates = await get_user_templates(user_id, locale, expand_blocks)
    official_templates = await get_official_templates(user_id, locale, expand_blocks)
    company_templates = await get_company_templates(user_id, locale, expand_blocks)
    
    # Combine all templates
    all_templates = user_templates + official_templates + company_templates
    return APIResponse(success=True, data=all_templates)

    #except Exception as e:
    #    raise HTTPException(status_code=500, detail=f"Error retrieving all templates: {str(e)}")
