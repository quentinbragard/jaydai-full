from fastapi import Depends, HTTPException
from models.common import APIResponse
from utils import supabase_helpers
from .helpers import router, supabase

@router.post("/seed-sample-blocks")
async def seed_sample_blocks(
    user_id: str = Depends(supabase_helpers.get_user_from_session_token),
):
    """Seed some sample blocks for testing (development only)"""
    try:
        sample_blocks = [
            {
                "type": "content",
                "content": {"en": "Write a comprehensive analysis of [topic]"},
                "title": {"en": "Analysis Template"},
                "description": {"en": "Template for comprehensive analysis"},
                "user_id": None,
                "organization_id": None,
                "company_id": None
            },
            {
                "type": "context",
                "content": {"en": "You are working with a professional audience"},
                "title": {"en": "Professional Context"},
                "description": {"en": "Context for professional communications"},
                "user_id": None,
                "organization_id": None,
                "company_id": None
            },
            {
                "type": "role",
                "content": {"en": "You are an expert copywriter"},
                "title": {"en": "Copywriter Role"},
                "description": {"en": "Expert copywriter persona"},
                "user_id": None,
                "organization_id": None,
                "company_id": None
            }
        ]

        response = supabase.table("prompt_blocks").insert(sample_blocks).execute()

        return APIResponse(success=True, data=response.data, message="Sample blocks created")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error seeding sample blocks: {str(e)}")
