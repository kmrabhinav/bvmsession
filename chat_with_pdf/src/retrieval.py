"""
Vector Store and Retrieval Module
Manages embeddings and retrieves relevant chunks
"""

from typing import List, Tuple, Dict
import numpy as np
try:
    from .chunking import TextChunk, EmbeddingGenerator
    from .azure_integration import AzureOpenAIIntegration
except ImportError:
    from chunking import TextChunk, EmbeddingGenerator
    try:
        from azure_integration import AzureOpenAIIntegration
    except ImportError:
        AzureOpenAIIntegration = None


class VectorStore:
    """Store and retrieve text embeddings."""
    
    def __init__(self):
        """Initialize vector store."""
        self.chunks: List[TextChunk] = []
        self.embeddings: Dict[int, np.ndarray] = {}
        self.embedding_generator = EmbeddingGenerator()
    
    def add_chunks(self, chunks: List[TextChunk]):
        """
        Add chunks to vector store.
        
        Args:
            chunks: List of TextChunk objects
        """
        self.chunks.extend(chunks)
        
        # Generate embeddings for all chunks using the embedding generator
        # (which will use Azure if configured)
        self.embedding_generator.embed_chunks(chunks)
        
        # Store embeddings reference
        for chunk in chunks:
            if chunk.embedding is not None:
                self.embeddings[chunk.id] = chunk.embedding
    
    def retrieve(
        self,
        query: str,
        top_k: int = 3,
        threshold: float = 0.3
    ) -> Tuple[List[TextChunk], List[float]]:
        """
        Retrieve relevant chunks for a query.
        
        Args:
            query: Query text
            top_k: Number of results to return
            threshold: Minimum similarity threshold
            
        Returns:
            Tuple of (list of chunks, list of similarity scores)
        """
        # Generate query embedding
        query_embedding = self.embedding_generator.embed_query(query)
        
        # Find similar chunks
        results = self.embedding_generator.find_similar_chunks(
            query_embedding,
            self.chunks,
            top_k=top_k
        )
        
        # Filter by threshold
        filtered_results = [(chunk, score) for chunk, score in results if score >= threshold]
        
        if not filtered_results:
            # If no results above threshold, return top result anyway
            filtered_results = results[:1]
        
        chunks = [chunk for chunk, _ in filtered_results]
        scores = [score for _, score in filtered_results]
        
        return chunks, scores
    
    def get_stats(self) -> Dict:
        """Get statistics about vector store."""
        if not self.chunks:
            return {}
        
        embeddings_array = np.array([emb for emb in self.embeddings.values()])
        
        return {
            'total_chunks': len(self.chunks),
            'total_embeddings': len(self.embeddings),
            'embedding_dim': embeddings_array.shape[1] if embeddings_array.size > 0 else 0,
            'avg_chunk_size': np.mean([len(c.text) for c in self.chunks]),
            'sparsity': np.sum(embeddings_array == 0) / embeddings_array.size if embeddings_array.size > 0 else 0,
        }
    
    def get_all_embeddings(self) -> np.ndarray:
        """Get all embeddings as numpy array."""
        return np.array([chunk.embedding for chunk in self.chunks if chunk.embedding is not None])
    
    def get_query_embedding(self, query: str) -> np.ndarray:
        """Get embedding for a query."""
        return self.embedding_generator.embed_query(query)


class RAGSynthesizer:
    """Generate answers from retrieved context using Azure OpenAI or template."""
    
    def __init__(self):
        """Initialize synthesizer with Azure OpenAI if available."""
        self.azure_client = None
        self.use_azure = False
        
        if AzureOpenAIIntegration:
            try:
                self.azure_client = AzureOpenAIIntegration()
                if self.azure_client.is_configured():
                    self.use_azure = True
                    print("✓ Using Azure OpenAI for answer synthesis (grounded results)")
                else:
                    print("⚠ Azure OpenAI not configured for synthesis, using templates")
            except Exception as e:
                print(f"⚠ Azure OpenAI synthesis initialization failed: {e}")
    
    def synthesize_answer(
        self,
        query: str,
        retrieved_chunks: List[TextChunk],
        scores: List[float]
    ) -> str:
        """
        Generate an answer from retrieved chunks using Azure OpenAI LLM.
        
        Args:
            query: Original query
            retrieved_chunks: List of relevant chunks
            scores: Similarity scores for chunks
            
        Returns:
            Generated answer
        """
        if not retrieved_chunks:
            return "I couldn't find relevant information to answer your question."
        
        # Try Azure LLM synthesis first
        if self.use_azure and self.azure_client:
            try:
                context_texts = [chunk.text for chunk in retrieved_chunks]
                answer, model_info = self.azure_client.generate_answer(query, context_texts)
                
                if answer:
                    # Format with sources
                    sources_info = "\n".join([
                        f"[Source {i+1}, confidence: {score:.2%}] Chunk {chunk.id}"
                        for i, (chunk, score) in enumerate(zip(retrieved_chunks, scores))
                    ])
                    
                    formatted_answer = (
                        f"**Question:** {query}\n\n"
                        f"**LLM-Generated Answer:**\n{answer}\n\n"
                        f"**Sources:** \n{sources_info}\n"
                        f"**Model:** {model_info}\n"
                    )
                    return formatted_answer
                else:
                    print(f"Azure synthesis error: {model_info}")
            except Exception as e:
                print(f"Azure synthesis failed: {e}, falling back to template")
        
        # Fall back to template-based synthesis
        return self._synthesize_template(query, retrieved_chunks, scores)
    
    def _synthesize_template(
        self,
        query: str,
        retrieved_chunks: List[TextChunk],
        scores: List[float]
    ) -> str:
        """
        Generate answer using template (fallback when Azure not available).
        
        Args:
            query: Original query
            retrieved_chunks: List of relevant chunks
            scores: Similarity scores for chunks
            
        Returns:
            Template-based answer
        """
        # Build context from top chunks
        context_parts = []
        for i, (chunk, score) in enumerate(zip(retrieved_chunks, scores)):
            context_parts.append(
                f"[Source {i+1}, confidence: {score:.2%}]\n{chunk.text}\n"
            )
        
        # Generate answer prompt
        answer = (
            f"**Question:** {query}\n\n"
            f"**Answer based on the document:**\n\n"
            + "\n".join(context_parts) + "\n"
            f"**Synthesis:** Based on the retrieved sections above, "
            f"this information directly addresses the query with "
            f"{scores[0]:.0%} relevance confidence.\n"
        )
        
        return answer
    
    @staticmethod
    def get_answer_sources(
        retrieved_chunks: List[TextChunk],
        scores: List[float]
    ) -> List[Dict]:
        """
        Get metadata about answer sources.
        
        Args:
            retrieved_chunks: Retrieved chunks
            scores: Similarity scores
            
        Returns:
            List of source information dicts
        """
        sources = []
        
        for chunk, score in zip(retrieved_chunks, scores):
            sources.append({
                'chunk_id': chunk.id,
                'page': chunk.page,
                'text_preview': chunk.text[:100] + "...",
                'confidence': score,
                'full_text': chunk.text
            })
        
        return sources
