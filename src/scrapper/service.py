import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from src.database import create_article
from newsplease import NewsPlease, NewsArticle
from src.scrapper.constants import journeaux
from urllib.parse import urlparse, urljoin


class ScraperService:
    def __init__(self):
        self.nb_articles_scraped = 0
        self.articles_scraped_limit = 100

    # element and class_selector are for the parent element of the targeted <a>

    async def scrape(self):
        for journal in journeaux:
            self.nb_articles_scraped = 0  # Reset the count for each journal
            for category in journal["categories"]:
                url = journal["url"] + "/" + category
                response = requests.get(url)

                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    articles = soup.find_all(
                        journal["element_selector"], class_=journal["class_selector"])
                    links = []

                    for article in articles:
                        fixed_url = self.fix_url(
                            article.find('a'), journal["url"])
                        if fixed_url:
                            links.append(fixed_url)

                    for link in links:
                        if self.nb_articles_scraped >= self.articles_scraped_limit:
                            break  # Stop processing links if the limit is reached
                        await self.process_article(link, journal["name"])
                        self.nb_articles_scraped += 1  # Increment the count

                    if self.nb_articles_scraped >= self.articles_scraped_limit:
                        break  # Stop processing categories if the limit is reached

                else:
                    print(f"Failed to retrieve data. HTTP Status Code: {
                          response.status_code}")

        print("Finished")

    def fix_url(self, tag, base_url):
        # Ensure the tag exists and has an href attribute
        if tag and tag.has_attr('href'):
            url = tag['href']
        else:
            return None  # Or handle this case as needed

        # Parse the given URL
        parsed_url = urlparse(url)

        # Check if the scheme (e.g., http) and netloc (e.g., www.example.com) are missing
        if not parsed_url.scheme or not parsed_url.netloc:
            # Fix the URL by adding the base URL
            fixed_url = urljoin(base_url, url)
        else:
            fixed_url = url

        return fixed_url

    """
    check if the date of the article is either today or one of the seven last days
    """

    def is_date_valid(self, date_string):
        if date_string is None:
            return True
        else:
            input_date = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")

            today = datetime.now()
            seven_days_ago = today - timedelta(days=7)
            # Check if the input date is today or within the last seven days
            return seven_days_ago <= input_date <= today

    async def process_article(self, url, journal):
        article: NewsArticle = NewsPlease.from_url(url)

        try:
            # Check if the required properties are present
            if article:
                if article.date_publish is not None and article.title is not None and article.description is not None:
                    article_id = await create_article(
                        url,
                        "N/A",
                        "N/A",
                        article.title,
                        article.date_publish,
                        article.description,
                        journal
                    )
                    print(article_id)  # Handle or log the article ID
                    return article_id

            else:
                print("Missing required article properties")
        except ValueError as e:
            print(f"Error: {e}")
