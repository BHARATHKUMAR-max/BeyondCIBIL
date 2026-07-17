interface LogoProps {
  variant?: 'full' | 'icon' | 'compact';
  className?: string;
  size?: number;
}

export default function Logo({ variant = 'full', className = '', size = 40 }: LogoProps) {
  if (variant === 'icon') {
    return (
      <svg
        width={size}
        height={size}
        viewBox="0 0 40 40"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        className={className}
      >
        <circle cx="20" cy="20" r="18" fill="currentColor" className="text-primary-600 dark:text-primary-400" opacity="0.1"/>
        <path
          d="M20 4L24 12H16L20 4Z"
          fill="currentColor"
          className="text-primary-600 dark:text-primary-400"
        />
        <path
          d="M20 36L16 28H24L20 36Z"
          fill="currentColor"
          className="text-primary-600 dark:text-primary-400"
        />
        <path
          d="M4 20L12 16V24L4 20Z"
          fill="currentColor"
          className="text-secondary-600 dark:text-secondary-400"
        />
        <path
          d="M36 20L28 24V16L36 20Z"
          fill="currentColor"
          className="text-secondary-600 dark:text-secondary-400"
        />
        <circle cx="20" cy="20" r="6" fill="currentColor" className="text-primary-600 dark:text-primary-400"/>
        <path
          d="M20 16V24M16 20H24"
          stroke="white"
          strokeWidth="2"
          strokeLinecap="round"
        />
      </svg>
    );
  }

  if (variant === 'compact') {
    return (
      <div className={`flex items-center space-x-2 ${className}`}>
        <svg
          width={size}
          height={size}
          viewBox="0 0 40 40"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          <circle cx="20" cy="20" r="18" fill="currentColor" className="text-primary-600 dark:text-primary-400" opacity="0.1"/>
          <path
            d="M20 4L24 12H16L20 4Z"
            fill="currentColor"
            className="text-primary-600 dark:text-primary-400"
          />
          <path
            d="M20 36L16 28H24L20 36Z"
            fill="currentColor"
            className="text-primary-600 dark:text-primary-400"
          />
          <path
            d="M4 20L12 16V24L4 20Z"
            fill="currentColor"
            className="text-secondary-600 dark:text-secondary-400"
          />
          <path
            d="M36 20L28 24V16L36 20Z"
            fill="currentColor"
            className="text-secondary-600 dark:text-secondary-400"
          />
          <circle cx="20" cy="20" r="6" fill="currentColor" className="text-primary-600 dark:text-primary-400"/>
          <path
            d="M20 16V24M16 20H24"
            stroke="white"
            strokeWidth="2"
            strokeLinecap="round"
          />
        </svg>
        <span className="text-sm font-bold text-primary-600 dark:text-primary-400">
          BeyondCIBIL
        </span>
      </div>
    );
  }

  return (
    <div className={`flex items-center space-x-3 ${className}`}>
      <svg
        width={size}
        height={size}
        viewBox="0 0 40 40"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        <circle cx="20" cy="20" r="18" fill="currentColor" className="text-primary-600 dark:text-primary-400" opacity="0.1"/>
        <path
          d="M20 4L24 12H16L20 4Z"
          fill="currentColor"
          className="text-primary-600 dark:text-primary-400"
        />
        <path
          d="M20 36L16 28H24L20 36Z"
          fill="currentColor"
          className="text-primary-600 dark:text-primary-400"
        />
        <path
          d="M4 20L12 16V24L4 20Z"
          fill="currentColor"
          className="text-secondary-600 dark:text-secondary-400"
        />
        <path
          d="M36 20L28 24V16L36 20Z"
          fill="currentColor"
          className="text-secondary-600 dark:text-secondary-400"
        />
        <circle cx="20" cy="20" r="6" fill="currentColor" className="text-primary-600 dark:text-primary-400"/>
        <path
          d="M20 16V24M16 20H24"
          stroke="white"
          strokeWidth="2"
          strokeLinecap="round"
        />
      </svg>
      <div className="flex flex-col">
        <span className="text-xl font-bold text-primary-600 dark:text-primary-400 leading-tight">
          BEYOND
        </span>
        <span className="text-xl font-bold text-secondary-600 dark:text-secondary-400 leading-tight">
          CIBIL
        </span>
      </div>
    </div>
  );
}
