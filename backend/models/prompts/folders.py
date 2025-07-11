# models/prompts/folders.py
from pydantic import BaseModel
from typing import Optional, Dict
from enum import Enum

class FolderBase(BaseModel):
    id: Optional[int] = None
    title: str
    
class FolderCreate(FolderBase):
    description: str = None
    user_id: Optional[str] = None
    organization_id: Optional[str] = None
    company_id: Optional[str] = None
    parent_folder_id: Optional[int] = None
    type: Optional[str] = None
    
class FolderUpdate(FolderCreate):
    pass

class FolderResponse(FolderBase):
    id: int
    title: str
    description: Optional[str] = None
    user_id: Optional[str] = None
    organization_id: Optional[str] = None
    company_id: Optional[str] = None
    parent_folder_id: Optional[int] = None