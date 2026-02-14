import React from 'react';

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  helperText?: string;
}

export const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ label, error, helperText, className = '', ...props }, ref) => {
    const inputId = props.id || props.name;

    return (
      <div className="w-full">
        {label && (
          <label
            htmlFor={inputId}
            className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2"
          >
            {label}
          </label>
        )}
        <input
          ref={ref}
          id={inputId}
          className={`
            appearance-none relative block w-full px-3 py-2.5 sm:px-4 sm:py-3
            bg-white/50 dark:bg-gray-700/50
            border ${error ? 'border-red-500 focus:ring-red-500' : 'border-gray-300 dark:border-gray-600'}
            placeholder-gray-500 text-gray-900 dark:text-gray-100
            rounded-xl
            focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500
            focus:z-10 text-sm sm:text-base
            transition-all duration-200
            hover:border-gray-400 dark:hover:border-gray-500
            disabled:opacity-50 disabled:cursor-not-allowed
            touch-manipulation
            ${className}
          `}
          {...props}
        />
        {error && (
          <p className="mt-2 text-xs sm:text-sm text-red-600 dark:text-red-400">{error}</p>
        )}
        {helperText && !error && (
          <p className="mt-2 text-xs sm:text-sm text-gray-500 dark:text-gray-400">{helperText}</p>
        )}
      </div>
    );
  }
);

Input.displayName = 'Input';
