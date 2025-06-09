# Add to your main.py or create utils/logging.py
import logging
import json
import time
from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

# Configure structured logging
class StructuredLogging(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        # Process the request
        try:
            response = await call_next(request)
            status_code = response.status_code
            error = None
        except Exception as e:
            status_code = 500
            error = str(e)
            raise e
        finally:
            # Calculate request processing time
            process_time = time.time() - start_time
            
            # Log in structured JSON format
            log_dict = {
                "timestamp": time.time(),
                "method": request.method,
                "path": request.url.path,
                "status_code": status_code,
                "duration_ms": round(process_time * 1000, 2),
                "client_ip": request.client.host,
                "user_agent": request.headers.get("user-agent", ""),
            }
            
            if error:
                log_dict["error"] = error
                
            # Add custom fields if available
            if hasattr(request.state, "auth_user"):
                log_dict["user_id"] = request.state.auth_user
                
            # Print as JSON for Cloud Logging to parse properly
            print(json.dumps(log_dict))
            
        return response

# Add this middleware to your FastAPI app
app = FastAPI()
app.add_middleware(StructuredLogging)