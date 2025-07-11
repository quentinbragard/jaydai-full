# utils/middleware/__init__.py (NEW FILE)
"""
Middleware package for the application.
"""

from .access_control_middleware import AccessControlMiddleware

__all__ = ["AccessControlMiddleware"]