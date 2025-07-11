# utils/middleware/access_control_middleware.py (FIXED VERSION)
"""
Fixed Access Control Middleware - Properly handles response modification
"""

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from utils.access_control import get_user_metadata, filter_accessible_items
import json
import os
from supabase import create_client

class AccessControlMiddleware(BaseHTTPMiddleware):
    """
    Middleware that automatically filters API responses to only include
    items the user has access to.
    """
    
    def __init__(self, app, supabase_client=None):
        super().__init__(app)
        self.supabase = supabase_client or create_client(
            os.getenv("SUPABASE_URL"), 
            os.getenv("SUPABASE_SERVICE_ROLE_KEY")
        )
        
        # Define which endpoints need automatic access control
        self.protected_endpoints = {
            "/prompts/templates": "template",
            "/prompts/folders": "folder", 
            "/prompts/blocks": "block"
        }
    
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        
        # Only process successful JSON responses from GET requests
        if (request.method == "GET" and 
            response.status_code == 200 and 
            response.headers.get("content-type", "").startswith("application/json")):
            
            # Check if this is a protected endpoint
            path = request.url.path
            endpoint_type = None
            
            for endpoint, item_type in self.protected_endpoints.items():
                if path.startswith(endpoint):
                    endpoint_type = item_type
                    break
            
            if endpoint_type:
                # Get user ID from request
                try:
                    user_id = await self._extract_user_id(request)
                    if user_id:
                        # Filter response data
                        filtered_response = await self._filter_response_data(
                            response, user_id, endpoint_type
                        )
                        return filtered_response
                except Exception as e:
                    # Log error but don't break the response
                    print(f"Access control middleware error: {str(e)}")
        
        return response
    
    async def _extract_user_id(self, request: Request) -> str:
        """Extract user ID from authorization header."""
        auth_header = request.headers.get("authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return None
        
        try:
            token = auth_header.split(" ")[1]
            user_info = self.supabase.auth.get_user(token)
            return user_info.user.id if user_info and user_info.user else None
        except Exception:
            return None
    
    async def _filter_response_data(self, response, user_id: str, item_type: str):
        """Filter response data to only include accessible items."""
        try:
            # Read the entire response body
            body = b""
            async for chunk in response.body_iterator:
                body += chunk
            
            # Parse JSON
            try:
                data = json.loads(body.decode())
            except json.JSONDecodeError:
                # If it's not valid JSON, return original response
                return JSONResponse(
                    content=body.decode(),
                    status_code=response.status_code,
                    headers={k: v for k, v in response.headers.items() if k.lower() != 'content-length'}
                )
            
            # Filter data if it contains items
            if isinstance(data, dict):
                if "data" in data:
                    if isinstance(data["data"], list):
                        # Filter list of items
                        filtered_items = filter_accessible_items(
                            self.supabase, user_id, data["data"], item_type
                        )
                        data["data"] = filtered_items
                        
                    elif isinstance(data["data"], dict):
                        # Handle nested structure (like folders with templates)
                        if "folders" in data["data"]:
                            for folder_type, folders in data["data"]["folders"].items():
                                if isinstance(folders, list):
                                    # Filter folders
                                    filtered_folders = filter_accessible_items(
                                        self.supabase, user_id, folders, "folder"
                                    )
                                    
                                    # Filter templates within folders
                                    for folder in filtered_folders:
                                        if "templates" in folder and isinstance(folder["templates"], list):
                                            folder["templates"] = filter_accessible_items(
                                                self.supabase, user_id, folder["templates"], "template"
                                            )
                                    
                                    data["data"]["folders"][folder_type] = filtered_folders
            
            # Create new response with filtered data
            # Remove content-length header to let FastAPI recalculate it
            headers = {k: v for k, v in response.headers.items() if k.lower() != 'content-length'}
            
            return JSONResponse(
                content=data,
                status_code=response.status_code,
                headers=headers
            )
            
        except Exception as e:
            print(f"Error filtering response data: {str(e)}")
            # Return original response on error
            return JSONResponse(
                content=json.loads(body.decode()) if body else {},
                status_code=response.status_code,
                headers={k: v for k, v in response.headers.items() if k.lower() != 'content-length'}
            )