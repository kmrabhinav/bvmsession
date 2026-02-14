"""
Vector algebra operations and demonstrations.
"""

import numpy as np
from typing import List, Tuple, Dict
from scipy.spatial.distance import cosine


class VectorAlgebra:
    """Perform vector algebra operations."""
    
    @staticmethod
    def add_vectors(vectors: List[np.ndarray]) -> np.ndarray:
        """Add multiple vectors."""
        return np.sum(vectors, axis=0)
    
    @staticmethod
    def subtract_vector(base: np.ndarray, subtract: np.ndarray) -> np.ndarray:
        """Subtract one vector from another."""
        return base - subtract
    
    @staticmethod
    def normalize(vector: np.ndarray) -> np.ndarray:
        """Normalize vector to unit length."""
        return vector / np.linalg.norm(vector)
    
    @staticmethod
    def magnitude(vector: np.ndarray) -> float:
        """Calculate vector magnitude (length)."""
        return float(np.linalg.norm(vector))
    
    @staticmethod
    def dot_product(vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Calculate dot product of two vectors."""
        return float(np.dot(vec1, vec2))
    
    @staticmethod
    def cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Calculate cosine similarity between vectors (0 to 1)."""
        norm_vec1 = vec1 / np.linalg.norm(vec1)
        norm_vec2 = vec2 / np.linalg.norm(vec2)
        return float(np.dot(norm_vec1, norm_vec2))
    
    @staticmethod
    def cosine_distance(vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Calculate cosine distance between vectors (0 to 2)."""
        return float(cosine(vec1, vec2))
    
    @staticmethod
    def euclidean_distance(vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Calculate Euclidean distance between vectors."""
        return float(np.linalg.norm(vec1 - vec2))
    
    @staticmethod
    def vector_space_analysis(vectors: Dict[str, np.ndarray]) -> Dict:
        """
        Analyze a collection of vectors.
        
        Args:
            vectors: Dictionary of name -> vector
            
        Returns:
            Analysis dictionary
        """
        vector_list = list(vectors.values())
        names = list(vectors.keys())
        
        analysis = {
            'count': len(vectors),
            'dimensions': vector_list[0].shape[0] if vector_list else 0,
            'magnitudes': {name: VectorAlgebra.magnitude(vec) for name, vec in vectors.items()},
            'pairwise_similarities': {}
        }
        
        # Calculate pairwise similarities
        for i, name1 in enumerate(names):
            for name2 in names[i+1:]:
                sim = VectorAlgebra.cosine_similarity(vectors[name1], vectors[name2])
                pair = f"{name1} ↔ {name2}"
                analysis['pairwise_similarities'][pair] = sim
        
        return analysis
    
    @staticmethod
    def projection(vector: np.ndarray, onto: np.ndarray) -> np.ndarray:
        """Project vector onto another vector."""
        onto_normalized = onto / np.linalg.norm(onto)
        projection_length = np.dot(vector, onto_normalized)
        return projection_length * onto_normalized
    
    @staticmethod
    def angle_between(vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Calculate angle between two vectors in degrees."""
        cos_angle = VectorAlgebra.cosine_similarity(vec1, vec2)
        # Clamp to avoid numerical errors
        cos_angle = np.clip(cos_angle, -1.0, 1.0)
        angle_rad = np.arccos(cos_angle)
        return float(np.degrees(angle_rad))
