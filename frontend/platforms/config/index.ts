// src/platforms/config/index.ts
import { PlatformConfig } from './base';
import { chatGptConfig } from './chatgpt.config';
import { claudeConfig } from './claude.config';
import { mistralConfig } from './mistral.config';
import { copilotConfig } from './copilot.config';

export const platformConfigs: PlatformConfig[] = [
  chatGptConfig,
  claudeConfig,
  mistralConfig,
  copilotConfig
];

export { chatGptConfig, claudeConfig, mistralConfig, copilotConfig };
export * from './base';

export function getConfigByHostname(hostname: string): PlatformConfig | null {
  return platformConfigs.find(config => 
    config.hostnames.some(h => hostname.includes(h))
  ) || null;
}

export function getConfigByName(name: string): PlatformConfig | null {
  return platformConfigs.find(config => config.name === name) || null;
}