# routes/auth/sign_up.py - Updated
from fastapi import HTTPException
from . import router, supabase
from .schemas import SignUpData
from utils.notification_service import NotificationService
import logging
from utils.onboarding.folder_mapping import FolderRecommendationEngine

logger = logging.getLogger(__name__)

JAYDAI_ORG_ID = "19864b30-936d-4a8d-996a-27d17f11f00f"

@router.post("/sign_up")
async def sign_up(sign_up_data: SignUpData):
    """Sign up a new user with automatic starter pack assignment."""
    try:
        response = supabase.auth.sign_up({
            "email": sign_up_data.email,
            "password": sign_up_data.password,
            "options": {"data": {"name": sign_up_data.name}}
        })
        
        user_with_metadata = None
        if response.user:
            # Create user metadata record
            metadata_response = supabase.table("users_metadata").insert({
                "user_id": response.user.id,
                "pinned_folder_ids": [FolderRecommendationEngine.STARTER_PACK_FOLDER_ID],
                "name": sign_up_data.name,
                "organization_ids": [JAYDAI_ORG_ID],
                "additional_email": None,
                "phone_number": None,
                "additional_organization": None
            }).execute()
            
            metadata = metadata_response.data[0] if metadata_response.data else None
            user_with_metadata = {**response.user.__dict__, "metadata": metadata}
            
            # Create welcome notification
            await NotificationService.create_welcome_notification(response.user.id, sign_up_data.name)
        
        return {
            "success": True,
            "message": "Sign up successful. Please check your email to verify your account.",
            "user": user_with_metadata,
            "session": {
                "access_token": response.session.access_token,
                "refresh_token": response.session.refresh_token,
                "expires_at": response.session.expires_at,
            }
        }
    except Exception as e:
        logger.error(f"Error during sign up: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error during sign up: {str(e)}")