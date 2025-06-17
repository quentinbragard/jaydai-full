from .helpers import router, supabase, get_user_organizations, get_user_company

# Import route modules to register them with the router
from . import create_template
from . import delete_template
from . import duplicate_template
from . import get_available_folders
from . import get_template_by_id
from . import get_templates
from . import get_unorganized_templates
from . import move_template
from . import reorder_templates
from . import toggle_priority
from . import track_template_usage
from . import update_template
from . import get_available_folders

__all__ = [
    "router",
    "supabase",
    "get_user_organizations",
    "get_user_company",
    "create_template",
    "delete_template",
    "duplicate_template",
    "get_available_folders",
    "get_template_by_id",
    "get_templates",
    "get_unorganized_templates",
    "move_template",
    "reorder_templates",
    "toggle_priority",
    "track_template_usage",
    "update_template",
    "get_available_folders",
]