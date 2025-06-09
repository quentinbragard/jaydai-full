from typing import List, Optional
from fastapi import Depends, HTTPException
from .helpers import router, supabase, get_access_conditions
from models.prompts.blocks import BlockResponse, BlockType
from models.common import APIResponse
from utils import supabase_helpers

@router.get("", response_model=APIResponse[List[BlockResponse]])
async def get_blocks(
    type: Optional[BlockType] = None,
    user_id: str = Depends(supabase_helpers.get_user_from_session_token),
):
    """Get blocks accessible to the user"""
    try:
        query = supabase.table("prompt_blocks").select("*")
        if type:
            query = query.eq("type", type)
        access_conditions = get_access_conditions(supabase, user_id)
        query = query.or_(",".join(access_conditions))
        query = query.order("created_at", desc=True)
        response = query.execute()
        return APIResponse(success=True, data=response.data or [])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching blocks: {str(e)}")
