import { motion } from 'framer-motion';

interface SkeletonProps {
  variant?: 'text' | 'circular' | 'rectangular';
  width?: string | number;
  height?: string | number;
  className?: string;
  count?: number;
}

export default function Skeleton({ 
  variant = 'text', 
  width, 
  height, 
  className = '',
  count = 1
}: SkeletonProps) {
  const baseClasses = 'bg-gray-200 dark:bg-gray-700 animate-pulse';
  
  const variantClasses = {
    text: 'rounded h-4',
    circular: 'rounded-full',
    rectangular: 'rounded'
  };

  const getWidth = () => {
    if (width) return typeof width === 'number' ? `${width}px` : width;
    if (variant === 'text') return '100%';
    return '40px';
  };

  const getHeight = () => {
    if (height) return typeof height === 'number' ? `${height}px` : height;
    if (variant === 'text') return '16px';
    if (variant === 'circular') return '40px';
    return '100px';
  };

  const renderSkeleton = () => (
    <motion.div
      className={`${baseClasses} ${variantClasses[variant]} ${className}`}
      style={{ width: getWidth(), height: getHeight() }}
      initial={{ opacity: 0.5 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5, repeat: Infinity, repeatType: "reverse" }}
    />
  );

  if (count > 1) {
    return (
      <div className="space-y-2">
        {[...Array(count)].map((_, i) => (
          <div key={i}>{renderSkeleton()}</div>
        ))}
      </div>
    );
  }

  return renderSkeleton();
}
