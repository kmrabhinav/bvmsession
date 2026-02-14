"""
Text Chunking and Embedding Module
Splits text into chunks and creates vector embeddings
"""

from typing import List, Dict, Tuple
import numpy as np
from dataclasses import dataclass


@dataclass
class TextChunk:
    """Represents a chunk of text with metadata."""
    id: int
    text: str
    start_pos: int
    end_pos: int
    page: int
    embedding: np.ndarray = None
    is_query: bool = False
    
    def __repr__(self):
        text_preview = self.text[:50].replace('\n', ' ') + "..."
        return f"Chunk({self.id}): {text_preview}"


class TextChunker:
    """Split text into chunks for embedding."""
    
    def __init__(self, chunk_size: int = 500, overlap: int = 50):
        """
        Initialize chunker.
        
        Args:
            chunk_size: Size of each chunk in characters
            overlap: Overlap between chunks in characters
        """
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.chunks: List[TextChunk] = []
    
    def chunk_text(self, text: str, page: int = 1) -> List[TextChunk]:
        """
        Split text into overlapping chunks.
        
        Args:
            text: Text to chunk
            page: Page number for metadata
            
        Returns:
            List of TextChunk objects
        """
        chunks = []
        chunk_id = 0
        
        # Split by sentences/paragraphs first for better chunking
        sentences = self._split_into_sentences(text)
        
        current_chunk = ""
        start_pos = 0
        
        for sent_idx, sentence in enumerate(sentences):
            if len(current_chunk) + len(sentence) <= self.chunk_size:
                current_chunk += sentence + " "
            else:
                if current_chunk.strip():
                    chunk = TextChunk(
                        id=chunk_id,
                        text=current_chunk.strip(),
                        start_pos=start_pos,
                        end_pos=start_pos + len(current_chunk),
                        page=page
                    )
                    chunks.append(chunk)
                    chunk_id += 1
                    
                    # Create overlap
                    overlap_sentences = sentences[max(0, sent_idx - 2):sent_idx]
                    current_chunk = " ".join(overlap_sentences) + " " + sentence + " "
                    start_pos = start_pos + len(current_chunk) - len(sentence) - 1
                else:
                    current_chunk = sentence + " "
                    start_pos = start_pos + len(current_chunk)
        
        # Add last chunk
        if current_chunk.strip():
            chunk = TextChunk(
                id=chunk_id,
                text=current_chunk.strip(),
                start_pos=start_pos,
                end_pos=start_pos + len(current_chunk),
                page=page
            )
            chunks.append(chunk)
        
        self.chunks.extend(chunks)
        return chunks
    
    def _split_into_sentences(self, text: str) -> List[str]:
        """Split text into sentences."""
        # Simple sentence splitting
        sentences = []
        current_sentence = ""
        
        for char in text:
            current_sentence += char
            if char in '.!?':
                if current_sentence.strip():
                    sentences.append(current_sentence.strip())
                current_sentence = ""
        
        if current_sentence.strip():
            sentences.append(current_sentence.strip())
        
        return sentences
    
    def get_chunk_stats(self) -> Dict:
        """Get statistics about chunks."""
        if not self.chunks:
            return {}
        
        sizes = [len(c.text) for c in self.chunks]
        
        return {
            'total_chunks': len(self.chunks),
            'avg_chunk_size': np.mean(sizes),
            'min_chunk_size': np.min(sizes),
            'max_chunk_size': np.max(sizes),
            'total_text_length': sum(sizes),
            'chunk_size_std': np.std(sizes)
        }


class EmbeddingGenerator:
    """Generate embeddings for text chunks."""
    
    def __init__(self, embedding_dim: int = 100):
        """
        Initialize embedding generator.
        
        Args:
            embedding_dim: Dimension of embeddings (100 for demo, typically 768+ for production)
        """
        self.embedding_dim = embedding_dim
        self.embeddings = {}
    
    def generate_simple_embedding(self, text: str, seed: int = None) -> np.ndarray:
        """
        Generate a simple deterministic embedding for demo purposes.
        Uses a combination of character frequencies and text statistics.
        
        Args:
            text: Text to embed
            seed: Random seed for reproducibility
            
        Returns:
            Embedding vector
        """
        if seed is not None:
            np.random.seed(seed)
        
        # Method: Combine multiple text features
        words = text.lower().split()
        
        # Character frequency features
        char_freq = {}
        for char in text.lower():
            if char.isalpha():
                char_freq[char] = char_freq.get(char, 0) + 1
        
        # Get alphabet letters (a-z)
        alphabet = 'abcdefghijklmnopqrstuvwxyz'
        char_features = np.array([char_freq.get(c, 0) for c in alphabet])
        
        # Normalize
        if char_features.sum() > 0:
            char_features = char_features / (char_features.sum() + 1e-8)
        
        # Statistical features
        word_lengths = [len(w) for w in words] if words else [0]
        stat_features = np.array([
            len(text) / 1000.0,  # Text length normalized
            len(words) / 100.0,  # Word count normalized
            np.mean(word_lengths) / 20.0,  # Average word length
            len(set(words)) / len(words) if words else 0,  # Unique word ratio
        ])
        
        # Combine features
        combined = np.concatenate([char_features, stat_features])
        
        # Pad or truncate to embedding_dim
        if len(combined) < self.embedding_dim:
            padding = np.random.randn(self.embedding_dim - len(combined)) * 0.1
            embedding = np.concatenate([combined, padding])
        else:
            embedding = combined[:self.embedding_dim]
        
        # Normalize to unit vector
        norm = np.linalg.norm(embedding)
        if norm > 0:
            embedding = embedding / norm
        
        return embedding
    
    def embed_chunks(self, chunks: List[TextChunk]) -> Dict[int, np.ndarray]:
        """
        Generate embeddings for all chunks.
        
        Args:
            chunks: List of TextChunk objects
            
        Returns:
            Dictionary mapping chunk id to embedding
        """
        embeddings = {}
        
        for i, chunk in enumerate(chunks):
            # Use chunk id as seed for reproducibility
            embedding = self.generate_simple_embedding(chunk.text, seed=chunk.id)
            chunk.embedding = embedding
            embeddings[chunk.id] = embedding
        
        self.embeddings = embeddings
        return embeddings
    
    def cosine_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """
        Calculate cosine similarity between two vectors.
        
        Args:
            vec1: First vector
            vec2: Second vector
            
        Returns:
            Similarity score (0-1)
        """
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return (dot_product / (norm1 * norm2) + 1) / 2  # Normalize to 0-1
    
    def embed_query(self, query: str) -> np.ndarray:
        """
        Generate embedding for a query.
        
        Args:
            query: Query text
            
        Returns:
            Query embedding vector
        """
        # Use large seed to differentiate query embeddings
        embedding = self.generate_simple_embedding(query, seed=999999)
        return embedding
    
    def find_similar_chunks(
        self,
        query_embedding: np.ndarray,
        chunks: List[TextChunk],
        top_k: int = 5
    ) -> List[Tuple[TextChunk, float]]:
        """
        Find most similar chunks to query.
        
        Args:
            query_embedding: Query embedding
            chunks: List of chunks to search
            top_k: Number of top results to return
            
        Returns:
            List of (chunk, similarity_score) tuples
        """
        similarities = []
        
        for chunk in chunks:
            if chunk.embedding is not None:
                sim = self.cosine_similarity(query_embedding, chunk.embedding)
                similarities.append((chunk, sim))
        
        # Sort by similarity descending
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        return similarities[:top_k]
