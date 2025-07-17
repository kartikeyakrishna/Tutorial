import React from 'react';
import SearchBar from '../components/SearchBar';
import TutorialCard from '../components/TutorialCard';
import { useTutorialSearch } from '../hooks/useTutorialSearch';

const TutorialListPage: React.FC = () => {
  const { tutorials, isLoading, error, search, setSearch } = useTutorialSearch();

  return (
    <div className="max-w-6xl mx-auto py-8 px-4">
      <h1 className="text-3xl font-bold mb-6">Tutorials</h1>
      <SearchBar value={search} onChange={setSearch} placeholder="Search tutorials..." />
      {isLoading && <div>Loading...</div>}
      {error && <div className="text-red-500">{error}</div>}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mt-6">
        {tutorials.map(tutorial => (
          <TutorialCard key={tutorial.id} tutorial={tutorial} />
        ))}
      </div>
    </div>
  );
};

export default TutorialListPage; 