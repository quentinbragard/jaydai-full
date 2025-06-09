from fastapi import HTTPException
from . import router, supabase
from .schemas import SignInData

@router.post("/sign_in")
async def sign_in(sign_in_data: SignInData):
    """Authenticate user via email & password."""
    try:
        response = supabase.auth.sign_in_with_password({
            "email": sign_in_data.email,
            "password": sign_in_data.password,
        })
        metadata_response = (
            supabase.table("users_metadata")
            .select("*")
            .eq("user_id", response.user.id)
            .single()
            .execute()
        )
        metadata = metadata_response.data if metadata_response.data else {
            "name": None,
            "additional_email": None,
            "phone_number": None,
            "additional_organization": None,
            "pinned_official_folder_ids": [],
            "pinned_organization_folder_ids": [],
        }
        user_with_metadata = {**response.user.__dict__, "metadata": metadata}
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
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
