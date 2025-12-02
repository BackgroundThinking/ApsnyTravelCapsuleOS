"""
Orchestrator Module
Manages the execution of the entire algorithm pipeline
"""

import json
import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

from ingest import DataIngestor, DataIngestionError
from mapper import SchemaMapper, SchemaMappingError
from enrich import ContentEnricher
from graph import GraphBuilder
from models import CapsuleCollectionModel

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('algorithm.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


class AlgorithmOrchestrator:
    """Orchestrates the entire data synchronization and enrichment pipeline"""

    def __init__(self, source_url: str = "https://apsnytravel.ru/capsules.json",
                 output_dir: str = "../client/public"):
        """
        Initialize the orchestrator

        Args:
            source_url: URL to fetch capsules.json from
            output_dir: Directory to write output files to
        """
        self.source_url = source_url
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def run(self) -> bool:
        """
        Run the entire pipeline

        Returns:
            True if successful, False otherwise
        """
        try:
            logger.info("=" * 70)
            logger.info("Starting ApsnyTravel-CapsuleOS Synchronization Pipeline")
            logger.info("=" * 70)

            # Stage 1: Data Ingestion
            logger.info("\n[Stage 1] Data Ingestion")
            logger.info("-" * 70)
            raw_data = self._ingest_data()
            if not raw_data:
                return False

            # Stage 2: Schema Mapping & Validation
            logger.info("\n[Stage 2] Schema Mapping & Validation")
            logger.info("-" * 70)
            collection = self._map_and_validate(raw_data)
            if not collection:
                return False

            # Stage 3: Content Enrichment
            logger.info("\n[Stage 3] Content Enrichment")
            logger.info("-" * 70)
            collection = self._enrich_content(collection)

            # Stage 4: Relationship Discovery
            logger.info("\n[Stage 4] Relationship Discovery & Graph Building")
            logger.info("-" * 70)
            collection = self._build_graph(collection)

            # Stage 5: Data Serialization
            logger.info("\n[Stage 5] Data Serialization")
            logger.info("-" * 70)
            success = self._serialize_data(collection)
            if not success:
                return False

            logger.info("\n" + "=" * 70)
            logger.info("✅ Pipeline completed successfully!")
            logger.info("=" * 70)
            return True

        except Exception as e:
            logger.error(f"Pipeline failed: {str(e)}", exc_info=True)
            return False

    def _ingest_data(self) -> Dict[str, Any]:
        """
        Stage 1: Ingest data from source

        Returns:
            Raw data dictionary or None if failed
        """
        try:
            ingestor = DataIngestor(self.source_url)
            raw_data = ingestor.fetch_live_data()
            ingestor.validate_raw_data(raw_data)
            stats = ingestor.get_data_stats(raw_data)

            logger.info(f"✓ Data ingested successfully")
            logger.info(f"  Total capsules: {stats['total_capsules']}")
            logger.info(f"  Types: {stats['types']}")
            logger.info(f"  Regions: {stats['regions']}")

            ingestor.close()
            return raw_data

        except DataIngestionError as e:
            logger.error(f"✗ Data ingestion failed: {str(e)}")
            return None

    def _map_and_validate(self, raw_data: Dict[str, Any]) -> CapsuleCollectionModel:
        """
        Stage 2: Map and validate data

        Returns:
            CapsuleCollectionModel or None if failed
        """
        try:
            collection = SchemaMapper.map_collection(raw_data)
            SchemaMapper.validate_collection(collection)

            logger.info(f"✓ Schema mapping completed")
            logger.info(f"  Capsules mapped: {len(collection.capsules)}")
            logger.info(f"  Mapping errors: {collection.metadata.get('errors', 0)}")

            return collection

        except SchemaMappingError as e:
            logger.error(f"✗ Schema mapping failed: {str(e)}")
            return None

    def _enrich_content(self, collection: CapsuleCollectionModel) -> CapsuleCollectionModel:
        """
        Stage 3: Enrich content

        Returns:
            Enriched CapsuleCollectionModel
        """
        try:
            enriched_capsules = ContentEnricher.enrich_collection(collection.capsules)
            collection.capsules = enriched_capsules

            logger.info(f"✓ Content enrichment completed")
            logger.info(f"  Capsules enriched: {len(enriched_capsules)}")

            return collection

        except Exception as e:
            logger.error(f"✗ Content enrichment failed: {str(e)}")
            return collection

    def _build_graph(self, collection: CapsuleCollectionModel) -> CapsuleCollectionModel:
        """
        Stage 4: Build knowledge graph

        Returns:
            CapsuleCollectionModel with graph relationships
        """
        try:
            capsules_with_graph = GraphBuilder.build_graph(collection.capsules)
            collection.capsules = capsules_with_graph

            stats = GraphBuilder.get_graph_stats(capsules_with_graph)
            logger.info(f"✓ Knowledge graph built")
            logger.info(f"  Total edges: {stats['total_edges']}")
            logger.info(f"  Connected capsules: {stats['connected_capsules']}/{stats['total_capsules']}")
            logger.info(f"  Connectivity: {stats['connectivity_percentage']:.1f}%")

            return collection

        except Exception as e:
            logger.error(f"✗ Graph building failed: {str(e)}")
            return collection

    def _serialize_data(self, collection: CapsuleCollectionModel) -> bool:
        """
        Stage 5: Serialize data to JSON files

        Returns:
            True if successful, False otherwise
        """
        try:
            # Prepare output data
            output_data = {
                'capsules': [c.dict() for c in collection.capsules],
                'metadata': {
                    'total': len(collection.capsules),
                    'generated': datetime.now().isoformat(),
                    'version': '0.0.1',
                    'source': 'apsnytravel.ru'
                }
            }

            # Write capsules.json
            capsules_file = self.output_dir / 'capsules.json'
            with open(capsules_file, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, ensure_ascii=False, indent=2)

            logger.info(f"✓ Generated capsules.json ({capsules_file.stat().st_size / 1024:.1f} KB)")

            # Generate search index
            search_index = self._generate_search_index(collection.capsules)
            search_file = self.output_dir / 'search-index.json'
            with open(search_file, 'w', encoding='utf-8') as f:
                json.dump(search_index, f, ensure_ascii=False, indent=2)

            logger.info(f"✓ Generated search-index.json ({search_file.stat().st_size / 1024:.1f} KB)")

            # Generate structured data
            structured_data = self._generate_structured_data(collection.capsules)
            structured_file = self.output_dir / 'structured-data.json'
            with open(structured_file, 'w', encoding='utf-8') as f:
                json.dump(structured_data, f, ensure_ascii=False, indent=2)

            logger.info(f"✓ Generated structured-data.json ({structured_file.stat().st_size / 1024:.1f} KB)")

            return True

        except Exception as e:
            logger.error(f"✗ Data serialization failed: {str(e)}")
            return False

    @staticmethod
    def _generate_search_index(capsules) -> list:
        """Generate search index from capsules"""
        search_docs = []
        for capsule in capsules:
            search_docs.append({
                'id': capsule.id,
                'slug': capsule.slug,
                'title': capsule.title,
                'type': capsule.type,
                'description': capsule.seo.description,
                'keywords': capsule.seo.keywords,
                'content': capsule.content[:500],
                'region': capsule.geo.region,
                'emoji': capsule.emoji
            })
        return search_docs

    @staticmethod
    def _generate_structured_data(capsules) -> list:
        """Generate JSON-LD structured data from capsules"""
        structured_data = []
        for capsule in capsules:
            schema_type = 'Place' if capsule.type == 'place' else 'Product'
            structured_data.append({
                '@context': 'https://schema.org',
                '@type': schema_type,
                'name': capsule.title,
                'description': capsule.seo.description,
                'url': f"https://apsnytravel.com/capsule/{capsule.slug}",
                'keywords': ', '.join(capsule.seo.keywords),
                'geo': {
                    '@type': 'GeoCoordinates',
                    'latitude': capsule.geo.lat,
                    'longitude': capsule.geo.lng
                }
            })
        return structured_data


def main():
    """Main entry point"""
    orchestrator = AlgorithmOrchestrator()
    success = orchestrator.run()
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
