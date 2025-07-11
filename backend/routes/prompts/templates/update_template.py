# routes/prompts/templates/create_template.py - REPLACE ENTIRE FUNCTION
from fastapi import Depends, HTTPException, Request
from models.prompts.templates import TemplateUpdate, TemplateResponse
from models.common import APIResponse
from utils import supabase_helpers
from utils.prompts import process_template_for_response, normalize_localized_field
from utils.access_control import user_has_access_to_template, user_has_access_to_folder
from utils.middleware.localization import extract_locale_from_request
from . import router, supabase


# routes/prompts/templates/update_template.py - REPLACE ENTIRE FUNCTION
@router.put("/{template_id}", response_model=APIResponse[TemplateResponse])
async def update_template(
    template_id: str,
    template: TemplateUpdate,
    request: Request,
    user_id: str = Depends(supabase_helpers.get_user_from_session_token),
):
    """Update an existing template with access control validation."""
    try:
        locale = extract_locale_from_request(request)
        
        # Validate template access
        try:
            template_id_int = int(template_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid template ID format")
        
        access = user_has_access_to_template(supabase, user_id, template_id_int)
        if access is None:
            raise HTTPException(status_code=404, detail="Template not found")
        if not access:
            raise HTTPException(status_code=403, detail="Access denied to this template")

        # Validate folder access if folder_id is being updated
        if template.folder_id is not None and template.folder_id != 0:
            folder_access = user_has_access_to_folder(supabase, user_id, template.folder_id)
            if folder_access is None:
                raise HTTPException(status_code=404, detail="Folder not found")
            if not folder_access:
                raise HTTPException(status_code=403, detail="Access denied to specified folder")

        # Build update data
        update_data = {}
        
        if template.title is not None:
            update_data["title"] = normalize_localized_field(template.title, locale)
        if template.content is not None:
            update_data["content"] = normalize_localized_field(template.content, locale)
        if template.description is not None:
            update_data["description"] = normalize_localized_field(template.description, locale)
        if template.folder_id is not None:
            update_data["folder_id"] = template.folder_id if template.folder_id != 0 else None
        if template.metadata is not None:
            update_data["metadata"] = template.metadata.dict() if template.metadata else {}

        if not update_data:
            raise HTTPException(status_code=400, detail="No valid fields to update")

        response = supabase.table("prompt_templates").update(update_data).eq("id", template_id).execute()

        if response.data:
            processed_template = process_template_for_response(response.data[0], locale)
            return APIResponse(success=True, data=processed_template)
        else:
            raise HTTPException(status_code=400, detail="Failed to update template")

    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"Error updating template: {str(e)}")


