import React, { Component, ErrorInfo, ReactNode } from 'react';
import { AlertTriangle } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { errorReporter } from '@/core/errors/ErrorReporter';
import { AppError, ErrorCode } from '@/core/errors/AppError';

interface Props {
  children: ReactNode;
  fallback?: ReactNode | ((error: Error, reset: () => void) => ReactNode);
  onError?: (error: Error, errorInfo: ErrorInfo) => void;
}

interface State {
  hasError: boolean;
  error: Error | null;
}

/**
 * Generic error boundary component to catch and handle React errors
 * Includes ability to render a fallback UI and attempt recovery
 */
export class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {
      hasError: false,
      error: null
    };
  }

  static getDerivedStateFromError(error: Error): State {
    // Update state so the next render will show the fallback UI
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo): void {
    // Report the error
    errorReporter.captureError(
      new AppError(error.message, ErrorCode.COMPONENT_ERROR, error, {
        componentStack: errorInfo.componentStack
      })
    );
    
    // Call onError callback if provided
    if (this.props.onError) {
      this.props.onError(error, errorInfo);
    }
  }

  // Reset the error boundary state
  resetErrorBoundary = (): void => {
    this.setState({
      hasError: false,
      error: null
    });
  };

  render(): ReactNode {
    if (this.state.hasError) {
      // If a custom fallback is provided, use it
      if (this.props.fallback) {
        if (typeof this.props.fallback === 'function' && this.state.error) {
          return this.props.fallback(this.state.error, this.resetErrorBoundary);
        }
        return this.props.fallback as ReactNode;
      }

      // Default fallback UI
      return (
        <div className="jd-p-4 jd-bg-red-900/20 jd-border jd-border-red-700/30 jd-rounded-md jd-text-center">
          <AlertTriangle className="jd-h-10 jd-w-10 jd-text-red-500 jd-mx-auto jd-mb-2" />
          <h3 className="jd-text-lg jd-font-medium jd-text-red-200 jd-mb-2">
            Something went wrong
          </h3>
          <p className="jd-text-sm jd-text-red-300 jd-mb-4">
            {this.state.error?.message || 'An unexpected error occurred'}
          </p>
          <Button 
            variant="outline" 
            className="jd-border-red-700 jd-text-red-200 hover:jd-bg-red-900/30"
            onClick={this.resetErrorBoundary}
          >
            Try Again
          </Button>
        </div>
      );
    }

    return this.props.children;
  }
}

// Function component wrapper for easier use with hooks
export function withErrorBoundary<P extends JSX.IntrinsicAttributes>(
  Component: React.ComponentType<P>,
  errorBoundaryProps: Omit<Props, 'children'>
): React.FC<P> {
  const WithErrorBoundary: React.FC<P> = (props) => (
    <ErrorBoundary {...errorBoundaryProps}>
      <Component {...props} />
    </ErrorBoundary>
  );

  // Set display name for better debugging
  const displayName = Component.displayName || Component.name || 'Component';
  WithErrorBoundary.displayName = `WithErrorBoundary(${displayName})`;

  return WithErrorBoundary;
}

export default ErrorBoundary;