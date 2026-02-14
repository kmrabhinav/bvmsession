"""
Vector visualization utilities for 2D and 3D representations.
"""

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d
import numpy as np
from sklearn.decomposition import PCA
from typing import List, Dict, Optional, Tuple


class Vector2DVisualizer:
    """Visualize vectors in 2D space."""
    
    @staticmethod
    def plot_vector_arithmetic(vectors: Dict[str, np.ndarray], result_vector: np.ndarray,
                               result_name: str = "Result", save_path: Optional[str] = None):
        """
        Visualize vector arithmetic operation.
        
        Args:
            vectors: Dictionary of vector name -> vector
            result_vector: The resulting vector from operation
            result_name: Name for the result vector
            save_path: Path to save figure
        """
        # Reduce to 2D using PCA
        all_vectors = list(vectors.values()) + [result_vector]
        pca = PCA(n_components=2)
        vectors_2d = pca.fit_transform(all_vectors)
        
        fig, ax = plt.subplots(figsize=(12, 10))
        
        # Plot vectors
        colors = plt.cm.Set3(np.linspace(0, 1, len(vectors)))
        
        for i, (name, vector_2d) in enumerate(zip(vectors.keys(), vectors_2d[:-1])):
            ax.arrow(0, 0, vector_2d[0], vector_2d[1], 
                    head_width=0.15, head_length=0.1, fc=colors[i], ec=colors[i], 
                    linewidth=2.5, label=name, alpha=0.8)
            
            # Add label
            offset = vector_2d * 1.15
            ax.text(offset[0], offset[1], name, fontsize=11, weight='bold',
                   bbox=dict(boxstyle='round', facecolor=colors[i], alpha=0.7))
        
        # Plot result vector
        result_2d = vectors_2d[-1]
        ax.arrow(0, 0, result_2d[0], result_2d[1],
                head_width=0.15, head_length=0.1, fc='red', ec='darkred',
                linewidth=3, label=result_name, alpha=0.9, linestyle='--')
        
        offset = result_2d * 1.15
        ax.text(offset[0], offset[1], result_name, fontsize=12, weight='bold',
               bbox=dict(boxstyle='round', facecolor='red', alpha=0.8, edgecolor='darkred'))
        
        # Configure plot
        ax.set_xlim(-2.5, 2.5)
        ax.set_ylim(-2.5, 2.5)
        ax.axhline(y=0, color='k', linewidth=0.5, alpha=0.3)
        ax.axvline(x=0, color='k', linewidth=0.5, alpha=0.3)
        ax.grid(True, alpha=0.3)
        ax.set_aspect('equal')
        ax.set_xlabel('PC1', fontsize=11, weight='bold')
        ax.set_ylabel('PC2', fontsize=11, weight='bold')
        ax.set_title('Vector Arithmetic: King - Man + Woman ≈ Queen', 
                    fontsize=13, weight='bold', pad=20)
        ax.legend(loc='upper right', fontsize=10)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Visualization saved to {save_path}")
        
        return fig
    
    @staticmethod
    def plot_word_relationships(word_vectors: Dict[str, np.ndarray], 
                               save_path: Optional[str] = None):
        """
        Plot words in 2D space using PCA.
        
        Args:
            word_vectors: Dictionary of word -> vector
            save_path: Path to save figure
        """
        # Reduce to 2D
        vectors = np.array(list(word_vectors.values()))
        pca = PCA(n_components=2)
        vectors_2d = pca.fit_transform(vectors)
        
        fig, ax = plt.subplots(figsize=(12, 10))
        
        # Categorize words for coloring
        male_words = ['king', 'man', 'prince', 'actor', 'boy', 'husband']
        female_words = ['queen', 'woman', 'princess', 'actress', 'girl', 'wife']
        
        for (word, vector_2d), i in zip(zip(word_vectors.keys(), vectors_2d), 
                                         range(len(word_vectors))):
            if word in male_words:
                color = 'steelblue'
                marker = 's'
            elif word in female_words:
                color = 'crimson'
                marker = '^'
            else:
                color = 'gray'
                marker = 'o'
            
            ax.scatter(vector_2d[0], vector_2d[1], s=200, c=color, marker=marker, 
                      alpha=0.7, edgecolors='black', linewidth=1.5)
            ax.text(vector_2d[0], vector_2d[1]+0.1, word, fontsize=10, weight='bold',
                   ha='center', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        ax.axhline(y=0, color='k', linewidth=0.5, alpha=0.3)
        ax.axvline(x=0, color='k', linewidth=0.5, alpha=0.3)
        ax.grid(True, alpha=0.3)
        ax.set_xlabel('PC1 (Gender Dimension)', fontsize=11, weight='bold')
        ax.set_ylabel('PC2 (Royalty Dimension)', fontsize=11, weight='bold')
        ax.set_title('Word Embedding Space - Semantic Relationships', 
                    fontsize=13, weight='bold', pad=20)
        
        # Add legend
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor='steelblue', label='Male Words'),
            Patch(facecolor='crimson', label='Female Words'),
            Patch(facecolor='gray', label='Other Words')
        ]
        ax.legend(handles=legend_elements, loc='upper right', fontsize=10)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Visualization saved to {save_path}")
        
        return fig
    
    @staticmethod
    def plot_similarity_heatmap(word_pairs: Dict[str, float], save_path: Optional[str] = None):
        """
        Plot similarity heatmap for word pairs.
        
        Args:
            word_pairs: Dictionary of (word1 ↔ word2) -> similarity
            save_path: Path to save figure
        """
        fig, ax = plt.subplots(figsize=(12, 8))
        
        pairs = list(word_pairs.keys())
        similarities = list(word_pairs.values())
        
        colors = plt.cm.RdYlGn(np.array(similarities))
        bars = ax.barh(range(len(pairs)), similarities, color=colors, edgecolor='black', linewidth=1.5)
        
        # Add value labels
        for i, (bar, sim) in enumerate(zip(bars, similarities)):
            ax.text(sim + 0.02, i, f'{sim:.3f}', va='center', fontsize=9, weight='bold')
        
        ax.set_yticks(range(len(pairs)))
        ax.set_yticklabels(pairs, fontsize=10)
        ax.set_xlabel('Cosine Similarity', fontsize=11, weight='bold')
        ax.set_title('Word Similarity Measurements', fontsize=13, weight='bold', pad=20)
        ax.set_xlim(0, 1.1)
        ax.grid(axis='x', alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Visualization saved to {save_path}")
        
        return fig
