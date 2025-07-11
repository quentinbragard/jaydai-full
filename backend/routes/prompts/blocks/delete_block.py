# routes/prompts/blocks/delete_block.py - REPLACE ENTIRE FUNCTION
from fastapi import Depends, HTTPException, Request
from models.common import APIResponse
from utils import supabase_helpers
from .helpers import router, supabase
from utils.middleware.localization import extract_locale_from_request
from utils.access_control import user_has_access_to_block

@router.delete("/{block_id}")
async def delete_block(
    block_id: int,
    request: Request,
    user_id: str = Depends(supabase_helpers.get_user_from_session_token),
):
    """Delete a block with access control validation."""
    try:
        locale = extract_locale_from_request(request)
        
        # Validate block access
        access = user_has_access_to_block(supabase, user_id, block_id)
        if access is None:
            raise HTTPException(status_code=404, detail="Block not found")
        if not access:
            raise HTTPException(status_code=403, detail="Access denied to this block")

        # Check if block is being used in templates
        templates_using_block = (
            supabase.table("prompt_templates")
            .select("id")
            .filter("metadata", "cs", f'"{block_id}"')  # Check if block_id exists in metadata JSON
            .execute()
        )

        if templates_using_block.data:
            raise HTTPException(status_code=400, detail="Cannot delete block that is being used in templates")

        # Delete the block
        supabase.table("prompt_blocks").delete().eq("id", block_id).execute()
        return APIResponse(success=True, message="Block deleted")

    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"Error deleting block: {str(e)}")