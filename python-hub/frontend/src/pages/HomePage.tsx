import React from 'react';

const HomePage: React.FC = () => {
  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white flex flex-col items-center justify-center">
      <section className="w-full max-w-4xl text-center py-16">
        <h1 className="text-5xl font-bold mb-4 text-blue-700">Welcome to Python Hub</h1>
        <p className="text-lg text-gray-600 mb-8">Your all-in-one platform for mastering Python with interactive tutorials, articles, and code snippets.</p>
        <a href="/tutorials" className="inline-block bg-blue-600 text-white px-6 py-3 rounded-lg shadow hover:bg-blue-700 transition">Get Started</a>
      </section>
      <section className="w-full max-w-5xl py-8">
        <h2 className="text-2xl font-semibold mb-4 text-gray-800">Featured Content</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {/* TODO: Map featured tutorials/articles here */}
          <div className="bg-white rounded-lg shadow p-6 flex flex-col items-center justify-center text-gray-500">Featured content coming soon...</div>
        </div>
      </section>
    </div>
  );
};

export default HomePage; 