from fastapi import Depends, HTTPException
from .helpers import router, supabase, get_access_conditions
from models.prompts.blocks import BlockResponse
from models.common import APIResponse
from utils import supabase_helpers

@router.get("/{block_id}", response_model=APIResponse[BlockResponse])
async def get_block(
    block_id: int,
    user_id: str = Depends(supabase_helpers.get_user_from_session_token),
):
    """Retrieve a single block by ID if user has access."""
    try:
        access_conditions = get_access_conditions(supabase, user_id)
        response = (
            supabase.table("prompt_blocks")
            .select("*")
            .eq("id", block_id)
            .or_(",".join(access_conditions))
            .single()
            .execute()
        )
        if not response.data:
            raise HTTPException(status_code=404, detail="Block not found")
        return APIResponse(success=True, data=response.data)
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"Error retrieving block: {str(e)}")

