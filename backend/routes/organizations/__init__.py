# routes/organizations/__init__.py
from fastapi import APIRouter

router = APIRouter(tags=["Organizations"])

# Import the route functions and register them
from .get_organizations import get_organizations
from .get_organization_by_id import get_organization_by_id

# Register the routes with the main router
router.add_api_route("", get_organizations, methods=["GET"])
router.add_api_route("/{organization_id}", get_organization_by_id, methods=["GET"])

__all__ = [
    "router",
]