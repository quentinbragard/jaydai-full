import React, { useEffect, useState, useCallback } from 'react';
import { BaseDialog } from '@/components/dialogs/BaseDialog';
import { useDialog } from '@/components/dialogs/DialogContext';
import { DIALOG_TYPES } from '@/components/dialogs/DialogRegistry';
import { blocksApi } from '@/services/api/BlocksApi';
import { Block, BlockType } from '@/types/prompts/blocks';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Textarea } from '@/components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import LoadingSpinner from '@/components/common/LoadingSpinner';
import { EmptyMessage } from '@/components/panels/TemplatesPanel/EmptyMessage';
import {
  buildPromptPart,
  buildPromptPartHtml,
  BLOCK_TYPE_LABELS,
  getBlockTypeIcon,
  getBlockIconColors,
  BLOCK_TYPES
} from '@/components/prompts/blocks/blockUtils';
import { useThemeDetector } from '@/hooks/useThemeDetector';
import { insertIntoPromptArea } from '@/utils/templates/placeholderUtils';
import { 
  DndContext, 
  closestCenter, 
  KeyboardSensor, 
  PointerSensor, 
  useSensor, 
  useSensors,
  DragEndEvent,
  DragStartEvent
} from '@dnd-kit/core';
import {
  arrayMove,
  SortableContext,
  sortableKeyboardCoordinates,
  verticalListSortingStrategy,
} from '@dnd-kit/sortable';

import { 
  Search,
  Plus,
  Eye,
  Code,
  Sparkles,
  ArrowRight,
  Copy,
  Filter,
  X,
  Check,
  Save
} from 'lucide-react';
import { cn } from '@/core/utils/classNames';
import { toast } from 'sonner';

import { SortableSelectedBlock } from './SortableSelectedBlock';
import { AvailableBlockCard } from './AvailableBlockCard';
import { PreviewBlock } from './PreviewBlock';

// Metadata type groups for filtering
const METADATA_FILTERS = [
  { type: 'role', label: 'Role', icon: '👤' },
  { type: 'context', label: 'Context', icon: '📝' },
  { type: 'goal', label: 'Goal', icon: '🎯' },
  { type: 'constraint', label: 'Constraints', icon: '🚫' },
  { type: 'example', label: 'Examples', icon: '💡' },
  { type: 'output_format', label: 'Format', icon: '📋' },
  { type: 'tone_style', label: 'Tone', icon: '🎨' },
  { type: 'audience', label: 'Audience', icon: '👥' },
] as const;

