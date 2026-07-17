import ErrorState from '../ui/ErrorState';

interface ApiErrorProps {
  error: Error;
  onRetry?: () => void;
}

export default function ApiError({ error, onRetry }: ApiErrorProps) {
  return (
    <ErrorState
      title="API Error"
      description={error.message || 'An error occurred while fetching data.'}
      onRetry={onRetry}
    />
  );
}
