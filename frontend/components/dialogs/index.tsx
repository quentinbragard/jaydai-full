
// src/components/dialogs/index.tsx
import React from 'react';
import { DialogManagerProvider } from './DialogContext';
import { CreateTemplateDialog } from './prompts/CreateTemplateDialog';
import { CreateFolderDialog } from './prompts/CreateFolderDialog';
import { FolderManagerDialog } from './prompts/FolderManagerDialog';
import { CustomizeTemplateDialog } from './prompts/CustomizeTemplateDialog';
import { AuthDialog } from './auth/AuthDialog';
import { SettingsDialog } from './settings/SettingsDialog';
import { ConfirmationDialog } from './common/ConfirmationDialog';
import { EnhancedStatsDialog } from './analytics/EnhancedStatsDialog';
import { BrowseMoreFoldersDialog } from './prompts/BrowseMoreFoldersDialog';
import { CreateBlockDialog } from './prompts/CreateBlockDialog';
import { TutorialsDialog } from './tutorials/TutorialsDialog';
import { TutorialVideoDialog } from './tutorials/TutorialVideoDialog';

/**
 * Main dialog provider that includes all dialog components
 * This component ensures window.dialogManager is available
 */
export const DialogProvider: React.FC<{children: React.ReactNode}> = ({ children }) => {
  // Debug check to verify dialog manager initialization
  React.useEffect(() => {
    
    // Monitor for any errors in dialog functionality
    const handleError = (error: ErrorEvent) => {
      if (error.message.includes('dialogManager') || error.message.includes('Dialog')) {
        console.error('Dialog system error detected:', error);
      }
    };
    
    window.addEventListener('error', handleError);
    
    return () => {
      window.removeEventListener('error', handleError);
    };
  }, []);
  
  return (
    <DialogManagerProvider>
      {children}
      
      {/* Register all dialogs here */}
      <CreateTemplateDialog />

      <CreateFolderDialog  />
      <FolderManagerDialog />
      <AuthDialog />
      <SettingsDialog />
      <ConfirmationDialog />
      <EnhancedStatsDialog />
      <BrowseMoreFoldersDialog />
      <TutorialsDialog />
      <TutorialVideoDialog />
      {/* Place the customize dialog last so it appears above others */}
      <CustomizeTemplateDialog />
      <CreateBlockDialog />
    </DialogManagerProvider>
  );
};

// Export individual components and hooks
export { DialogManagerProvider } from './DialogContext';
export { useDialog, useDialogManager } from './DialogContext';
export { CreateTemplateDialog as TemplateDialog } from './prompts/CreateTemplateDialog';
export { CreateFolderDialog } from './prompts/CreateFolderDialog';
export { AuthDialog } from './auth/AuthDialog';
export { SettingsDialog } from './settings/SettingsDialog';
export { ConfirmationDialog } from './common/ConfirmationDialog';
export { EnhancedStatsDialog } from './analytics/EnhancedStatsDialog';
export { FolderManagerDialog } from './prompts/FolderManagerDialog';
export { BrowseMoreFoldersDialog } from './prompts/BrowseMoreFoldersDialog';
export { BaseDialog } from './BaseDialog';
export { CreateBlockDialog } from './prompts/CreateBlockDialog';
export { TutorialsDialog } from './tutorials/TutorialsDialog';
export { TutorialVideoDialog } from './tutorials/TutorialVideoDialog';
