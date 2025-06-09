from fastapi import APIRouter
from supabase import create_client, Client
import os
from utils.access_control import get_access_conditions
from utils import supabase_helpers
from models.prompts.blocks import BlockCreate, BlockUpdate, BlockResponse, BlockType
from models.common import APIResponse

supabase: Client = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_SERVICE_ROLE_KEY"))
router = APIRouter(tags=["Blocks"])
