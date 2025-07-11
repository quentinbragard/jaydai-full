from fastapi import APIRouter

router = APIRouter(tags=["Onboarding"])

# Import all route modules to register them with the router
from .complete_onboarding import complete_onboarding
from .preview_folder_recommendations import preview_folder_recommendations

router.add_api_route("/complete", complete_onboarding, methods=["POST"])
router.add_api_route("/preview-folder-recommendations", preview_folder_recommendations, methods=["POST"])

__all__ = [
    "router",
    "supabase",
    "complete_onboarding",
    "preview_folder_recommendations",
]