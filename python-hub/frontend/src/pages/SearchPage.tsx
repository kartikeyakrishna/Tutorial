import React from 'react';
import SearchBar from '../components/SearchBar';
import { useAdvancedSearch } from '../hooks/useAdvancedSearch';
import TutorialCard from '../components/TutorialCard';
import ArticleCard from '../components/ArticleCard';

const SearchPage: React.FC = () => {
  const { query, setQuery, results, isLoading, error } = useAdvancedSearch();
  return (
    <div className="max-w-6xl mx-auto py-8 px-4">
      <h1 className="text-3xl font-bold mb-6">Search</h1>
      <SearchBar value={query} onChange={setQuery} placeholder="Search tutorials, articles, code snippets..." />
      {isLoading && <div>Loading...</div>}
      {error && <div className="text-red-500">{error}</div>}
      <div className="mt-8">
        <h2 className="text-xl font-semibold mb-4">Tutorials</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {results.tutorials.map((t: any) => <TutorialCard key={t.id} tutorial={t} />)}
        </div>
        <h2 className="text-xl font-semibold mt-8 mb-4">Articles</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {results.articles.map((a: any) => <ArticleCard key={a.id} article={a} />)}
        </div>
        {/* TODO: Add code snippets results */}
      </div>
    </div>
  );
};

export default SearchPage; 