"""
AFA (American Finance Association) Conference Scraper
https://www.afajof.org/
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)

BASE_URL = "https://www.afajof.org"
ANNUAL_MEETING_URL = f"{BASE_URL}/annual-meeting"


def scrape() -> List[Dict]:
    """Scrape AFA annual meeting information."""
    conferences = []

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (compatible; AcademicConferenceScraper/1.0)'
        }
        response = requests.get(ANNUAL_MEETING_URL, timeout=30, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')

        # Extract text content
        content = soup.get_text()

        # Look for annual meeting information
        # Pattern variations: "2026 AFA Annual Meeting" or "AFA Annual Meeting 2026"
        year_pattern = r'(\d{4})\s+AFA\s+Annual\s+Meeting|AFA\s+Annual\s+Meeting\s+(\d{4})'
        year_matches = re.findall(year_pattern, content, re.IGNORECASE)

        for match in year_matches:
            year = int(match[0] or match[1])

            # Only process future meetings
            if year < datetime.now().year:
                continue

            # Try to extract dates
            date_pattern = rf'{year}.*?(\w+\s+\d+[-–]\d+,?\s*{year})'
            date_match = re.search(date_pattern, content, re.IGNORECASE | re.DOTALL)

            start_date, end_date = None, None
            if date_match:
                start_date, end_date = parse_date_range(date_match.group(1), year)

            # Try to extract location
            location_pattern = r'(?:in|at)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*,\s*[A-Z]{2})'
            location_match = re.search(location_pattern, content)
            location = location_match.group(1) if location_match else None

            # Try to extract submission deadline
            deadline_pattern = r'submission\s+deadline.*?(\w+\s+\d+,?\s*\d{4})'
            deadline_match = re.search(deadline_pattern, content, re.IGNORECASE)
            submission_deadline = None
            if deadline_match:
                submission_deadline = parse_single_date(deadline_match.group(1), year - 1)

            conferences.append({
                'name': f"AFA Annual Meeting {year}",
                'short_name': 'AFA',
                'field': 'finance',
                'category': 'major',
                'year': year,
                'conference_dates': {
                    'start': start_date,
                    'end': end_date,
                },
                'location': location,
                'submission_deadline': submission_deadline,
                'website': ANNUAL_MEETING_URL,
                'cfp_url': f"{BASE_URL}/call-for-papers",
                'source': 'scraped',
                'notes': 'Joint with ASSA. PhD poster session available.',
            })

    except requests.RequestException as e:
        logger.error(f"Network error scraping AFA: {e}")
    except Exception as e:
        logger.error(f"Error scraping AFA: {e}")

    return conferences


def parse_date_range(date_str: str, year: int) -> tuple:
    """Parse date range like 'January 3-5, 2026'."""
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


def parse_single_date(date_str: str, default_year: int) -> Optional[str]:
    """Parse a single date string."""
    date_str = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', date_str)

    formats = [
        '%B %d, %Y',
        '%B %d %Y',
        '%B %d',
    ]

    for fmt in formats:
        try:
            dt = datetime.strptime(date_str.strip(), fmt)
            if dt.year == 1900:
                dt = dt.replace(year=default_year)
            return dt.strftime('%Y-%m-%d')
        except ValueError:
            continue

    return None
