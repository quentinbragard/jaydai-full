# routes/save.py - Updated with onboarding completion endpoint

from fastapi import Depends, HTTPException, Request
from utils import supabase_helpers
from utils.onboarding.folder_assignment_service import FolderAssignmentService
import dotenv
import logging
from models.onboarding import OnboardingCompletionData
from .helpers import router, supabase
from utils.middleware.localization import extract_locale_from_request

logger = logging.getLogger(__name__)

dotenv.load_dotenv()



@router.post("/complete")
async def complete_onboarding(
    request: Request,
    onboarding_data: OnboardingCompletionData,
    user_id: str = Depends(supabase_helpers.get_user_from_session_token)
):
    """
    Complete user onboarding and assign personalized folders.
    This processes the onboarding data and automatically pins relevant folders.
    """
    try:
        # Extract locale from request
        locale = extract_locale_from_request(request)
        
        # Save onboarding data to user metadata
        update_data = {}
        
        # Process job information
        if onboarding_data.job_type:
            if onboarding_data.job_type == 'other' and onboarding_data.job_other_details:
                update_data["job_type"] = f"other:{onboarding_data.job_other_details}"
            else:
                update_data["job_type"] = onboarding_data.job_type
        
        if onboarding_data.job_industry:
            update_data["job_industry"] = onboarding_data.job_industry
            
        if onboarding_data.job_seniority:
            update_data["job_seniority"] = onboarding_data.job_seniority
        
        # Process interests
        interests_to_save = onboarding_data.interests or []
        if onboarding_data.other_interests:
            interests_to_save.append(f"other:{onboarding_data.other_interests}")
        update_data["interests"] = interests_to_save
        
        # Process signup source
        if onboarding_data.signup_source:
            if onboarding_data.signup_source == 'other' and onboarding_data.other_source:
                update_data["signup_source"] = f"other:{onboarding_data.other_source}"
            else:
                update_data["signup_source"] = onboarding_data.signup_source
        
        # Save onboarding data to database
        update_response = supabase.table("users_metadata") \
            .update(update_data) \
            .eq("user_id", user_id) \
            .execute()
        
        if not update_response.data:
            raise HTTPException(status_code=500, detail="Failed to save onboarding data")
        
        # Process folder recommendations with locale
        folder_service = FolderAssignmentService(supabase)
        folder_result = await folder_service.process_onboarding_completion(
            user_id=user_id,
            job_type=onboarding_data.job_type,
            job_industry=onboarding_data.job_industry,
            job_seniority=onboarding_data.job_seniority,
            interests=interests_to_save,
            locale=locale  # Pass locale for proper localization
        )
        
        logger.info(f"Completed onboarding for user {user_id}. Folder assignment: {folder_result['success']}")
        
        return {
            "success": True,
            "message": "Onboarding completed successfully",
            "data": update_response.data[0],
            "folder_recommendations": folder_result,
            "total_new_folders": len(folder_result.get("new_folders", [])) if folder_result["success"] else 0
        }
        
    except Exception as e:
        logger.error(f"Error completing onboarding for user {user_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error completing onboarding: {str(e)}")
