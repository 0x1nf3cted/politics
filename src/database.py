from datetime import datetime
import os
from dotenv import load_dotenv
from fastapi import HTTPException
from src.prisma import prisma

# Load environment variables
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# Initialize Prisma Client


async def fetch_articles():
    try:
        articles = await prisma.article.find_many()
        return articles
    except Exception as e:
        raise RuntimeError(f"Error querying the database: {e}")


async def create_newspaper(data):
    try:
        print(f"Creating newspaper: {data['name']}")
        newspaper = await prisma.newspaper.create(
            data={
                "name": data["name"],
                "url": data["url"],
                "orientation": data["orientation"],
            }
        )
        return newspaper
    except Exception as e:
        raise RuntimeError(f"Error creating newspaper: {e}")


async def remove_duplicates(articles):
    unique_articles = []
    seen_urls = set()
    for article in articles:
        if article.url not in seen_urls:
            unique_articles.append(article)
            seen_urls.add(article.url)
    return unique_articles


async def get_collection(id: str):
    collection = await prisma.collection.find_first(
        where={"id": id},
        include={"articles": True}
    )
    if collection is None:
        raise HTTPException(status_code=404, detail="Collection not found")
    return collection


async def retrieve_collection_data():
    collections = await prisma.collection.find_many()
    return collections


async def create_collection_from_articles(articles, collection_title):
    articles = await remove_duplicates(articles)
    article_ids = [article.id for article in articles]
    current_date = datetime.now()
    collection_title = articles[0].title if articles else collection_title
    new_collection = await prisma.collection.create(
        data={
            'title': collection_title,
            'date': current_date,
            'category': "N/A",
            'articles': {
                'connect': [{'id': article_id} for article_id in article_ids]
            }
        }
    )
    await prisma.article.update_many(
        where={'id': {'in': article_ids}},
        data={'collectionId': new_collection.id}
    )
    print(f"Collection '{collection_title}' created with ID: {
          new_collection.id}")
    return new_collection

