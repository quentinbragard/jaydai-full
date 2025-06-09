from fastapi import Depends, HTTPException
from .helpers import router, supabase
from models.prompts.blocks import BlockUpdate, BlockResponse
from models.common import APIResponse
from utils import supabase_helpers

@router.put("/{block_id}", response_model=APIResponse[BlockResponse])
async def update_block(
    block_id: int,
    block: BlockUpdate,
    user_id: str = Depends(supabase_helpers.get_user_from_session_token),
):
    """Update a block (only if user owns it)"""
    try:
        existing_block = supabase.table("prompt_blocks").select("*").eq("id", block_id).eq("user_id", user_id).single().execute()
        if not existing_block.data:
            raise HTTPException(status_code=404, detail="Block not found or access denied")

        update_data = {}
        if block.type is not None:
            update_data["type"] = block.type
        if block.content is not None:
            update_data["content"] = block.content
        if block.title is not None:
            update_data["title"] = block.title
        if block.description is not None:
            update_data["description"] = block.description

        if not update_data:
            raise HTTPException(status_code=400, detail="No valid fields to update")

        response = supabase.table("prompt_blocks").update(update_data).eq("id", block_id).execute()
        if response.data:
            return APIResponse(success=True, data=response.data[0])
        else:
            raise HTTPException(status_code=400, detail="Failed to update block")
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"Error updating block: {str(e)}")
