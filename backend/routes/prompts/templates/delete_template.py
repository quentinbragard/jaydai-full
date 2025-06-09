from fastapi import Depends, HTTPException
from models.common import APIResponse
from utils import supabase_helpers
from . import router, supabase, get_user_company, get_user_organizations

@router.delete("/{template_id}")
async def delete_template(
    template_id: str,
    user_id: str = Depends(supabase_helpers.get_user_from_session_token),
):
    """Delete a template."""
    try:
        template_response = supabase.table("prompt_templates").select("*").eq("id", template_id).single().execute()

        if not template_response.data:
            raise HTTPException(status_code=404, detail="Template not found")

        template_data = template_response.data

        if template_data.get("type") == "user" and template_data.get("user_id") != user_id:
            raise HTTPException(status_code=403, detail="Access denied")
        elif template_data.get("type") == "company":
            user_company = await get_user_company(user_id)
            if template_data.get("company_id") != user_company:
                raise HTTPException(status_code=403, detail="Access denied")
        elif template_data.get("type") == "official" and template_data.get("organization_id"):
            user_orgs = await get_user_organizations(user_id)
            if template_data.get("organization_id") not in user_orgs:
                raise HTTPException(status_code=403, detail="Access denied")
        elif template_data.get("type") == "official" and not template_data.get("organization_id"):
            raise HTTPException(status_code=403, detail="Cannot delete global official templates")

        supabase.table("prompt_templates").delete().eq("id", template_id).execute()

        return APIResponse(success=True, message="Template deleted")
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"Error deleting template: {str(e)}")
