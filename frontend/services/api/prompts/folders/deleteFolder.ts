import { apiClient } from "@/services/api/ApiClient";

/**
* Delete a folder
*/
export async function deleteFolder(folderId: number): Promise<{ success: boolean; message?: string; data?: any }> {
    try {
      const response = await apiClient.request(`/prompts/folders/${folderId}`, {
        method: 'DELETE'
      });
      return response;
    } catch (error) {
      console.error('Error deleting folder:', error);
      return {
        success: false,
        message: error instanceof Error ? error.message : 'Unknown error'
      };
    }
  }