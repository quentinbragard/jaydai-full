
// src/utils/prompts/metadataUtils.ts
import {
  PromptMetadata,
  DEFAULT_METADATA,
  MetadataType,
  SingleMetadataType,
  MultipleMetadataType,
  MetadataItem,
  PRIMARY_METADATA,
  SECONDARY_METADATA,
  isMultipleMetadataType,
  isSingleMetadataType,
  generateMetadataItemId
} from '@/types/prompts/metadata';

// Map singular metadata types to their property keys on PromptMetadata
const MULTI_TYPE_KEY_MAP: Record<MultipleMetadataType, 'constraint' | 'example'> = {
  constraint: 'constraint',
  example: 'example'
};

// ============================================================================
// CORE METADATA OPERATIONS
// ============================================================================

/**
 * Create a fresh metadata instance
 */
export function createMetadata(initial?: Partial<PromptMetadata>): PromptMetadata {
  return {
    ...DEFAULT_METADATA,
    values: {},
    ...initial
  };
}

/**
 * Deep clone metadata to avoid mutations
 */
export function cloneMetadata(metadata: PromptMetadata): PromptMetadata {
  return {
    ...metadata,
    values: { ...metadata.values },
    constraint: metadata.constraint?.map(item => ({ ...item })),
    example: metadata.example?.map(item => ({ ...item }))
  };
}

// ============================================================================
// SINGLE METADATA OPERATIONS
// ============================================================================

/**
 * Update a single metadata type (role, context, goal, etc.)
 */
export function updateSingleMetadata(
  metadata: PromptMetadata,
  type: SingleMetadataType,
  blockId: number,
  customValue?: string
): PromptMetadata {
  const updated = cloneMetadata(metadata);
  
  // Set the block ID
  (updated as any)[type] = blockId;
  
  // Clear custom value when selecting a block, or set it when provided
  if (!updated.values) updated.values = {};
  updated.values[type] = blockId === 0 ? (customValue || '') : '';
  
  return updated;
}

/**
 * Update custom value for a single metadata type
 */
export function updateCustomValue(
  metadata: PromptMetadata,
  type: SingleMetadataType,
  value: string
): PromptMetadata {
  const updated = cloneMetadata(metadata);
  
  // Clear block ID when entering custom value, set custom value
  (updated as any)[type] = value.trim() ? 0 : (metadata[type] || 0);
  if (!updated.values) updated.values = {};
  updated.values[type] = value;
  
  return updated;
}

// ============================================================================
// MULTIPLE METADATA OPERATIONS
// ============================================================================

/**
 * Add a new item to multiple metadata (constraint, example)
 */
export function addMetadataItem(
  metadata: PromptMetadata,
  type: MultipleMetadataType,
  item?: Partial<MetadataItem>
): PromptMetadata {
  const updated = cloneMetadata(metadata);
  
  const newItem: MetadataItem = {
    id: generateMetadataItemId(),
    value: '',
    blockId: undefined,
    ...item
  };
  
  const key = MULTI_TYPE_KEY_MAP[type];
  const currentItems = (updated as any)[key] || [];
  // Insert the new item at the beginning so that recently added blocks
  // always appear before the "add new block" button in the UI.
  (updated as any)[key] = [newItem, ...currentItems];
  
  return updated;
}

/**
 * Remove an item from multiple metadata
 */
export function removeMetadataItem(
  metadata: PromptMetadata,
  type: MultipleMetadataType,
  itemId: string
): PromptMetadata {
  const updated = cloneMetadata(metadata);
  const key = MULTI_TYPE_KEY_MAP[type];
  const currentItems = (updated as any)[key] || [];
  (updated as any)[key] = currentItems.filter((item: MetadataItem) => item.id !== itemId);
  return updated;
}

/**
 * Update an item in multiple metadata
 */
export function updateMetadataItem(
  metadata: PromptMetadata,
  type: MultipleMetadataType,
  itemId: string,
  updates: Partial<MetadataItem>
): PromptMetadata {
  const updated = cloneMetadata(metadata);
  const key = MULTI_TYPE_KEY_MAP[type];
  const currentItems: MetadataItem[] = (updated as any)[key] || [];

  (updated as any)[key] = currentItems.map(item =>
    item.id === itemId ? { ...item, ...updates } : item
  );

  return updated;
}

/**
 * Reorder items in multiple metadata
 */
