from fastapi import Header, HTTPException
from supabase import create_client, Client
import dotenv
import os

dotenv.load_dotenv()

# Read Supabase URL and API Key from .env file
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)

def get_user_from_session_token(authorization: str = Header(None)):
    """Extract user ID from Supabase JWT token."""
    if not authorization or not authorization.startswith("Bearer "):
        print("Missing or invalid Authorization Header")
        raise HTTPException(status_code=403, detail="Missing or invalid Authorization Header")

    token = authorization.split(" ")[1]
    try:
        user_info = supabase.auth.get_user(token)
        if not user_info or not user_info.user:
            raise HTTPException(status_code=403, detail="Invalid token")
        return user_info.user.id
    except Exception as e:
        print("Error validating token:", str(e))
        raise HTTPException(status_code=500, detail=f"Error validating token: {str(e)}")
