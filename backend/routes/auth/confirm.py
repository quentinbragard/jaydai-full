from fastapi import HTTPException
from fastapi.responses import RedirectResponse
from . import router, supabase

@router.get("/confirm")
async def confirm_email(token: str, type: str = "signup"):
    """Confirm email address and redirect to ChatGPT or app UI."""
    try:
        response = supabase.auth.verify_otp({"token": token, "type": type})
        if response.user:
            return RedirectResponse("https://chat.openai.com")
        raise HTTPException(status_code=400, detail="Invalid or expired confirmation token")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to confirm email: {str(e)}")
