"""
AAA (American Accounting Association) Conference Scraper
https://aaahq.org/
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

BASE_URL = "https://aaahq.org"
MEETINGS_URL = f"{BASE_URL}/Meetings"


def scrape() -> List[Dict]:
    """Scrape AAA annual meeting information."""
    conferences = []

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; AcademicConferenceScraper/1.0)'
        }
        response = requests.get(MEETINGS_URL, timeout=30, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')

        content = soup.get_text()

        # Look for AAA Annual Meeting
        year_pattern = r'Annual\s+Meeting\s+(\d{4})|(\d{4})\s+Annual\s+Meeting'
        year_matches = re.findall(year_pattern, content, re.IGNORECASE)

        for match in year_matches:
            year = int(match[0] or match[1])

            if year < datetime.now().year:
                continue

            # Try to extract dates - typically August
            date_pattern = r'(\w+\s+\d+[-–]\d+,?\s*\d{4})'
            date_matches = re.findall(date_pattern, content)

            start_date, end_date = None, None
            for date_str in date_matches:
                if str(year) in date_str and 'august' in date_str.lower():
                    start_date, end_date = parse_date_range(date_str, year)
                    if start_date:
                        break

            # Try to extract location
            location_pattern = r'(?:in|at)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*,\s*[A-Z]{2})'
            location_match = re.search(location_pattern, content)
            location = location_match.group(1) if location_match else None

            conferences.append({
                'name': f"AAA Annual Meeting {year}",
                'short_name': 'AAA',
                'field': 'accounting',
                'category': 'major',
                'year': year,
                'conference_dates': {
                    'start': start_date,
                    'end': end_date,
                },
                'location': location,
                'website': MEETINGS_URL,
                'source': 'scraped',
                'notes': 'Largest accounting conference. Multiple sections.',
            })

    except requests.RequestException as e:
        logger.error(f"Network error scraping AAA: {e}")
    except Exception as e:
        logger.error(f"Error scraping AAA: {e}")

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
