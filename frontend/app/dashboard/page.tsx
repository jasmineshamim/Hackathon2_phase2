'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import TaskCard from '@/components/TaskCard';
import { apiClient, Task, TaskStatistics } from '@/lib/api-client';

type FilterType = 'all' | 'pending' | 'completed';

export default function DashboardPage() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [statistics, setStatistics] = useState<TaskStatistics>({ total_count: 0, pending_count: 0, completed_count: 0 });
  const [filter, setFilter] = useState<FilterType>('all');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();

  // Check if user is authenticated
  useEffect(() => {
    if (!apiClient.isAuthenticated()) {
      router.push('/auth/signin');
      return;
    }
  }, [router]);

  // Fetch tasks and statistics
  const fetchTasksAndStatistics = async () => {
    try {
      if (!apiClient.isAuthenticated()) {
        router.push('/auth/signin');
        return;
      }

      const [tasksData, statsData] = await Promise.all([
        apiClient.getTasks(),
        apiClient.getTaskStatistics()
      ]);

      setTasks(tasksData);
      setStatistics(statsData);
    } catch (err: any) {
      // If it's an auth error, redirect to login
      if (err.message && (err.message.includes('Authentication required') || err.message.includes('Unauthorized'))) {
        router.push('/auth/signin');
        return;
      }
      setError(err.message || 'An error occurred while fetching tasks');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTasksAndStatistics();
  }, [router]);

  // Toggle task completion
  const toggleTaskCompletion = async (taskId: number, currentStatus: boolean) => {
    try {
      if (!apiClient.isAuthenticated()) {
        router.push('/auth/signin');
        return;
      }

      const updatedTask = await apiClient.toggleTaskCompletion(taskId, !currentStatus);

      // Update the task in the UI
      setTasks(prevTasks =>
        prevTasks.map(task =>
          task.id === taskId ? updatedTask : task
        )
      );

      // Refresh statistics
      const statsData = await apiClient.getTaskStatistics();
      setStatistics(statsData);
    } catch (err: any) {
      // If it's an auth error, redirect to login
      if (err.message && (err.message.includes('Authentication required') || err.message.includes('Unauthorized'))) {
        router.push('/auth/signin');
        return;
      }
      setError(err.message || 'An error occurred while updating the task');
    }
  };

  // Delete task
  const deleteTask = async (taskId: number) => {
    if (!window.confirm('Are you sure you want to delete this task?')) {
      return;
    }

    try {
      if (!apiClient.isAuthenticated()) {
        router.push('/auth/signin');
        return;
      }

      await apiClient.deleteTask(taskId);

      // Remove the task from the UI
      setTasks(prevTasks => prevTasks.filter(task => task.id !== taskId));

      // Refresh statistics
      const statsData = await apiClient.getTaskStatistics();
      setStatistics(statsData);
    } catch (err: any) {
      // If it's an auth error, redirect to login
      if (err.message && (err.message.includes('Authentication required') || err.message.includes('Unauthorized'))) {
        router.push('/auth/signin');
        return;
      }
      setError(err.message || 'An error occurred while deleting the task');
    }
  };

  // Filter tasks based on selected filter
  const filteredTasks = tasks.filter(task => {
    if (filter === 'pending') return !task.completed;
    if (filter === 'completed') return task.completed;
    return true; // 'all' filter
  });

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-xl">Loading tasks...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen py-8">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-8 gap-4">
          <div>
            <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">Your Tasks</h1>
            <p className="text-gray-600 dark:text-gray-400 mt-1">Manage your tasks efficiently</p>
          </div>
          <Link
            href="/dashboard/tasks"
            className="bg-gradient-to-r from-blue-500 to-purple-600 text-white px-5 py-3 rounded-xl hover:from-blue-600 hover:to-purple-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-all duration-200 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 flex items-center"
          >
            <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>
            </svg>
            Add New Task
          </Link>
        </div>

        {/* Statistics Dashboard */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
          <div className="bg-white/90 dark:bg-gray-800/90 backdrop-blur-sm rounded-xl shadow-lg p-6 border border-gray-200 dark:border-gray-700">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Total Tasks</p>
                <p className="text-3xl font-bold text-gray-900 dark:text-white mt-2">{statistics.total_count}</p>
              </div>
              <div className="w-12 h-12 bg-gradient-to-r from-blue-100 to-purple-100 rounded-full flex items-center justify-center">
                <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path>
                </svg>
              </div>
            </div>
          </div>

          <div className="bg-white/90 dark:bg-gray-800/90 backdrop-blur-sm rounded-xl shadow-lg p-6 border border-gray-200 dark:border-gray-700">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Pending Tasks</p>
                <p className="text-3xl font-bold text-orange-600 dark:text-orange-400 mt-2">{statistics.pending_count}</p>
              </div>
              <div className="w-12 h-12 bg-orange-100 rounded-full flex items-center justify-center">
                <svg className="w-6 h-6 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
              </div>
            </div>
          </div>

          <div className="bg-white/90 dark:bg-gray-800/90 backdrop-blur-sm rounded-xl shadow-lg p-6 border border-gray-200 dark:border-gray-700">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Completed Tasks</p>
                <p className="text-3xl font-bold text-green-600 dark:text-green-400 mt-2">{statistics.completed_count}</p>
              </div>
              <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center">
                <svg className="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
              </div>
            </div>
          </div>
        </div>

        {/* Filter Buttons */}
        <div className="flex gap-3 mb-6">
          <button
            onClick={() => setFilter('all')}
            className={`px-6 py-2.5 rounded-xl font-medium transition-all duration-200 ${
              filter === 'all'
                ? 'bg-gradient-to-r from-blue-500 to-purple-600 text-white shadow-lg'
                : 'bg-white/90 dark:bg-gray-800/90 text-gray-700 dark:text-gray-300 border border-gray-200 dark:border-gray-700 hover:border-blue-500'
            }`}
          >
            All Tasks
          </button>
          <button
            onClick={() => setFilter('pending')}
            className={`px-6 py-2.5 rounded-xl font-medium transition-all duration-200 ${
              filter === 'pending'
                ? 'bg-orange-500 text-white shadow-lg'
                : 'bg-white/90 dark:bg-gray-800/90 text-gray-700 dark:text-gray-300 border border-gray-200 dark:border-gray-700 hover:border-orange-500'
            }`}
          >
            Pending Tasks
          </button>
          <button
            onClick={() => setFilter('completed')}
            className={`px-6 py-2.5 rounded-xl font-medium transition-all duration-200 ${
              filter === 'completed'
                ? 'bg-green-500 text-white shadow-lg'
                : 'bg-white/90 dark:bg-gray-800/90 text-gray-700 dark:text-gray-300 border border-gray-200 dark:border-gray-700 hover:border-green-500'
            }`}
          >
            Completed Tasks
          </button>
        </div>

        {error && (
          <div className="mb-6 rounded-xl bg-red-50 dark:bg-red-900/20 p-4 border border-red-200 dark:border-red-800">
            <div className="flex">
              <div className="flex-shrink-0">
                <svg className="h-5 w-5 text-red-400" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                </svg>
              </div>
              <div className="ml-3">
                <h3 className="text-sm font-medium text-red-800 dark:text-red-200">Error</h3>
                <div className="mt-2 text-sm text-red-700 dark:text-red-300">
                  <p>{error}</p>
                </div>
              </div>
            </div>
          </div>
        )}

        {filteredTasks.length === 0 ? (
          <div className="bg-card bg-white/90 dark:bg-gray-800/90 backdrop-blur-sm rounded-2xl shadow-lg p-12 text-center border border-gray-200 dark:border-gray-700">
            <div className="mx-auto w-16 h-16 bg-gradient-to-r from-blue-100 to-purple-100 rounded-full flex items-center justify-center mb-6">
              <svg className="w-8 h-8 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path>
              </svg>
            </div>
            <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-2">
              {filter === 'all' ? 'No tasks yet' : filter === 'pending' ? 'No pending tasks' : 'No completed tasks'}
            </h3>
            <p className="text-gray-600 dark:text-gray-400 mb-6">
              {filter === 'all' ? 'Get started by creating your first task' : filter === 'pending' ? 'All tasks are completed!' : 'Complete some tasks to see them here'}
            </p>
            {filter === 'all' && (
              <Link
                href="/dashboard/tasks"
                className="inline-flex items-center px-5 py-3 border border-transparent text-base font-medium rounded-xl shadow-md text-white bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-all duration-200"
              >
                <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>
                </svg>
                Create your first task
              </Link>
            )}
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredTasks.map((task) => (
              <TaskCard
                key={task.id}
                id={task.id}
                title={task.title}
                description={task.description || undefined}
                completed={task.completed}
                createdAt={task.created_at}
                updatedAt={task.updated_at}
                onToggle={toggleTaskCompletion}
                onDelete={deleteTask}
              />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}