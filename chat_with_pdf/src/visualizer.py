"""
Visualization Module for RAG Pipeline
Creates charts showing embeddings, retrieval, and synthesis
"""

import matplotlib.pyplot as plt
import numpy as np
from typing import List, Tuple, Optional
try:
    from .chunking import TextChunk
except ImportError:
    from chunking import TextChunk
import plotly.graph_objects as go
import plotly.express as px
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE


class RAGVisualizer:
    """Visualize RAG pipeline stages."""
    
    @staticmethod
    def plot_pipeline_overview(save_path: Optional[str] = None):
        """
        Create overview of RAG pipeline stages.
        
        Args:
            save_path: Path to save figure
        """
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('RAG Pipeline: From PDF to Answers', fontsize=16, weight='bold')
        
        # Stage 1: Ingestion
        ax = axes[0, 0]
        ax.text(0.5, 0.7, '📄 INGESTION', ha='center', fontsize=14, weight='bold',
               transform=ax.transAxes)
        ax.text(0.5, 0.5, 'Load raw PDF\n↓\nExtract text', ha='center', fontsize=11,
               transform=ax.transAxes, bbox=dict(boxstyle='round', facecolor='#E8F4F8'))
        ax.text(0.5, 0.2, 'Raw character sequence', ha='center', fontsize=9,
               transform=ax.transAxes, style='italic')
        ax.axis('off')
        
        # Stage 2: Chunking & Embedding
        ax = axes[0, 1]
        ax.text(0.5, 0.7, '✂️ CHUNKING & EMBEDDING', ha='center', fontsize=14, weight='bold',
               transform=ax.transAxes)
        ax.text(0.5, 0.5, 'Split into chunks\n↓\nCreate embeddings', ha='center', fontsize=11,
               transform=ax.transAxes, bbox=dict(boxstyle='round', facecolor='#E8F8E8'))
        ax.text(0.5, 0.2, 'Vector representations', ha='center', fontsize=9,
               transform=ax.transAxes, style='italic')
        ax.axis('off')
        
        # Stage 3: Retrieval
        ax = axes[1, 0]
        ax.text(0.5, 0.7, '🔍 RETRIEVAL', ha='center', fontsize=14, weight='bold',
               transform=ax.transAxes)
        ax.text(0.5, 0.5, 'Query embedding\n↓\nFind similar chunks', ha='center', fontsize=11,
               transform=ax.transAxes, bbox=dict(boxstyle='round', facecolor='#F8F4E8'))
        ax.text(0.5, 0.2, 'Relevant context', ha='center', fontsize=9,
               transform=ax.transAxes, style='italic')
        ax.axis('off')
        
        # Stage 4: Synthesis
        ax = axes[1, 1]
        ax.text(0.5, 0.7, '📝 SYNTHESIS', ha='center', fontsize=14, weight='bold',
               transform=ax.transAxes)
        ax.text(0.5, 0.5, 'Combine context\n↓\nGenerate answer', ha='center', fontsize=11,
               transform=ax.transAxes, bbox=dict(boxstyle='round', facecolor='#F8E8F4'))
        ax.text(0.5, 0.2, 'Factual answer', ha='center', fontsize=9,
               transform=ax.transAxes, style='italic')
        ax.axis('off')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Pipeline overview saved to {save_path}")
        
        return fig
    
    @staticmethod
    def plot_chunking_visualization(chunks: List[TextChunk], save_path: Optional[str] = None):
        """
        Visualize how text is chunked.
        
        Args:
            chunks: List of text chunks
            save_path: Path to save figure
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        fig.suptitle('Text Chunking: Splitting Documents for Embedding', fontsize=14, weight='bold')
        
        # Plot 1: Chunk distribution
        chunk_sizes = [len(c.text) for c in chunks]
        chunk_ids = list(range(len(chunks)))
        
        colors = plt.cm.viridis(np.linspace(0, 1, len(chunks)))
        bars = ax1.bar(chunk_ids, chunk_sizes, color=colors, edgecolor='black', linewidth=1)
        ax1.set_xlabel('Chunk ID', fontsize=11, weight='bold')
        ax1.set_ylabel('Chunk Size (characters)', fontsize=11, weight='bold')
        ax1.set_title('Chunk Size Distribution', fontsize=12, weight='bold')
        ax1.grid(axis='y', alpha=0.3)
        
        # Add value labels on bars
        for bar, size in zip(bars, chunk_sizes):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{int(size)}', ha='center', va='bottom', fontsize=8)
        
        # Plot 2: Cumulative text
        cumulative_sizes = np.cumsum(chunk_sizes)
        ax2.plot(chunk_ids, cumulative_sizes, marker='o', linewidth=2, markersize=6, color='#1f77b4')
        ax2.fill_between(chunk_ids, 0, cumulative_sizes, alpha=0.3, color='#1f77b4')
        ax2.set_xlabel('Chunk ID', fontsize=11, weight='bold')
        ax2.set_ylabel('Cumulative Characters', fontsize=11, weight='bold')
        ax2.set_title('Cumulative Text Coverage', fontsize=12, weight='bold')
        ax2.grid(alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Chunking visualization saved to {save_path}")
        
        return fig
    
    @staticmethod
    def plot_embedding_space_interactive(
        chunks: List[TextChunk],
        query_embedding: np.ndarray = None,
        retrieved_chunks: List[TextChunk] = None,
        save_path: Optional[str] = None
    ):
        """
        Create interactive 2D visualization of embeddings using Plotly.
        
        Args:
            chunks: List of text chunks with embeddings
            query_embedding: Query embedding vector
            retrieved_chunks: Retrieved chunks (highlighted)
            save_path: Path to save HTML file
        """
        # Get all embeddings
        embeddings = np.array([c.embedding for c in chunks if c.embedding is not None])
        
        if len(embeddings) == 0:
            print("No embeddings to visualize")
            return None
        
        # Reduce to 2D using PCA
        pca = None
        embeddings_2d = None
        explained_var = [1.0, 0.0]
        
        if embeddings.shape[1] > 2:
            pca = PCA(n_components=2, random_state=42)
            embeddings_2d = pca.fit_transform(embeddings)
            explained_var = pca.explained_variance_ratio_
        else:
            embeddings_2d = embeddings
            explained_var = [1.0, 0.0]
        
        # Prepare data for scatter plot
        retrieved_ids = set(c.id for c in (retrieved_chunks or []))
        
        colors = []
        sizes = []
        hover_texts = []
        
        for chunk in chunks:
            if chunk.id in retrieved_ids:
                colors.append('red')
                sizes.append(15)
            else:
                colors.append('blue')
                sizes.append(8)
            
            text_preview = chunk.text[:80].replace('\n', ' ')
            hover = (f"<b>Chunk {chunk.id}</b><br>"
                    f"Page: {chunk.page}<br>"
                    f"Text: {text_preview}...<br>"
                    f"Size: {len(chunk.text)} chars")
            hover_texts.append(hover)
        
        # Create scatter plot
        fig = go.Figure()
        
        # Add non-retrieved chunks
        non_retrieved = ~np.isin([c.id for c in chunks], list(retrieved_ids))
        fig.add_trace(go.Scatter(
            x=embeddings_2d[non_retrieved, 0],
            y=embeddings_2d[non_retrieved, 1],
            mode='markers',
            marker=dict(
                size=8,
                color='#1f77b4',
                line=dict(width=1, color='darkblue')
            ),
            text=[h for i, h in enumerate(hover_texts) if non_retrieved[i]],
            hovertemplate='%{text}<extra></extra>',
            name='Document Chunks'
        ))
        
        # Add retrieved chunks
        if retrieved_ids:
            retrieved = np.isin([c.id for c in chunks], list(retrieved_ids))
            fig.add_trace(go.Scatter(
                x=embeddings_2d[retrieved, 0],
                y=embeddings_2d[retrieved, 1],
                mode='markers',
                marker=dict(
                    size=15,
                    color='#ff7f0e',
                    symbol='star',
                    line=dict(width=2, color='darkred')
                ),
                text=[h for i, h in enumerate(hover_texts) if retrieved[i]],
                hovertemplate='%{text}<extra></extra>',
                name='Retrieved Chunks'
            ))
        
        # Add query point if provided
        if query_embedding is not None and pca is not None:
            query_embedding_2d = pca.transform([query_embedding])
            fig.add_trace(go.Scatter(
                x=query_embedding_2d[:, 0],
                y=query_embedding_2d[:, 1],
                mode='markers',
                marker=dict(
                    size=25,
                    color='#d62728',
                    symbol='diamond',
                    line=dict(width=3, color='darkred')
                ),
                text=['<b>Query Embedding</b>'],
                hovertemplate='%{text}<extra></extra>',
                name='Query'
            ))
        
        fig.update_layout(
            title='Interactive Vector Embedding Space',
            xaxis_title=f'PC1 ({explained_var[0]:.1%} variance)',
            yaxis_title=f'PC2 ({explained_var[1]:.1%} variance)',
            hovermode='closest',
            width=1000,
            height=700,
            template='plotly_white',
            font=dict(size=11),
            showlegend=True,
            legend=dict(x=0.02, y=0.98)
        )
        
        if save_path:
            fig.write_html(save_path)
            print(f"Interactive embedding space saved to {save_path}")
        
        return fig
    
    @staticmethod
    def plot_retrieval_process(
        query: str,
        retrieved_chunks: List[TextChunk],
        scores: List[float],
        save_path: Optional[str] = None
    ):
        """
        Visualize the retrieval process and relevance scores.
        
        Args:
            query: Query text
            retrieved_chunks: Retrieved chunks
            scores: Relevance scores
            save_path: Path to save figure
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        fig.suptitle(f'Query Retrieval: "{query[:50]}..."', fontsize=14, weight='bold')
        
        # Plot 1: Relevance scores
        chunk_labels = [f'Chunk {c.id}' for c in retrieved_chunks]
        colors_scores = plt.cm.RdYlGn(scores)
        
        bars = ax1.barh(chunk_labels, scores, color=colors_scores, edgecolor='black', linewidth=1.5)
        ax1.set_xlabel('Relevance Score', fontsize=11, weight='bold')
        ax1.set_title('Chunk Relevance Scores', fontsize=12, weight='bold')
        ax1.set_xlim(0, 1)
        ax1.grid(axis='x', alpha=0.3)
        
        # Add value labels
        for bar, score in zip(bars, scores):
            width = bar.get_width()
            ax1.text(width + 0.02, bar.get_y() + bar.get_height()/2.,
                    f'{score:.1%}', ha='left', va='center', fontsize=10, weight='bold')
        
        # Plot 2: Chunk content preview
        ax2.axis('off')
        
        y_pos = 0.95
        for i, (chunk, score) in enumerate(zip(retrieved_chunks, scores)):
            # Chunk header
            ax2.text(0.05, y_pos, f'Chunk {chunk.id} (Page {chunk.page}) - Confidence: {score:.0%}',
                    fontsize=10, weight='bold', transform=ax2.transAxes,
                    bbox=dict(boxstyle='round', facecolor='lightgray', alpha=0.7))
            y_pos -= 0.08
            
            # Chunk preview
            text_preview = chunk.text[:100].replace('\n', ' ')
            if len(chunk.text) > 100:
                text_preview += "..."
            
            ax2.text(0.05, y_pos, f'"{text_preview}"', fontsize=9, transform=ax2.transAxes,
                    style='italic', wrap=True, bbox=dict(boxstyle='round', facecolor='lightyellow'))
            y_pos -= 0.15
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Retrieval process visualization saved to {save_path}")
        
        return fig
    
    @staticmethod
    def plot_rag_statistics(
        num_chunks: int,
        embedding_dim: int,
        avg_chunk_size: float,
        total_text: int,
        save_path: Optional[str] = None
    ):
        """
        Visualize RAG pipeline statistics.
        
        Args:
            num_chunks: Number of chunks
            embedding_dim: Embedding dimension
            avg_chunk_size: Average chunk size
            total_text: Total text size
            save_path: Path to save figure
        """
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        fig.suptitle('RAG Pipeline Statistics', fontsize=14, weight='bold')
        
        # Plot 1: Chunk count
        ax = axes[0, 0]
        ax.bar(['Total Chunks'], [num_chunks], color='#1f77b4', edgecolor='black', linewidth=2)
        ax.set_ylabel('Count', fontsize=11, weight='bold')
        ax.set_title('Number of Chunks', fontsize=12, weight='bold')
        ax.text(0, num_chunks + 5, str(num_chunks), ha='center', fontsize=12, weight='bold')
        ax.set_ylim(0, num_chunks * 1.2)
        
        # Plot 2: Embedding dimension
        ax = axes[0, 1]
        ax.bar(['Embedding\nDimension'], [embedding_dim], color='#ff7f0e', edgecolor='black', linewidth=2)
        ax.set_ylabel('Dimension', fontsize=11, weight='bold')
        ax.set_title('Vector Embedding Size', fontsize=12, weight='bold')
        ax.text(0, embedding_dim + 2, str(embedding_dim), ha='center', fontsize=12, weight='bold')
        ax.set_ylim(0, embedding_dim * 1.2)
        
        # Plot 3: Average chunk size
        ax = axes[1, 0]
        ax.bar(['Avg Chunk\nSize'], [avg_chunk_size], color='#2ca02c', edgecolor='black', linewidth=2)
        ax.set_ylabel('Characters', fontsize=11, weight='bold')
        ax.set_title('Average Chunk Size', fontsize=12, weight='bold')
        ax.text(0, avg_chunk_size + 5, f'{avg_chunk_size:.0f}', ha='center', fontsize=12, weight='bold')
        ax.set_ylim(0, avg_chunk_size * 1.2)
        
        # Plot 4: Total text
        ax = axes[1, 1]
        ax.bar(['Total\nCharacters'], [total_text / 1000], color='#d62728', edgecolor='black', linewidth=2)
        ax.set_ylabel('Kilobytes', fontsize=11, weight='bold')
        ax.set_title('Total Document Size', fontsize=12, weight='bold')
        ax.text(0, total_text / 1000 + 10, f'{total_text / 1000:.1f}KB', ha='center', fontsize=12, weight='bold')
        ax.set_ylim(0, total_text / 1000 * 1.2)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Statistics visualization saved to {save_path}")
        
        return fig
