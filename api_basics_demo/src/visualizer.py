"""
Visualization utilities for API parameter demonstrations.
"""

import matplotlib.pyplot as plt
import numpy as np
from typing import Dict, List, Optional


class ParameterVisualizer:
    """Visualize API parameter effects."""
    
    @staticmethod
    def plot_temperature_spectrum(save_path: Optional[str] = None):
        """
        Plot the temperature spectrum and its effects.
        
        Args:
            save_path: Optional path to save figure
        """
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('Temperature Parameter Effects', fontsize=16, weight='bold')
        
        temperatures = np.array([0.0, 0.3, 0.7, 1.0, 1.5, 2.0])
        creativity = np.array([0, 1, 5, 7, 10, 10])
        consistency = np.array([10, 9, 6, 5, 3, 1])
        unpredictability = np.array([0, 1, 4, 5, 7, 9])
        
        # Plot 1: Creativity vs Temperature
        ax = axes[0, 0]
        ax.plot(temperatures, creativity, 'o-', linewidth=2.5, markersize=8, color='#FF6B6B')
        ax.fill_between(temperatures, 0, creativity, alpha=0.3, color='#FF6B6B')
        ax.set_xlabel('Temperature', fontsize=10, weight='bold')
        ax.set_ylabel('Creativity Level', fontsize=10, weight='bold')
        ax.set_title('Creativity Increases with Temperature', fontsize=11, weight='bold')
        ax.grid(True, alpha=0.3)
        ax.set_ylim(0, 11)
        
        # Plot 2: Consistency vs Temperature
        ax = axes[0, 1]
        ax.plot(temperatures, consistency, 's-', linewidth=2.5, markersize=8, color='#4ECDC4')
        ax.fill_between(temperatures, 0, consistency, alpha=0.3, color='#4ECDC4')
        ax.set_xlabel('Temperature', fontsize=10, weight='bold')
        ax.set_ylabel('Consistency Level', fontsize=10, weight='bold')
        ax.set_title('Consistency Decreases with Temperature', fontsize=11, weight='bold')
        ax.grid(True, alpha=0.3)
        ax.set_ylim(0, 11)
        
        # Plot 3: Trade-off
        ax = axes[1, 0]
        ax.plot(temperatures, creativity, 'o-', label='Creativity', linewidth=2.5, markersize=8)
        ax.plot(temperatures, consistency, 's-', label='Consistency', linewidth=2.5, markersize=8)
        ax.set_xlabel('Temperature', fontsize=10, weight='bold')
        ax.set_ylabel('Level', fontsize=10, weight='bold')
        ax.set_title('Creativity-Consistency Trade-off', fontsize=11, weight='bold')
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3)
        ax.set_ylim(0, 11)
        
        # Plot 4: Temperature zones
        ax = axes[1, 1]
        zones = ['0.0\nDeterministic', '0.3\nFocused', '0.7\nBalanced', '1.0\nCreative', '1.5+\nChaotic']
        zone_temps = [0, 0.3, 0.7, 1.0, 1.5]
        colors = ['#3498db', '#2ecc71', '#f39c12', '#e74c3c', '#9b59b6']
        
        bars = ax.bar(zones, [2.5, 2.5, 2.5, 2.5, 2.5], color=colors, edgecolor='black', linewidth=2)
        ax.set_ylabel('Temperature Range', fontsize=10, weight='bold')
        ax.set_title('Temperature Operating Zones', fontsize=11, weight='bold')
        ax.set_ylim(0, 3)
        ax.set_yticks([])
        
        # Add zone descriptions
        descriptions = [
            'Identical\noutputs',
            'Very\nconsistent',
            'Balanced\nvariation',
            'Creative\nresponses',
            'Highly\nunpredictable'
        ]
        for i, (bar, desc) in enumerate(zip(bars, descriptions)):
            ax.text(bar.get_x() + bar.get_width()/2., bar.get_height()/2.,
                   desc, ha='center', va='center', fontsize=9, weight='bold', color='white')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Visualization saved to {save_path}")
        
        return fig
    
    @staticmethod
    def plot_response_variance(analyses: Dict, save_path: Optional[str] = None):
        """
        Plot response variance across temperatures.
        
        Args:
            analyses: Dictionary of temperature -> TemperatureAnalysis
            save_path: Optional path to save figure
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
        fig.suptitle('Response Variance Analysis', fontsize=14, weight='bold')
        
        temperatures = sorted(analyses.keys())
        variances = [analyses[t].variance for t in temperatures]
        repetitions = [analyses[t].repetition_rate for t in temperatures]
        
        # Plot 1: Variance
        colors1 = plt.cm.RdYlGn(np.linspace(0.3, 0.7, len(temperatures)))
        bars1 = ax1.bar([str(t) for t in temperatures], variances, color=colors1, edgecolor='black', linewidth=1.5)
        ax1.set_ylabel('Response Variance', fontsize=11, weight='bold')
        ax1.set_xlabel('Temperature', fontsize=11, weight='bold')
        ax1.set_title('Variance in Responses', fontsize=12, weight='bold')
        ax1.set_ylim(0, 1.0)
        ax1.grid(axis='y', alpha=0.3)
        
        for bar, var in zip(bars1, variances):
            ax1.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.02,
                    f'{var:.3f}', ha='center', va='bottom', fontsize=10, weight='bold')
        
        # Plot 2: Repetition Rate
        colors2 = plt.cm.RdYlGn_r(np.linspace(0.3, 0.7, len(temperatures)))
        bars2 = ax2.bar([str(t) for t in temperatures], repetitions, color=colors2, edgecolor='black', linewidth=1.5)
        ax2.set_ylabel('Repetition Rate', fontsize=11, weight='bold')
        ax2.set_xlabel('Temperature', fontsize=11, weight='bold')
        ax2.set_title('Repeated Patterns in Responses', fontsize=12, weight='bold')
        ax2.set_ylim(0, 1.0)
        ax2.grid(axis='y', alpha=0.3)
        
        for bar, rep in zip(bars2, repetitions):
            ax2.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.02,
                    f'{rep:.3f}', ha='center', va='bottom', fontsize=10, weight='bold')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Visualization saved to {save_path}")
        
        return fig
    
    @staticmethod
    def plot_parameter_comparison(param_values: Dict[str, List], 
                                  param_names: List[str],
                                  save_path: Optional[str] = None):
        """
        Plot comparison of different parameters.
        
        Args:
            param_values: Dictionary mapping parameter names to values
            param_names: Names of parameters to plot
            save_path: Optional path to save figure
        """
        fig, axes = plt.subplots(1, len(param_names), figsize=(4*len(param_names), 4))
        if len(param_names) == 1:
            axes = [axes]
        
        fig.suptitle('API Parameter Effects Comparison', fontsize=14, weight='bold')
        
        for ax, param_name in zip(axes, param_names):
            if param_name in param_values:
                values = param_values[param_name]
                colors = plt.cm.viridis(np.linspace(0, 1, len(values)))
                
                bars = ax.bar(range(len(values)), values, color=colors, edgecolor='black', linewidth=1.5)
                ax.set_ylabel('Effect Level', fontsize=10, weight='bold')
                ax.set_xlabel('Setting', fontsize=10, weight='bold')
                ax.set_title(f'{param_name}', fontsize=11, weight='bold')
                ax.grid(axis='y', alpha=0.3)
                
                for bar, val in zip(bars, values):
                    ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.02,
                           f'{val:.2f}', ha='center', va='bottom', fontsize=9, weight='bold')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Visualization saved to {save_path}")
        
        return fig
