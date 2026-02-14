"""
Visualization utilities for tokenization demonstration.
"""

import matplotlib.pyplot as plt
from typing import List, Tuple, Dict, Optional
import numpy as np


class TokenizationVisualizer:
    """Creates visualizations of tokenization process."""
    
    @staticmethod
    def visualize_tokens_breakdown(text: str, token_details: List[Tuple[int, str]], 
                                    save_path: Optional[str] = None):
        """
        Visualize how text is broken down into tokens.
        
        Args:
            text: Original text
            token_details: List of (token_id, token_string) tuples
            save_path: Optional path to save figure
        """
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8))
        
        # Plot 1: Original text with character positions
        ax1.text(0.05, 0.95, f"Original Text ({len(text)} characters):", 
                fontsize=12, weight='bold', transform=ax1.transAxes, 
                verticalalignment='top')
        ax1.text(0.05, 0.80, f'"{text}"', 
                fontsize=11, transform=ax1.transAxes, 
                verticalalignment='top', family='monospace',
                bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.7))
        ax1.axis('off')
        
        # Plot 2: Token visualization
        ax2.set_title(f'Tokens Breakdown ({len(token_details)} tokens)', 
                     fontsize=12, weight='bold', pad=20)
        
        token_strs = []
        token_ids = []
        for token_id, token_str in token_details:
            token_ids.append(token_id)
            display_str = repr(token_str)[1:-1]
            token_strs.append(display_str)
        
        x_pos = np.arange(len(token_strs))
        colors = plt.cm.Set3(np.linspace(0, 1, len(token_strs)))
        
        bars = ax2.bar(x_pos, [1] * len(token_strs), color=colors, edgecolor='black', linewidth=1.5)
        
        for i, (bar, token_str, token_id) in enumerate(zip(bars, token_strs, token_ids)):
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height/2.,
                    f'ID: {token_id}\n{token_str}',
                    ha='center', va='center', fontsize=9, weight='bold',
                    family='monospace',
                    bbox=dict(boxstyle='round', facecolor='white', alpha=0.8, pad=0.3))
        
        ax2.set_ylabel('Token', fontsize=10)
        ax2.set_xlabel('Token Position', fontsize=10)
        ax2.set_xticks(x_pos)
        ax2.set_xticklabels([str(i) for i in range(len(token_strs))])
        ax2.set_ylim(0, 1.3)
        ax2.set_yticks([])
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Visualization saved to {save_path}")
        
        return fig
    
    @staticmethod
    def compare_texts_tokenization(analyses: List[Dict], save_path: Optional[str] = None):
        """
        Compare tokenization statistics across multiple texts.
        
        Args:
            analyses: List of analysis dictionaries
            save_path: Optional path to save figure
        """
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('Tokenization Analysis Comparison', fontsize=16, weight='bold')
        
        texts_labels = [f"Text {i+1}" for i in range(len(analyses))]
        
        # Chart 1: Token counts
        ax = axes[0, 0]
        token_counts = [a['token_count'] for a in analyses]
        bars = ax.bar(texts_labels, token_counts, color='steelblue', edgecolor='black')
        ax.set_ylabel('Token Count', fontsize=10, weight='bold')
        ax.set_title('Number of Tokens', fontsize=11, weight='bold')
        ax.grid(axis='y', alpha=0.3)
        for bar, count in zip(bars, token_counts):
            ax.text(bar.get_x() + bar.get_width()/2., bar.get_height(),
                   str(count), ha='center', va='bottom', weight='bold')
        
        # Chart 2: Character vs Token ratio
        ax = axes[0, 1]
        char_counts = [a['character_count'] for a in analyses]
        x = np.arange(len(texts_labels))
        width = 0.35
        bars1 = ax.bar(x - width/2, char_counts, width, label='Characters', 
                      color='coral', edgecolor='black')
        bars2 = ax.bar(x + width/2, token_counts, width, label='Tokens', 
                      color='lightgreen', edgecolor='black')
        ax.set_ylabel('Count', fontsize=10, weight='bold')
        ax.set_title('Characters vs Tokens', fontsize=11, weight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(texts_labels)
        ax.legend()
        ax.grid(axis='y', alpha=0.3)
        
        # Chart 3: Average chars per token
        ax = axes[1, 0]
        avg_chars = [a['avg_chars_per_token'] for a in analyses]
        bars = ax.bar(texts_labels, avg_chars, color='mediumpurple', edgecolor='black')
        ax.set_ylabel('Characters per Token', fontsize=10, weight='bold')
        ax.set_title('Compression Ratio (Avg Chars/Token)', fontsize=11, weight='bold')
        ax.grid(axis='y', alpha=0.3)
        for bar, avg in zip(bars, avg_chars):
            ax.text(bar.get_x() + bar.get_width()/2., bar.get_height(),
                   f'{avg:.2f}', ha='center', va='bottom', weight='bold')
        
        # Chart 4: Text statistics table
        ax = axes[1, 1]
        ax.axis('tight')
        ax.axis('off')
        
        table_data = []
        for i, a in enumerate(analyses):
            table_data.append([
                f"Text {i+1}",
                str(a['character_count']),
                str(a['word_count']),
                str(a['token_count']),
                f"{a['avg_chars_per_token']:.2f}"
            ])
        
        table = ax.table(cellText=table_data,
                        colLabels=['Text', 'Chars', 'Words', 'Tokens', 'Chars/Token'],
                        cellLoc='center',
                        loc='center',
                        colWidths=[0.15, 0.15, 0.15, 0.15, 0.2])
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1, 2)
        
        for i in range(5):
            table[(0, i)].set_facecolor('#4CAF50')
            table[(0, i)].set_text_props(weight='bold', color='white')
        
        for i in range(1, len(table_data) + 1):
            for j in range(5):
                if i % 2 == 0:
                    table[(i, j)].set_facecolor('#f0f0f0')
                else:
                    table[(i, j)].set_facecolor('#ffffff')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Comparison visualization saved to {save_path}")
        
        return fig
