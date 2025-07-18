/**
 * TemplateService
 * 
 * This file re-exports all template-related functionality from the modular structure.
 * All the actual implementation has been moved to the templates/ directory.
 */

export {
  useUserMetadata,
  usePinnedFolders,
  useAllFoldersOfType,
  useUserFolders,
  useUnorganizedTemplates,
  usePinnedTemplates,
  useToggleFolderPin,
  toggleTemplatePin,
  useDeleteFolder,
  useCreateFolder,
  useDeleteTemplate,
  useTemplateActions
} from './templates';