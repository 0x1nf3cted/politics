from fastapi import APIRouter, HTTPException
from sklearn.metrics.pairwise import cosine_similarity
import pickle
from src.database import create_collection_from_articles, fetch_articles, retrieve_collection_data, get_collection
import os
router = APIRouter()

# Load the pre-trained model with error handling

model_path = os.path.join(os.path.dirname(__file__), "model")
try:
    with open(model_path, "rb") as model_file:
        model = pickle.load(model_file)
except Exception as e:
    raise RuntimeError(f"Failed to load the model: {e}")


@router.get("/collections")
async def retrieve_collections():
    try:
        collections = await retrieve_collection_data()
        return collections

    except Exception as e:
        print('Error retrieving collections:', e)
        raise HTTPException(
            status_code=500, detail="Error retrieving collections")


@router.get("/collections/{collection_id}")
async def get_collection_by_id(collection_id: str):
    try:
        collection = await get_collection(collection_id)
        return collection
    except ValueError as e:
        print(e)



async def get_articles_and_split():
    try:
        articles = await fetch_articles()
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

    if not articles:
        return []

    titles = [item.title for item in articles]


    """
    split articles in chunks of 100 articles each
    """
    chunk_size = 100
    articles_chunk = [titles[i:i + chunk_size] for i in range(0, len(titles), chunk_size)]

    """
    should create collections from each chunks
    """

@router.get("/similarity")
async def compare_titles():
    try:
        articles = await fetch_articles()
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

    if not articles:
        return []

    titles = [item.title for item in articles]


    """
    split articles in chunks of 100 articles each
    """
    chunk_size = 100
    articles_chunk = [titles[i:i + chunk_size] for i in range(0, len(titles), chunk_size)]

    
    # Encode titles using the pre-trained model
    try:
        embeddings = model.encode(titles)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error encoding titles: {e}")

    # Calculate cosine similarities
    similarities = cosine_similarity(embeddings)

    # Threshold for similarity
    threshold = 0.6

    # Create collections of articles
    collections = []
    visited = set()

    for i in range(len(articles)):
        if i not in visited:
            # Start a new collection with the current article
            collection = [articles[i]]
            visited.add(i)

            for j in range(i + 1, len(articles)):
                if j not in visited:
                    # Check similarity and different newspaperId
                    if similarities[i][j] > threshold and articles[i].newspaperId != articles[j].newspaperId:
                        collection.append(articles[j])
                        visited.add(j)

            collections.append(collection)

    result_collections = []
    for collection in collections:
        if (len(collection) > 1):
            created_collection = await create_collection_from_articles(collection, "title")
            result_collections.append(created_collection)

    return collections
