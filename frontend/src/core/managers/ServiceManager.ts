// src/core/managers/ServiceManager.ts
import { BaseService } from '@/services/BaseService';
import { debug } from '@/core/config';
import { errorReporter } from '@/core/errors/ErrorReporter';
import { AppError, ErrorCode } from '@/core/errors/AppError';

/**
 * Service dependency graph type
 */
type ServiceDependencyGraph = Map<string, string[]>;

/**
 * Centralized service management with dependency management
 */
export class ServiceManager {
  private services: Map<string, BaseService> = new Map();
  private dependencies: ServiceDependencyGraph = new Map();
  private initialized: Set<string> = new Set();
  private isInitializing: boolean = false;
  
  /**
   * Register a service with optional dependencies
   */
  public registerService(name: string, service: BaseService, dependencies: string[] = []): void {
    if (this.services.has(name)) {
      debug(`Service '${name}' is already registered. Overwriting.`);
    }
    this.services.set(name, service);
    this.dependencies.set(name, dependencies);
  }
  
  /**
   * Get a registered service
   */
  public getService<T extends BaseService>(name: string): T | undefined {
    return this.services.get(name) as T | undefined;
  }
  
  /**
   * Get all registered services
   */
  public getAllServices(): Array<[string, BaseService]> {
    return Array.from(this.services.entries());
  }
  
  /**
   * Check if a service is registered
   */
  public hasService(name: string): boolean {
    return this.services.has(name);
  }
  
  /**
   * Check if a service is initialized
   */
  public isServiceInitialized(name: string): boolean {
    return this.initialized.has(name);
  }
  
  /**
   * Initialize all registered services with dependency resolution
   */
  public async initializeAll(): Promise<boolean> {
    if (this.isInitializing) {
      debug('Services are already being initialized');
      return false;
    }
    
    this.isInitializing = true;
    
    try {
      // Sort services by dependency order
      const initOrder = this.getInitializationOrder();
      
      debug('Initializing services in order:', initOrder);
      
      // Initialize services in order
      for (const serviceName of initOrder) {
        await this.initializeService(serviceName);
      }
      
      debug('All services initialized successfully');
      this.isInitializing = false;
      return true;
    } catch (error) {
      errorReporter.captureError(
        new AppError('Failed to initialize services', ErrorCode.EXTENSION_ERROR, error)
      );
      this.isInitializing = false;
      return false;
    }
  }
  
  /**
   * Initialize a specific service and its dependencies
   */
  private async initializeService(serviceName: string): Promise<void> {
    // Skip if already initialized
    if (this.initialized.has(serviceName)) {
      return;
    }
    
    const service = this.services.get(serviceName);
    
    if (!service) {
      debug(`Service '${serviceName}' not found, skipping initialization`);
      return;
    }
    
    // First initialize dependencies
    const dependencies = this.dependencies.get(serviceName) || [];
    for (const dependency of dependencies) {
      await this.initializeService(dependency);
    }
    
    debug(`Initializing service: ${serviceName}`);
    try {
      await service.initialize();
      this.initialized.add(serviceName);
      debug(`Service initialized: ${serviceName}`);
    } catch (error) {
      debug(`Error initializing service '${serviceName}':`, error);
      throw new AppError(
        `Failed to initialize service '${serviceName}'`,
        ErrorCode.EXTENSION_ERROR,
        error
      );
    }
  }
  
  /**
   * Clean up all services in reverse initialization order
   */
  public cleanupAll(): void {
    debug('Cleaning up all services');
    
    // Get initialization order and reverse it for cleanup
    const cleanupOrder = [...this.getInitializationOrder()].reverse();
    
    for (const serviceName of cleanupOrder) {
      this.cleanupService(serviceName);
    }
    
    this.initialized.clear();
    debug('All services cleaned up');
  }
  
  /**
   * Clean up a specific service
   */
  private cleanupService(serviceName: string): void {
    // Skip if not initialized
    if (!this.initialized.has(serviceName)) {
      return;
    }
    
    const service = this.services.get(serviceName);
    
    if (!service) {
      return;
    }
    
    debug(`Cleaning up service: ${serviceName}`);
    try {
      service.cleanup();
      this.initialized.delete(serviceName);
    } catch (error) {
      errorReporter.captureError(
        new AppError(`Error cleaning up service '${serviceName}'`, ErrorCode.EXTENSION_ERROR, error)
      );
    }
  }
  
  /**
   * Get order for initializing services based on dependencies
   */
  private getInitializationOrder(): string[] {
    const result: string[] = [];
    const visited = new Set<string>();
    const temp = new Set<string>();
    
    const visit = (name: string) => {
      // Skip if already in result
      if (visited.has(name)) return;
      
      // Check for circular dependency
      if (temp.has(name)) {
        throw new Error(`Circular dependency detected for service: ${name}`);
      }
      
      // Skip if service doesn't exist
      if (!this.services.has(name)) {
        debug(`Dependency '${name}' not found in registered services, skipping`);
        return;
      }
      
      // Mark as being visited
      temp.add(name);
      
      // Visit dependencies first
      const dependencies = this.dependencies.get(name) || [];
      for (const dep of dependencies) {
        visit(dep);
      }
      
      // Mark as visited and add to result
      temp.delete(name);
      visited.add(name);
      result.push(name);
    };
    
    // Visit all services
    for (const name of this.services.keys()) {
      visit(name);
    }
    
    return result;
  }
  
  /**
   * Clear all services and state
   * Primarily used for testing
   */
  public clear(): void {
    this.services.clear();
    this.dependencies.clear();
    this.initialized.clear();
    this.isInitializing = false;
  }
}

// Export a singleton instance
export const serviceManager = new ServiceManager();