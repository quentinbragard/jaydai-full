from fastapi import Depends, HTTPException, Request  # ADD Request import
from .helpers import router, supabase, process_block_for_response  # ADD process_block_for_response import
from models.prompts.blocks import BlockUpdate, BlockResponse
from models.common import APIResponse
from utils import supabase_helpers
from utils.middleware.localization import extract_locale_from_request  # ADD this import
from utils.prompts.locales import ensure_localized_field  # ADD this import

@router.put("/{block_id}", response_model=APIResponse[BlockResponse])
async def update_block(
    block_id: int,
    block: BlockUpdate,
    request: Request,  # ADD this parameter
    user_id: str = Depends(supabase_helpers.get_user_from_session_token),
):
    """Update a block (only if user owns it)"""
    try:
        # Extract locale from request
        locale = extract_locale_from_request(request)
        print(f"🌍 UPDATE_BLOCK - LOCALE DETECTED: {locale} for block_id: {block_id}")  # DEBUG PRINT
        print(f"📝 UPDATE_BLOCK - DATA RECEIVED: title='{block.title}', content='{block.content}', description='{block.description}'")  # DEBUG PRINT
        
        existing_block = supabase.table("prompt_blocks").select("*").eq("id", block_id).eq("user_id", user_id).single().execute()
        if not existing_block.data:
            raise HTTPException(status_code=404, detail="Block not found or access denied")

        update_data = {}
        if block.type is not None:
            update_data["type"] = block.type
        if block.content is not None:
            localized_content = ensure_localized_field(block.content, locale)
            update_data["content"] = localized_content
            print(f"💾 UPDATE_BLOCK - LOCALIZED CONTENT: {localized_content}")  # DEBUG PRINT
        if block.title is not None:
            localized_title = ensure_localized_field(block.title, locale)
            update_data["title"] = localized_title
            print(f"💾 UPDATE_BLOCK - LOCALIZED TITLE: {localized_title}")  # DEBUG PRINT
        if block.description is not None:
            localized_description = ensure_localized_field(block.description, locale)
            update_data["description"] = localized_description
            print(f"💾 UPDATE_BLOCK - LOCALIZED DESCRIPTION: {localized_description}")  # DEBUG PRINT

        if not update_data:
            raise HTTPException(status_code=400, detail="No valid fields to update")

        response = supabase.table("prompt_blocks").update(update_data).eq("id", block_id).execute()
        if response.data:
            # Process the response to return localized strings
            updated_block = response.data[0]
            processed_block = process_block_for_response(updated_block, locale)
            print(f"📤 UPDATE_BLOCK - RESPONSE SENT: {processed_block}")  # DEBUG PRINT
            
            return APIResponse(success=True, data=processed_block)
        else:
            raise HTTPException(status_code=400, detail="Failed to update block")
    except Exception as e:
        print(f"❌ UPDATE_BLOCK ERROR: {str(e)}")  # DEBUG PRINT
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=f"Error updating block: {str(e)}")