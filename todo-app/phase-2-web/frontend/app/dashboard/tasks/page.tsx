'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import TaskForm from '@/components/TaskForm';
import { apiClient } from '@/lib/api-client';

export default function TasksPage() {
  const [isLoading, setIsLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    // Check if user is authenticated after component mounts (client-side only)
    if (!apiClient.isAuthenticated()) {
      router.push('/auth/signin');
    } else {
      setIsLoading(false); // User is authenticated, allow form to render
    }
  }, [router]);

  const handleSubmit = async (title: string, description: string, completed: boolean) => {
    try {
      // Check authentication before making the request
      if (!apiClient.isAuthenticated()) {
        router.push('/auth/signin');
        return;
      }

      await apiClient.createTask({ title, description, completed });
      // Navigate to dashboard - the dashboard page will fetch fresh data on mount
      router.push('/dashboard');
    } catch (err: any) {
      console.error('Task creation error:', err);
      alert(err.message || 'An error occurred while creating the task');
    }
  };

  const handleCancel = () => {
    router.push('/dashboard');
  };

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-xl">Checking authentication...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen py-8">
      <div className="max-w-2xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="bg-card bg-white/90 dark:bg-gray-800/90 backdrop-blur-sm shadow-xl rounded-2xl overflow-hidden border border-gray-200 dark:border-gray-700">
          <div className="px-6 py-6 sm:px-8 sm:py-8">
            <div className="flex items-center mb-6">
              <div className="w-10 h-10 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg flex items-center justify-center mr-3">
                <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path>
                </svg>
              </div>
              <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Create New Task</h2>
            </div>

            <TaskForm
              onSubmit={handleSubmit}
              onCancel={handleCancel}
              submitButtonText="Create Task"
            />
          </div>
        </div>
      </div>
    </div>
  );
}