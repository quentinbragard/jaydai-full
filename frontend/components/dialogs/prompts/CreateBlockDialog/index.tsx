// src/components/dialogs/blocks/CreateBlockDialog.tsx
import React, { useState, useEffect } from 'react';
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Save, X } from 'lucide-react';
import { cn } from '@/core/utils/classNames';
import { toast } from 'sonner';
import { getMessage } from '@/core/utils/i18n';
import { blocksApi } from '@/services/api/BlocksApi';
import { BaseDialog } from '@/components/dialogs/BaseDialog';
import { useDialog } from '@/components/dialogs/DialogContext';
import { DIALOG_TYPES } from '@/components/dialogs/DialogRegistry';
import { BlockType } from '@/types/prompts/blocks';
import { BLOCK_TYPE_LABELS, getBlockTypeIcon, getBlockTypeColors } from '@/utils/prompts/blockUtils';
import { useThemeDetector } from '@/hooks/useThemeDetector';
import { trackEvent, EVENTS } from '@/utils/amplitude';

const AVAILABLE_BLOCK_TYPES: BlockType[] = [
  'role', 'context', 'goal', 'custom',
  'output_format', 'example', 'constraint', 'tone_style', 'audience'
];

export const CreateBlockDialog: React.FC = () => {
  const { isOpen, data, dialogProps } = useDialog(DIALOG_TYPES.CREATE_BLOCK);
  
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [content, setContent] = useState('');
  const [blockType, setBlockType] = useState<BlockType>('role');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [validationErrors, setValidationErrors] = useState<Record<string, string>>({});
  
  const isDarkMode = useThemeDetector();
  const Icon = getBlockTypeIcon(blockType);
  const typeColors = getBlockTypeColors(blockType, isDarkMode);

  // Extract data from dialog context
  const initialType = data?.initialType as BlockType;
  const initialTitle = data?.initialTitle || '';
  const initialContent = data?.initialContent || '';
  const initialDescription = data?.initialDescription || '';
  const onBlockCreated = data?.onBlockCreated as
    | ((blockData: any) => Promise<boolean> | boolean)
    | undefined;
  const isEdit = data?.isEdit || false;

  // Reset form when dialog opens/closes
  useEffect(() => {
    if (isOpen) {
      setContent(initialContent);
      setBlockType(initialType || 'role');
      setName(initialTitle);
      setDescription(initialDescription);
      setValidationErrors({});
      setIsSubmitting(false);
    }
  }, [isOpen, initialType, initialTitle, initialContent, initialDescription]);


  const validateForm = () => {
    const errors: Record<string, string> = {};
    
    if (!name.trim()) {
      errors.name = getMessage('blockNameRequired', undefined, 'Block name is required');
    }
    
    if (!content.trim()) {
      errors.content = getMessage('blockContentRequired', undefined, 'Block content is required');
    }
    
    if (!blockType) {
      errors.type = getMessage('blockTypeRequired', undefined, 'Block type is required');
    }
    
    setValidationErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    e.stopPropagation();
    
    if (!validateForm()) {
      return;
    }
  
    setIsSubmitting(true);
    try {
      const blockData = {
        type: blockType,
        content: content.trim(),
        title: name.trim(),
        description: description.trim() || undefined
      };

      if (onBlockCreated) {
        const result = await onBlockCreated(blockData);
        if (result) {
          handleClose();
        }
      } else {
        const response = await blocksApi.createBlock(blockData);
        if (response.success && response.data) {
          toast.success(getMessage('blockCreated', undefined, 'Block created successfully'));
          trackEvent(EVENTS.BLOCK_CREATED, {
            block_id: response.data.id,
            block_type: response.data.type,
            source: (data?.source as string) || 'CreateBlockDialog'
          });
          handleClose();
        } else {
          toast.error(response.message || getMessage('errorCreatingBlock', undefined, 'Failed to create block'));
        }
      }
    } catch (error) {
      console.error('Error creating block:', error);
      toast.error(getMessage('errorCreatingBlock', undefined, 'Failed to create block'));
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleClose = () => {
    setName('');
    setDescription('');
    setContent('');
    setBlockType('custom');
    setValidationErrors({});
    setIsSubmitting(false);
    dialogProps.onOpenChange(false);
  };

  if (!isOpen) return null;


  // Create footer with action buttons
  const footer = (
    <div className="jd-flex jd-justify-end jd-gap-2">
      <Button 
        type="button" 
        variant="outline" 
        onClick={handleClose}
        disabled={isSubmitting}
      >
        <X className="jd-h-4 jd-w-4 jd-mr-2" />
        {getMessage('cancel', undefined, 'Cancel')}
      </Button>
      <Button
        type="submit"
        disabled={isSubmitting || !name.trim() || !content.trim()}
        onClick={handleSubmit}
        className={cn(
          'jd-transition-all jd-duration-300',
          typeColors
        )}
      >
        {isSubmitting ? (
          <>
            <div className="jd-animate-spin jd-h-4 jd-w-4 jd-border-2 jd-border-current jd-border-t-transparent jd-rounded-full jd-mr-2 !jd-text-white !jd-text-bold"></div>
            {getMessage(isEdit ? 'updating' : 'creating', undefined, isEdit ? 'Updating...' : 'Creating...')}
          </>
        ) : (
          <>
            <Save className="jd-h-4 jd-w-4 jd-mr-2 jd-text-primary-foreground" />
            <span className="jd-text-primary-foreground">
              {getMessage(isEdit ? 'updateBlock' : 'createBlock', undefined, isEdit ? 'Update Block' : 'Create Block')}
            </span>
          </>
        )}
      </Button>
    </div>
  );

  return (
    <BaseDialog
      open={isOpen}
      footer={footer}
      onOpenChange={handleClose}
      title={getMessage(isEdit ? 'editBlockTitle' : 'createBlockTitle', undefined, isEdit ? 'Edit Block' : 'Create Block')}
      description={getMessage(
        isEdit ? 'editBlockDescription' : 'createBlockDescription',
        undefined,
        isEdit ? 'Update your block details' : 'Create a new reusable block for your prompts'
      )}
      className="jd-max-w-2xl"
      baseZIndex={10010}
    >
      <form onSubmit={handleSubmit} className="jd-space-y-6">
        {/* Block Type Selection */}
        <div>
          <label className="jd-text-sm jd-font-medium jd-mb-2 jd-block">{getMessage('blockType', undefined, 'Block Type')}</label>
          <Select value={blockType} onValueChange={(value) => setBlockType(value as BlockType)}>
            <SelectTrigger className={cn("jd-w-full", validationErrors.type && "jd-border-red-500")}>
              <SelectValue>
                <div className="jd-flex jd-items-center jd-gap-2">
                  <Icon className="jd-h-4 jd-w-4" />
                  {BLOCK_TYPE_LABELS[blockType]}
                </div>
              </SelectValue>
            </SelectTrigger>
            <SelectContent className="jd-z-[10010]">
              {AVAILABLE_BLOCK_TYPES.map((type) => {
                const TypeIcon = getBlockTypeIcon(type);
                return (
                  <SelectItem key={type} value={type}>
                    <div className="jd-flex jd-items-center jd-gap-2">
                      <TypeIcon className="jd-h-4 jd-w-4" />
                      {BLOCK_TYPE_LABELS[type]}
                    </div>
                  </SelectItem>
                );
              })}
            </SelectContent>
          </Select>
          {validationErrors.type && (
            <p className="jd-text-xs jd-text-red-500 jd-mt-1">{validationErrors.type}</p>
          )}
        </div>

        {/* Block Name */}
        <div>
          <label className="jd-text-sm jd-font-medium jd-mb-2 jd-block">{getMessage('blockName', undefined, 'Block Name')}</label>
          <Input
            value={name}
            onChange={(e) => {
              setName(e.target.value);
              if (validationErrors.name) {
                setValidationErrors(prev => ({ ...prev, name: '' }));
              }
            }}
            placeholder={getMessage('enterBlockName', undefined, 'Enter block name')}
            className={cn("jd-w-full", validationErrors.name && "jd-border-red-500")}
            autoFocus
            onKeyDown={(e) => {
              e.stopPropagation();
              if (e.key === 'Escape') {
                e.preventDefault();
                return;
              }
            }}
            onKeyPress={(e) => e.stopPropagation()}
            onKeyUp={(e) => e.stopPropagation()}
          />
          {validationErrors.name ? (
            <p className="jd-text-xs jd-text-red-500 jd-mt-1">{validationErrors.name}</p>
          ) : (
            !name.trim() && (
              <p className="jd-text-xs jd-text-muted-foreground jd-mt-1">{getMessage('blockNameHint', undefined, 'Please enter a block name')}</p>
            )
          )}
        </div>
        
        {/* Block Content */}
        <div>
          <label className="jd-text-sm jd-font-medium jd-mb-2 jd-block">{getMessage('blockContent', undefined, 'Block Content')}</label>
          <Textarea
            value={content}
            onChange={(e) => {
              setContent(e.target.value);
              if (validationErrors.content) {
                setValidationErrors(prev => ({ ...prev, content: '' }));
              }
            }}
            placeholder={getMessage('enterBlockContent', undefined, 'Enter block content...')}
            className={cn("jd-w-full jd-min-h-[120px] jd-resize-none", validationErrors.content && "jd-border-red-500")}
            rows={6}
            onKeyDown={(e) => {
              e.stopPropagation();
              if (e.key === 'Escape') {
                e.preventDefault();
                return;
              }
            }}
            onKeyPress={(e) => e.stopPropagation()}
            onKeyUp={(e) => e.stopPropagation()}
          />
          {validationErrors.content && (
            <p className="jd-text-xs jd-text-red-500 jd-mt-1">{validationErrors.content}</p>
          )}
          {content && (
            <div className="jd-flex jd-justify-between jd-text-xs jd-text-muted-foreground jd-mt-1">
              <span>
                {content.length}{' '}
                {getMessage('charactersLabel', undefined, 'characters')}
              </span>
              <span>
                {content.split('\n').length}{' '}
                {getMessage('linesLabel', undefined, 'lines')}
              </span>
            </div>
          )}
        </div>

        {/* Block Description (Optional) */}
        <div>
          <label className="jd-text-sm jd-font-medium jd-mb-2 jd-block">
            {getMessage('templateDescription', undefined, 'Description (optional)')}
          </label>
          <Textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder={getMessage('blockDescriptionPlaceholder', undefined, 'Enter block description...')}
            className="jd-w-full jd-resize-none"
            rows={3}
            onKeyDown={(e) => {
              e.stopPropagation();
              if (e.key === 'Escape') {
                e.preventDefault();
                return;
              }
            }}
            onKeyPress={(e) => e.stopPropagation()}
            onKeyUp={(e) => e.stopPropagation()}
          />
        </div>
      </form>
    </BaseDialog>
  );
};