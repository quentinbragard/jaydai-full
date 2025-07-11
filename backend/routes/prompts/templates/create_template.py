# routes/prompts/templates/create_template.py - REPLACE ENTIRE FUNCTION
from fastapi import Depends, HTTPException, Request
from models.prompts.templates import TemplateCreate, TemplateResponse
from models.common import APIResponse
from utils import supabase_helpers
from utils.prompts import process_template_for_response, validate_block_access, normalize_localized_field
from utils.access_control import get_user_metadata, user_has_access_to_folder
from utils.middleware.localization import extract_locale_from_request
from . import router, supabase

@router.post("", response_model=APIResponse[TemplateResponse])
async def create_template(
    template: TemplateCreate,
    request: Request,
    user_id: str = Depends(supabase_helpers.get_user_from_session_token),
):
    """Create a new template with access control validation."""
    try:
        locale = extract_locale_from_request(request)
        
        # Validate template type
        if template.type not in ["user", "company", "organization", "official"]:
            raise HTTPException(status_code=400, detail="Invalid template type")
        
        # Get user metadata
        user_metadata = get_user_metadata(supabase, user_id)
        
        # Validate folder access if folder_id is provided
        if template.folder_id:
            folder_access = user_has_access_to_folder(supabase, user_id, template.folder_id)
            if folder_access is None:
                raise HTTPException(status_code=404, detail="Folder not found")
            if not folder_access:
                raise HTTPException(status_code=403, detail="Access denied to specified folder")
        
        # Validate block access if metadata is provided
        if template.metadata:
            all_block_ids = set()
            metadata_blocks = [
                template.metadata.role,
                template.metadata.context, 
                template.metadata.goal,
                template.metadata.tone_style,
                template.metadata.output_format,
                template.metadata.audience,
            ]
            if template.metadata.example:
                metadata_blocks.extend(template.metadata.example)
            if template.metadata.constraint:
                metadata_blocks.extend(template.metadata.constraint)
                
            all_block_ids.update(bid for bid in metadata_blocks if bid and bid != 0)
            
            if all_block_ids and not await validate_block_access(list(all_block_ids), user_id):
                raise HTTPException(status_code=403, detail="Access denied to one or more referenced blocks")
        
        # Prepare template data based on type
        template_data = {
            "type": template.type,
            "title": normalize_localized_field(template.title, locale),
            "content": normalize_localized_field(template.content, locale),
            "description": normalize_localized_field(template.description, locale) if template.description else {},
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
            organization_ids = user_metadata.get("organization_ids", [])
            if not organization_ids:
                raise HTTPException(status_code=400, detail="User doesn't belong to any organization")
            template_data["organization_id"] = organization_ids[0]  # Default to first org
        
        # Insert template into database
        response = supabase.table("prompt_templates").insert(template_data).execute()
        
        if not response.data:
            raise HTTPException(status_code=400, detail="Failed to create template")
        
        created_template = response.data[0]
        processed_template = process_template_for_response(created_template, locale)
        return APIResponse(success=True, data=processed_template)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating template: {str(e)}")
