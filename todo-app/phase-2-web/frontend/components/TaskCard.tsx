import React from 'react';

type TaskCardProps = {
  id: number;
  title: string;
  description?: string;
  completed: boolean;
  createdAt: string;
  updatedAt: string;
  onToggle: (id: number, currentStatus: boolean) => void;
  onDelete: (id: number) => void;
};

export default function TaskCard({
  id,
  title,
  description,
  completed,
  createdAt,
  updatedAt,
  onToggle,
  onDelete
}: TaskCardProps) {
  return (
    <div className="bg-card bg-white/90 dark:bg-gray-800/90 backdrop-blur-sm rounded-xl p-5 shadow-lg border border-gray-200 dark:border-gray-700 hover:shadow-xl transition-shadow duration-300 group">
      <div className="flex items-start">
        <button
          onClick={() => onToggle(id, completed)}
          className={`flex-shrink-0 w-6 h-6 rounded-full border-2 flex items-center justify-center transition-all duration-200 ${
            completed
              ? 'bg-gradient-to-r from-green-400 to-green-500 border-green-500'
              : 'border-gray-300 dark:border-gray-600 hover:border-blue-500'
          }`}
          aria-label={completed ? 'Mark as incomplete' : 'Mark as complete'}
        >
          {completed && (
            <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
            </svg>
          )}
        </button>
        <div className="ml-4 flex-1 min-w-0">
          <div className="flex items-start justify-between">
            <h3 className={`text-lg font-semibold truncate ${completed ? 'line-through text-gray-500 dark:text-gray-400' : 'text-gray-900 dark:text-white'}`}>
              {title}
            </h3>
            <button
              onClick={() => onDelete(id)}
              className="text-gray-400 hover:text-red-500 dark:hover:text-red-400 ml-2 flex-shrink-0 p-1 rounded-full hover:bg-red-50 dark:hover:bg-red-900/20 transition-colors duration-200 opacity-0 group-hover:opacity-100"
              aria-label="Delete task"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
              </svg>
            </button>
          </div>
          {description && (
            <p className={`mt-2 text-gray-600 dark:text-gray-300 ${completed ? 'text-gray-400 dark:text-gray-500' : ''}`}>
              {description}
            </p>
          )}
          <div className="mt-3 flex items-center text-xs text-gray-500 dark:text-gray-400">
            <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
            <span>Created: {new Date(createdAt).toLocaleDateString()}</span>
          </div>
        </div>
      </div>
    </div>
  );
}