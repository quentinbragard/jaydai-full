# routes/prompts/folders/__init__.py
from fastapi import APIRouter

router = APIRouter(tags=["Folders"])

# Import all route modules to register them with the router
# Existing routes

from .helpers import (
    router,
    supabase,
    FolderCreate,
    FolderUpdate,
    PromptType,
    get_user_organizations,
    get_user_company,
    fetch_folders_by_type,
    fetch_templates_for_folders,
    organize_templates_by_folder,
    add_templates_to_folders,
    get_user_pinned_folders,
    update_user_pinned_folders,
    add_pinned_status_to_folders,
    create_localized_field,
    determine_folder_type,
)

from . import get_folders
get_template_folders_by_type = fetch_folders_by_type
from . import create_folder
from . import update_folder
from . import delete_folder
from . import pin_folder
from . import unpin_folder
from . import update_pinned_folders_endpoint
from . import get_template_folders
from . import get_folders
from . import create_folder
from . import update_folder
from . import delete_folder
from . import pin_folder
from . import unpin_folder
from . import update_pinned_folders_endpoint
from . import get_template_folders
from . import reorder_folders
from . import toggle_priority
from . import move_folder
from . import get_available_parents

__all__ = [
    "router",
    "supabase",
    "FolderCreate",
    "FolderUpdate",
    "PromptType",
    "get_user_organizations",
    "get_user_company",
    "fetch_folders_by_type",
    "get_template_folders_by_type",
    "fetch_templates_for_folders",
    "organize_templates_by_folder",
    "add_templates_to_folders",
    "get_user_pinned_folders",
    "update_user_pinned_folders",
    "add_pinned_status_to_folders",
    "create_localized_field",
    "determine_folder_type",
]
