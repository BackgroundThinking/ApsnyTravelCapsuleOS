"""
Relationship Discovery & Graph Building Module
Intelligently discovers and maps relationships between capsules
"""

import logging
from typing import List, Dict, Set, Tuple
from models import CapsuleModel
import re

logger = logging.getLogger(__name__)


class GraphBuilder:
    """Builds a knowledge graph by discovering relationships between capsules"""

    # Define type hierarchies
    TYPE_HIERARCHY = {
        'product': 1,  # Top level
        'place': 2,    # Middle level
        'guide': 2     # Middle level
    }

    @staticmethod
    def calculate_similarity(text1: str, text2: str) -> float:
        """
        Calculate similarity between two texts using simple keyword matching

        Args:
            text1: First text
            text2: Second text

        Returns:
            Similarity score between 0 and 1
        """
        # Extract words
        words1 = set(re.findall(r'\b\w{3,}\b', text1.lower()))
        words2 = set(re.findall(r'\b\w{3,}\b', text2.lower()))

        if not words1 or not words2:
            return 0.0

        # Calculate Jaccard similarity
        intersection = len(words1 & words2)
        union = len(words1 | words2)

        return intersection / union if union > 0 else 0.0

    @staticmethod
    def find_parent_capsules(capsule: CapsuleModel, all_capsules: List[CapsuleModel]) -> List[str]:
        """
        Find parent capsules for a given capsule

        Args:
            capsule: The capsule to find parents for
            all_capsules: All available capsules

        Returns:
            List of parent capsule IDs
        """
        parents = []

        # Products are top-level, so they have no parents
        if capsule.type == 'product':
            return parents

        # Places and guides can have product parents
        for other in all_capsules:
            if other.type == 'product':
                # Check if the product mentions this place/guide
                similarity = GraphBuilder.calculate_similarity(
                    other.title + ' ' + other.content,
                    capsule.title + ' ' + capsule.content
                )

                if similarity > 0.15:  # Threshold for parent relationship
                    parents.append(other.id)

        return parents

    @staticmethod
    def find_related_capsules(capsule: CapsuleModel, all_capsules: List[CapsuleModel]) -> List[str]:
        """
        Find related capsules for a given capsule

        Args:
            capsule: The capsule to find related items for
            all_capsules: All available capsules

        Returns:
            List of related capsule IDs
        """
        related = []

        for other in all_capsules:
            # Skip self
            if other.id == capsule.id:
                continue

            # Calculate similarity
            similarity = GraphBuilder.calculate_similarity(
                capsule.title + ' ' + capsule.content,
                other.title + ' ' + other.content
            )

            # Check geographic proximity
            geo_distance = GraphBuilder.calculate_geo_distance(
                capsule.geo.lat, capsule.geo.lng,
                other.geo.lat, other.geo.lng
            )

            # Combine scores
            combined_score = (similarity * 0.7) + ((1 - min(geo_distance / 100, 1)) * 0.3)

            if combined_score > 0.25:  # Threshold for related relationship
                related.append(other.id)

        return related

    @staticmethod
    def find_sibling_capsules(capsule: CapsuleModel, all_capsules: List[CapsuleModel]) -> List[str]:
        """
        Find sibling capsules (same type, same region)

        Args:
            capsule: The capsule to find siblings for
            all_capsules: All available capsules

        Returns:
            List of sibling capsule IDs
        """
        siblings = []

        for other in all_capsules:
            # Skip self
            if other.id == capsule.id:
                continue

            # Same type and region
            if (other.type == capsule.type and
                other.geo.region == capsule.geo.region):
                siblings.append(other.id)

        return siblings

    @staticmethod
    def calculate_geo_distance(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
        """
        Calculate approximate distance between two geographic points in kilometers

        Args:
            lat1, lng1: First point coordinates
            lat2, lng2: Second point coordinates

        Returns:
            Distance in kilometers (approximate)
        """
        # Simple approximation using Pythagorean theorem
        # For more accuracy, use Haversine formula
        lat_diff = (lat2 - lat1) * 111  # 1 degree latitude ≈ 111 km
        lng_diff = (lng2 - lng1) * 111 * (1 / (1 + ((lat1 + lat2) / 2) ** 2) ** 0.5)

        distance = (lat_diff ** 2 + lng_diff ** 2) ** 0.5
        return distance

    @staticmethod
    def build_graph(capsules: List[CapsuleModel]) -> List[CapsuleModel]:
        """
        Build a knowledge graph by discovering relationships between all capsules

        Args:
            capsules: List of capsules to build graph for

        Returns:
            List of capsules with updated relationship links
        """
        logger.info("Building knowledge graph...")

        for i, capsule in enumerate(capsules):
            # Find parents
            parents = GraphBuilder.find_parent_capsules(capsule, capsules)
            capsule.links.parent = parents

            # Find children (reverse of parent relationship)
            children = [c.id for c in capsules if capsule.id in c.links.parent]
            capsule.links.children = children

            # Find related capsules
            related = GraphBuilder.find_related_capsules(capsule, capsules)
            capsule.links.related = related

            # Find siblings
            siblings = GraphBuilder.find_sibling_capsules(capsule, capsules)
            capsule.links.siblings = siblings

            if (i + 1) % 10 == 0:
                logger.debug(f"Processed {i + 1}/{len(capsules)} capsules")

        logger.info(f"Knowledge graph built with {len(capsules)} capsules")
        return capsules

    @staticmethod
    def get_graph_stats(capsules: List[CapsuleModel]) -> Dict[str, any]:
        """
        Generate statistics about the knowledge graph

        Args:
            capsules: List of capsules

        Returns:
            Dictionary containing graph statistics
        """
        total_edges = 0
        connected_capsules = 0
        orphaned_capsules = 0

        for capsule in capsules:
            edge_count = (len(capsule.links.parent) +
                         len(capsule.links.children) +
                         len(capsule.links.related) +
                         len(capsule.links.siblings))

            total_edges += edge_count

            if edge_count > 0:
                connected_capsules += 1
            else:
                orphaned_capsules += 1

        return {
            'total_capsules': len(capsules),
            'total_edges': total_edges,
            'connected_capsules': connected_capsules,
            'orphaned_capsules': orphaned_capsules,
            'connectivity_percentage': (connected_capsules / len(capsules) * 100) if capsules else 0
        }
