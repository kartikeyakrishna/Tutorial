import React from 'react';

const ProfilePage: React.FC = () => {
  // TODO: Fetch user profile and progress
  return (
    <div className="max-w-2xl mx-auto py-8 px-4">
      <h1 className="text-3xl font-bold mb-4">My Profile</h1>
      <div className="bg-white rounded-lg shadow p-6 mb-6">
        <h2 className="text-xl font-semibold mb-2">User Settings</h2>
        {/* TODO: User settings form */}
        <div className="text-gray-500">Settings form coming soon...</div>
      </div>
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-semibold mb-2">My Progress</h2>
        {/* TODO: Progress list */}
        <div className="text-gray-500">Progress tracking coming soon...</div>
      </div>
    </div>
  );
};

export default ProfilePage; 