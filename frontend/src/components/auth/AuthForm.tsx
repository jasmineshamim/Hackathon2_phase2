import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '../ui/Card';
import { cn } from '@/src/lib/utils';

interface AuthFormProps {
  title: string;
  subtitle?: string;
  children: React.ReactNode;
  className?: string;
}

const AuthForm: React.FC<AuthFormProps> = ({
  title,
  subtitle,
  children,
  className = ''
}) => {
  return (
    <Card className={cn("w-full max-w-md mx-auto shadow-xl rounded-lg", className)}>
      <CardHeader className="text-center">
        <CardTitle className="text-2xl font-bold">{title}</CardTitle>
        {subtitle && <p className="text-sm text-gray-500 mt-2">{subtitle}</p>}
      </CardHeader>
      <CardContent>
        {children}
      </CardContent>
    </Card>
  );
};

export { AuthForm };