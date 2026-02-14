"""
Word Embedding utilities for vector algebra demonstrations.
Uses pre-trained word embeddings to show how words map to vectors.
"""

import numpy as np
import gensim.downloader as api
from typing import Tuple, List, Dict
import warnings

warnings.filterwarnings('ignore')


class WordEmbeddings:
    """Manages word embeddings and vector operations."""
    
    def __init__(self, model_name: str = "glove-wiki-gigaword-100"):
        """
        Initialize word embeddings model.
        
        Args:
            model_name: Name of pre-trained model to download
                       Available: "glove-wiki-gigaword-100", "word2vec-google-news-300"
        """
        self.model_name = model_name
        print(f"Loading {model_name} model... (this may take a moment)")
        self.model = api.load(model_name)
        self.vector_size = self.model.vector_size
        print(f"✓ Model loaded. Vector dimensions: {self.vector_size}")
    
    def get_vector(self, word: str) -> np.ndarray:
        """Get the vector representation of a word."""
        if word in self.model:
            return self.model[word]
        else:
            raise ValueError(f"Word '{word}' not in vocabulary")
    
    def vector_arithmetic(self, positive: List[str], negative: List[str]) -> Tuple[np.ndarray, str]:
        """
        Perform vector arithmetic: add positive words, subtract negative words.
        
        Args:
            positive: Words to add (e.g., ["queen", "man"])
            negative: Words to subtract (e.g., ["king"])
            
        Returns:
            Tuple of (resulting vector, calculation description)
        """
        result_vector = np.zeros(self.vector_size)
        
        # Add positive words
        for word in positive:
            result_vector += self.get_vector(word)
        
        # Subtract negative words
        for word in negative:
            result_vector -= self.get_vector(word)
        
        # Normalize
        result_vector = result_vector / np.linalg.norm(result_vector)
        
        # Create description
        desc = " + ".join(positive)
        if negative:
            desc += " - " + " - ".join(negative)
        
        return result_vector, desc
    
    def find_nearest_words(self, vector: np.ndarray, top_n: int = 5, 
                          exclude_words: List[str] = None) -> List[Tuple[str, float]]:
        """
        Find words nearest to a given vector.
        
        Args:
            vector: Query vector
            top_n: Number of nearest words to return
            exclude_words: Words to exclude from results
            
        Returns:
            List of (word, similarity) tuples
        """
        if exclude_words is None:
            exclude_words = []
        
        # Normalize query vector
        vector = vector / np.linalg.norm(vector)
        
        similarities = {}
        for word in self.model.index_to_key:
            if word not in exclude_words:
                word_vector = self.model[word]
                word_vector = word_vector / np.linalg.norm(word_vector)
                similarity = np.dot(vector, word_vector)
                similarities[word] = similarity
        
        # Sort and return top N
        sorted_words = sorted(similarities.items(), key=lambda x: x[1], reverse=True)
        return sorted_words[:top_n]
    
    def get_similarity(self, word1: str, word2: str) -> float:
        """Get cosine similarity between two words."""
        if word1 not in self.model or word2 not in self.model:
            raise ValueError(f"One or both words not in vocabulary")
        
        vec1 = self.model[word1] / np.linalg.norm(self.model[word1])
        vec2 = self.model[word2] / np.linalg.norm(self.model[word2])
        
        return float(np.dot(vec1, vec2))
    
    def analogy(self, word_a: str, word_b: str, word_c: str, top_n: int = 5) -> List[Tuple[str, float]]:
        """
        Solve analogy: a is to b as c is to ?
        
        Args:
            word_a: First word
            word_b: Second word (related to word_a)
            word_c: Third word
            top_n: Number of results
            
        Returns:
            List of (word, score) tuples
        """
        vec_a = self.get_vector(word_a)
        vec_b = self.get_vector(word_b)
        vec_c = self.get_vector(word_c)
        
        # Calculate: b - a + c
        result_vector, _ = self.vector_arithmetic([word_b, word_c], [word_a])
        
        # Find nearest words
        exclude = [word_a, word_b, word_c]
        return self.find_nearest_words(result_vector, top_n=top_n, exclude_words=exclude)
    
    def vocabulary_size(self) -> int:
        """Get size of vocabulary."""
        return len(self.model)