// Inline block creation component
const InlineBlockCreator: React.FC<{
  onBlockCreated: (block: Block) => void;
  onCancel: () => void;
}> = ({ onBlockCreated, onCancel }) => {
  const [type, setType] = useState<BlockType>('custom');
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [isCreating, setIsCreating] = useState(false);
  const isDark = useThemeDetector();

  const handleCreate = async () => {
    if (!content.trim()) {
      toast.error('Block content is required');
      return;
    }

    setIsCreating(true);
    try {
      const blockData = {
        type,
        content: { en: content.trim() },
        title: title.trim() ? { en: title.trim() } : { en: `${BLOCK_TYPE_LABELS[type]} Block` },
        description: { en: `Custom ${type} block` }
      };
      
      const response = await blocksApi.createBlock(blockData);

      if (response.success && response.data) {
        toast.success('Block created successfully');
        onBlockCreated(response.data);
      } else {
        toast.error(response.message || 'Failed to create block');
      }
    } catch (error) {
      console.error('Error creating block:', error);
      toast.error('An error occurred while creating the block');
    } finally {
      setIsCreating(false);
    }
  };

  const Icon = getBlockTypeIcon(type);
  const iconBg = getBlockIconColors(type, isDark);

  return (
    <div className="jd-border jd-rounded-lg jd-p-4 jd-bg-muted/20 jd-space-y-3">
      <div className="jd-flex jd-items-center jd-gap-2 jd-mb-3">
        <div className={cn('jd-p-1.5 jd-rounded-md', iconBg)}>
          <Icon className="jd-h-4 jd-w-4" />
        </div>
        <h3 className="jd-font-medium jd-text-sm">Create New Block</h3>
      </div>

      <div className="jd-space-y-3">
        <div>
          <label className="jd-text-xs jd-font-medium jd-mb-1 jd-block">Type</label>
          <Select value={type} onValueChange={(value) => setType(value as BlockType)}>
            <SelectTrigger className="jd-h-8 jd-text-xs">
              <SelectValue />
            </SelectTrigger>
            <SelectContent className="jd-z-[10010]">
              {BLOCK_TYPES.map((blockType) => {
                const TypeIcon = getBlockTypeIcon(blockType);
                return (
                  <SelectItem key={blockType} value={blockType}>
                    <div className="jd-flex jd-items-center jd-gap-2">
                      <TypeIcon className="jd-h-3 jd-w-3" />
                      {BLOCK_TYPE_LABELS[blockType]}
                    </div>
                  </SelectItem>
                );
              })}
            </SelectContent>
          </Select>
        </div>

        <div>
          <label className="jd-text-xs jd-font-medium jd-mb-1 jd-block">Title (optional)</label>
          <Input
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder={`${BLOCK_TYPE_LABELS[type]} Block`}
            className="jd-h-8 jd-text-xs"
            onKeyDown={(e) => e.stopPropagation()}
            onKeyPress={(e) => e.stopPropagation()}
            onKeyUp={(e) => e.stopPropagation()}
          />
        </div>

        <div>
          <label className="jd-text-xs jd-font-medium jd-mb-1 jd-block">Content</label>
          <Textarea
            value={content}
            onChange={(e) => setContent(e.target.value)}
            placeholder={`Enter ${type} content...`}
            className="jd-min-h-[80px] jd-text-xs jd-resize-none"
            rows={4}
            onKeyDown={(e) => e.stopPropagation()}
            onKeyPress={(e) => e.stopPropagation()}
            onKeyUp={(e) => e.stopPropagation()}
          />
        </div>

        <div className="jd-flex jd-gap-2 jd-pt-2">
          <Button
            size="sm"
            variant="outline"
            onClick={onCancel}
            disabled={isCreating}
            className="jd-flex-1 jd-h-8 jd-text-xs"
          >
            <X className="jd-h-3 jd-w-3 jd-mr-1" />
            Cancel
          </Button>
          <Button
            size="sm"
            onClick={handleCreate}
            disabled={isCreating || !content.trim()}
            className="jd-flex-1 jd-h-8 jd-text-xs"
          >
            {isCreating ? (
              <>
                <div className="jd-h-3 jd-w-3 jd-border jd-border-current jd-border-t-transparent jd-animate-spin jd-rounded-full jd-mr-1"></div>
                Creating...
              </>
            ) : (
              <>
                <Save className="jd-h-3 jd-w-3 jd-mr-1" />
                Create
              </>
            )}
          </Button>
        </div>
      </div>
    </div>
  );
};

