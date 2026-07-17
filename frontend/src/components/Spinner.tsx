import { motion } from 'framer-motion';

interface SpinnerProps {
  size?: 'sm' | 'md' | 'lg';
  color?: 'primary' | 'secondary' | 'success' | 'error' | 'warning' | 'info';
  className?: string;
}

export default function Spinner({ size = 'md', color = 'primary', className = '' }: SpinnerProps) {
  const sizeClasses = {
    sm: 'w-4 h-4',
    md: 'w-8 h-8',
    lg: 'w-12 h-12'
  };

  const colorClasses = {
    primary: 'border-primary-600 dark:border-primary-400',
    secondary: 'border-secondary-600 dark:border-secondary-400',
    success: 'border-success-600 dark:border-success-400',
    error: 'border-error-600 dark:border-error-400',
    warning: 'border-warning-600 dark:border-warning-400',
    info: 'border-info-600 dark:border-info-400'
  };

  return (
    <div className={`relative ${sizeClasses[size]} ${className}`}>
      <motion.div
        className={`absolute inset-0 border-4 ${colorClasses[color]} border-t-transparent rounded-full`}
        animate={{ rotate: 360 }}
        transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
      />
    </div>
  );
}