export function reorderMetadataItems(
  metadata: PromptMetadata,
  type: MultipleMetadataType,
  newItems: MetadataItem[]
): PromptMetadata {
  const updated = cloneMetadata(metadata);
  const key = MULTI_TYPE_KEY_MAP[type];
  (updated as any)[key] = newItems.map(item => ({ ...item }));
  return updated;
}

// ============================================================================
// SECONDARY METADATA MANAGEMENT
// ============================================================================

/**
 * Add a secondary metadata type
 */
export function addSecondaryMetadata(
  metadata: PromptMetadata,
  type: MetadataType
): PromptMetadata {
  const updated = cloneMetadata(metadata);
  
  if (isMultipleMetadataType(type)) {
    // For multiple types, add an empty item
    return addMetadataItem(updated, type as MultipleMetadataType);
  } else {
    // For single types, initialize with empty values
    const singleType = type as SingleMetadataType;
    (updated as any)[singleType] = 0;
    if (!updated.values) updated.values = {};
    updated.values[singleType] = '';
    return updated;
  }
}

/**
 * Remove a secondary metadata type
 */
export function removeSecondaryMetadata(
  metadata: PromptMetadata,
  type: MetadataType
): PromptMetadata {
  const updated = cloneMetadata(metadata);
  
  if (isMultipleMetadataType(type)) {
    const multiType = type as MultipleMetadataType;
    const key = MULTI_TYPE_KEY_MAP[multiType];
    delete (updated as any)[key];
  } else {
    const singleType = type as SingleMetadataType;
    delete (updated as any)[singleType];
    if (updated.values) {
      delete updated.values[singleType];
    }
  }
  
  return updated;
}

// ============================================================================
// METADATA ANALYSIS
// ============================================================================

/**
 * Get active secondary metadata types - includes types that have been added to the metadata
 * FIXED: Now correctly shows added metadata (even if empty) but not uninitialized metadata
 */
export function getActiveSecondaryMetadata(metadata: PromptMetadata): Set<MetadataType> {
  const activeSet = new Set<MetadataType>();
  
  SECONDARY_METADATA.forEach(type => {
    if (isMultipleMetadataType(type)) {
      // For multiple metadata types (constraint, example)
      const key = MULTI_TYPE_KEY_MAP[type];
      const items = (metadata as any)[key];

      // Include only if the array contains at least one item
      if (items && Array.isArray(items) && items.length > 0) {
        activeSet.add(type);
      }
    } else {
      // For single metadata types (audience, output_format, tone_style)
      const hasField = Object.prototype.hasOwnProperty.call(metadata, type);
      const hasCustom =
        metadata.values && Object.prototype.hasOwnProperty.call(metadata.values, type as SingleMetadataType);

      // Include if the field exists (even with blockId 0) or a custom value is present
      if (hasField || hasCustom) {
        activeSet.add(type);
      }
    }
  });
  
  return activeSet;
}

/**
 * Extract custom values for all single metadata types
 */
export function extractCustomValues(metadata: PromptMetadata): Record<SingleMetadataType, string> {
  const values: Record<SingleMetadataType, string> = {} as Record<SingleMetadataType, string>;
  
  [...PRIMARY_METADATA, ...SECONDARY_METADATA].forEach((type) => {
    if (!isMultipleMetadataType(type)) {
      values[type as SingleMetadataType] = metadata.values?.[type as SingleMetadataType] || '';
    }
  });
  
  return values;
}

/**
 * Get the first metadata type that contains a value. Useful for
 * automatically expanding metadata sections when editing templates.
 */
export function getFirstActiveMetadataType(metadata: PromptMetadata): MetadataType | null {
  const allTypes: MetadataType[] = [...PRIMARY_METADATA, ...SECONDARY_METADATA];

  for (const type of allTypes) {
    if (isMultipleMetadataType(type)) {
      const key = MULTI_TYPE_KEY_MAP[type];
      if ((metadata as any)[key] && (metadata as any)[key].length > 0) {
        return type;
      }
    } else {
      const singleType = type as SingleMetadataType;
      const blockId = metadata[singleType];
      const customValue = metadata.values?.[singleType];
      if ((blockId && blockId !== 0) || (customValue && customValue.trim())) {
        return type;
      }
    }
  }

  return null;
}

/**
 * Get metadata types that currently contain meaningful values.
 */
