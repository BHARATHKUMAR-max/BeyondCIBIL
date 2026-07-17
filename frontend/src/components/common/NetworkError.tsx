import ErrorState from '../ui/ErrorState';

interface NetworkErrorProps {
  onRetry?: () => void;
}

export default function NetworkError({ onRetry }: NetworkErrorProps) {
  return (
    <ErrorState
      title="Network Error"
      description="Unable to connect to the server. Please check your internet connection and try again."
      onRetry={onRetry}
    />
  );
}
