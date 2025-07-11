// src/types/prompts/metadata.ts - Enhanced version
import { BlockType } from './blocks';
import { getMessage } from '@/core/utils/i18n';

// Base metadata types
export type SingleMetadataType = 'role' | 'context' | 'goal' | 'audience' | 'tone_style' | 'output_format';
export type MultipleMetadataType = 'constraint' | 'example';
export type MetadataType = SingleMetadataType | MultipleMetadataType;

// Metadata item for multiple types (constraint, example)
export interface MetadataItem {
  id: string; // Unique identifier for the item
  blockId?: number; // Reference to a saved block
  value: string; // Custom value or content from block
}

// Enhanced metadata structure
export interface PromptMetadata {
  // Single value metadata
  role?: number;
  context?: number;
  goal?: number;
  audience?: number;
  tone_style?: number;
  output_format?: number;
  
  // Multiple value metadata (arrays)
  constraint?: MetadataItem[];
  example?: MetadataItem[];
  
  // Custom values for single metadata types
  values?: Record<SingleMetadataType, string>;
}

// Configuration for each metadata type
export interface MetadataConfig {
  label: string;
  description: string;
  blockType: BlockType;
  placeholder: string;
  allowMultiple: boolean; // New field to indicate if multiple values are allowed
}

export const METADATA_CONFIGS: Record<MetadataType, MetadataConfig> = {
  role: {
    label: getMessage('blockRoleLabel', undefined, 'Role'),
    description: 'Define the AI\'s role and expertise',
    blockType: 'role',
    placeholder: 'e.g., You are an expert software developer...',
    allowMultiple: false
  },
  context: {
    label: getMessage('blockContextLabel', undefined, 'Context'),
    description: 'Provide background information',
    blockType: 'context',
    placeholder: 'e.g., The user is working on a React project...',
    allowMultiple: false
  },
  goal: {
    label: getMessage('blockGoalLabel', undefined, 'Goal'),
    description: 'Specify the desired outcome',
    blockType: 'goal',
    placeholder: 'e.g., Help improve code quality and performance...',
    allowMultiple: false
  },
  audience: {
    label: getMessage('blockAudienceLabel', undefined, 'Audience'),
    description: 'Define the target audience',
    blockType: 'audience',
    placeholder: 'e.g., Intermediate developers familiar with React...',
    allowMultiple: false
  },
  tone_style: {
    label: getMessage('blockToneStyleLabel', undefined, 'Tone & Style'),
    description: 'Set the communication style',
    blockType: 'tone_style',
    placeholder: 'e.g., Professional but friendly, use clear example...',
    allowMultiple: false
  },
  output_format: {
    label: getMessage('blockOutputFormatLabel', undefined, 'Output Format'),
    description: 'Specify how the response should be structured',
    blockType: 'output_format',
    placeholder: 'e.g., Provide code example with explanations...',
    allowMultiple: false
  },
  constraint: {
    label: getMessage('blockConstraintLabel', undefined, 'Constraint'),
    description: 'Add limitations or requirements',
    blockType: 'constraint',
    placeholder: 'e.g., Keep responses under 500 words...',
    allowMultiple: true
  },
  example: {
    label: getMessage('blockExampleLabel', undefined, 'Example'),
    description: 'Provide example to guide the response',
    blockType: 'example',
    placeholder: 'e.g., Good: const data = await fetch()...',
    allowMultiple: true
  }
};

// Primary metadata (always visible)
export const PRIMARY_METADATA: SingleMetadataType[] = ['role', 'context', 'goal'];

// Secondary metadata (can be added as needed)
export const SECONDARY_METADATA: (SingleMetadataType | MultipleMetadataType)[] = [
  'audience', 'tone_style', 'output_format', 'constraint', 'example'
];

// All metadata types
export const ALL_METADATA_TYPES: MetadataType[] = [...PRIMARY_METADATA, ...SECONDARY_METADATA];

// Default metadata state
export const DEFAULT_METADATA: PromptMetadata = {
  constraint: [],
  example: [],
  values: {} as Record<SingleMetadataType, string>
};

// Helper functions
export function isMultipleMetadataType(type: MetadataType): type is MultipleMetadataType {
  return ['constraint', 'example'].includes(type);
}

export function isSingleMetadataType(type: MetadataType): type is SingleMetadataType {
  return !isMultipleMetadataType(type);
}

// Generate unique ID for metadata items
export function generateMetadataItemId(): string {
  return `metadata-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
}