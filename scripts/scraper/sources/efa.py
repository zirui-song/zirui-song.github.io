"""
EFA (European Finance Association) Conference Scraper
https://www.european-finance.org/
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

BASE_URL = "https://www.european-finance.org"


def scrape() -> List[Dict]:
    """Scrape EFA annual meeting information."""
    conferences = []

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; AcademicConferenceScraper/1.0)'
        }
        response = requests.get(BASE_URL, timeout=30, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')

        content = soup.get_text()

        # Look for EFA meeting information
        year_pattern = r'EFA\s+(\d{4})|(\d{4})\s+EFA|Annual\s+Meeting\s+(\d{4})'
        year_matches = re.findall(year_pattern, content, re.IGNORECASE)

        for match in year_matches:
            year = int(match[0] or match[1] or match[2])

            if year < datetime.now().year:
                continue

            # Try to extract dates - typically August
            date_pattern = r'(\w+\s+\d+[-–]\d+,?\s*\d{4})'
            date_matches = re.findall(date_pattern, content)

            start_date, end_date = None, None
            for date_str in date_matches:
                if str(year) in date_str:
                    start_date, end_date = parse_date_range(date_str, year)
                    if start_date:
                        break

            # Try to extract location (European cities)
            location_pattern = r'(?:in|at)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*,?\s*(?:[A-Z][a-z]+)?)'
            location_match = re.search(location_pattern, content)
            location = location_match.group(1).strip() if location_match else None

            conferences.append({
                'name': f"EFA Annual Meeting {year}",
                'short_name': 'EFA',
                'field': 'finance',
                'category': 'major',
                'year': year,
                'conference_dates': {
                    'start': start_date,
                    'end': end_date,
                },
                'location': location,
                'website': BASE_URL,
                'source': 'scraped',
            })

    except requests.RequestException as e:
        logger.error(f"Network error scraping EFA: {e}")
    except Exception as e:
        logger.error(f"Error scraping EFA: {e}")

    return conferences


def parse_date_range(date_str: str, year: int) -> tuple:
    """Parse date range."""
    pattern = r'(\w+)\s+(\d+)[-–](\d+),?\s*(\d{4})?'
    match = re.match(pattern, date_str)

    if match:
        month = match.group(1)
        start_day = int(match.group(2))
        end_day = int(match.group(3))
        year = int(match.group(4)) if match.group(4) else year

        try:
            month_num = datetime.strptime(month[:3], '%b').month
            start = f"{year}-{month_num:02d}-{start_day:02d}"
            end = f"{year}-{month_num:02d}-{end_day:02d}"
            return start, end
        except ValueError:
            pass

    return None, None
