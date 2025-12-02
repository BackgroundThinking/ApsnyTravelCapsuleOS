#!/usr/bin/env python3
"""
ApsnyTravel-CapsuleOS Synchronization Script
Fetches live data from ApsnyTravel.ru and synchronizes it with CapsuleOS
This script should be called as part of the build process
"""

import sys
import os

# Add algorithm directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'algorithm'))

from orchestrator import AlgorithmOrchestrator
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def main():
    """Main entry point for the synchronization script"""
    
    print("\n" + "=" * 70)
    print("ApsnyTravel-CapsuleOS Synchronization")
    print("=" * 70 + "\n")
    
    # Get configuration from environment or use defaults
    source_url = os.getenv(
        'APSNYTRAVEL_SOURCE_URL',
        'https://apsnytravel.ru/capsules.json'
    )
    
    output_dir = os.getenv(
        'CAPSULEOS_OUTPUT_DIR',
        os.path.join(os.path.dirname(__file__), '..', 'client', 'public')
    )
    
    logger.info(f"Source URL: {source_url}")
    logger.info(f"Output Directory: {output_dir}\n")
    
    # Run the orchestrator
    orchestrator = AlgorithmOrchestrator(source_url=source_url, output_dir=output_dir)
    success = orchestrator.run()
    
    if success:
        print("\n" + "=" * 70)
        print("✅ Synchronization completed successfully!")
        print("=" * 70 + "\n")
        return 0
    else:
        print("\n" + "=" * 70)
        print("❌ Synchronization failed!")
        print("=" * 70 + "\n")
        return 1


if __name__ == '__main__':
    sys.exit(main())
