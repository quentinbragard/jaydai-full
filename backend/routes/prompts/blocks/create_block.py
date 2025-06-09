from fastapi import Depends, HTTPException
from .helpers import router, supabase
from models.prompts.blocks import BlockCreate, BlockResponse
from models.common import APIResponse
from utils import supabase_helpers

@router.post("", response_model=APIResponse[BlockResponse])
async def create_block(
    block: BlockCreate,
    user_id: str = Depends(supabase_helpers.get_user_from_session_token),
):
    """Create a new block"""
    try:
        block_data = {
            "type": block.type,
            "content": block.content,
            "title": block.title,
            "description": block.description,
            "user_id": user_id,
            "organization_id": block.organization_id,
            "company_id": block.company_id,
        }
        response = supabase.table("prompt_blocks").insert(block_data).execute()
        if response.data:
            return APIResponse(success=True, data=response.data[0])
        else:
            raise HTTPException(status_code=400, detail="Failed to create block")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating block: {str(e)}")