export function getFilledMetadataTypes(metadata: PromptMetadata): Set<MetadataType> {
  const filled = new Set<MetadataType>();

  [...PRIMARY_METADATA, ...SECONDARY_METADATA].forEach(type => {
    if (isMultipleMetadataType(type)) {
      const key = MULTI_TYPE_KEY_MAP[type];
      const items = (metadata as any)[key];
      if (Array.isArray(items) && items.some((item: MetadataItem) => item.value && item.value.trim())) {
        filled.add(type);
      }
    } else {
      const singleType = type as SingleMetadataType;
      const blockId = metadata[singleType];
      const customValue = metadata.values?.[singleType];
      if ((blockId && blockId !== 0) || (customValue && customValue.trim())) {
        filled.add(type);
      }
    }
  });

  return filled;
}

/**
 * Validate metadata completeness
 */
export function validateMetadata(metadata: PromptMetadata): {
  isValid: boolean;
  errors: string[];
  warnings: string[];
} {
  const errors: string[] = [];
  const warnings: string[] = [];

  const primaryCount = PRIMARY_METADATA.reduce((count, type) => {
    const blockId = metadata[type as SingleMetadataType];
    const custom = metadata.values?.[type as SingleMetadataType];
    return (blockId && blockId !== 0) || (custom && custom.trim()) ? count + 1 : count;
  }, 0);

  if (primaryCount === 0) {
    warnings.push('noPrimary');
  } else if (primaryCount < PRIMARY_METADATA.length) {
    warnings.push('missingPrimary');
  }
  
  // Check for empty multiple metadata items
  if (metadata.constraint?.some(item => !item.value.trim())) {
    warnings.push('Some constraint are empty');
  }
  
  if (metadata.example?.some(item => !item.value.trim())) {
    warnings.push('Some example are empty');
  }
  
  return {
    isValid: errors.length === 0,
    errors,
    warnings
  };
}

/**
 * Count total metadata items
 */
export function countMetadataItems(metadata: PromptMetadata): number {
  let count = 0;
  
  // Count single metadata with values
  [...PRIMARY_METADATA, ...SECONDARY_METADATA].forEach(type => {
    if (!isMultipleMetadataType(type)) {
      const singleType = type as SingleMetadataType;
      const blockId = metadata[singleType];
      const customValue = metadata.values?.[singleType];
      if ((blockId && blockId !== 0) || (customValue && customValue.trim())) {
        count++;
      }
    }
  });
  
  // Count multiple metadata items
  if (metadata.constraint) {
    count += metadata.constraint.filter(item => item.value.trim()).length;
  }
  
  if (metadata.example) {
    count += metadata.example.filter(item => item.value.trim()).length;
  }
  
  return count;
}

/**
 * Create a list of metadata types that contain values. Multiple metadata
 * types (like `example`) will appear as many times as there are filled items.
 */
export function listFilledMetadataFields(metadata: PromptMetadata): string[] {
  const fields: string[] = [];

  [...PRIMARY_METADATA, ...SECONDARY_METADATA].forEach(type => {
    if (isMultipleMetadataType(type)) {
      const key = MULTI_TYPE_KEY_MAP[type];
      const items = (metadata as any)[key];
      if (Array.isArray(items)) {
        items.forEach((item: MetadataItem) => {
          if (item.value && item.value.trim()) {
            fields.push(type);
          }
        });
      }
    } else {
      const singleType = type as SingleMetadataType;
      const blockId = metadata[singleType];
      const customValue = metadata.values?.[singleType];
      if ((blockId && blockId !== 0) || (customValue && customValue.trim())) {
        fields.push(type);
      }
    }
  });

  return fields;
}

// ============================================================================
// METADATA CONVERSION
// ============================================================================

/**
 * Convert metadata to block mapping for backend storage
 */
export function metadataToBlockMapping(metadata: PromptMetadata): Record<string, number | number[]> {
  const mapping: Record<string, number | number[]> = {};
  
  // Handle single metadata types
  [...PRIMARY_METADATA, ...SECONDARY_METADATA].forEach(type => {
    if (!isMultipleMetadataType(type)) {
      const singleType = type as SingleMetadataType;
      const blockId = metadata[singleType];
      if (blockId && blockId !== 0) {
        mapping[singleType] = blockId;
      }
    }
  });
  
  // Handle multiple metadata types
  if (metadata.constraint && metadata.constraint.length > 0) {
    const constraintBlockIds = metadata.constraint
      .map(c => c.blockId)
      .filter((id): id is number => typeof id === 'number' && id !== 0);
    if (constraintBlockIds.length > 0) {
      mapping.constraint = constraintBlockIds;
    }
  }

  if (metadata.example && metadata.example.length > 0) {
    const exampleBlockIds = metadata.example
      .map(e => e.blockId)
      .filter((id): id is number => typeof id === 'number' && id !== 0);
    if (exampleBlockIds.length > 0) {
      mapping.example = exampleBlockIds;
    }
  }
  
  return mapping;
}

