# utils/middleware/localization.py
from fastapi import Request
from typing import Optional

def extract_locale_from_request(request: Request) -> str:
    """Extract locale from request headers or query params"""
    # Try Accept-Language header first
    accept_language = request.headers.get("Accept-Language", "")
    if accept_language.startswith("fr"):
        return "fr"
    elif accept_language.startswith("en"):
        return "en"
    
    # Fallback to query param
    locale = request.query_params.get("locale", "en")
    return locale if locale in ["en", "fr"] else "en"