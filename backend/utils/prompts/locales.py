"""
Utility functions for handling localization in prompts system.
"""
from typing import Dict, Any, Union
import json

def extract_localized_field(json_field: Union[Dict, str, None], locale: str = "en", is_user_content: bool = False) -> str:
    """
    Extract localized content from JSON field with fallback to English.
    
    Args:
        json_field: JSON object with localized strings or plain string
        locale: Requested locale (default: "en")
        is_user_content: If True, just returns first available content regardless of locale
        
    Returns:
        Localized string with fallback logic
    """
    if not json_field:
        return ""
    
    # If it's already a string, return it
    if isinstance(json_field, str):
        return json_field
    
    # If it's a dict/JSON object, extract the appropriate locale
    if isinstance(json_field, dict):
        # For user content, just return the first available value
        if is_user_content:
            for value in json_field.values():
                if value:
                    return value
            return ""
        
        # For official/organization content, use locale-specific logic
        # Try to get the requested locale
        if locale in json_field and json_field[locale]:
            return json_field[locale]
        # Fallback to English
        elif "en" in json_field and json_field["en"]:
            return json_field["en"]
        # If no English, return first non-empty value
        else:
            for value in json_field.values():
                if value:
                    return value
    
    return ""

def create_localized_field(content: str, locale: str = "en") -> Dict[str, str]:
    """
    Create a localized JSON field from a string.
    
    Args:
        content: The content string
        locale: The locale to set (default: "en")
        
    Returns:
        JSON object with localized content
    """
    return {locale: content}

def update_localized_field(existing_field: Dict, content: str, locale: str = "en") -> Dict[str, str]:
    """
    Update an existing localized field with new content.
    
    Args:
        existing_field: Existing JSON object
        content: New content
        locale: Locale to update
        
    Returns:
        Updated JSON object
    """
    if not existing_field:
        existing_field = {}
    
    existing_field[locale] = content
    return existing_field

def get_supported_locales() -> list[str]:
    """Get list of supported locales."""
    return ["en", "fr"]

def is_locale_supported(locale: str) -> bool:
    """Check if a locale is supported."""
    return locale in get_supported_locales()