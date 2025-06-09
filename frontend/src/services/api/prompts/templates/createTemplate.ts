/**
 * Create a new template
 */

import { apiClient } from "@/services/api/ApiClient";

export async function createTemplate(templateData: any): Promise<any> {
    try {
      // Ensure required fields are present
      if (!templateData.title || !templateData.content) {
        return {
          success: false,
          message: 'Title and content are required'
        };
      }
    
      // Create a proper API request body
      const requestBody = {
        title: templateData.title,
        content: templateData.content,
        tags: templateData.tags || [],
        locale: templateData.locale || 'en',
        folder_id: templateData.folder_id || null,
        type: templateData.type || 'user',
        // Include advanced editor fields when present
        blocks: templateData.blocks || [],
        metadata: templateData.metadata || {},
        enhanced_metadata: templateData.enhanced_metadata || undefined
      };

      const response = await apiClient.request('/prompts/templates', {
        method: 'POST',
        body: JSON.stringify(requestBody)
      });
      return response;
    } catch (error) {
      console.error('Error creating template:', error);
      return {
        success: false,
        message: error instanceof Error ? error.message : 'Unknown error'
      };
    }
  }
