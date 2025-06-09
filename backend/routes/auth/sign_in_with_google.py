from fastapi import HTTPException
from . import router, supabase
from .schemas import GoogleAuthRequest
from utils.notification_service import NotificationService
from utils.prompts import get_all_folder_ids_by_type

@router.post("/sign_in_with_google")
async def sign_in_with_google(google_sign_in_data: GoogleAuthRequest):
    """Authenticate user via Google OAuth and pin all available folders for new users."""
    try:
        response = supabase.auth.sign_in_with_id_token({
            "provider": "google",
            "token": google_sign_in_data.id_token,
        })
        if not response.user:
            raise HTTPException(status_code=400, detail="Invalid Google ID token")
        user_id = response.user.id
        metadata_response = (
            supabase.table("users_metadata")
            .select("*")
            .eq("user_id", user_id)
            .execute()
        )
        if not metadata_response.data:
            user_email = response.user.email
            user_name = response.user.user_metadata.get("full_name", "")
            official_folder_ids = await get_all_folder_ids_by_type(supabase, "official")
            organization_folder_ids = []
            metadata_response = supabase.table("users_metadata").insert({
                "user_id": user_id,
                "name": user_name,
                "email": user_email,
                "google_id": response.user.user_metadata.get("sub", ""),
                "pinned_official_folder_ids": official_folder_ids,
                "pinned_organization_folder_ids": organization_folder_ids,
            }).execute()
            metadata = metadata_response.data[0] if metadata_response.data else {
                "name": user_name,
                "email": user_email,
                "pinned_official_folder_ids": official_folder_ids,
                "pinned_organization_folder_ids": organization_folder_ids,
            }
            await NotificationService.create_welcome_notification(response.user.id, user_name)
        else:
            metadata = metadata_response.data[0] if metadata_response.data else {}
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
        }
    except Exception as e:
        error_message = str(e)
        raise HTTPException(status_code=500, detail=f"Google Sign-In error: {error_message}")
