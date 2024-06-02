# Utility functions for collections
def filter_articles(articles, threshold):
    filtered = [article for article in articles if article['score'] > threshold]
    return filtered