/**
 * Convert block mapping back to metadata IDs (for loading templates)
 */
export function blockMappingToMetadata(
  mapping: Record<string, number | number[]>
): PromptMetadata {
  const metadata: PromptMetadata = createMetadata();
  
  for (const [type, value] of Object.entries(mapping)) {
    if (typeof value === 'number') {
      if (value && value > 0) {
        const key = type;
        (metadata as any)[key] = value;
      }
    } else if (Array.isArray(value)) {
      const items = value
        .filter(id => id && typeof id === 'number' && id > 0)
        .map(id => ({
          id: generateMetadataItemId(),
          blockId: id,
          value: ''
        }));
      if (items.length > 0) {
        const key = type;
        (metadata as any)[key] = items;
      }
    }
  }
  
  return metadata;
}

/**
 * Apply content overrides keyed by block ID to the metadata structure.
 * This keeps the original block references while updating the associated
 * custom values so modified text persists across editors.
 */
export function applyBlockOverridesToMetadata(
  metadata: PromptMetadata,
  overrides: Record<number, string>
): PromptMetadata {
  const updated = cloneMetadata(metadata);

  const singleTypes: SingleMetadataType[] = [
    'role',
    'context',
    'goal',
    'audience',
    'output_format',
    'tone_style'
  ];

  singleTypes.forEach(type => {
    const blockId = metadata[type];
    if (blockId && overrides.hasOwnProperty(blockId)) {
      if (!updated.values) updated.values = {} as any;
      updated.values[type] = overrides[blockId];
    }
  });

  if (metadata.constraint) {
    updated.constraint = metadata.constraint.map(item => {
      if (item.blockId && overrides.hasOwnProperty(item.blockId)) {
        return { ...item, value: overrides[item.blockId] };
      }
      return item;
    });
  }

  if (metadata.example) {
    updated.example = metadata.example.map(item => {
      if (item.blockId && overrides.hasOwnProperty(item.blockId)) {
        return { ...item, value: overrides[item.blockId] };
      }
      return item;
    });
  }

  return updated;
}

// Enhanced function to parse template metadata into proper format
export function parseTemplateMetadata(rawMetadata: any): PromptMetadata {
  if (!rawMetadata || typeof rawMetadata !== 'object') {
    return createMetadata();
  }

  const parsed: PromptMetadata = createMetadata();

  // Handle single metadata types (role, context, goal, etc.)
  const singleTypes: SingleMetadataType[] = ['role', 'context', 'goal', 'audience', 'output_format', 'tone_style'];
  
  singleTypes.forEach(type => {
    if (rawMetadata[type]) {
      // Handle both direct ID assignment and object format
      if (typeof rawMetadata[type] === 'number') {
        parsed[type] = rawMetadata[type];
      } else if (typeof rawMetadata[type] === 'object' && rawMetadata[type].blockId) {
        parsed[type] = rawMetadata[type].blockId;
      } else if (typeof rawMetadata[type] === 'string') {
        // Handle custom values
        parsed.values = parsed.values || {};
        parsed.values[type] = rawMetadata[type];
        parsed[type] = 0; // No block selected, custom value
      }
    }
  });

  // Handle multiple metadata types (constraint, example)
  const multipleTypes: MultipleMetadataType[] = ['constraint', 'example'];
  
  multipleTypes.forEach(type => {
    if (rawMetadata[type] && Array.isArray(rawMetadata[type])) {
      parsed[type] = rawMetadata[type].map((item: any, index: number) => {
        // Ensure each item has required structure
        const metadataItem: MetadataItem = {
          id: item.id || `${type}_${Date.now()}_${index}`,
          value: item.value || '',
          blockId: item.blockId || undefined
        };
        
        return metadataItem;
      });
    }
  });

  // Handle values object for custom inputs
  if (rawMetadata.values && typeof rawMetadata.values === 'object') {
    parsed.values = { ...parsed.values, ...rawMetadata.values };
  }

  
  return parsed;
}