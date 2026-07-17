interface ErrorStateProps {
  title: string;
  description?: string;
  onRetry?: () => void;
}

export default function ErrorState({ title, description, onRetry }: ErrorStateProps) {
  return (
    <div className="flex flex-col items-center justify-center py-12">
      <div className="text-6xl mb-4">⚠️</div>
      <h3 className="text-xl font-semibold text-error-600 mb-2">{title}</h3>
      {description && (
        <p className="text-gray-600 text-center max-w-md mb-6">{description}</p>
      )}
      {onRetry && (
        <button
          onClick={onRetry}
          className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
        >
          Retry
        </button>
      )}
    </div>
  );
}
