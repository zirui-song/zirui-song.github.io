"""
SFS (Society for Financial Studies) Cavalcade Scraper
https://sfs.org/
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

BASE_URL = "https://sfs.org"
CAVALCADE_URL = f"{BASE_URL}/sfs-cavalcade/"


def scrape() -> List[Dict]:
    """Scrape SFS Cavalcade information."""
    conferences = []

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; AcademicConferenceScraper/1.0)'
        }
        response = requests.get(CAVALCADE_URL, timeout=30, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')

        content = soup.get_text()

        # Look for Cavalcade information
        year_pattern = r'Cavalcade\s+(?:North\s+America\s+)?(\d{4})|(\d{4})\s+Cavalcade'
        year_matches = re.findall(year_pattern, content, re.IGNORECASE)

        for match in year_matches:
            year = int(match[0] or match[1])

            if year < datetime.now().year:
                continue

            # Try to extract dates - typically May
            date_pattern = r'(\w+\s+\d+[-–]\d+,?\s*\d{4})'
            date_matches = re.findall(date_pattern, content)

            start_date, end_date = None, None
            for date_str in date_matches:
                if str(year) in date_str:
                    start_date, end_date = parse_date_range(date_str, year)
                    if start_date:
                        break

            # Try to find submission deadline
            deadline_pattern = r'(?:deadline|due).*?(\w+\s+\d+,?\s*\d{4})'
            deadline_match = re.search(deadline_pattern, content, re.IGNORECASE)
            submission_deadline = None
            if deadline_match:
                submission_deadline = parse_single_date(deadline_match.group(1), year)

            conferences.append({
                'name': f"SFS Cavalcade North America {year}",
                'short_name': 'SFS',
                'field': 'finance',
                'category': 'major',
                'year': year,
                'conference_dates': {
                    'start': start_date,
                    'end': end_date,
                },
                'submission_deadline': submission_deadline,
                'website': CAVALCADE_URL,
                'source': 'scraped',
            })

    except requests.RequestException as e:
        logger.error(f"Network error scraping SFS: {e}")
    except Exception as e:
        logger.error(f"Error scraping SFS: {e}")

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


def parse_single_date(date_str: str, default_year: int) -> str:
    """Parse a single date string."""
    date_str = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', date_str)

    formats = ['%B %d, %Y', '%B %d %Y', '%B %d']

    for fmt in formats:
        try:
            dt = datetime.strptime(date_str.strip(), fmt)
            if dt.year == 1900:
                dt = dt.replace(year=default_year)
            return dt.strftime('%Y-%m-%d')
        except ValueError:
            continue

    return None
