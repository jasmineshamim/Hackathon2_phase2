'use client';

import React from 'react';
import { useRouter } from 'next/navigation';
import { zodResolver } from '@hookform/resolvers/zod';
import { useForm } from 'react-hook-form';
import { z } from 'zod';

import { Button } from '@/src/components/ui/Button';
import { Input } from '@/src/components/ui/Input';
import { Label } from '@/src/components/ui/Label';
import { GradientBackground } from '@/src/components/auth/GradientBackground';
import { AuthForm } from '@/src/components/auth/AuthForm';
import { GradientButton } from '@/src/components/auth/GradientButton';
import { apiClient, type LoginResponse } from '@/src/lib/api-client';
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '@/src/components/ui/Form';

const signinSchema = z.object({
  usernameOrEmail: z.string().min(1, { message: 'Username or email is required' }),
  password: z.string().min(1, { message: 'Password is required' }),
});

type SigninFormValues = z.infer<typeof signinSchema>;

export default function SigninPage() {
  const router = useRouter();
  const [isLoading, setIsLoading] = React.useState(false);

  const form = useForm<SigninFormValues>({
    resolver: zodResolver(signinSchema),
    defaultValues: {
      usernameOrEmail: '',
      password: '',
    },
  });

  async function onSubmit(data: SigninFormValues) {
    setIsLoading(true);

    try {
      const loginResponse: LoginResponse = await apiClient.login({
        email: data.usernameOrEmail,
        password: data.password,
      });

      // Store tokens in localStorage
      if (typeof window !== 'undefined') {
        localStorage.setItem('accessToken', loginResponse.access_token);
        localStorage.setItem('refreshToken', loginResponse.refresh_token);
      }

      console.log('Login successful, redirecting to dashboard...');
      router.push('/dashboard');
    } catch (error) {
      console.error('Signin error:', error);
      // Handle error (show message to user, etc.)
      alert('Sign in failed. Please check your credentials and try again.');
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <GradientBackground>
      <Form {...form}>
        <form onSubmit={form.handleSubmit(onSubmit)} className="w-full max-w-sm space-y-6">
          <AuthForm title="Welcome Back" subtitle="Sign in to your account">
            <FormField
              control={form.control}
              name="usernameOrEmail"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Username or Email</FormLabel>
                  <FormControl>
                    <Input placeholder="Enter your username or email" {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            
            <FormField
              control={form.control}
              name="password"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Password</FormLabel>
                  <FormControl>
                    <Input type="password" placeholder="Enter your password" {...field} />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
            
            <div className="flex flex-col gap-4 pt-2">
              <GradientButton 
                type="submit" 
                className="w-full" 
                isLoading={isLoading}
              >
                Sign In
              </GradientButton>
              
              <div className="relative my-4">
                <div className="absolute inset-0 flex items-center">
                  <span className="w-full border-t" />
                </div>
                <div className="relative flex justify-center text-xs uppercase">
                  <span className="bg-background px-2 text-muted-foreground">
                    Or continue with
                  </span>
                </div>
              </div>
              
              <Button variant="outline" type="button" className="w-full">
                Sign in with Google
              </Button>
            </div>
            
            <div className="text-center text-sm text-gray-500 mt-4">
              Don't have an account?{' '}
              <a href="/signup" className="font-medium underline text-blue-500">
                Sign up
              </a>
            </div>
          </AuthForm>
        </form>
      </Form>
    </GradientBackground>
  );
}