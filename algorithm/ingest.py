"""
Data Ingestion Module
Fetches live data from ApsnyTravel.ru and handles data validation
"""

import json
import requests
from typing import Dict, Any, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class DataIngestionError(Exception):
    """Custom exception for data ingestion errors"""
    pass


class DataIngestor:
    """Handles fetching and initial validation of data from ApsnyTravel.ru"""

    def __init__(self, source_url: str = "https://apsnytravel.ru/capsules.json", timeout: int = 30):
        """
        Initialize the data ingestor

        Args:
            source_url: The URL to fetch capsules.json from
            timeout: Request timeout in seconds
        """
        self.source_url = source_url
        self.timeout = timeout
        self.session = requests.Session()

    def fetch_live_data(self) -> Dict[str, Any]:
        """
        Fetch live capsules.json from ApsnyTravel.ru

        Returns:
            Dictionary containing the fetched data

        Raises:
            DataIngestionError: If the fetch fails
        """
        try:
            logger.info(f"Fetching data from {self.source_url}...")
            response = self.session.get(self.source_url, timeout=self.timeout)
            response.raise_for_status()

            data = response.json()
            logger.info(f"Successfully fetched {len(data.get('capsules', []))} capsules")
            return data

        except requests.exceptions.Timeout:
            raise DataIngestionError(f"Request timeout after {self.timeout} seconds")
        except requests.exceptions.ConnectionError as e:
            raise DataIngestionError(f"Connection error: {str(e)}")
        except requests.exceptions.HTTPError as e:
            raise DataIngestionError(f"HTTP error: {response.status_code} - {str(e)}")
        except json.JSONDecodeError:
            raise DataIngestionError("Failed to parse JSON response")
        except Exception as e:
            raise DataIngestionError(f"Unexpected error during data ingestion: {str(e)}")

    def validate_raw_data(self, data: Dict[str, Any]) -> bool:
        """
        Perform basic validation on the fetched data

        Args:
            data: The raw data dictionary

        Returns:
            True if data is valid

        Raises:
            DataIngestionError: If validation fails
        """
        if not isinstance(data, dict):
            raise DataIngestionError("Data must be a dictionary")

        if 'capsules' not in data:
            raise DataIngestionError("Data must contain 'capsules' key")

        if not isinstance(data['capsules'], list):
            raise DataIngestionError("'capsules' must be a list")

        if len(data['capsules']) == 0:
            raise DataIngestionError("No capsules found in data")

        logger.info(f"Raw data validation passed: {len(data['capsules'])} capsules found")
        return True

    def get_data_stats(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate statistics about the fetched data

        Args:
            data: The data dictionary

        Returns:
            Dictionary containing statistics
        """
        capsules = data.get('capsules', [])
        types = {}
        regions = {}

        for capsule in capsules:
            ctype = capsule.get('type', 'unknown')
            types[ctype] = types.get(ctype, 0) + 1

            geo = capsule.get('geo', {})
            region = geo.get('region', 'unknown')
            regions[region] = regions.get(region, 0) + 1

        return {
            'total_capsules': len(capsules),
            'types': types,
            'regions': regions,
            'timestamp': datetime.now().isoformat()
        }

    def close(self):
        """Close the session"""
        self.session.close()


def ingest_data(source_url: str = "https://apsnytravel.ru/capsules.json") -> Dict[str, Any]:
    """
    Convenience function to fetch and validate data in one call

    Args:
        source_url: The URL to fetch data from

    Returns:
        Dictionary containing the validated data

    Raises:
        DataIngestionError: If ingestion fails
    """
    ingestor = DataIngestor(source_url)
    try:
        data = ingestor.fetch_live_data()
        ingestor.validate_raw_data(data)
        stats = ingestor.get_data_stats(data)
        logger.info(f"Data ingestion complete: {stats}")
        return data
    finally:
        ingestor.close()
