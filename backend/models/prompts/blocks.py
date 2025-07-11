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
    content: str

class BlockCreate(BaseModel):
    company_id: Optional[str] = None
    organization_id: Optional[str] = None
    type: BlockType
    title: str
    description: Optional[str] = None
    content: str
    published: Optional[bool] = True
    
class BlockUpdate(BaseModel):
    type: Optional[BlockType] = None
    content: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    published: Optional[bool] = True

class BlockResponse(BlockBase):
    id: int
    created_at: str
    company_id: Optional[str]
    organization_id: Optional[str]
    user_id: Optional[str]
    title: str
    description: Optional[str] = None
    published: Optional[bool] = False
