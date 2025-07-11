# utils/folder_assignment_service.py
from typing import List, Dict, Optional
from supabase import Client
from utils.onboarding.folder_mapping import FolderRecommendationEngine
from utils.prompts.locales import extract_localized_field
import logging

logger = logging.getLogger(__name__)

class FolderAssignmentService:
    """
    Service for assigning and managing user folder pins based on onboarding data.
    """
    
    def __init__(self, supabase_client: Client):
        self.supabase = supabase_client
        self.recommendation_engine = FolderRecommendationEngine()
    
    async def process_onboarding_completion(self, 
                                          user_id: str,
                                          job_type: Optional[str] = None,
                                          job_industry: Optional[str] = None,
                                          job_seniority: Optional[str] = None,
                                          interests: Optional[List[str]] = None,
                                          locale: str = "en") -> Dict:
        """
        Process completed onboarding data and assign relevant folders.
        """
        try:
            # Clean up the data (handle "other:" prefixes)
            clean_job_type = self._clean_field_value(job_type)
            clean_job_industry = self._clean_field_value(job_industry)
            clean_job_seniority = self._clean_field_value(job_seniority)
            clean_interests = interests or []
            
            # Get folder recommendations
            recommended_folders = self.recommendation_engine.recommend_folders_for_user(
                job_type=clean_job_type,
                job_industry=clean_job_industry,
                job_seniority=clean_job_seniority,
                interests=clean_interests
            )
            
            # Get current pinned folders
            metadata_response = self.supabase.table("users_metadata") \
                .select("pinned_folder_ids") \
                .eq("user_id", user_id) \
                .single() \
                .execute()
            
            current_pinned = []
            if metadata_response.data and metadata_response.data.get("pinned_folder_ids"):
                current_pinned = metadata_response.data["pinned_folder_ids"]
            
            # Merge recommendations with existing pinned folders
            updated_pinned = list(set(current_pinned + recommended_folders))
            
            # Update user metadata with new pinned folders
            update_response = self.supabase.table("users_metadata") \
                .update({"pinned_folder_ids": updated_pinned}) \
                .eq("user_id", user_id) \
                .execute()
            
            # Get folder details for the frontend with proper localization
            folder_details = []
            if updated_pinned:
                folders_response = self.supabase.table("prompt_folders") \
                    .select("id, title, description, type") \
                    .in_("id", updated_pinned) \
                    .execute()
                
                # Process folder details with localization
                raw_folders = folders_response.data or []
                for folder in raw_folders:
                    # Extract localized title and description
                    localized_title = extract_localized_field(
                        folder.get("title"), 
                        locale, 
                        is_user_content=(folder.get("type") == "user")
                    )
                    localized_description = extract_localized_field(
                        folder.get("description"), 
                        locale, 
                        is_user_content=(folder.get("type") == "user")
                    )
                    
                    processed_folder = {
                        "id": folder["id"],
                        "title": localized_title,
                        "description": localized_description,
                        "type": folder.get("type", "")
                    }
                    folder_details.append(processed_folder)
            
            # Get explanation for transparency
            explanation = self.recommendation_engine.explain_recommendations(
                job_type=clean_job_type,
                job_industry=clean_job_industry,
                job_seniority=clean_job_seniority,
                interests=clean_interests
            )
            
            new_folders = [f for f in recommended_folders if f not in current_pinned]
            
            logger.info(f"Processed onboarding for user {user_id}. Added {len(new_folders)} new folders")
            
            return {
                "success": True,
                "new_folders": new_folders,
                "total_recommended": recommended_folders,
                "total_pinned": updated_pinned,
                "folder_details": folder_details,
                "explanation": explanation,
                "message": f"Added {len(new_folders)} personalized folders based on your profile"
            }
            
        except Exception as e:
            logger.error(f"Error processing onboarding for user {user_id}: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to process onboarding recommendations"
            }
    
    def _clean_field_value(self, value: Optional[str]) -> Optional[str]:
        """
        Clean field values by removing "other:" prefixes and handling None values.
        """
        if not value:
            return None
        
        if value.startswith("other:"):
            # For "other:" values, we could try to map them to known categories
            # or just return None for now since they're custom values
            return None
        
        return value
    
    async def get_folder_recommendations_preview(self,
                                               job_type: Optional[str] = None,
                                               job_industry: Optional[str] = None,
                                               job_seniority: Optional[str] = None,
                                               interests: Optional[List[str]] = None,
                                               locale: str = "en") -> Dict:
        """
        Get a preview of folder recommendations without actually assigning them.
        Useful for showing users what they'll get before completing onboarding.
        """
        try:
            clean_job_type = self._clean_field_value(job_type)
            clean_job_industry = self._clean_field_value(job_industry)
            clean_job_seniority = self._clean_field_value(job_seniority)
            clean_interests = interests or []
            
            recommended_folders = self.recommendation_engine.recommend_folders_for_user(
                job_type=clean_job_type,
                job_industry=clean_job_industry,
                job_seniority=clean_job_seniority,
                interests=clean_interests
            )
            
            explanation = self.recommendation_engine.explain_recommendations(
                job_type=clean_job_type,
                job_industry=clean_job_industry,
                job_seniority=clean_job_seniority,
                interests=clean_interests
            )
            
            # Get folder details for the recommendations with localization
            folder_details = []
            if recommended_folders:
                folders_response = self.supabase.table("prompt_folders") \
                    .select("id, title, description, type") \
                    .in_("id", recommended_folders) \
                    .execute()
                
                # Process folder details with localization
                raw_folders = folders_response.data or []
                for folder in raw_folders:
                    # Extract localized title and description
                    localized_title = extract_localized_field(
                        folder.get("title"), 
                        locale, 
                        is_user_content=(folder.get("type") == "user")
                    )
                    localized_description = extract_localized_field(
                        folder.get("description"), 
                        locale, 
                        is_user_content=(folder.get("type") == "user")
                    )
                    
                    processed_folder = {
                        "id": folder["id"],
                        "title": localized_title,
                        "description": localized_description,
                        "type": folder.get("type", "")
                    }
                    folder_details.append(processed_folder)
            
            return {
                "success": True,
                "recommended_folder_ids": recommended_folders,
                "folder_details": folder_details,
                "explanation": explanation,
                "total_count": len(recommended_folders)
            }
            
        except Exception as e:
            logger.error(f"Error getting folder recommendations preview: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to generate recommendations preview"
            }