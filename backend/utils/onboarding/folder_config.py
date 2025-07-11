# utils/folder_config.py
"""
Folder configuration mapping based on actual database folder IDs.
This maps the strategic recommendations to real folder IDs from the prompt_folders table.

Based on the CSV data showing folder IDs 1-23, this configuration should be updated
to match the actual folder purposes in your database.
"""

class FolderConfig:
    """
    Configuration for folder assignments based on strategic recommendations.
    Update these mappings to match your actual folder IDs and purposes.
    """
    
    # STARTER PACK - Essential folders for all new users
    STARTER_PACK_FOLDER_IDS = [1, 2, 3]  # Update these to your actual starter pack folder IDs
    
    # CORE PROFESSIONAL PACKS (Tier 1)
    PROFESSIONAL_ROLE_FOLDERS = {
        # Executive/Leadership roles
        'leadership': [4, 5],  # Executive Decision Maker Pack, Strategic Leadership
        'executive': [4, 5],
        
        # Technical roles  
        'product_dev_teams': [6, 7],  # Technical Lead's Toolkit, Product Development
        'content_comm_specialists': [8, 9],  # Creative Content, Communication
        'analysts_researchers': [10, 11],  # Data Analysis, Research Tools
        
        # Sales & Marketing
        'sales_marketing': [12, 13],  # Marketing Growth Hacker, Sales Excellence
        
        # Customer facing
        'customer_client_facing': [14, 15],  # Customer Success, Client Relations
        
        # HR & Training
        'hr_training_professionals': [16, 17],  # HR Excellence, Training & Development
        
        # Business & Entrepreneurship
        'entrepreneurs_business_owners': [18, 19],  # Entrepreneur's Toolkit, Business Strategy
        
        # Finance
        'finance': [20, 21],  # Financial Analysis, Finance Professional
        
        # Freelance
        'freelance': [22, 23],  # Freelancer's Toolkit, Independent Professional
    }
    
    # INDUSTRY-SPECIFIC FOLDERS (Tier 2)
    INDUSTRY_FOLDERS = {
        'tech_software_dev': [6, 7, 10],  # Technical + Data focus
        'healthcare_medical': [15, 16],  # Healthcare Compliance, Medical
        'legal_law': [17, 18],  # Legal Research, Compliance
        'finance_banking': [20, 21],  # Finance-specific
        'marketing_advertising': [12, 13, 8],  # Marketing + Creative
        'consulting_professional_services': [4, 5, 10],  # Executive + Analysis
        'manufacturing_production': [4, 10],  # Leadership + Analysis
        'media_entertainment': [8, 9],  # Creative + Communication
        'real_estate': [12, 14],  # Marketing + Customer relations
        'ecommerce_retail': [12, 13, 14],  # Marketing + Customer
        'education_training': [16, 17],  # Training & Development
        'hr_recruitment': [16, 17],  # HR specific
        'customer_service_support': [14, 15],  # Customer service
    }
    
    # SENIORITY-BASED FOLDERS (Tier 3)
    SENIORITY_FOLDERS = {
        'student': [1, 2],  # Basic starter + learning
        'junior_0_5': [1, 2, 3],  # Starter + junior development
        'mid_5_10': [3, 4],  # Career development + leadership prep
        'senior_10_15': [4, 5],  # Senior professional + leadership
        'lead_15_plus': [4, 5, 6],  # Executive + strategic
        'executive': [4, 5, 6],  # Full executive suite
    }
    
    # INTEREST-DRIVEN FOLDERS (Tier 4)
    INTEREST_FOLDERS = {
        'writing': [8, 9],  # Creative content, communication
        'coding': [6, 7],  # Technical development
        'data_analysis': [10, 11],  # Data & analytics
        'research': [10, 11, 17],  # Research + legal research
        'creativity': [8, 9],  # Creative work
        'learning': [16, 17, 1],  # Learning & development
        'marketing': [12, 13],  # Marketing focused
        'email': [9, 14],  # Communication + customer
        'summarizing': [10, 11],  # Analysis tools
        'critical_thinking': [4, 10, 11],  # Executive + analysis
        'customer_support': [14, 15],  # Customer service
        'decision_making': [4, 5],  # Executive decision making
        'language_learning': [1, 16],  # Basic + learning
    }
    
    @classmethod
    def get_folder_mapping_summary(cls) -> dict:
        """Get a summary of all folder mappings for debugging."""
        return {
            'starter_pack': cls.STARTER_PACK_FOLDER_IDS,
            'professional_roles': cls.PROFESSIONAL_ROLE_FOLDERS,
            'industries': cls.INDUSTRY_FOLDERS,
            'seniority_levels': cls.SENIORITY_FOLDERS,
            'interests': cls.INTEREST_FOLDERS,
            'total_unique_folders': len(set([
                *cls.STARTER_PACK_FOLDER_IDS,
                *[f for folders in cls.PROFESSIONAL_ROLE_FOLDERS.values() for f in folders],
                *[f for folders in cls.INDUSTRY_FOLDERS.values() for f in folders],
                *[f for folders in cls.SENIORITY_FOLDERS.values() for f in folders],
                *[f for folders in cls.INTEREST_FOLDERS.values() for f in folders],
            ]))
        }

