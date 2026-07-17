import { motion } from 'framer-motion';

interface SkeletonLoaderProps {
  className?: string;
}

export default function SkeletonLoader({ className = '' }: SkeletonLoaderProps) {
  return (
    <motion.div
      animate={{
        opacity: [0.5, 1, 0.5],
      }}
      transition={{
        duration: 1.5,
        repeat: Infinity,
        ease: 'easeInOut',
      }}
      className={`bg-gray-200 rounded ${className}`}
    />
  );
}
