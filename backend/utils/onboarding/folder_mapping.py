# utils/welcome/folder_mapping.py
from typing import List, Dict, Set
import re

class FolderRecommendationEngine:
    """
    Maps user onboarding data to relevant folder IDs based on strategic recommendations.
    This follows the 4-dimensional personalization matrix from the strategy document.
    """
    
    # Starter pack folder - should be assigned to all new users
    STARTER_PACK_FOLDER_ID = 1  # Adjust this based on your actual starter pack folder ID
    
    # Core Professional Packs (Tier 1 - Highest Priority)
    PROFESSIONAL_ROLE_MAPPING = {
        # Executive/Leadership focused
        'leadership': [2, 3],  # Executive Decision Maker Pack, Strategic Leadership Pack
        'executive': [2, 3],
        
        # Technical roles
        'product_dev_teams': [4, 5],  # Technical Lead's Toolkit, Product Development Pack
        'analysts_researchers': [6, 7],  # Data Storyteller's Arsenal, Research & Analysis Pack
        
        # Marketing & Sales
        'sales_marketing': [8, 9],  # Marketing Growth Hacker Pack, Sales Excellence Pack
        'content_comm_specialists': [10, 11],  # Creative Content Multiplier, Communication Pack
        
        # Customer & Support
        'customer_client_facing': [12, 13],  # Customer Success Pack, Client Relations Pack
        
        # HR & Training
        'hr_training_professionals': [14, 15],  # HR Excellence Pack, Training & Development Pack
        
        # Business & Entrepreneurship
        'entrepreneurs_business_owners': [16, 17],  # Entrepreneur's Toolkit, Business Strategy Pack
        
        # Finance
        'finance': [18, 19],  # Financial Analysis Pack, Finance Professional Pack
        
        # Freelance
        'freelance': [20, 21],  # Freelancer's Toolkit, Independent Professional Pack
    }
    
    # Industry-Specific Packs (Tier 2)
    INDUSTRY_MAPPING = {
        'tech_software_dev': [4, 5, 6],  # Technical + Data focus
        'healthcare_medical': [22],  # Healthcare Compliance Navigator Pack
        'legal_law': [23],  # Legal Research Assistant Pack
        'finance_banking': [18, 19],  # Finance-specific packs
        'marketing_advertising': [8, 9, 10],  # Marketing + Creative packs
        'consulting_professional_services': [2, 3, 6],  # Executive + Analysis packs
        'manufacturing_production': [2, 6],  # Leadership + Analysis
        'media_entertainment': [10, 11],  # Creative + Communication
        'real_estate': [8, 12],  # Marketing + Customer relations
        'ecommerce_retail': [8, 9, 12],  # Marketing + Customer focus
        'education_training': [14, 15],  # Training & Development
        'hr_recruitment': [14, 15],  # HR packs
        'customer_service_support': [12, 13],  # Customer service packs
    }
    
    # Seniority-Specific Packs (Tier 3)
    SENIORITY_MAPPING = {
        'student': [24],  # New Graduate's Professional Accelerator Pack
        'junior_0_5': [24, 25],  # Graduate pack + Junior Development Pack
        'mid_5_10': [26],  # Mid-Career Pivot Navigator Pack
        'senior_10_15': [27],  # Senior Professional Pack
        'lead_15_plus': [2, 3],  # Executive packs
        'executive': [2, 3],  # Executive Decision Maker packs
    }
    
    # Interest-Driven Specialty Packs (Tier 4)
    INTEREST_MAPPING = {
        'writing': [10, 11],  # Creative Content Multiplier, Communication
        'coding': [4, 5],  # Technical packs
        'data_analysis': [6, 7],  # Data Storyteller's Arsenal
        'research': [6, 7, 23],  # Research + Legal research
        'creativity': [10, 11],  # Creative packs
        'learning': [14, 15, 24],  # Learning & Development
        'marketing': [8, 9],  # Marketing packs
        'email': [11, 12],  # Communication + Customer relations
        'summarizing': [6, 7],  # Analysis packs
        'critical_thinking': [2, 6, 7],  # Executive + Analysis
        'customer_support': [12, 13],  # Customer service
        'decision_making': [2, 3],  # Executive packs
        'language_learning': [24, 25],  # Learning packs
    }
    
    @classmethod
    def get_starter_pack_folders(cls) -> List[int]:
        """Get the starter pack folder IDs for new users."""
        return [cls.STARTER_PACK_FOLDER_ID]
    
    @classmethod
    def recommend_folders_for_user(cls, 
                                 job_type: str = None,
                                 job_industry: str = None, 
                                 job_seniority: str = None,
                                 interests: List[str] = None) -> List[int]:
        """
        Recommend folder IDs based on user onboarding data.
        Returns a prioritized list of folder IDs.
        """
        recommended_folders = set()
        
        # Always include starter pack
        recommended_folders.update(cls.get_starter_pack_folders())
        
        # Add folders based on professional role (Tier 1 - Highest Priority)
        if job_type and job_type in cls.PROFESSIONAL_ROLE_MAPPING:
            recommended_folders.update(cls.PROFESSIONAL_ROLE_MAPPING[job_type])
        
        # Add folders based on industry (Tier 2)
        if job_industry and job_industry in cls.INDUSTRY_MAPPING:
            recommended_folders.update(cls.INDUSTRY_MAPPING[job_industry])
        
        # Add folders based on seniority (Tier 3)
        if job_seniority and job_seniority in cls.SENIORITY_MAPPING:
            recommended_folders.update(cls.SENIORITY_MAPPING[job_seniority])
        
        # Add folders based on interests (Tier 4)
        if interests:
            for interest in interests:
                # Handle "other:" prefixed interests
                clean_interest = interest.replace('other:', '') if interest.startswith('other:') else interest
                if clean_interest in cls.INTEREST_MAPPING:
                    recommended_folders.update(cls.INTEREST_MAPPING[clean_interest])
        
        # Convert to sorted list (lower IDs first - typically higher priority)
        return sorted(list(recommended_folders))
    
    @classmethod
    def explain_recommendations(cls, 
                              job_type: str = None,
                              job_industry: str = None, 
                              job_seniority: str = None,
                              interests: List[str] = None) -> Dict[str, List[int]]:
        """
        Get detailed explanation of why each folder was recommended.
        Useful for debugging and user transparency.
        """
        explanation = {
            'starter_pack': cls.get_starter_pack_folders(),
            'professional_role': [],
            'industry': [],
            'seniority': [],
            'interests': []
        }
        
        if job_type and job_type in cls.PROFESSIONAL_ROLE_MAPPING:
            explanation['professional_role'] = cls.PROFESSIONAL_ROLE_MAPPING[job_type]
            
        if job_industry and job_industry in cls.INDUSTRY_MAPPING:
            explanation['industry'] = cls.INDUSTRY_MAPPING[job_industry]
            
        if job_seniority and job_seniority in cls.SENIORITY_MAPPING:
            explanation['seniority'] = cls.SENIORITY_MAPPING[job_seniority]
            
        if interests:
            interest_folders = set()
            for interest in interests:
                clean_interest = interest.replace('other:', '') if interest.startswith('other:') else interest
                if clean_interest in cls.INTEREST_MAPPING:
                    interest_folders.update(cls.INTEREST_MAPPING[clean_interest])
            explanation['interests'] = list(interest_folders)
        
        return explanation