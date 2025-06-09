from fastapi import APIRouter

router = APIRouter(tags=["Templates"])

from .helpers import (
    supabase,
    get_user_organizations,
    get_user_company,
    get_user_templates,
    get_official_templates,
    get_company_templates,
    get_all_templates,
)

# Import endpoints so they register with the router
from . import get_templates
from . import get_unorganized_templates
from . import create_template
from . import update_template
from . import delete_template
from . import track_template_usage
from . import get_template_by_id
from . import duplicate_template

__all__ = [
    "router",
    "supabase",
    "get_user_organizations",
    "get_user_company",
    "get_user_templates",
    "get_official_templates",
    "get_company_templates",
    "get_all_templates",
]
