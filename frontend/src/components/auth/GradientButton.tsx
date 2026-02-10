import React from 'react';
import { Button, ButtonProps } from '../ui/Button';

interface GradientButtonProps extends ButtonProps {
  gradientStart?: string;
  gradientEnd?: string;
}

const GradientButton: React.FC<GradientButtonProps> = ({
  children,
  gradientStart = 'from-blue-500',
  gradientEnd = 'to-purple-600',
  className = '',
  ...props
}) => {
  const gradientClass = `bg-gradient-to-r ${gradientStart} ${gradientEnd}`;
  const combinedClassName = `${gradientClass} ${className}`;

  return (
    <Button
      className={combinedClassName}
      {...props}
    >
      {children}
    </Button>
  );
};

export { GradientButton };