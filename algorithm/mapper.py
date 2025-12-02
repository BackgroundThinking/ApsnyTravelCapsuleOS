"""
Schema Mapping & Validation Module
Maps source data to CapsuleOS schema and validates integrity
"""

import logging
from typing import Dict, Any, List
from models import CapsuleModel, CapsuleCollectionModel, GeoModel, SEOModel, LinksModel, MetadataModel
from pydantic import ValidationError

logger = logging.getLogger(__name__)


class SchemaMappingError(Exception):
    """Custom exception for schema mapping errors"""
    pass


class SchemaMapper:
    """Maps source data to CapsuleOS schema"""

    @staticmethod
    def map_capsule(source_capsule: Dict[str, Any]) -> CapsuleModel:
        """
        Map a source capsule to the CapsuleOS schema

        Args:
            source_capsule: The source capsule data

        Returns:
            A validated CapsuleModel instance

        Raises:
            SchemaMappingError: If mapping fails
        """
        try:
            # Extract required fields
            capsule_id = source_capsule.get('id')
            capsule_type = source_capsule.get('type')
            title = source_capsule.get('title')
            content = source_capsule.get('content', '')

            if not all([capsule_id, capsule_type, title]):
                raise SchemaMappingError(f"Missing required fields in capsule: {capsule_id}")

            # Map geospatial data
            geo_data = source_capsule.get('geo', {})
            geo = GeoModel(
                lat=geo_data.get('lat', 0.0),
                lng=geo_data.get('lng', 0.0),
                region=geo_data.get('region', 'unknown')
            )

            # Map SEO data
            seo_data = source_capsule.get('seo', {})
            seo = SEOModel(
                title=seo_data.get('title', title),
                description=seo_data.get('description', f"Discover {title}"),
                keywords=seo_data.get('keywords', [title.lower()])
            )

            # Map links
            links_data = source_capsule.get('links', {})
            links = LinksModel(
                parent=links_data.get('parent', []),
                children=links_data.get('children', []),
                related=links_data.get('related', []),
                siblings=links_data.get('siblings', [])
            )

            # Map metadata
            metadata_data = source_capsule.get('metadata', {})
            metadata = MetadataModel(
                created=metadata_data.get('created', '2025-01-01'),
                updated=metadata_data.get('updated', '2025-12-02'),
                source=metadata_data.get('source', 'apsnytravel.ru'),
                version=metadata_data.get('version', '1.0')
            )

            # Create the capsule model
            capsule = CapsuleModel(
                id=capsule_id,
                type=capsule_type,
                tier=source_capsule.get('tier', 2),
                slug=source_capsule.get('slug', f"{capsule_type}/{capsule_id}"),
                title=title,
                emoji=source_capsule.get('emoji', '📍'),
                geo=geo,
                links=links,
                seo=seo,
                content=content,
                metadata=metadata
            )

            logger.debug(f"Successfully mapped capsule: {capsule_id}")
            return capsule

        except ValidationError as e:
            raise SchemaMappingError(f"Validation error for capsule {source_capsule.get('id')}: {str(e)}")
        except Exception as e:
            raise SchemaMappingError(f"Unexpected error mapping capsule: {str(e)}")

    @staticmethod
    def map_collection(source_data: Dict[str, Any]) -> CapsuleCollectionModel:
        """
        Map a collection of source capsules to CapsuleOS schema

        Args:
            source_data: The source data dictionary

        Returns:
            A validated CapsuleCollectionModel instance

        Raises:
            SchemaMappingError: If mapping fails
        """
        try:
            source_capsules = source_data.get('capsules', [])
            mapped_capsules = []
            errors = []

            for i, source_capsule in enumerate(source_capsules):
                try:
                    mapped_capsule = SchemaMapper.map_capsule(source_capsule)
                    mapped_capsules.append(mapped_capsule)
                except SchemaMappingError as e:
                    errors.append(f"Capsule {i}: {str(e)}")
                    logger.warning(f"Failed to map capsule {i}: {str(e)}")

            if errors:
                logger.warning(f"Mapping completed with {len(errors)} errors")

            # Create the collection
            collection = CapsuleCollectionModel(
                capsules=mapped_capsules,
                metadata={
                    'total': len(mapped_capsules),
                    'errors': len(errors),
                    'source': 'apsnytravel.ru',
                    'version': '0.0.1'
                }
            )

            logger.info(f"Successfully mapped {len(mapped_capsules)} capsules")
            return collection

        except Exception as e:
            raise SchemaMappingError(f"Failed to map collection: {str(e)}")

    @staticmethod
    def validate_collection(collection: CapsuleCollectionModel) -> bool:
        """
        Validate a capsule collection for integrity

        Args:
            collection: The collection to validate

        Returns:
            True if valid

        Raises:
            SchemaMappingError: If validation fails
        """
        issues = []

        # Check for duplicate IDs
        ids = [c.id for c in collection.capsules]
        if len(ids) != len(set(ids)):
            issues.append("Duplicate capsule IDs found")

        # Check for duplicate slugs
        slugs = [c.slug for c in collection.capsules]
        if len(slugs) != len(set(slugs)):
            issues.append("Duplicate slugs found")

        # Check for broken links
        id_set = set(ids)
        for capsule in collection.capsules:
            for link_type in ['parent', 'children', 'related', 'siblings']:
                for link_id in getattr(capsule.links, link_type):
                    if link_id not in id_set:
                        issues.append(f"Capsule {capsule.id}: Broken {link_type} link to {link_id}")

        if issues:
            logger.error(f"Validation failed with {len(issues)} issues:")
            for issue in issues:
                logger.error(f"  - {issue}")
            raise SchemaMappingError(f"Collection validation failed: {len(issues)} issues")

        logger.info("Collection validation passed")
        return True
