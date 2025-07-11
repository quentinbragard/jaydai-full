from typing import List
from fastapi import Depends, HTTPException, Request  # ADD Request import
from .helpers import router, supabase, get_access_conditions, process_block_for_response  # ADD process_block_for_response import
from models.prompts.blocks import BlockResponse
from models.common import APIResponse
from utils import supabase_helpers
from utils.middleware.localization import extract_locale_from_request  # ADD this import

@router.get("/by-type/{block_type}", response_model=APIResponse[List[BlockResponse]])
async def get_blocks_by_type(
    block_type: str,
    request: Request,  # ADD this parameter
    user_id: str = Depends(supabase_helpers.get_user_from_session_token),
):
    """Get all blocks of a specific type accessible to the user."""
    try:
        # Extract locale from request
        locale = extract_locale_from_request(request)
        print(f"🌍 GET_BLOCKS_BY_TYPE - LOCALE DETECTED: {locale} for type: {block_type}")  # DEBUG PRINT
        
        query = supabase.table("prompt_blocks").select("*").eq("type", block_type)
        access_conditions = get_access_conditions(supabase, user_id)
        query = query.or_(",".join(access_conditions))
        query = query.order("created_at", desc=True)
        response = query.execute()
        
        # Process blocks for localized response
        processed_blocks = []
        for block_data in (response.data or []):
            processed_block = process_block_for_response(block_data, locale)
            processed_blocks.append(processed_block)
        
        print(f"📤 GET_BLOCKS_BY_TYPE - RETURNING {len(processed_blocks)} {block_type} blocks in {locale}")  # DEBUG PRINT
        
        return APIResponse(success=True, data=processed_blocks)
    except Exception as e:
        print(f"❌ GET_BLOCKS_BY_TYPE ERROR: {str(e)}")  # DEBUG PRINT
        raise HTTPException(status_code=500, detail=f"Error fetching blocks: {str(e)}")