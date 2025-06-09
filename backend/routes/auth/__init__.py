import os
import dotenv
from fastapi import APIRouter
from supabase import create_client, Client
from unittest.mock import MagicMock

dotenv.load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
if SUPABASE_URL and SUPABASE_KEY:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
else:
    supabase = MagicMock()
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")

router = APIRouter(prefix="/auth", tags=["Authentication"])

# Import endpoints to register them with the router
from . import confirm, sign_up, sign_in, sign_in_with_google, refresh_token, me

__all__ = [
    "router",
    "supabase",
    "GOOGLE_CLIENT_ID",
]
