import asyncio
from scrapper.service import ScraperService
from database import seed


async def some_async_function():
    scraper = ScraperService()
    await scraper.scrape()


# Now, you need to run this asynchronous function within an event loop


async def main():
    # await some_async_function()
    await seed()


# Run the main function within an event loop
asyncio.run(main())
