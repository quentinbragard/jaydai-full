// src/components/dialogs/settings/SettingsDialog.tsx
import React, { useState, useEffect } from 'react';
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Separator } from "@/components/ui/separator";
import { toast } from "sonner";
import { useDialog } from '@/components/dialogs/DialogContext';
import { DIALOG_TYPES } from '@/components/dialogs/DialogRegistry';
import { getMessage } from '@/core/utils/i18n';
import { BaseDialog } from '../BaseDialog';

interface Settings {
  autoSave: boolean;
  autoSaveInterval: number;
  syncEnabled: boolean;
  statsVisible: boolean;
}

/**
 * Dialog for application settings
 */
export const SettingsDialog: React.FC = () => {
  const { isOpen, dialogProps } = useDialog(DIALOG_TYPES.SETTINGS);
  const [settings, setSettings] = useState<Settings>({
    autoSave: true,
    autoSaveInterval: 60,
    syncEnabled: true,
    statsVisible: true
  });

  const [loading, setLoading] = useState(true);

  // Load settings when dialog opens
  useEffect(() => {
    if (isOpen) {
      loadSettings();
    }
  }, [isOpen]);

  const loadSettings = async () => {
    setLoading(true);
    try {
      // Get settings from chrome storage
      chrome.storage.sync.get(['jaydaiSettings'], (result) => {
        if (result.jaydaiSettings) {
          setSettings(result.jaydaiSettings);
        }
        setLoading(false);
      });
    } catch (error) {
      console.error('Failed to load settings:', error);
      setLoading(false);
    }
  };

  const saveSettings = async () => {
    try {
      // Save settings to chrome storage
      chrome.storage.sync.set({ jaydaiSettings: settings }, () => {
        toast.success(getMessage('saveChanges', undefined, 'Settings saved'));
        
        // Notify content script to apply changes
        chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
          if (tabs[0]?.id) {
            chrome.tabs.sendMessage(tabs[0].id, { 
              action: 'applySettings', 
              settings 
            });
          }
        });
        
        // Close the dialog
        dialogProps.onOpenChange(false);
      });
    } catch (error) {
      console.error('Failed to save settings:', error);
      toast.error(getMessage('saveFailed', undefined, 'Failed to save settings'));
    }
  };

  const handleChange = (key: keyof Settings, value: any) => {
    setSettings(prev => ({
      ...prev,
      [key]: value
    }));
  };

  const handleCancel = () => {
    dialogProps.onOpenChange(false);
  };
  
  return (
    <BaseDialog
      open={isOpen}
      onOpenChange={(open: boolean) => {
        if (!open) {
          handleCancel();
        }
        dialogProps.onOpenChange(open);
      }}
      title={getMessage('settings', undefined, 'Settings')}
      description={getMessage('settingsDescription', undefined, 'Configure your application settings')}
      className="jd-max-w-md"
    >
      <div className="jd-flex jd-flex-col jd-space-y-4 jd-mt-4">
        <div className="jd-space-y-2">
          <div className="jd-flex jd-items-center jd-justify-between">
            <label className="jd-text-sm jd-font-medium" htmlFor="auto-save">
              {getMessage('autoSaveConversations', undefined, 'Auto-save conversations')}
            </label>
            <input
              id="auto-save"
              type="checkbox"
              checked={settings.autoSave}
              onChange={(e) => handleChange('autoSave', e.target.checked)}
              className="jd-h-4 jd-w-4 jd-rounded jd-border-gray-300 jd-text-primary focus:ring-primary"
            />
          </div>
          
          {settings.autoSave && (
            <div className="jd-flex jd-items-center jd-justify-between jd-pl-4">
              <label className="jd-text-sm jd-font-medium" htmlFor="auto-save-interval">
                {getMessage('autoSaveInterval', undefined, 'Auto-save interval (seconds)')}
              </label>
              <Input
                id="auto-save-interval"
                type="number"
                min={10}
                max={300}
                value={settings.autoSaveInterval}
                onChange={(e) => handleChange('autoSaveInterval', parseInt(e.target.value, 10))}
                className="jd-w-20"
              />
            </div>
          )}
        </div>
        
        <Separator />
        
        <div className="jd-space-y-2">
          <div className="jd-flex jd-items-center jd-justify-between">
            <label className="jd-text-sm jd-font-medium" htmlFor="sync-enabled">
              {getMessage('enableSync', undefined, 'Enable synchronization')}
            </label>
            <input
              id="sync-enabled"
              type="checkbox"
              checked={settings.syncEnabled}
              onChange={(e) => handleChange('syncEnabled', e.target.checked)}
              className="jd-h-4 jd-w-4 jd-rounded jd-border-gray-300 jd-text-primary focus:ring-primary"
            />
          </div>
          
          <div className="jd-flex jd-items-center jd-justify-between">
            <label className="jd-text-sm jd-font-medium" htmlFor="stats-visible">
              {getMessage('showStatsPanel', undefined, 'Show stats panel')}
            </label>
            <input
              id="stats-visible"
              type="checkbox"
              checked={settings.statsVisible}
              onChange={(e) => handleChange('statsVisible', e.target.checked)}
              className="jd-h-4 jd-w-4 jd-rounded jd-border-gray-300 jd-text-primary focus:ring-primary"
            />
          </div>
        </div>
      </div>
      
      <div className="jd-mt-4 jd-flex jd-justify-end">
        <Button variant="outline" onClick={handleCancel}>
          {getMessage('cancel', undefined, 'Cancel')}
        </Button>
        <Button onClick={saveSettings} disabled={loading}>
          {getMessage('saveChanges', undefined, 'Save Changes')}
        </Button>
      </div>
    </BaseDialog>
  );
};