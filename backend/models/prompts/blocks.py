# models/prompts/blocks.py
from pydantic import BaseModel
from typing import Optional, Dict
from enum import Enum

class BlockType(str, Enum):
    ROLE = "role"
    CONTEXT = "context"
    GOAL = "goal"
    TONE_STYLE = "tone_style"
    OUTPUT_FORMAT = "output_format"
    AUDIENCE = "audience"
    EXAMPLE = "example"
    CONSTRAINT = "constraint"
    CUSTOM = "custom"
    

class BlockBase(BaseModel):
    type: BlockType
    content: Dict[str, str]  # {"en": "...", "fr": "..."}

class BlockCreate(BlockBase):
    company_id: Optional[str] = None
    organization_id: Optional[str] = None
    type: BlockType
    title: Optional[Dict[str, str]] = None
    description: Optional[Dict[str, str]] = None
    content: Optional[Dict[str, str]] = None
    
class BlockUpdate(BaseModel):
    type: Optional[BlockType] = None
    content: Optional[Dict[str, str]] = None
    title: Optional[Dict[str, str]] = None
    description: Optional[Dict[str, str]] = None

class BlockResponse(BlockBase):
    id: int
    created_at: str
    company_id: Optional[str]
    organization_id: Optional[str]
    user_id: Optional[str]
    title: Optional[Dict[str, str]] = None
    description: Optional[Dict[str, str]] = None
