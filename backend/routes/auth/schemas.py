from pydantic import BaseModel
from typing import Optional

class SignInData(BaseModel):
    email: str
    password: str

class GoogleAuthRequest(BaseModel):
    id_token: str

class RefreshTokenData(BaseModel):
    refresh_token: str

class SignUpData(BaseModel):
    email: str
    password: str
    name: Optional[str] = None

class VerifyOTPData(BaseModel):
    email: str
    token: str
    linkedin_id: Optional[str] = None
    name: Optional[str] = None
