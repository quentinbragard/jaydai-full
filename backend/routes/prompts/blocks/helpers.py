from fastapi import APIRouter
from supabase import create_client, Client
import os
from utils.access_control import get_access_conditions
from utils import supabase_helpers
from models.prompts.blocks import BlockCreate, BlockUpdate, BlockResponse, BlockType
from models.common import APIResponse
from utils.prompts.locales import extract_localized_field


supabase: Client = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_SERVICE_ROLE_KEY"))
router = APIRouter(tags=["Blocks"])

def process_block_for_response(block_data: dict, locale: str = "en") -> dict:
    """Process block data for API response with localized strings"""
    return {
        "id": block_data.get("id"),
        "type": block_data.get("type"),
        "title": extract_localized_field(block_data.get("title", {}), locale),
        "content": extract_localized_field(block_data.get("content", {}), locale),
        "description": extract_localized_field(block_data.get("description", {}), locale),
        "created_at": block_data.get("created_at"),
        "user_id": block_data.get("user_id"),
        "organization_id": block_data.get("organization_id"),
        "company_id": block_data.get("company_id"),
        "published": block_data.get("published"),
    }