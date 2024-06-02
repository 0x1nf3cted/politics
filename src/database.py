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
    print(f"Collection '{collection_title}' created with ID: {new_collection.id}")
    return new_collection

async def create_article(articleUrl, author, category, title, date, summary, journal):
    # Find the newspaper by its name
    newspaper = await prisma.newspaper.find_first(
        where={"name": journal}
    )

    if newspaper is None:
        raise RuntimeError(f"Newspaper with name '{journal}' not found.")

    # Check if the article already exists
    existing_article = await prisma.article.find_first(
        where={"title": title, "newspaperId": newspaper.id}
    )

    if existing_article:
        print(f"Article with title '{title}' already exists.")
        return existing_article.id

    # Create the new article
    article = await prisma.article.create(
        data={
            "url": articleUrl,
            "author": author,
            "category": category,
            "title": title,
            "date": date,
            "description": summary,
            "newspaperId": newspaper.id  # Ensure the newspaperId is set
        }
    )
    return article.id


# async def seed():


#     newspapers = [
#         {
#             "name": "Le Monde",
#             "orientation": "centre gauche",
#             "url": "https://www.lemonde.fr",
#         },
#         {
#             "name": "Le Figaro",
#             "orientation": "droite",
#             "url": "https://www.lefigaro.fr",
#         },
#         {
#             "name": "Le Parisien",
#             "orientation": "centre droite",
#             "url": "https://www.leparisien.fr",
#         },
#         {
#             "name": "La Voix du Nord",
#             "orientation": "gauche",
#             "url": "https://www.lavoixdunord.fr",
#         },
#         {
#             "name": "Le Télégramme",
#             "orientation": "centre gauche",
#             "url": "https://www.letelegramme.fr",
#         },
#         {
#             "name": "Les Echos",
#             "orientation": "centre droite",
#             "url": "https://www.lesechos.fr",
#         },
#         {
#             "name": "Libération",
#             "orientation": "gauche",
#             "url": "https://www.liberation.fr",
#         },
#         {
#             "name": "La Croix",
#             "orientation": "gauche",
#             "url": "https://www.la-croix.com",
#         },
#         {
#             "name": "L’Humanité",
#             "orientation": "extrême gauche",
#             "url": "https://www.humanite.fr",
#         },
#         {
#             "name": "L’Opinion",
#             "orientation": "centre droite",
#             "url": "https://www.lopinion.fr",
#         },
#         {
#             "name": "L’Obs",
#             "orientation": "gauche",
#             "url": "https://www.nouvelobs.com",
#         },
#         {
#             "name": "L’Express",
#             "orientation": "droite",
#             "url": "https://www.lexpress.fr",
#         },
#         {
#             "name": "Le Point",
#             "orientation": "droite",
#             "url": "https://www.lepoint.fr",
#         },
#         {
#             "name": "Marianne",
#             "orientation": "extrême droite",
#             "url": "https://www.marianne.net",
#         },
#         {
#             "name": "Courrier international",
#             "orientation": "gauche",
#             "url": "https://www.courrierinternational.com",
#         },
#         {
#             "name": "Journal du dimanche",
#             "orientation": "extrême droite",
#             "url": "https://www.lejdd.fr",
#         },
#         {
#             "name": "Charlie Hebdo",
#             "orientation": "gauche",
#             "url": "https://charliehebdo.fr",
#         },
#         {
#             "name": "Alternatives économiques",
#             "orientation": "gauche",
#             "url": "https://www.alternatives-economiques.fr",
#         },
#         {
#             "name": "Valeurs actuelles",
#             "orientation": "extrême droite",
#             "url": "https://www.valeursactuelles.com",
#         },
#         {
#             "name": "Minute",
#             "orientation": "extrême droite",
#             "url": "http://www.minute-hebdo.fr",
#         },
#     ]

#     for newspaper in newspapers:
#         await create_newspaper(newspaper)


# Example usage (in an async function)
# import asyncio
# asyncio.run(create_article("http://example.com", "Author Name", "Category", "Title", "2024-05-26", "Summary", "Le Monde"))
