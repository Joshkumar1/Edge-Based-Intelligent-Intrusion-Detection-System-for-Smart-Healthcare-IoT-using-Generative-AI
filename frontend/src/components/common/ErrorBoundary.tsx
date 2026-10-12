import React, { Component, ErrorInfo, ReactNode } from 'react';
import { AlertTriangle, RefreshCw, Home } from 'lucide-react';

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
  onReset?: () => void;
}

interface State {
  hasError: boolean;
  error: Error | null;
}

export class ErrorBoundary extends Component<Props, State> {
  public state: State = {
    hasError: false,
    error: null,
  };

  public static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('Uncaught component error caught by ErrorBoundary:', error, errorInfo);
  }

  public handleReset = () => {
    this.setState({ hasError: false, error: null });
    if (this.props.onReset) {
      this.props.onReset();
    }
  };

  public render() {
    if (this.state.hasError) {
      if (this.props.fallback) {
        return this.props.fallback;
      }
      return (
        <div className="min-h-screen flex items-center justify-center p-6 bg-background text-foreground">
          <div className="max-w-md w-full p-8 rounded-2xl bg-card border border-border shadow-2xl space-y-6 text-center">
            <div className="h-16 w-16 mx-auto rounded-2xl bg-rose-500/10 text-rose-500 border border-rose-500/20 flex items-center justify-center">
              <AlertTriangle className="h-8 w-8" />
            </div>
            <div className="space-y-2">
              <h2 className="text-xl font-bold tracking-tight">Cockpit Workspace Notice</h2>
              <p className="text-xs text-muted-foreground leading-relaxed">
                An unexpected view state occurred while rendering this interface module. The edge IDS telemetry pipeline is still operational.
              </p>
              {this.state.error && (
                <div className="text-[11px] font-mono text-rose-400 bg-rose-500/10 p-2.5 rounded-lg text-left overflow-auto max-h-24">
                  {this.state.error.message}
                </div>
              )}
            </div>
            <div className="flex gap-3 justify-center">
              <button
                onClick={this.handleReset}
                className="flex items-center space-x-2 px-5 py-2.5 rounded-xl bg-medical-teal text-white font-semibold text-xs shadow-glow-teal hover:opacity-90 transition-all"
              >
                <RefreshCw className="h-3.5 w-3.5" />
                <span>Reload View</span>
              </button>
              <button
                onClick={() => window.location.reload()}
                className="flex items-center space-x-2 px-5 py-2.5 rounded-xl bg-secondary text-foreground font-semibold text-xs border hover:bg-secondary/80 transition-all"
              >
                <Home className="h-3.5 w-3.5" />
                <span>Restart Session</span>
              </button>
            </div>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}
