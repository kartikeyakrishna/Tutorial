import os
import meilisearch

MEILI_URL = os.getenv('MEILI_URL', 'http://localhost:7700')
MEILI_API_KEY = os.getenv('MEILI_API_KEY', None)

client = meilisearch.Client(MEILI_URL, MEILI_API_KEY)

TUTORIAL_INDEX = 'tutorials'
ARTICLE_INDEX = 'articles'
SNIPPET_INDEX = 'code_snippets'

# Indexing helpers
def index_tutorial(tutorial):
    client.index(TUTORIAL_INDEX).add_documents([tutorial])

def index_article(article):
    client.index(ARTICLE_INDEX).add_documents([article])

def index_snippet(snippet):
    client.index(SNIPPET_INDEX).add_documents([snippet])

# Search helpers
def search_tutorials(query, filters=None, facets=None):
    return client.index(TUTORIAL_INDEX).search(query, {'filter': filters, 'facets': facets})

def search_articles(query, filters=None, facets=None):
    return client.index(ARTICLE_INDEX).search(query, {'filter': filters, 'facets': facets})

def search_snippets(query, filters=None, facets=None):
    return client.index(SNIPPET_INDEX).search(query, {'filter': filters, 'facets': facets})

def update_tutorial(tutorial):
    client.index(TUTORIAL_INDEX).update_documents([tutorial])

def delete_tutorial(tutorial_id):
    client.index(TUTORIAL_INDEX).delete_document(tutorial_id)

def update_article(article):
    client.index(ARTICLE_INDEX).update_documents([article])

def delete_article(article_id):
    client.index(ARTICLE_INDEX).delete_document(article_id)

def update_snippet(snippet):
    client.index(SNIPPET_INDEX).update_documents([snippet])

def delete_snippet(snippet_id):
    client.index(SNIPPET_INDEX).delete_document(snippet_id) 