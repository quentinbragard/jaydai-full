from fastapi import HTTPException
from . import router, supabase
from .schemas import SignUpData
from utils.notification_service import NotificationService
from utils.prompts import get_all_folder_ids_by_type

@router.post("/sign_up")
async def sign_up(sign_up_data: SignUpData):
    """Sign up a new user and pin all available folders."""
    try:
        response = supabase.auth.sign_up({
            "email": sign_up_data.email,
            "password": sign_up_data.password,
            "options": {"data": {"name": sign_up_data.name}}
        })
        user_with_metadata = None
        if response.user:
            official_folder_ids = await get_all_folder_ids_by_type(supabase, "official")
            organization_folder_ids = []
            metadata_response = supabase.table("users_metadata").insert({
                "user_id": response.user.id,
                "pinned_official_folder_ids": official_folder_ids,
                "pinned_organization_folder_ids": organization_folder_ids,
                "name": sign_up_data.name,
                "additional_email": None,
                "phone_number": None,
                "additional_organization": None
            }).execute()
            metadata = metadata_response.data[0] if metadata_response.data else None
            user_with_metadata = {**response.user.__dict__, "metadata": metadata}
            await NotificationService.create_welcome_notification(response.user.id, sign_up_data.name)
        return {
            "success": True,
            "message": "Sign up successful. Please check your email to verify your account.",
            "user": user_with_metadata,
            "session": {
                "access_token": response.session.access_token,
                "refresh_token": response.session.refresh_token,
                "expires_at": response.session.expires_at,
            },
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during sign up: {str(e)}")
