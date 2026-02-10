import React, { useState } from 'react';

type TaskFormProps = {
  initialTitle?: string;
  initialDescription?: string;
  initialCompleted?: boolean;
  onSubmit: (title: string, description: string, completed: boolean) => void;
  onCancel?: () => void;
  submitButtonText?: string;
};

export default function TaskForm({ 
  initialTitle = '', 
  initialDescription = '', 
  initialCompleted = false, 
  onSubmit, 
  onCancel, 
  submitButtonText = 'Save Task' 
}: TaskFormProps) {
  const [title, setTitle] = useState(initialTitle);
  const [description, setDescription] = useState(initialDescription);
  const [completed, setCompleted] = useState(initialCompleted);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(title, description, completed);
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div>
        <label htmlFor="title" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Task Title *
        </label>
        <input
          type="text"
          id="title"
          required
          className="w-full px-4 py-3 bg-white/50 dark:bg-gray-700/50 border border-gray-300 dark:border-gray-600 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm transition-all duration-200"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="Enter task title..."
        />
      </div>

      <div>
        <label htmlFor="description" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Description
        </label>
        <textarea
          id="description"
          rows={4}
          className="w-full px-4 py-3 bg-white/50 dark:bg-gray-700/50 border border-gray-300 dark:border-gray-600 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 sm:text-sm transition-all duration-200 resize-vertical"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="Enter task description..."
        />
      </div>

      <div className="flex items-center pt-2">
        <input
          type="checkbox"
          id="completed"
          className="h-5 w-5 text-blue-600 focus:ring-blue-500 border-gray-300 rounded focus:ring-blue-500"
          checked={completed}
          onChange={(e) => setCompleted(e.target.checked)}
        />
        <label htmlFor="completed" className="ml-3 block text-sm text-gray-700 dark:text-gray-300">
          Mark as completed
        </label>
      </div>

      <div className="flex justify-end space-x-4 pt-4">
        {onCancel && (
          <button
            type="button"
            onClick={onCancel}
            className="inline-flex items-center px-5 py-3 border border-gray-300 dark:border-gray-600 text-sm font-medium rounded-xl text-gray-700 dark:text-gray-300 bg-white/50 dark:bg-gray-700/50 hover:bg-gray-50 dark:hover:bg-gray-600/50 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 transition-colors duration-200"
          >
            Cancel
          </button>
        )}
        <button
          type="submit"
          className="inline-flex items-center px-5 py-3 border border-transparent text-sm font-medium rounded-xl shadow-md text-white bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-all duration-200 transform hover:scale-[1.02]"
        >
          <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
          </svg>
          {submitButtonText}
        </button>
      </div>
    </form>
  );
}