# Updated folder mapping utility to use the configuration
class SmartFolderRecommendationEngine:
    """
    Enhanced folder recommendation engine using configurable folder mappings.
    """
    
    def __init__(self):
        self.config = FolderConfig()
    
    def get_starter_pack_folders(self) -> list[int]:
        """Get starter pack folder IDs."""
        return self.config.STARTER_PACK_FOLDER_IDS.copy()
    
    def recommend_folders_for_user(self, 
                                 job_type: str = None,
                                 job_industry: str = None, 
                                 job_seniority: str = None,
                                 interests: list[str] = None) -> list[int]:
        """
        Recommend folder IDs based on user profile with weighted scoring.
        """
        folder_scores = {}
        
        # Start with starter pack (high priority)
        for folder_id in self.config.STARTER_PACK_FOLDER_IDS:
            folder_scores[folder_id] = folder_scores.get(folder_id, 0) + 100
        
        # Professional role (Tier 1 - High Priority: +50 points)
        if job_type and job_type in self.config.PROFESSIONAL_ROLE_FOLDERS:
            for folder_id in self.config.PROFESSIONAL_ROLE_FOLDERS[job_type]:
                folder_scores[folder_id] = folder_scores.get(folder_id, 0) + 50
        
        # Industry (Tier 2 - Medium Priority: +30 points)
        if job_industry and job_industry in self.config.INDUSTRY_FOLDERS:
            for folder_id in self.config.INDUSTRY_FOLDERS[job_industry]:
                folder_scores[folder_id] = folder_scores.get(folder_id, 0) + 30
        
        # Seniority (Tier 3 - Medium Priority: +25 points)
        if job_seniority and job_seniority in self.config.SENIORITY_FOLDERS:
            for folder_id in self.config.SENIORITY_FOLDERS[job_seniority]:
                folder_scores[folder_id] = folder_scores.get(folder_id, 0) + 25
        
        # Interests (Tier 4 - Lower Priority: +15 points each)
        if interests:
            for interest in interests:
                clean_interest = interest.replace('other:', '') if interest.startswith('other:') else interest
                if clean_interest in self.config.INTEREST_FOLDERS:
                    for folder_id in self.config.INTEREST_FOLDERS[clean_interest]:
                        folder_scores[folder_id] = folder_scores.get(folder_id, 0) + 15
        
        # Sort by score (highest first) and return folder IDs
        # Only include folders with meaningful scores (>= 20 points unless it's starter pack)
        recommended = [
            folder_id for folder_id, score in sorted(folder_scores.items(), key=lambda x: x[1], reverse=True)
            if score >= 20 or folder_id in self.config.STARTER_PACK_FOLDER_IDS
        ]
        
        return recommended
    
    def explain_recommendations(self, 
                              job_type: str = None,
                              job_industry: str = None, 
                              job_seniority: str = None,
                              interests: list[str] = None) -> dict:
        """Get detailed explanation of recommendations."""
        explanation = {
            'starter_pack': self.config.STARTER_PACK_FOLDER_IDS.copy(),
            'professional_role': [],
            'industry': [],
            'seniority': [],
            'interests': [],
            'scores': {}
        }
        
        # Calculate scores for transparency
        folder_scores = {}
        
        # Starter pack
        for folder_id in self.config.STARTER_PACK_FOLDER_IDS:
            folder_scores[folder_id] = folder_scores.get(folder_id, 0) + 100
        
        # Professional role
        if job_type and job_type in self.config.PROFESSIONAL_ROLE_FOLDERS:
            explanation['professional_role'] = self.config.PROFESSIONAL_ROLE_FOLDERS[job_type].copy()
            for folder_id in self.config.PROFESSIONAL_ROLE_FOLDERS[job_type]:
                folder_scores[folder_id] = folder_scores.get(folder_id, 0) + 50
        
        # Industry
        if job_industry and job_industry in self.config.INDUSTRY_FOLDERS:
            explanation['industry'] = self.config.INDUSTRY_FOLDERS[job_industry].copy()
            for folder_id in self.config.INDUSTRY_FOLDERS[job_industry]:
                folder_scores[folder_id] = folder_scores.get(folder_id, 0) + 30
        
        # Seniority
        if job_seniority and job_seniority in self.config.SENIORITY_FOLDERS:
            explanation['seniority'] = self.config.SENIORITY_FOLDERS[job_seniority].copy()
            for folder_id in self.config.SENIORITY_FOLDERS[job_seniority]:
                folder_scores[folder_id] = folder_scores.get(folder_id, 0) + 25
        
        # Interests
        if interests:
            interest_folders = set()
            for interest in interests:
                clean_interest = interest.replace('other:', '') if interest.startswith('other:') else interest
                if clean_interest in self.config.INTEREST_FOLDERS:
                    interest_folders.update(self.config.INTEREST_FOLDERS[clean_interest])
                    for folder_id in self.config.INTEREST_FOLDERS[clean_interest]:
                        folder_scores[folder_id] = folder_scores.get(folder_id, 0) + 15
            explanation['interests'] = list(interest_folders)
        
        explanation['scores'] = folder_scores
        
        return explanation