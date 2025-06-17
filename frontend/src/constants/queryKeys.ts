// src/constants/queryKeys.ts

/**
 * Query keys for React Query
 * Centralizing these prevents typos and makes refactoring easier
 */

export const QUERY_KEYS = {
    // Template and folder related queries
    USER_FOLDERS: 'userFolders',
    COMPANY_FOLDERS: 'companyFolders',
    ORGANIZATION_FOLDERS: 'organizationFolders',
    OFFICIAL_FOLDERS: 'officialFolders',
    MIXED_FOLDERS: 'mixedFolders',
    ALL_FOLDERS: 'allFolders',
    USER_TEMPLATES: 'userTemplates',
    UNORGANIZED_TEMPLATES: 'unorganizedTemplates',
    PINNED_FOLDERS: 'pinnedFolders',
    
    // User related queries
    USER_METADATA: 'userMetadata',
    USER_PROFILE: 'userProfile',
    
    // Stats related queries
    USER_STATS: 'userStats',
    WEEKLY_STATS: 'weeklyStats',
  };