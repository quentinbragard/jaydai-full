# routes/prompts/templates/create_template.py - REPLACE ENTIRE FUNCTION
from fastapi import Depends, HTTPException
from models.common import APIResponse
from utils import supabase_helpers
from utils.access_control import user_has_access_to_template

from . import router, supabase


# routes/prompts/templates/delete_template.py - REPLACE ENTIRE FUNCTION
@router.delete("/{template_id}")
async def delete_template(
    template_id: str,
    user_id: str = Depends(supabase_helpers.get_user_from_session_token),
):
    """Delete a template with access control validation."""
    try:
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

        # Delete the template
        supabase.table("prompt_templates").delete().eq("id", template_id).execute()
        return APIResponse(success=True, message="Template deleted")
        
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"Error deleting template: {str(e)}")

