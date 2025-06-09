from fastapi import HTTPException, Depends
from . import router, supabase

@router.get("/me")
async def get_current_user(user_id: str = Depends(supabase.auth.get_user)):
    """Get the current authenticated user."""
    try:
        return {"success": True, "user_id": user_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