// Editable preview component with placeholder highlighting and colors
const EditablePreview: React.FC<{
  content: string;
  htmlContent: string;
  onChange: (content: string) => void;
  isDark: boolean;
}> = ({ content, htmlContent, onChange, isDark }) => {
  const [isEditing, setIsEditing] = useState(false);
  const editorRef = React.useRef<HTMLDivElement>(null);

  const highlightPlaceholders = (text: string) => {
    if (!text) return '<span class="jd-text-muted-foreground jd-italic">Your prompt will appear here...</span>';
    
    return text
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/\n/g, '<br>')
      .replace(
        /\[(.*?)\]/g, 
        `<span class="jd-bg-yellow-300 jd-text-yellow-900 jd-font-bold jd-px-1 jd-rounded jd-inline-block jd-my-0.5">[$1]</span>`
      );
  };

  // Update display when not editing
  React.useEffect(() => {
    if (editorRef.current && !isEditing) {
      if (htmlContent && htmlContent.trim()) {
        const coloredWithPlaceholders = htmlContent.replace(
          /\[(.*?)\]/g, 
          `<span class="jd-bg-yellow-300 jd-text-yellow-900 jd-font-bold jd-px-1 jd-rounded jd-inline-block jd-my-0.5">[$1]</span>`
        );
        editorRef.current.innerHTML = coloredWithPlaceholders;
      } else {
        editorRef.current.innerHTML = highlightPlaceholders(content);
      }
    }
  }, [content, htmlContent, isEditing]);

  // Set up editing mode when it changes
  React.useEffect(() => {
    if (isEditing && editorRef.current) {
      // Convert to plain text for editing
      editorRef.current.textContent = content;
      editorRef.current.focus();

      // Place cursor at the end
      setTimeout(() => {
        if (editorRef.current) {
          const range = document.createRange();
          const selection = window.getSelection();
          range.selectNodeContents(editorRef.current);
          range.collapse(false);
          selection?.removeAllRanges();
          selection?.addRange(range);
        }
      }, 0);
    }
    // Only run when entering edit mode to preserve cursor position during typing
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isEditing]);

  const startEditing = (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsEditing(true);
  };

  const stopEditing = () => {
    if (isEditing && editorRef.current) {
      const newContent = editorRef.current.textContent || '';
      onChange(newContent);
      setIsEditing(false);
    }
  };

  const handleInput = () => {
    if (isEditing && editorRef.current) {
      const newContent = editorRef.current.textContent || '';
      onChange(newContent);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    // CRITICAL: Stop all key events from bubbling up to prevent dialog from closing
    e.stopPropagation();
    
    if (isEditing && e.key === 'Escape') {
      e.preventDefault();
      stopEditing();
      return;
    }
    
    // Let all other keys work naturally for contentEditable
  };

  const handleBlur = (e: React.FocusEvent) => {
    // Only stop editing if focus is going outside the editor
    const relatedTarget = e.relatedTarget as HTMLElement;
    if (!editorRef.current?.contains(relatedTarget)) {
      stopEditing();
    }
  };

  return (
    <div
      ref={editorRef}
      contentEditable={isEditing}
      onClick={!isEditing ? startEditing : undefined}
      onBlur={handleBlur}
      onInput={handleInput}
      onKeyDown={handleKeyDown}
      // Stop all events from bubbling to prevent interference
      onKeyPress={(e) => e.stopPropagation()}
      onKeyUp={(e) => e.stopPropagation()}
      className={cn(
        'jd-min-h-[200px] jd-p-4 jd-rounded-lg jd-border jd-text-sm jd-leading-relaxed',
        'jd-whitespace-pre-wrap jd-break-words jd-transition-all jd-duration-200',
        'focus:jd-outline-none',
        isEditing 
          ? 'jd-ring-2 jd-ring-primary/50 jd-cursor-text jd-bg-opacity-95' 
          : 'jd-cursor-pointer hover:jd-bg-muted/10 hover:jd-border-primary/30',
        isDark 
          ? 'jd-bg-gray-800 jd-border-gray-700 jd-text-white' 
          : 'jd-bg-white jd-border-gray-200 jd-text-gray-900'
      )}
      style={{ 
        minHeight: '200px',
        wordBreak: 'break-word',
        // Ensure text is visible while editing
        ...(isEditing && {
          color: isDark ? '#ffffff' : '#000000',
          backgroundColor: isDark ? '#1f2937' : '#ffffff'
        })
      }}
      suppressContentEditableWarning={true}
      title={isEditing ? 'Press Escape to finish editing' : 'Click to edit your prompt'}
      spellCheck={false}
    />
  );
};

