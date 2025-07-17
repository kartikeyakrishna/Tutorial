import React, { useState } from 'react';
import AuthForm from '../components/AuthForm';

const AuthPage: React.FC = () => {
  const [mode, setMode] = useState<'login' | 'register'>('login');
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="w-full max-w-md bg-white rounded-lg shadow p-8">
        <div className="flex justify-center mb-6">
          <button className={`px-4 py-2 font-semibold rounded-l ${mode === 'login' ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-700'}`} onClick={() => setMode('login')}>Login</button>
          <button className={`px-4 py-2 font-semibold rounded-r ${mode === 'register' ? 'bg-blue-600 text-white' : 'bg-gray-200 text-gray-700'}`} onClick={() => setMode('register')}>Register</button>
        </div>
        <AuthForm mode={mode} />
      </div>
    </div>
  );
};

export default AuthPage; 