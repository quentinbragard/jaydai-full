from fastapi import Depends, HTTPException, Request  # ADD Request import
from .helpers import router, supabase, get_access_conditions, process_block_for_response  # ADD process_block_for_response import
from models.prompts.blocks import BlockResponse
from models.common import APIResponse
from utils import supabase_helpers
from utils.middleware.localization import extract_locale_from_request  # ADD this import

@router.get("/{block_id}", response_model=APIResponse[BlockResponse])
async def get_block(
    block_id: int,
    request: Request,  # ADD this parameter
    user_id: str = Depends(supabase_helpers.get_user_from_session_token),
):
    """Retrieve a single block by ID if user has access."""
    try:
        # Extract locale from request
        locale = extract_locale_from_request(request)
        print(f"🌍 GET_BLOCK - LOCALE DETECTED: {locale} for block_id: {block_id}")  # DEBUG PRINT
        
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
        
        # Process block for localized response
        processed_block = process_block_for_response(response.data, locale)
        print(f"📤 GET_BLOCK - RETURNING block in {locale}: {processed_block['title']}")  # DEBUG PRINT
        
        return APIResponse(success=True, data=processed_block)
    except Exception as e:
        print(f"❌ GET_BLOCK ERROR: {str(e)}")  # DEBUG PRINT
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"Error retrieving block: {str(e)}")