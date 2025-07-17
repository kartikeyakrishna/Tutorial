import React from 'react';
import SearchBar from '../components/SearchBar';
import ArticleCard from '../components/ArticleCard';
import { useArticleSearch } from '../hooks/useArticleSearch';

const ArticleListPage: React.FC = () => {
  const { articles, isLoading, error, search, setSearch } = useArticleSearch();

  return (
    <div className="max-w-6xl mx-auto py-8 px-4">
      <h1 className="text-3xl font-bold mb-6">Articles</h1>
      <SearchBar value={search} onChange={setSearch} placeholder="Search articles..." />
      {isLoading && <div>Loading...</div>}
      {error && <div className="text-red-500">{error}</div>}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mt-6">
        {articles.map(article => (
          <ArticleCard key={article.id} article={article} />
        ))}
      </div>
    </div>
  );
};

export default ArticleListPage; 