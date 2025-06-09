# models/prompts/templates.py
from pydantic import BaseModel
from typing import Optional, List, Union, Dict
from models.prompts.blocks import BlockType
from enum import Enum


class TemplateMetadata(BaseModel):
    """Metadata references block IDs, 0 means empty/no value"""
    role: Optional[int] = 0
    context: Optional[int] = 0
    goal: Optional[int] = 0
    tone_style: Optional[int] = 0
    output_format: Optional[int] = 0
    audience: Optional[int] = 0
    examples: Optional[List[int]] = []
    constraints: Optional[List[int]] = []
    thinking_steps: Optional[List[int]] = []

class TemplateBase(BaseModel):
    title: Union[str, Dict[str, str]]
    content: Union[str, Dict[str, str]]
    metadata: Optional[TemplateMetadata] = None
    description: Optional[Union[str, Dict[str, str]]] = None
    folder_id: Optional[int] = None

class TemplateCreate(TemplateBase):
    type: str = "user"

class TemplateUpdate(BaseModel):
    title: Optional[Union[str, Dict[str, str]]] = None
    content: Optional[Union[str, Dict[str, str]]] = None
    metadata: Optional[TemplateMetadata] = None
    description: Optional[Union[str, Dict[str, str]]] = None
    folder_id: Optional[int] = None

class TemplateResponse(BaseModel):
    id: int
    title: str
    content: Union[str, Dict[str, str]]
    metadata: Optional[TemplateMetadata] = None
    description: Optional[str] = None
    folder_id: Optional[int] = None
    type: str
    usage_count: Optional[int] = 0
    last_used_at: Optional[str] = None
    created_at: str
    user_id: Optional[str] = None
    organization_id: Optional[str] = None
    company_id: Optional[str] = None