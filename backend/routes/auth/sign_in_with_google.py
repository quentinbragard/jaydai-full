# routes/auth/sign_in_with_google.py - Updated
from fastapi import HTTPException
from . import router, supabase
from .schemas import GoogleAuthRequest
from utils.notification_service import NotificationService
import logging
from utils.onboarding.folder_mapping import FolderRecommendationEngine

logger = logging.getLogger(__name__)

JAYDAI_ORG_ID = "19864b30-936d-4a8d-996a-27d17f11f00f"

@router.post("/sign_in_with_google")
async def sign_in_with_google(google_sign_in_data: GoogleAuthRequest):
    """Authenticate user via Google OAuth with automatic starter pack for new users."""
    try:
        response = supabase.auth.sign_in_with_id_token({
            "provider": "google",
            "token": google_sign_in_data.id_token,
        })
        
        if not response.user:
            raise HTTPException(status_code=400, detail="Invalid Google ID token")
        
        user_id = response.user.id
        is_new_user = False
        
        # Check if user metadata exists
        metadata_response = (
            supabase.table("users_metadata")
            .select("*")
            .eq("user_id", user_id)
            .execute()
        )
        
        if not metadata_response.data:
            # New user - create metadata and assign starter pack
            is_new_user = True
            user_email = response.user.email
            user_name = response.user.user_metadata.get("full_name", "")

            metadata_response = supabase.table("users_metadata").insert({
                "user_id": user_id,
                "name": user_name,
                "email": user_email,
                "organization_ids": [JAYDAI_ORG_ID],
                "google_id": response.user.user_metadata.get("sub", ""),
                "pinned_folder_ids": [FolderRecommendationEngine.STARTER_PACK_FOLDER_ID],
            }).execute()
            
            metadata = metadata_response.data[0] if metadata_response.data else {
                "name": user_name,
                "email": user_email,
                "pinned_folder_ids": [],
            }
            
            # Create welcome notification
            await NotificationService.create_welcome_notification(user_id, user_name)
        else:
            # Existing user
            metadata = metadata_response.data[0] if metadata_response.data else {}
        
        # Prepare user object for response
        user_dict = response.user.__dict__ if hasattr(response.user, "__dict__") else {
            "id": response.user.id,
            "email": response.user.email,
            "app_metadata": response.user.app_metadata,
            "user_metadata": response.user.user_metadata,
        }
        user_with_metadata = {**user_dict, "metadata": metadata}
        
        return {
            "success": True,
            "user": user_with_metadata,
            "session": {
                "access_token": response.session.access_token,
                "refresh_token": response.session.refresh_token,
                "expires_at": response.session.expires_at,
            },
            "is_new_user": is_new_user,
        }
    except Exception as e:
        error_message = str(e)
        logger.error(f"Google Sign-In error: {error_message}")
        raise HTTPException(status_code=500, detail=f"Google Sign-In error: {error_message}")