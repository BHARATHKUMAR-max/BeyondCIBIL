import { motion } from 'framer-motion';

interface AnimatedBackgroundProps {
  variant?: 'gradient' | 'floating' | 'particles' | 'stars' | 'bubbles';
  className?: string;
}

export default function AnimatedBackground({ variant = 'gradient', className = '' }: AnimatedBackgroundProps) {

  if (variant === 'gradient') {
    return (
      <div className={`fixed inset-0 -z-10 overflow-hidden ${className}`}>
        <motion.div
          className="absolute inset-0 bg-gradient-to-br from-primary-100 via-primary-50 to-secondary-100 dark:from-gray-800 dark:via-gray-900 dark:to-gray-800"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 1 }}
        />
        <motion.div
          className="absolute top-0 left-0 w-96 h-96 bg-primary-400/40 dark:bg-primary-600/30 rounded-full blur-3xl"
          animate={{
            x: [0, 100, 0],
            y: [0, -100, 0],
            scale: [1, 1.2, 1],
          }}
          transition={{
            duration: 20,
            repeat: Infinity,
            ease: "easeInOut",
          }}
        />
        <motion.div
          className="absolute bottom-0 right-0 w-96 h-96 bg-secondary-400/40 dark:bg-secondary-600/30 rounded-full blur-3xl"
          animate={{
            x: [0, -100, 0],
            y: [0, 100, 0],
            scale: [1, 1.1, 1],
          }}
          transition={{
            duration: 25,
            repeat: Infinity,
            ease: "easeInOut",
          }}
        />
        <motion.div
          className="absolute top-1/2 left-1/2 w-64 h-64 bg-accent-400/30 dark:bg-accent-600/20 rounded-full blur-3xl"
          animate={{
            x: [0, 50, -50, 0],
            y: [0, -50, 50, 0],
            scale: [1, 0.8, 1.2, 1],
          }}
          transition={{
            duration: 15,
            repeat: Infinity,
            ease: "easeInOut",
          }}
        />
      </div>
    );
  }

  if (variant === 'floating') {
    return (
      <div className={`fixed inset-0 -z-10 overflow-hidden ${className}`}>
        <motion.div
          className="absolute inset-0 bg-gradient-to-br from-primary-100 via-primary-50 to-secondary-100 dark:from-gray-800 dark:via-gray-900 dark:to-gray-800"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 1 }}
        />
        {[...Array(6)].map((_, i) => (
          <motion.div
            key={i}
            className="absolute rounded-full bg-primary-300/50 dark:bg-primary-700/40 blur-2xl"
            style={{
              width: Math.random() * 200 + 100,
              height: Math.random() * 200 + 100,
              left: `${Math.random() * 100}%`,
              top: `${Math.random() * 100}%`,
            }}
            animate={{
              y: [0, -30, 0],
              x: [0, Math.random() * 20 - 10, 0],
              scale: [1, 1.1, 1],
            }}
            transition={{
              duration: Math.random() * 5 + 5,
              repeat: Infinity,
              ease: "easeInOut",
              delay: i * 0.5,
            }}
          />
        ))}
      </div>
    );
  }

  if (variant === 'particles') {
    return (
      <div className={`fixed inset-0 -z-10 overflow-hidden ${className}`}>
        <motion.div
          className="absolute inset-0 bg-gradient-to-br from-primary-100 via-primary-50 to-secondary-100 dark:from-gray-800 dark:via-gray-900 dark:to-gray-800"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 1 }}
        />
        {[...Array(20)].map((_, i) => (
          <motion.div
            key={i}
            className="absolute w-2 h-2 rounded-full bg-primary-400/50 dark:bg-primary-600/50"
            style={{
              left: `${Math.random() * 100}%`,
              top: `${Math.random() * 100}%`,
            }}
            animate={{
              y: [0, -100, 0],
              opacity: [0.3, 0.8, 0.3],
              scale: [1, 0.5, 1],
            }}
            transition={{
              duration: Math.random() * 10 + 10,
              repeat: Infinity,
              ease: "easeInOut",
              delay: i * 0.3,
            }}
          />
        ))}
      </div>
    );
  }

  if (variant === 'stars') {
    return (
      <div className={`fixed inset-0 -z-10 overflow-hidden ${className}`}>
        <motion.div
          className="absolute inset-0 bg-gradient-to-br from-primary-100 via-primary-50 to-secondary-100 dark:from-gray-800 dark:via-gray-900 dark:to-gray-800"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 1 }}
        />
        {[...Array(50)].map((_, i) => (
          <motion.div
            key={i}
            className="absolute rounded-full bg-primary-500/50 dark:bg-primary-500/50"
            style={{
              width: Math.random() * 3 + 1,
              height: Math.random() * 3 + 1,
              left: `${Math.random() * 100}%`,
              top: `${Math.random() * 100}%`,
            }}
            animate={{
              opacity: [0.2, 1, 0.2],
              scale: [1, 1.5, 1],
            }}
            transition={{
              duration: Math.random() * 3 + 2,
              repeat: Infinity,
              ease: "easeInOut",
              delay: i * 0.1,
            }}
          />
        ))}
      </div>
    );
  }

  if (variant === 'bubbles') {
    return (
      <div className={`fixed inset-0 -z-10 overflow-hidden ${className}`}>
        <motion.div
          className="absolute inset-0 bg-gradient-to-br from-primary-100 via-primary-50 to-secondary-100 dark:from-gray-800 dark:via-gray-900 dark:to-gray-800"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 1 }}
        />
        {[...Array(15)].map((_, i) => (
          <motion.div
            key={i}
            className="absolute rounded-full border-2 border-primary-400/50 dark:border-primary-600/50"
            style={{
              width: Math.random() * 60 + 20,
              height: Math.random() * 60 + 20,
              left: `${Math.random() * 100}%`,
              top: `${Math.random() * 100}%`,
            }}
            animate={{
              y: [0, -200, -400],
              x: [0, Math.random() * 50 - 25, Math.random() * 50 - 25],
              opacity: [0.6, 0.3, 0],
              scale: [1, 1.2, 0.8],
            }}
            transition={{
              duration: Math.random() * 10 + 15,
              repeat: Infinity,
              ease: "easeInOut",
              delay: i * 0.8,
            }}
          />
        ))}
      </div>
    );
  }

  return null;
}
