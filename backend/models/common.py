from typing import Generic, TypeVar, Optional
from pydantic.generics import GenericModel

T = TypeVar("T")

class APIResponse(GenericModel, Generic[T]):
    success: bool
    data: Optional[T] = None
    message: Optional[str] = None  # Optional, for error/info messages