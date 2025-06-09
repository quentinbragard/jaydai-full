import { useCallback } from 'react';
import { useDialogManager } from '@/components/dialogs/DialogContext';
import { DIALOG_TYPES } from '@/components/dialogs/DialogRegistry';

export function useDialogActions() {
  const { openDialog } = useDialogManager();

  const openSettings = useCallback(() => openDialog(DIALOG_TYPES.SETTINGS, {}), [openDialog]);

  const openCreateTemplate = useCallback(
    (props?: any) => openDialog(DIALOG_TYPES.CREATE_TEMPLATE, props),
    [openDialog]
  );

  const openEditTemplate = useCallback(
    (props?: any) => openDialog(DIALOG_TYPES.EDIT_TEMPLATE, props),
    [openDialog]
  );

  const openCreateFolder = useCallback(
    (props?: any) => openDialog(DIALOG_TYPES.CREATE_FOLDER, props),
    [openDialog]
  );

  const openAuth = useCallback(
    (props?: any) => openDialog(DIALOG_TYPES.AUTH, props),
    [openDialog]
  );

  const openPlaceholderEditor = useCallback(
    (props?: any) => openDialog(DIALOG_TYPES.PLACEHOLDER_EDITOR, props),
    [openDialog]
  );

  const openConfirmation = useCallback(
    (props?: any) => openDialog(DIALOG_TYPES.CONFIRMATION, props),
    [openDialog]
  );

  const openEnhancedStats = useCallback(
    () => openDialog(DIALOG_TYPES.ENHANCED_STATS, {}),
    [openDialog]
  );

  const openCreateBlock = useCallback(
    (props?: any) => openDialog(DIALOG_TYPES.CREATE_BLOCK, props),
    [openDialog]
  );

  const openInsertBlock = useCallback(
    () => openDialog(DIALOG_TYPES.INSERT_BLOCK, {}),
    [openDialog]
  );

  return {
    openSettings,
    openCreateTemplate,
    openEditTemplate,
    openCreateFolder,
    openAuth,
    openPlaceholderEditor,
    openConfirmation,
    openEnhancedStats,
    openCreateBlock,
    openInsertBlock,
  };
}
