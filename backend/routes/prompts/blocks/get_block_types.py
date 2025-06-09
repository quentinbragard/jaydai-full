from typing import List
from models.common import APIResponse
from .helpers import router
from models.prompts.blocks import BlockType

@router.get("/types", response_model=APIResponse[List[str]])
async def get_block_types():
    """Get all available block types"""
    return APIResponse(success=True, data=[block_type.value for block_type in BlockType])
