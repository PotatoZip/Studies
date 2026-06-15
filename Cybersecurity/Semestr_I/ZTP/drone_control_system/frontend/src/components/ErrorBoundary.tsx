import { Component, type ErrorInfo, type ReactNode } from "react";

interface Props {
  children: ReactNode;
}

interface State {
  error: Error | null;
}

/**
 * Catches render-time exceptions in the subtree and shows a readable fallback
 * instead of unmounting to a blank white screen. Without this, any thrown error
 * in a dashboard component (e.g. reading an undefined telemetry field) takes the
 * whole app down silently.
 */
export default class ErrorBoundary extends Component<Props, State> {
  state: State = { error: null };

  static getDerivedStateFromError(error: Error): State {
    return { error };
  }

  componentDidCatch(error: Error, info: ErrorInfo) {
    // Surface it for debugging instead of failing silently.
    console.error("Uncaught render error:", error, info.componentStack);
  }

  private handleReload = () => {
    this.setState({ error: null });
    window.location.reload();
  };

  render() {
    if (this.state.error) {
      return (
        <div className="min-h-screen flex items-center justify-center bg-background p-6">
          <div className="max-w-md w-full rounded-lg border border-border bg-card p-6 text-center space-y-3">
            <h1 className="text-lg font-semibold text-foreground">Something went wrong</h1>
            <p className="text-sm text-muted-foreground">
              The dashboard hit an unexpected error and couldn’t render this view.
            </p>
            <pre className="text-left text-xs text-red-400 bg-muted/50 rounded p-2 overflow-auto max-h-40">
              {this.state.error.message}
            </pre>
            <button
              onClick={this.handleReload}
              className="inline-flex items-center justify-center rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground hover:opacity-90"
            >
              Reload
            </button>
          </div>
        </div>
      );
    }
    return this.props.children;
  }
}
