from fastapi import Depends, HTTPException
from typing import Optional
from models.prompts.templates import TemplateCreate, TemplateResponse
from models.common import APIResponse
from utils import supabase_helpers
from utils.prompts import process_template_for_response, expand_template_blocks, validate_block_access, normalize_localized_field
from utils.access_control import get_user_metadata
from . import router, supabase

async def _validate_template_blocks(template: TemplateCreate, user_id: str) -> None:
    """Validate all block references in template and metadata."""
    all_block_ids = set()
    # Collect block IDs from metadata if present
    if template.metadata:
        metadata_blocks = [
            template.metadata.role,
            template.metadata.context, 
            template.metadata.goal,
            template.metadata.tone_style,
            template.metadata.output_format,
            template.metadata.audience,
        ]
        # Add any list-based metadata blocks
        if template.metadata.examples:
            metadata_blocks.extend(template.metadata.examples)
        if template.metadata.constraints:
            metadata_blocks.extend(template.metadata.constraints)
        if template.metadata.thinking_steps:
            metadata_blocks.extend(template.metadata.thinking_steps)
            
        all_block_ids.update(bid for bid in metadata_blocks if bid and bid != 0)
    
    # Validate access to all blocks
    if all_block_ids and not await validate_block_access(list(all_block_ids), user_id):
        raise HTTPException(status_code=403, detail="Access denied to one or more referenced blocks")

def _prepare_template_data(template: TemplateCreate, user_id: str, user_metadata: dict) -> dict:
    """Prepare template data for database insertion."""
    # Determine ownership based on template type
    template_data = {
        "type": template.type,
        "title": normalize_localized_field(template.title),
        "content": normalize_localized_field(template.content),
        "description": normalize_localized_field(template.description) if template.description else {},
        "folder_id": template.folder_id,
        "metadata": template.metadata.model_dump() if template.metadata else {},
        "usage_count": 0,
        "user_id": None,
        "company_id": None,
        "organization_id": None,
    }
    
    # Set ownership based on type
    if template.type == "user":
        template_data["user_id"] = user_id
        
    elif template.type == "company":
        template_data["company_id"] = user_metadata.get("company_id")
        if not template_data["company_id"]:
            raise HTTPException(status_code=400, detail="User has no company for company template")
            
    elif template.type == "organization":
        # For organization templates, user must specify which organization
        organization_ids = user_metadata.get("organization_ids", [])
        if not organization_ids:
            raise HTTPException(status_code=400, detail="User doesn't belong to any organization")
        
        # If template has organization_id specified, validate user has access
        if hasattr(template, 'organization_id') and template.organization_id:
            if template.organization_id not in organization_ids:
                raise HTTPException(status_code=403, detail="User doesn't belong to specified organization")
            template_data["organization_id"] = template.organization_id
        else:
            raise HTTPException(status_code=403, detail="No organization specified")
            
    elif template.type == "official":
        # Official templates are global - no ownership IDs set
        # These would typically require admin permissions to create
        pass
    
    return template_data

@router.post("", response_model=APIResponse[TemplateResponse])
async def create_template(
    template: TemplateCreate,
    user_id: str = Depends(supabase_helpers.get_user_from_session_token),
):
    """Create a new template with blocks and metadata support."""
    try:
        # Validate template type
        if template.type not in ["user", "company", "organization", "official"]:
            raise HTTPException(status_code=400, detail="Invalid template type")
        
        # Get user metadata
        user_metadata = get_user_metadata(supabase, user_id)
        
        # Validate block access
        await _validate_template_blocks(template, user_id)
        
        # Prepare template data
        template_data = _prepare_template_data(template, user_id, user_metadata)
        
        # Insert template into database
        response = supabase.table("prompt_templates").insert(template_data).execute()
        
        if not response.data:
            raise HTTPException(status_code=400, detail="Failed to create template")
        
        # Process and return the created template
        created_template = response.data[0]
        processed_template = process_template_for_response(created_template, "en")
        expanded_template = await expand_template_blocks(processed_template, "en")
        
        return APIResponse(success=True, data=expanded_template)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating template: {str(e)}")