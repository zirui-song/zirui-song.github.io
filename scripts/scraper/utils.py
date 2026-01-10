"""
Shared utilities for conference scrapers
"""

from datetime import datetime, date
from typing import Dict, List, Optional, Any
import re
import logging

logger = logging.getLogger(__name__)


def normalize_date(date_input: Any) -> Optional[date]:
    """Convert various date formats to date object."""
    if date_input is None:
        return None

    if isinstance(date_input, date):
        return date_input

    if isinstance(date_input, datetime):
        return date_input.date()

    if isinstance(date_input, str):
        # Clean ordinal suffixes
        date_str = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', date_input)

        formats = [
            '%Y-%m-%d',
            '%m/%d/%Y',
            '%B %d, %Y',
            '%b %d, %Y',
            '%B %d %Y',
            '%b %d %Y',
        ]
        for fmt in formats:
            try:
                return datetime.strptime(date_str.strip(), fmt).date()
            except ValueError:
                continue

    return None


def parse_date_range(date_str: str, default_year: int) -> tuple:
    """
    Parse date range like 'January 3-5, 2026' or 'June 21-24, 2026'.
    Returns (start_date, end_date) as ISO format strings.
    """
    patterns = [
        # "January 3-5, 2026"
        r'(\w+)\s+(\d+)\s*[-–]\s*(\d+),?\s*(\d{4})?',
        # "January 3 - January 5, 2026"
        r'(\w+)\s+(\d+)\s*[-–]\s*(\w+)\s+(\d+),?\s*(\d{4})?',
    ]

    for pattern in patterns:
        match = re.match(pattern, date_str.strip())
        if match:
            groups = match.groups()

            if len(groups) == 4:
                # Same month format
                month = groups[0]
                start_day = int(groups[1])
                end_day = int(groups[2])
                year = int(groups[3]) if groups[3] else default_year

                try:
                    month_num = datetime.strptime(month[:3], '%b').month
                    start = f"{year}-{month_num:02d}-{start_day:02d}"
                    end = f"{year}-{month_num:02d}-{end_day:02d}"
                    return start, end
                except ValueError:
                    continue

    return None, None


def parse_single_date(date_str: str, default_year: int) -> Optional[str]:
    """Parse a single date string and return ISO format."""
    # Clean ordinal suffixes
    date_str = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', date_str)

    formats = [
        ('%B %d, %Y', True),
        ('%B %d %Y', True),
        ('%b %d, %Y', True),
        ('%b %d %Y', True),
        ('%B %d', False),
        ('%b %d', False),
    ]

    for fmt, has_year in formats:
        try:
            dt = datetime.strptime(date_str.strip(), fmt)
            if not has_year:
                dt = dt.replace(year=default_year)
            return dt.strftime('%Y-%m-%d')
        except ValueError:
            continue

    return None


def validate_conference(conf: Dict) -> bool:
    """Validate conference data has required fields."""
    required = ['name', 'short_name', 'year']
    return all(conf.get(field) for field in required)


def merge_conferences(scraped: List[Dict], manual: List[Dict]) -> List[Dict]:
    """
    Merge scraped and manual conference data.
    Manual entries take precedence for matching conferences.
    """
    # Create lookup by (short_name, year)
    merged = {}

    # Add scraped conferences
    for conf in scraped:
        key = (conf.get('short_name'), conf.get('year'))
        merged[key] = conf.copy()

    # Override with manual conferences
    for conf in manual:
        key = (conf.get('short_name'), conf.get('year'))
        if key in merged:
            # Merge: manual values override scraped
            merged[key].update({k: v for k, v in conf.items() if v is not None})
        else:
            merged[key] = conf.copy()

    return list(merged.values())


def determine_status(conf: Dict) -> str:
    """Determine conference status based on dates."""
    from datetime import timezone
    today = datetime.now(timezone.utc).date()

    # Check if conference is past
    if conf.get('conference_dates', {}).get('end'):
        end_date = normalize_date(conf['conference_dates']['end'])
        if end_date and end_date < today:
            return 'past'

    # Check submission deadline
    if conf.get('submission_deadline'):
        deadline = normalize_date(conf['submission_deadline'])
        if deadline:
            if deadline > today:
                return 'submissions_open'
            else:
                return 'submissions_closed'

    return 'upcoming'


def clean_text(text: str) -> str:
    """Clean and normalize text from HTML."""
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    return text
