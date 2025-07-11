from .helpers import router, supabase, get_user_organizations, get_user_company

# Import route modules to register them with the router
from . import create_template
from . import delete_template
from . import duplicate_template
from . import get_available_folders
from . import get_template_by_id
from . import get_templates
from . import get_unorganized_templates
from . import track_template_usage
from . import update_template
from . import pin_template
from . import get_pinned_templates
from . import pin_template
from . import unpin_template

__all__ = [
    "router",
    "supabase",
    "create_template",
    "delete_template",
    "duplicate_template",
    "get_available_folders",
    "get_template_by_id",
    "get_templates",
    "get_unorganized_templates",
    "track_template_usage",
    "update_template",
    "pin_template",
    "unpin_template",
    "get_pinned_templates"
]