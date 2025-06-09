from fastapi import Depends, HTTPException
from models.common import APIResponse
from utils import supabase_helpers
from .helpers import router, supabase

@router.delete("/{block_id}")
async def delete_block(
    block_id: int,
    user_id: str = Depends(supabase_helpers.get_user_from_session_token),
):
    """Delete a block (only if user owns it)"""
    try:
        existing_block = supabase.table("prompt_blocks").select("*").eq("id", block_id).eq("user_id", user_id).single().execute()
        print(existing_block.data)

        if not existing_block.data:
            raise HTTPException(status_code=404, detail="Block not found or access denied")

        templates_using_block = (
            supabase.table("prompt_templates")
            .select("id")
            .filter("blocks", "cs", f"{{{block_id}}}")
            .execute()
        )

        if templates_using_block.data:
            raise HTTPException(status_code=400, detail="Cannot delete block that is being used in templates")

        supabase.table("prompt_blocks").delete().eq("id", block_id).execute()

        return APIResponse(success=True, message="Block deleted")

    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"Error deleting block: {str(e)}")
