import React from 'react';
import { useParams } from 'react-router-dom';
import ProgressBar from '../components/ProgressBar';

const TutorialDetailPage: React.FC = () => {
  const { id } = useParams();
  // TODO: Fetch tutorial details and user progress
  return (
    <div className="max-w-3xl mx-auto py-8 px-4">
      <h1 className="text-3xl font-bold mb-4">Tutorial Title (ID: {id})</h1>
      <ProgressBar progress={50} />
      <div className="mt-6">Tutorial content and sections go here...</div>
    </div>
  );
};

export default TutorialDetailPage; 