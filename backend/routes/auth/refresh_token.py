from fastapi import HTTPException
from . import router, supabase
from .schemas import RefreshTokenData

@router.post("/refresh_token")
async def refresh_token(refresh_data: RefreshTokenData):
    """Refresh an expired access token using the refresh token."""
    try:
        response = supabase.auth.refresh_session(refresh_data.refresh_token)
        return {
            "success": True,
            "session": {
                "access_token": response.session.access_token,
                "refresh_token": response.session.refresh_token,
                "expires_at": response.session.expires_at,
            },
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
