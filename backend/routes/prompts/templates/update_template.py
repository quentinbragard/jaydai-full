from fastapi import Depends, HTTPException
from models.prompts.templates import TemplateUpdate, TemplateResponse
from models.common import APIResponse
from utils import supabase_helpers
from utils.prompts import validate_block_access, normalize_localized_field, process_template_for_response
from . import router, supabase

@router.put("/{template_id}", response_model=APIResponse[TemplateResponse])
async def update_template(
    template_id: str,
    template: TemplateUpdate,
    user_id: str = Depends(supabase_helpers.get_user_from_session_token),
):
    """Update an existing template with metadata support."""
    try:
        existing_template = supabase.table("prompt_templates").select("*").eq("id", template_id).single().execute()

        if not existing_template.data:
            raise HTTPException(status_code=404, detail="Template not found")

        template_data = existing_template.data

        if template_data.get("type") == "user" and template_data.get("user_id") != user_id:
            raise HTTPException(status_code=403, detail="Access denied")

        update_data = {}
        current_locale = "en"

        if template.title is not None:
            update_data["title"] = normalize_localized_field(template.title, current_locale)

        if template.content is not None:
            update_data["content"] = normalize_localized_field(template.content, current_locale)


        if template.metadata is not None:
            metadata_block_ids = []
            if template.metadata:
                metadata_block_ids = [
                    template.metadata.role,
                    template.metadata.context,
                    template.metadata.goal,
                    template.metadata.tone_style or 0,
                    template.metadata.output_format or 0,
                    template.metadata.audience or 0,
                ]
                if template.metadata.example:
                    metadata_block_ids.extend(template.metadata.example)
                if template.metadata.constraint:
                    metadata_block_ids.extend(template.metadata.constraint)
                metadata_block_ids = [bid for bid in metadata_block_ids if bid and bid != 0]

            if metadata_block_ids:
                has_access = await validate_block_access(metadata_block_ids, user_id)
                if not has_access:
                    raise HTTPException(status_code=403, detail="Access denied to one or more metadata blocks")

            update_data["metadata"] = template.metadata.dict()

        if template.description is not None:
            update_data["description"] = normalize_localized_field(template.description, current_locale)

        if template.folder_id is not None:
            update_data["folder_id"] = template.folder_id


        if not update_data:
            raise HTTPException(status_code=400, detail="No valid fields to update")

        response = supabase.table("prompt_templates").update(update_data).eq("id", template_id).execute()

        if response.data:
            processed_template = process_template_for_response(response.data[0], current_locale)
            return APIResponse(success=True, data=processed_template)
        else:
            raise HTTPException(status_code=400, detail="Failed to update template")

    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"Error updating template: {str(e)}")
