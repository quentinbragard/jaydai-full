"""
Utility functions for template operations in the prompts system.
"""
from typing import Dict, List , Union
from supabase import Client
from .locales import extract_localized_field, create_localized_field
import os
from supabase import create_client, Client

# Initialize Supabase client
supabase: Client = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_SERVICE_ROLE_KEY"))


def process_template_for_response(template_data: dict, locale: str = "en") -> dict:
    """Process template data for API response"""
    # Extract localized title and content
    title = extract_localized_content(template_data.get("title", {}), locale)
    
    # Make sure blocks field exists (even if empty)
    if "blocks" not in template_data:
        template_data["blocks"] = []
    
    # Create a processed template with all fields
    processed = {
        "id": template_data.get("id"),
        "title": title,
        "content": normalize_content_to_dict(template_data.get("content", {}), locale),
        "blocks": template_data.get("blocks", []),
        "description": extract_localized_content(template_data.get("description", {}), locale),
        "folder_id": template_data.get("folder_id"),
        "type": template_data.get("type"),
        "usage_count": template_data.get("usage_count", 0),
        "last_used_at": template_data.get("last_used_at"),
        "created_at": template_data.get("created_at"),
        "user_id": template_data.get("user_id"),
        "organization_id": template_data.get("organization_id"),
        "company_id": template_data.get("company_id"),
        "folder": template_data.get("folder")
    }
    
    return processed

async def fetch_templates_for_folders(
    supabase: Client,
    folder_ids: List[int],
    folder_type: str,
    locale: str = "en"
) -> List[Dict]:
    """
    Fetch templates for given folder IDs with proper locale handling.
    
    Args:
        supabase: Supabase client
        folder_ids: List of folder IDs
        folder_type: Type of folders ("user", "official", "organization")
        locale: Requested locale
        
    Returns:
        List of processed template dicts
    """
    if not folder_ids:
        return []
    
    response = supabase.table("prompt_templates") \
        .select("*") \
        .eq("type", folder_type) \
        .in_("folder_id", folder_ids) \
        .execute()
    
    templates = response.data or []
    
    # Process templates for locale
    return [process_template_for_response(template, locale) for template in templates]


def organize_templates_by_folder(templates: List[Dict]) -> Dict[int, List[Dict]]:
    """
    Group templates by their folder_id.
    
    Args:
        templates: List of template dicts
        
    Returns:
        Dict mapping folder_id to list of templates
    """
    templates_by_folder = {}
    for template in templates:
        folder_id = template.get("folder_id")
        if folder_id is not None:
            if folder_id not in templates_by_folder:
                templates_by_folder[folder_id] = []
            templates_by_folder[folder_id].append(template)
    return templates_by_folder

def add_templates_to_folders(folders: List[Dict], templates_by_folder: Dict[int, List[Dict]]) -> List[Dict]:
    """
    Add templates to their respective folders.
    
    Args:
        folders: List of folder dicts
        templates_by_folder: Dict mapping folder_id to templates
        
    Returns:
        Folders with templates added
    """
    folders_with_templates = []
    for folder in folders:
        folder_with_templates = folder.copy()
        folder_with_templates["templates"] = templates_by_folder.get(folder["id"], [])
        folders_with_templates.append(folder_with_templates)
    return folders_with_templates


async def expand_template_blocks(template_data: dict, locale: str = "en") -> dict:
    """Expand block references in a template"""
    if not template_data.get("blocks"):
        # If no blocks array, create default content block
        template_data["expanded_blocks"] = [{
            "id": 0,
            "type": "content",
            "content": normalize_content_to_dict(template_data.get("content", {}), locale),
            "name": "Template Content"
        }]
        return template_data
    
    # Get all referenced blocks (excluding 0)
    block_ids = [bid for bid in template_data["blocks"] if bid != 0]
    expanded_blocks = []
    
    # Process blocks in order
    for block_id in template_data["blocks"]:
        if block_id == 0:
            # Add template's own content
            expanded_blocks.append({
                "id": 0,
                "type": "content",
                "content": normalize_content_to_dict(template_data.get("content", {}), locale),
                "name": "Template Content"
            })
        else:
            # Fetch actual block from database
            block_response = supabase.table("prompt_blocks").select("*").eq("id", block_id).single().execute()
            if block_response.data:
                block = block_response.data
                expanded_blocks.append({
                    "id": block["id"],
                    "type": block["type"],
                    "content": normalize_content_to_dict(block.get("content", {}), locale),
                    "name": block.get("name"),
                    "description": block.get("description")
                })
    
    template_data["expanded_blocks"] = expanded_blocks
    return template_data

# Helper function to ensure content is always a dictionary
def normalize_content_to_dict(content, locale: str = "en"):
    """Ensure content is a dictionary format with locale keys"""
    if content is None:
        return {locale: ""}
        
    if isinstance(content, str):
        return {locale: content}
        
    if isinstance(content, dict):
        return content
        
    # For any other type, convert to string and wrap in dict
    return {locale: str(content)}

async def validate_block_access(block_ids: List[int], user_id: str) -> bool:
    """Validate that user has access to all referenced blocks"""
    if not block_ids:
        return True
    
    # Get user's metadata
    user_metadata_response = supabase.table("users_metadata").select("organization_ids, company_id").eq("user_id", user_id).single().execute()
    user_metadata = user_metadata_response.data or {}
    
    # Get user's organization IDs and company ID
    org_ids = user_metadata.get("organization_ids", [])
    company_id = user_metadata.get("company_id")
    
    # Need to use separate queries for each access type and combine results
    accessible_block_ids = set()
    
    # 1. User's own blocks
    user_blocks = supabase.table("prompt_blocks").select("id").eq("user_id", user_id).in_("id", block_ids).execute()
    if user_blocks.data:
        accessible_block_ids.update(block["id"] for block in user_blocks.data)
    
    # 2. Global blocks (no IDs)
    global_blocks = supabase.table("prompt_blocks").select("id").is_("user_id", "null").is_("company_id", "null").is_("organization_id", "null").in_("id", block_ids).execute()
    if global_blocks.data:
        accessible_block_ids.update(block["id"] for block in global_blocks.data)
    
    # 3. Company blocks if user has company
    if company_id:
        company_blocks = supabase.table("prompt_blocks").select("id").eq("company_id", company_id).in_("id", block_ids).execute()
        if company_blocks.data:
            accessible_block_ids.update(block["id"] for block in company_blocks.data)
    
    # 4. Organization blocks
    if org_ids and len(org_ids) > 0:
        for org_id in org_ids:
            org_blocks = supabase.table("prompt_blocks").select("id").eq("organization_id", org_id).in_("id", block_ids).execute()
            if org_blocks.data:
                accessible_block_ids.update(block["id"] for block in org_blocks.data)
        
    # Check if all requested blocks are accessible
    return all(block_id in accessible_block_ids for block_id in block_ids)


def normalize_localized_field(field: Union[str, Dict[str, str]], locale: str = "en") -> Dict[str, str]:
    """Normalize a field to be a localized dictionary"""
    if isinstance(field, str):
        return {locale: field}
    elif isinstance(field, dict):
        return field
    else:
        return {locale: str(field) if field else ""}

def extract_localized_content(field: Union[str, Dict[str, str]], locale: str = "en") -> str:
    """Extract content for a specific locale from a localized field"""
    if isinstance(field, str):
        return field
    elif isinstance(field, dict):
        return field.get(locale) or field.get("en") or list(field.values())[0] if field else ""
    else:
        return str(field) if field else ""
