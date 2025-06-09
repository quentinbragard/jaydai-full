from fastapi import Depends, HTTPException
from models.prompts.templates import TemplateResponse
from models.common import APIResponse
from utils import supabase_helpers
from utils.prompts import process_template_for_response, expand_template_blocks, validate_block_access
from utils.access_control import get_user_metadata
from . import router, supabase

@router.post("/{template_id}/duplicate", response_model=APIResponse[TemplateResponse])
async def duplicate_template(
    template_id: str,
    user_id: str = Depends(supabase_helpers.get_user_from_session_token),
):
    """Duplicate an existing template."""
    try:
        original_response = supabase.table("prompt_templates").select("*").eq("id", template_id).single().execute()

        if not original_response.data:
            raise HTTPException(status_code=404, detail="Template not found")

        original_template = original_response.data

        if original_template.get("type") == "user" and original_template.get("user_id") != user_id:
            raise HTTPException(status_code=403, detail="Access denied")
        elif original_template.get("type") == "organization":
            metadata = get_user_metadata(supabase, user_id)
            if original_template.get("organization_id") not in (metadata.get("organization_ids") or []):
                raise HTTPException(status_code=403, detail="Access denied")
        elif original_template.get("type") == "company":
            metadata = get_user_metadata(supabase, user_id)
            if original_template.get("company_id") != metadata.get("company_id"):
                raise HTTPException(status_code=403, detail="Access denied")

        blocks = original_template.get("blocks", [])
        block_ids = [bid for bid in blocks if bid != 0]
        if block_ids:
            has_access = await validate_block_access(block_ids, user_id)
            if not has_access:
                raise HTTPException(status_code=403, detail="Access denied to one or more referenced blocks")

        duplicate_data = {
            "user_id": user_id,
            "organization_id": None,
            "type": "user",
            "title": original_template["title"],
            "content": original_template["content"],
            "blocks": blocks,
            "description": original_template.get("description"),
            "folder_id": None,
            "tags": original_template.get("tags", []),
            "usage_count": 0
        }

        response = supabase.table("prompt_templates").insert(duplicate_data).execute()

        if response.data:
            processed_template = process_template_for_response(response.data[0], "en")
            expanded_template = await expand_template_blocks(processed_template, "en")
            return APIResponse(success=True, data=expanded_template)
        else:
            raise HTTPException(status_code=400, detail="Failed to duplicate template")

    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"Error duplicating template: {str(e)}")
