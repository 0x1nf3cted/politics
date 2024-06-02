import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
from src.scrapper.service import ScraperService

class TestScraperService(unittest.TestCase):

    @patch('scraper_service.requests.get')
    @patch('scraper_service.NewsPlease.from_url')
    @patch('scraper_service.create_article')
    def test_scrape(self, mock_create_article, mock_from_url, mock_requests_get):
        # Initialize ScraperService
        scraper_service = ScraperService()

        # Mock responses
        mock_requests_get.return_value.status_code = 200
        mock_response = MagicMock()
        mock_response.content = b'<html><body><a href="http://example.com/article1">Article 1</a></body></html>'
        mock_requests_get.return_value = mock_response

        mock_from_url.return_value = MagicMock(date_publish=datetime.now())

        # Call the method being tested
        scraper_service.scrape()

        # Assertions
        self.assertTrue(mock_requests_get.called)
        self.assertTrue(mock_create_article.called)

    def test_fix_url(self):
        # Initialize ScraperService
        scraper_service = ScraperService()

        # Test cases
        test_cases = [
            {'tag': None, 'base_url': 'http://example.com', 'expected': None},
            {'tag': {'href': 'article1'}, 'base_url': 'http://example.com', 'expected': 'http://example.com/article1'},
            {'tag': {'href': 'http://example.com/article1'}, 'base_url': 'http://example.com', 'expected': 'http://example.com/article1'}
        ]

        # Test each case
        for test_case in test_cases:
            result = scraper_service.fix_url(test_case['tag'], test_case['base_url'])
            self.assertEqual(result, test_case['expected'])

    def test_is_date_valid(self):
        # Initialize ScraperService
        scraper_service = ScraperService()

        # Test cases
        test_cases = [
            {'date_string': None, 'expected': True},  # No date provided
            {'date_string': datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'expected': True},  # Current date
            {'date_string': (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d %H:%M:%S"), 'expected': True},  # Five days ago
            {'date_string': (datetime.now() - timedelta(days=8)).strftime("%Y-%m-%d %H:%M:%S"), 'expected': False}  # Eight days ago
        ]

        # Test each case
        for test_case in test_cases:
            result = scraper_service.is_date_valid(test_case['date_string'])
            self.assertEqual(result, test_case['expected'])

if __name__ == '__main__':
    unittest.main()
