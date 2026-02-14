import Link from 'next/link';

export default function Home() {
  return (
    <div className="min-h-screen flex flex-col">
      <main className="flex-grow flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-md w-full space-y-8">
          <div className="text-center">
            <div className="mx-auto w-16 h-16 bg-gradient-to-r from-blue-500 to-purple-600 rounded-2xl flex items-center justify-center mb-6 shadow-lg">
              <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path>
              </svg>
            </div>
            <h1 className="mt-4 text-4xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
              TodoFlow
            </h1>
            <p className="mt-3 text-lg text-gray-600 dark:text-gray-300 max-w-md mx-auto">
              Streamline your productivity with our secure, modern task management platform
            </p>
          </div>
          <div className="mt-8 bg-card bg-white/90 dark:bg-gray-800/90 backdrop-blur-sm py-8 px-4 shadow-xl rounded-2xl sm:px-10 border border-gray-200 dark:border-gray-700">
            <div className="space-y-6">
              <div>
                <h2 className="text-xl font-semibold text-gray-800 dark:text-gray-200 mb-2">Get Started</h2>
                <p className="text-gray-600 dark:text-gray-400 mb-6">
                  Join thousands of users who trust us to organize their tasks securely.
                </p>
              </div>
              <div className="flex flex-col space-y-4">
                <Link
                  href="/auth/signup"
                  className="w-full flex justify-center items-center py-3 px-4 rounded-xl shadow-md text-base font-semibold text-white bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-all duration-200 transform hover:scale-[1.02] shadow-blue-500/20"
                >
                  <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z"></path>
                  </svg>
                  Create Account
                </Link>
                <div className="relative my-6">
                  <div className="absolute inset-0 flex items-center">
                    <div className="w-full border-t border-gray-300 dark:border-gray-600"></div>
                  </div>
                  <div className="relative flex justify-center">
                    <span className="px-3 bg-card bg-white/90 dark:bg-gray-800/90 text-gray-500 dark:text-gray-400 text-sm font-medium">
                      Or
                    </span>
                  </div>
                </div>
                <Link
                  href="/auth/signin"
                  className="w-full flex justify-center items-center py-3 px-4 border border-gray-300 dark:border-gray-600 rounded-xl shadow-sm text-base font-medium text-gray-700 dark:text-gray-300 bg-card bg-white/90 dark:bg-gray-800/90 hover:bg-gray-50 dark:hover:bg-gray-700/90 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors duration-200"
                >
                  <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1"></path>
                  </svg>
                  Sign in to your account
                </Link>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