export const InsertBlockDialog: React.FC = () => {
  const { isOpen, dialogProps } = useDialog(DIALOG_TYPES.INSERT_BLOCK);
  const [blocks, setBlocks] = useState<Block[]>([]);
  const [loading, setLoading] = useState(false);
  const [selectedBlocks, setSelectedBlocks] = useState<Block[]>([]);
  const [search, setSearch] = useState('');
  const [activeBlockId, setActiveBlockId] = useState<number | null>(null);
  const [expandedBlocks, setExpandedBlocks] = useState<Set<number>>(new Set());
  const [selectedTypeFilter, setSelectedTypeFilter] = useState<string>('all');
  const [previewMode, setPreviewMode] = useState<'visual' | 'text'>('text');
  const [showInlineCreator, setShowInlineCreator] = useState(false);
  const [editableContent, setEditableContent] = useState('');
  const [blockContents, setBlockContents] = useState<Record<number, string>>({});
  const isDark = useThemeDetector();

  // Drag & Drop sensors
  const sensors = useSensors(
    useSensor(PointerSensor, {
      activationConstraint: {
        distance: 8,
      },
    }),
    useSensor(KeyboardSensor, {
      coordinateGetter: sortableKeyboardCoordinates,
    })
  );

  useEffect(() => {
    if (isOpen) {
      setLoading(true);
      setSelectedBlocks([]);
      setBlockContents({});
      setSearch('');
      setSelectedTypeFilter('all');
      setShowInlineCreator(false);
      blocksApi.getBlocks().then(res => {
        if (res.success) {
          setBlocks(res.data);
        } else {
          setBlocks([]);
        }
        setLoading(false);
      });
    }
  }, [isOpen]);

  // Update editable content when selected blocks or their text change
  useEffect(() => {
    const parts = selectedBlocks.map(b => {
      const text = blockContents[b.id] ?? (typeof b.content === 'string' ? b.content : b.content.en || '');
      return buildPromptPart(b.type || 'custom', text);
    });
    setEditableContent(parts.join('\n\n'));
  }, [selectedBlocks, blockContents]);

  // Generate HTML content from the editable text so that updates made by the
  // user are reflected in the preview when they exit the editor.
  const generateFullPromptHtml = useCallback(() => {
    return selectedBlocks
      .map(b => {
        const text = blockContents[b.id] ?? (typeof b.content === 'string' ? b.content : b.content.en || '');
        return buildPromptPartHtml(b.type || 'custom', text, isDark);
      })
      .join('<br><br>');
  }, [selectedBlocks, blockContents, isDark]);


  const addBlock = (block: Block) => {
    if (!selectedBlocks.find(b => b.id === block.id)) {
      setSelectedBlocks(prev => [...prev, block]);
      const content = typeof block.content === 'string' ? block.content : block.content.en || '';
      setBlockContents(prev => ({ ...prev, [block.id]: content }));
    }
  };

  const removeBlock = (block: Block) => {
    setSelectedBlocks(prev => prev.filter(b => b.id !== block.id));
    setBlockContents(prev => {
      const { [block.id]: _removed, ...rest } = prev;
      return rest;
    });
  };

  const handleEditableContentChange = (text: string) => {
    const segments = text.split(/\n{2,}/);
    setBlockContents(prev => {
      const updated = { ...prev };
      selectedBlocks.forEach((b, idx) => {
        let seg = segments[idx] ?? '';
        const prefix = buildPromptPart(b.type || 'custom', '');
        if (prefix && seg.startsWith(prefix)) {
          seg = seg.slice(prefix.length);
        }
        updated[b.id] = seg;
      });
      return updated;
    });
    setEditableContent(text);
  };

  const insertBlocks = () => {
    // Use the editable content which might have been modified by the user
    insertIntoPromptArea(editableContent);
    dialogProps.onOpenChange(false);
    toast.success('Prompt inserted successfully');
  };

  const handleCreate = () => {
    setShowInlineCreator(true);
  };

  const handleBlockCreated = (newBlock: Block) => {
    setBlocks(prev => [newBlock, ...prev]);
    addBlock(newBlock);
    setShowInlineCreator(false);
  };

  // Filter blocks based on search and type
  const filteredBlocks = blocks.filter(b => {
    const title = typeof b.title === 'string' ? b.title : b.title?.en || '';
    const content = typeof b.content === 'string' ? b.content : b.content.en || '';
    const term = search.toLowerCase();
    const matchesSearch = title.toLowerCase().includes(term) || content.toLowerCase().includes(term);
    const matchesType = selectedTypeFilter === 'all' || b.type === selectedTypeFilter;
    return matchesSearch && matchesType;
  });

  // Get unique block types for filter
  const blockTypes = Array.from(new Set(blocks.map(b => b.type || 'custom')));

  const toggleExpanded = (id: number) => {
    setExpandedBlocks(prev => {
      const newSet = new Set(prev);
      if (newSet.has(id)) {
        newSet.delete(id);
      } else {
        newSet.add(id);
      }
      return newSet;
    });
  };

  const handleDragStart = (event: DragStartEvent) => {
    setActiveBlockId(event.active.id as number);
  };

  const handleDragEnd = (event: DragEndEvent) => {
    const { active, over } = event;
    setActiveBlockId(null);

    if (over && active.id !== over.id) {
      setSelectedBlocks((blocks) => {
        const oldIndex = blocks.findIndex(b => b.id === active.id);
        const newIndex = blocks.findIndex(b => b.id === over.id);
        return arrayMove(blocks, oldIndex, newIndex);
      });
    }
  };

  const copyToClipboard = async () => {
    try {
      await navigator.clipboard.writeText(editableContent);
      toast.success('Copied to clipboard');
    } catch (err) {
      console.error('Failed to copy to clipboard:', err);
    }
  };

  if (!isOpen) return null;

  return (
    <BaseDialog
      open={isOpen}
      onOpenChange={dialogProps.onOpenChange}
      title="Build Your Prompt"
      description="Select and arrange blocks to create your perfect prompt"
      className="jd-max-w-7xl jd-max-h-[90vh]"
    >
      <div className="jd-flex jd-h-full jd-gap-6">
        {/* Left Panel - Block Library */}
        <div className="jd-flex-1 jd-flex jd-flex-col jd-min-w-0">
          <div className="jd-space-y-4 jd-mb-4">
            {/* Search */}
            <div className="jd-relative">
              <Search className="jd-absolute jd-left-3 jd-top-1/2 jd-transform jd--translate-y-1/2 jd-h-4 jd-w-4 jd-text-muted-foreground" />
              <Input
                value={search}
                onChange={e => setSearch(e.target.value)}
                placeholder="Search blocks..."
                className="jd-pl-9"
                onKeyDown={(e) => e.stopPropagation()}
                onKeyPress={(e) => e.stopPropagation()}
                onKeyUp={(e) => e.stopPropagation()}
              />
            </div>

            {/* Quick Filters */}
            <div className="jd-space-y-2">
              <div className="jd-flex jd-items-center jd-gap-2 jd-text-xs jd-font-medium jd-text-muted-foreground">
                <Filter className="jd-h-3 jd-w-3" />
                Quick Filters
              </div>
              <div className="jd-flex jd-flex-wrap jd-gap-1">
                <Button
                  size="sm"
                  variant={selectedTypeFilter === 'all' ? 'default' : 'outline'}
                  onClick={() => setSelectedTypeFilter('all')}
                  className="jd-h-6 jd-text-xs jd-px-2"
                >
                  All
                </Button>
                {METADATA_FILTERS.map(filter => (
                  <Button
                    key={filter.type}
                    size="sm"
                    variant={selectedTypeFilter === filter.type ? 'default' : 'outline'}
                    onClick={() => setSelectedTypeFilter(filter.type)}
                    className="jd-h-6 jd-text-xs jd-px-2"
                  >
                    <span className="jd-mr-1">{filter.icon}</span>
                    {filter.label}
                  </Button>
                ))}
              </div>
            </div>

            {/* Stats */}
            <div className="jd-flex jd-items-center jd-gap-4 jd-text-sm jd-text-muted-foreground">
              <span>{filteredBlocks.length} blocks available</span>
              {selectedBlocks.length > 0 && (
                <>
                  <ArrowRight className="jd-h-3 jd-w-3" />
                  <span className="jd-text-primary">{selectedBlocks.length} selected</span>
                </>
              )}
            </div>
          </div>

          {/* Inline Block Creator */}
          {showInlineCreator && (
            <div className="jd-mb-4">
              <InlineBlockCreator
                onBlockCreated={handleBlockCreated}
                onCancel={() => setShowInlineCreator(false)}
              />
            </div>
          )}

          {/* Available Blocks */}
          <ScrollArea className="jd-h-[65vh]">
            <div className="jd-space-y-3 jd-pr-4">
              {loading ? (
                <LoadingSpinner size="sm" message="Loading blocks..." />
              ) : filteredBlocks.length === 0 ? (
                <EmptyMessage>
                  {search ? `No blocks found for "${search}"` : 'No blocks available'}
                </EmptyMessage>
              ) : (
                filteredBlocks.map(block => (
                  <AvailableBlockCard
                    key={block.id}
                    block={block}
                    isDark={isDark}
                    onAdd={addBlock}
                    isSelected={!!selectedBlocks.find(b => b.id === block.id)}
                    onRemove={removeBlock}
                  />
                ))
              )}
            </div>
          </ScrollArea>
        </div>

        {/* Right Panel - Selected Blocks & Preview */}
        <div className="jd-w-1/2 jd-flex jd-flex-col jd-max-h-full">
          <div className="jd-flex jd-items-center jd-justify-start jd-mb-4 jd-flex-shrink-0">
            <h3 className="jd-text-sm jd-font-medium">Selected Blocks</h3>
            <div className="jd-flex jd-items-center jd-gap-2 jd-ml-auto">
              <Button
                variant="outline"
                size="sm"
                onClick={copyToClipboard}
                disabled={selectedBlocks.length === 0}
              >
                <Copy className="jd-h-4 jd-w-4 jd-mr-1" />
                Copy
              </Button>
              <div className="jd-flex jd-bg-muted jd-rounded-md jd-p-1">
                <button
                  onClick={() => setPreviewMode('text')}
                  className={cn(
                    'jd-px-2 jd-py-1 jd-text-xs jd-rounded jd-transition-colors',
                    previewMode === 'text' ? 'jd-bg-background jd-shadow-sm' : 'jd-hover:bg-background/50'
                  )}
                >
                  <Code className="jd-h-3 jd-w-3" />
                </button>
                <button
                  onClick={() => setPreviewMode('visual')}
                  className={cn(
                    'jd-px-2 jd-py-1 jd-text-xs jd-rounded jd-transition-colors',
                    previewMode === 'visual' ? 'jd-bg-background jd-shadow-sm' : 'jd-hover:bg-background/50'
                  )}
                >
                  <Eye className="jd-h-3 jd-w-3" />
                </button>
              </div>
            </div>
          </div>

          {selectedBlocks.length === 0 ? (
            <div className="jd-flex jd-items-center jd-justify-center jd-border-2 jd-border-dashed jd-border-muted jd-rounded-lg jd-py-16 jd-flex-1">
              <div className="jd-text-center jd-text-muted-foreground">
                <Eye className="jd-h-8 jd-w-8 jd-mx-auto jd-mb-2 jd-opacity-50" />
                <p className="jd-text-sm jd-mb-1">Select blocks to build your prompt</p>
                <p className="jd-text-xs">Preview will appear here with colors and placeholder highlighting</p>
              </div>
            </div>
          ) : (
            <div className="jd-flex-1 jd-min-h-0 jd-border-t jd-pt-4">
              {previewMode === 'visual' ? (
                <ScrollArea className="jd-h-[65vh]">
                  <DndContext 
                    sensors={sensors}
                    collisionDetection={closestCenter}
                    onDragStart={handleDragStart}
                    onDragEnd={handleDragEnd}
                  >
                    <SortableContext items={selectedBlocks.map(b => b.id)} strategy={verticalListSortingStrategy}>
                      <div className="jd-space-y-3 jd-pr-4">
                        {selectedBlocks.map(block => (
                          <SortableSelectedBlock
                            key={block.id}
                            block={block}
                            isDark={isDark}
                            onRemove={(id) => {
                              const blockToRemove = selectedBlocks.find(b => b.id === id);
                              if (blockToRemove) removeBlock(blockToRemove);
                            }}
                            isExpanded={expandedBlocks.has(block.id)}
                            onToggleExpand={toggleExpanded}
                          />
                        ))}
                      </div>
                    </SortableContext>
                  </DndContext>
                </ScrollArea>
              ) : (
                <div className="jd-h-full jd-flex jd-flex-col">
                  <div className="jd-flex jd-items-center jd-justify-between jd-mb-2">
                    <span className="jd-text-xs jd-text-muted-foreground">
                      Click to edit your prompt preview
                    </span>
                    <div className="jd-flex jd-items-center jd-gap-1 jd-text-xs jd-text-muted-foreground">
                      <span className="jd-inline-block jd-w-3 jd-h-3 jd-bg-yellow-300 jd-rounded"></span>
                      <span>Placeholders</span>
                    </div>
                  </div>
                  <ScrollArea className="jd-h-full">
                    <div className="jd-pr-4">
                      <EditablePreview
                        content={editableContent}
                        htmlContent={generateFullPromptHtml()}
                        onChange={handleEditableContentChange}
                        isDark={isDark}
                      />
                    </div>
                  </ScrollArea>
                </div>
              )}
            </div>
          )}

          {/* Action Buttons */}
          <div className="jd-flex jd-justify-between jd-pt-4 jd-border-t jd-mt-4 jd-flex-shrink-0">
            <Button variant="outline" onClick={() => dialogProps.onOpenChange(false)}>
              Cancel
            </Button>
            <div className="jd-flex jd-gap-2">
              <Button variant="secondary" onClick={handleCreate}>
                <Plus className="jd-h-4 jd-w-4 jd-mr-1" />
                Create Block
              </Button>
              <Button 
                disabled={selectedBlocks.length === 0} 
                onClick={insertBlocks}
                className="jd-bg-gradient-to-r jd-from-blue-600 jd-to-purple-600 hover:jd-from-blue-700 hover:jd-to-purple-700"
              >
                <Sparkles className="jd-h-4 jd-w-4 jd-mr-1" />
                Insert Prompt ({selectedBlocks.length})
              </Button>
            </div>
          </div>
        </div>
      </div>
    </BaseDialog>
  );
};