from pydantic import BaseModel
from typing import Optional, List

class OnboardingCompletionData(BaseModel):
    job_type: Optional[str] = None
    job_industry: Optional[str] = None
    job_seniority: Optional[str] = None
    job_other_details: Optional[str] = None
    interests: Optional[List[str]] = None
    other_interests: Optional[str] = None
    signup_source: Optional[str] = None
    other_source: Optional[str] = None

class FolderRecommendationRequest(BaseModel):
    job_type: Optional[str] = None
    job_industry: Optional[str] = None
    job_seniority: Optional[str] = None
    interests: Optional[List[str]] = None
