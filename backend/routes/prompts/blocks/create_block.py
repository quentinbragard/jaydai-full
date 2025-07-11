# routes/prompts/blocks/create_block.py - REPLACE ENTIRE FUNCTION
from fastapi import Depends, HTTPException, Request 
from models.prompts.blocks import BlockCreate, BlockResponse
from models.common import APIResponse
from utils import supabase_helpers
from utils.middleware.localization import extract_locale_from_request 
from utils.prompts.locales import ensure_localized_field
from utils.access_control import get_user_metadata
from .helpers import router, supabase, process_block_for_response

@router.post("", response_model=APIResponse[BlockResponse])
async def create_block(
    block: BlockCreate,
    request: Request,
    user_id: str = Depends(supabase_helpers.get_user_from_session_token),
):
    """Create a new block with access control validation."""
    try:
        locale = extract_locale_from_request(request)
        
        # Get user metadata for validation
        user_metadata = get_user_metadata(supabase, user_id)
        
        # Validate organization/company access if specified
        if block.organization_id:
            user_org_ids = user_metadata.get("organization_ids", [])
            if block.organization_id not in user_org_ids:
                raise HTTPException(status_code=403, detail="Access denied to specified organization")
        
        if block.company_id:
            user_company_id = user_metadata.get("company_id")
            if block.company_id != user_company_id:
                raise HTTPException(status_code=403, detail="Access denied to specified company")
        
        # Convert string fields to localized format for database storage
        localized_title = ensure_localized_field(block.title, locale) if block.title else {}
        localized_content = ensure_localized_field(block.content, locale) if block.content else {}
        localized_description = ensure_localized_field(block.description, locale) if block.description else {}
        
        block_data = {
            "type": block.type,
            "content": localized_content,
            "title": localized_title,
            "description": localized_description,
            "user_id": user_id,
            "organization_id": block.organization_id,
            "company_id": block.company_id,
            "published": block.published if block.published is not None else True
        }
        
        response = supabase.table("prompt_blocks").insert(block_data).execute()
        
        if response.data:
            created_block = response.data[0]
            processed_block = process_block_for_response(created_block, locale)
            return APIResponse(success=True, data=processed_block)
        else:
            raise HTTPException(status_code=400, detail="Failed to create block")
            
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"Error creating block: {str(e)}")


