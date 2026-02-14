import React from 'react';

interface GradientBackgroundProps {
  children: React.ReactNode;
  className?: string;
}

const GradientBackground: React.FC<GradientBackgroundProps> = ({ 
  children, 
  className = '' 
}) => {
  return (
    <div 
      className={`min-h-screen bg-gradient-to-br from-blue-400 via-purple-500 to-pink-500 flex items-center justify-center p-4 ${className}`}
    >
      {children}
    </div>
  );
};

export { GradientBackground };