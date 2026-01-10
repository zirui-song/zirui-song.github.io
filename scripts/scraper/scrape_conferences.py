#!/usr/bin/env python3
"""
Academic Conference Scraper

Aggregates conference information from multiple sources for Finance and Accounting
academic conferences. Updates _data/conferences.yml for Jekyll site.

Usage:
    python scrape_conferences.py
"""

import os
import sys
import yaml
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Dict

# Add sources directory to path
sys.path.insert(0, str(Path(__file__).parent))

from utils import merge_conferences, determine_status, validate_conference

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def load_manual_conferences(data_dir: Path) -> List[Dict]:
    """Load manually maintained conference data."""
    manual_file = data_dir / 'manual_conferences.yml'
    if manual_file.exists():
        with open(manual_file, 'r') as f:
            data = yaml.safe_load(f)
            return data.get('conferences', [])
    return []


def load_existing_conferences(data_dir: Path) -> List[Dict]:
    """Load existing conference data to preserve manual entries in main file."""
    conf_file = data_dir / 'conferences.yml'
    if conf_file.exists():
        with open(conf_file, 'r') as f:
            data = yaml.safe_load(f)
            return data.get('conferences', [])
    return []


def scrape_all_conferences() -> List[Dict]:
    """
    Run all scrapers and collect conference data.

    Currently imports from individual scraper modules.
    Each scraper returns a list of conference dictionaries.
    """
    all_conferences = []

    # Import and run each scraper
    scrapers = {
        'AFA': 'sources.afa',
        'WFA': 'sources.wfa',
        'EFA': 'sources.efa',
        'SFS': 'sources.sfs',
        'AAA': 'sources.aaa',
    }

    for name, module_name in scrapers.items():
        try:
            logger.info(f"Attempting to scrape {name}...")
            module = __import__(module_name, fromlist=['scrape'])
            if hasattr(module, 'scrape'):
                conferences = module.scrape()
                for conf in conferences:
                    if validate_conference(conf):
                        all_conferences.append(conf)
                        logger.info(f"  Found: {conf.get('name')}")
                    else:
                        logger.warning(f"  Invalid conference data: {conf}")
            else:
                logger.warning(f"  Module {module_name} has no scrape() function")
        except ImportError as e:
            logger.warning(f"  Scraper module not found: {module_name} ({e})")
        except Exception as e:
            logger.error(f"  Error scraping {name}: {e}")

    return all_conferences


def main():
    """Main entry point for conference scraper."""
    # Determine paths
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent.parent
    data_dir = repo_root / '_data'
    output_file = data_dir / 'conferences.yml'

    logger.info(f"Repository root: {repo_root}")
    logger.info(f"Data directory: {data_dir}")

    # Ensure data directory exists
    data_dir.mkdir(parents=True, exist_ok=True)

    # Load existing conferences (to preserve data that wasn't scraped)
    existing_conferences = load_existing_conferences(data_dir)
    logger.info(f"Loaded {len(existing_conferences)} existing conferences")

    # Scrape new conference data
    logger.info("Starting conference scraping...")
    scraped_conferences = scrape_all_conferences()
    logger.info(f"Scraped {len(scraped_conferences)} conferences")

    # Load manual conferences (these always take precedence)
    manual_conferences = load_manual_conferences(data_dir)
    logger.info(f"Loaded {len(manual_conferences)} manual conferences")

    # Merge: existing + scraped + manual (later sources take precedence)
    # First merge existing with scraped
    combined = merge_conferences(existing_conferences, scraped_conferences)
    # Then merge with manual entries
    all_conferences = merge_conferences(combined, manual_conferences)

    # Update status for all conferences
    for conf in all_conferences:
        conf['status'] = determine_status(conf)
        conf['last_verified'] = datetime.now(timezone.utc).strftime('%Y-%m-%d')

    # Sort by submission deadline (upcoming first, then by date)
    all_conferences.sort(key=lambda x: (
        x.get('status') == 'past',  # Past conferences last
        x.get('submission_deadline') or '9999-12-31'
    ))

    # Prepare output
    output_data = {
        'metadata': {
            'last_updated': datetime.now(timezone.utc).isoformat(),
            'scraper_version': '1.0.0',
            'total_conferences': len(all_conferences),
        },
        'conferences': all_conferences
    }

    # Write output
    with open(output_file, 'w') as f:
        yaml.dump(output_data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

    logger.info(f"Successfully wrote {len(all_conferences)} conferences to {output_file}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
