from fastapi import APIRouter
from src.scrapper.service import ScraperService


router = APIRouter()


@router.get("/scrape")
async def scrape():
    scrape = ScraperService()
    await scrape.scrape()
