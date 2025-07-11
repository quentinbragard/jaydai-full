from fastapi import APIRouter, HTTPException
from supabase import create_client, Client
import dotenv
import os



dotenv.load_dotenv()

# Initialize Supabase client
supabase: Client = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_SERVICE_ROLE_KEY"))

router = APIRouter(tags=["Onboarding"])