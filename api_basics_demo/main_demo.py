#!/usr/bin/env python3
"""
API Basics Demo: Temperature Control & Creativity Parameters
===========================================================

Demonstrates how temperature and other parameters control the creativity
and consistency of API responses.

This demo shows:
1. Temperature parameter effects (deterministic to chaotic)
2. Same prompt at different temperatures
3. Variance in responses across temperatures
4. Parameter zone recommendations
5. Top-p and top-k sampling effects
6. Best practices for different use cases
"""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from colorama import Fore, Back, Style, init
from api_parameters import APIParameters, MockLLMResponses
from api_client import APIClient
from visualizer import ParameterVisualizer

# Initialize colorama for colored output
init(autoreset=True)


def print_header(text: str, level: int = 1):
    """Print formatted header."""
    if level == 1:
        print(f"\n{Fore.CYAN}{Style.BRIGHT}{'='*70}")
        print(f"{text.center(70)}")
        print(f"{'='*70}{Style.RESET_ALL}\n")
    elif level == 2:
        print(f"\n{Fore.GREEN}{Style.BRIGHT}▶ {text}{Style.RESET_ALL}\n")
    else:
        print(f"{Fore.YELLOW}{Style.BRIGHT}  • {text}{Style.RESET_ALL}")


def demo_1_temperature_spectrum():
    """Demo 1: Understand the temperature spectrum."""
    print_header("Demo 1: Temperature Spectrum", 2)
    
    print(f"{Fore.WHITE}Temperature controls the randomness of model responses:")
    print(f"{Fore.WHITE}• Low (0.0-0.3): Deterministic, factual, consistent")
    print(f"{Fore.WHITE}• Medium (0.7): Balanced, good for most tasks")
    print(f"{Fore.WHITE}• High (1.0-2.0): Creative, varied, sometimes unpredictable\n")
    
    for temp, info in APIParameters.TEMPERATURE_RANGES.items():
        print(f"{Fore.MAGENTA}{temp:>4.1f} {Fore.WHITE}→ {info['name']:<20} {info['description']}")
    
    print(f"\n{Fore.CYAN}Creating visualization...")
    output_dir = Path(__file__).parent / 'output'
    output_dir.mkdir(exist_ok=True)
    
    ParameterVisualizer.plot_temperature_spectrum(
        save_path=str(output_dir / 'temperature_spectrum.png')
    )
    print(f"{Fore.GREEN}✓ Visualization saved!")


def demo_2_same_prompt_different_temps():
    """Demo 2: Same prompt at different temperatures."""
    print_header("Demo 2: Same Prompt - Different Temperatures", 2)
    
    prompt = "What makes Paris special?"
    temperatures = [0.0, 0.3, 0.7, 1.0, 1.5]
    
    print(f"{Fore.WHITE}Prompt: {Fore.YELLOW}\"{prompt}\"\n")
    print(f"{Fore.WHITE}Responses at different temperatures:\n")
    
    responses = {}
    for temp in temperatures:
        responses[temp] = MockLLMResponses.get_responses(temp)
        info = APIParameters.get_temperature_info(temp)
        
        print(f"{Fore.MAGENTA}{temp:>4.1f}°C {Fore.CYAN}({info['name']:<10}){Fore.WHITE}")
        for i, response in enumerate(responses[temp], 1):
            print(f"  {i}. {response}")
        print()


def demo_3_response_analysis():
    """Demo 3: Analyze response variance."""
    print_header("Demo 3: Response Variance Analysis", 2)
    
    temperatures = [0.0, 0.3, 0.7, 1.0, 1.5]
    response_data = {}
    analyses = {}
    
    for temp in temperatures:
        responses = MockLLMResponses.get_responses(temp)
        response_data[temp] = responses
        analyses[temp] = APIParameters.analyze_responses(responses, temp)
    
    print(f"{Fore.WHITE}Analysis of response consistency:\n")
    print(f"{Fore.MAGENTA}{'Temp':<6} {'Zone':<15} {'Variance':<12} {'Repetition':<12} {'Characteristics':<30}")
    print(f"{Fore.WHITE}{'-'*75}")
    
    for temp, analysis in sorted(analyses.items()):
        info = APIParameters.get_temperature_info(temp)
        zone_name = info['name']
        
        print(f"{Fore.CYAN}{temp:<6.1f} {Fore.GREEN}{zone_name:<15} "
              f"{Fore.YELLOW}{analysis.variance:<12.3f} {analysis.repetition_rate:<12.3f} "
              f"{Fore.WHITE}{info['use_case']:<30}")
    
    # Find best for consistency and creativity
    best_consistent = min(analyses.items(), key=lambda x: x[1].variance)
    best_creative = max(analyses.items(), key=lambda x: x[1].variance)
    
    print(f"\n{Fore.GREEN}✓ Most consistent: {Fore.YELLOW}Temperature {best_consistent[0]} "
          f"({best_consistent[1].variance:.3f} variance)")
    print(f"{Fore.MAGENTA}✓ Most creative: {Fore.YELLOW}Temperature {best_creative[0]} "
          f"({best_creative[1].variance:.3f} variance)")
    
    # Create visualization
    output_dir = Path(__file__).parent / 'output'
    output_dir.mkdir(exist_ok=True)
    
    ParameterVisualizer.plot_response_variance(
        analyses,
        save_path=str(output_dir / 'response_variance.png')
    )
    print(f"\n{Fore.GREEN}✓ Visualization saved!")


def demo_4_creativity_scale():
    """Demo 4: Creativity scale explanation."""
    print_header("Demo 4: Creativity Scale (0-2)", 2)
    
    print(f"{Fore.WHITE}API temperature range from factual to creative:\n")
    
    scale = [
        (0.0, "Deterministic", "Identical", "Technical support, data retrieval, math"),
        (0.5, "Low Creativity", "Slight variation", "Email templates, summaries, FAQs"),
        (1.0, "Moderate Creativity", "Balanced", "General chat, content creation, brainstorming"),
        (1.5, "High Creativity", "Highly varied", "Creative writing, poetry, experimental"),
        (2.0, "Maximum Creativity", "Chaotic/Random", "Artistic exploration, game design"),
    ]
    
    for temp, level, variation, uses in scale:
        bar_length = int(temp / 2.0 * 20)
        bar = "█" * bar_length + "░" * (20 - bar_length)
        
        print(f"{Fore.CYAN}{temp:>3.1f}°C {Fore.WHITE}[{Fore.MAGENTA}{bar}{Fore.WHITE}] "
              f"{Fore.GREEN}{level:<18} {Fore.YELLOW}{variation:<20} {Fore.WHITE}{uses}")
    
    print(f"\n{Fore.YELLOW}PRO TIP: {Fore.WHITE}Temperature 0.7 is often the best balance for general use!")


def demo_5_use_case_recommendations():
    """Demo 5: Best practices for different use cases."""
    print_header("Demo 5: Use Case Recommendations", 2)
    
    use_cases = [
        {
            "name": "Technical Customer Support",
            "temp": 0.0,
            "reason": "Need consistent, accurate answers",
            "example": "Help desk chatbot, documentation queries"
        },
        {
            "name": "Email Composition",
            "temp": 0.3,
            "reason": "Slight variation for natural feel, maintain professionalism",
            "example": "Autocomplete, professional email drafting"
        },
        {
            "name": "General Conversation",
            "temp": 0.7,
            "reason": "Balanced creativity and consistency",
            "example": "Chatbot, personal assistant, Q&A"
        },
        {
            "name": "Creative Writing",
            "temp": 1.0,
            "reason": "Need variety and creative expression",
            "example": "Story generation, dialogue writing"
        },
        {
            "name": "Brainstorming & Ideation",
            "temp": 1.2,
            "reason": "Maximize creativity and novel ideas",
            "example": "Idea generation, exploration, experimental writing"
        },
    ]
    
    print(f"{Fore.WHITE}Recommended temperatures for different tasks:\n")
    
    for i, case in enumerate(use_cases, 1):
        print(f"{Fore.CYAN}{i}. {case['name']}")
        print(f"   {Fore.MAGENTA}Temperature: {case['temp']:.1f}°C")
        print(f"   {Fore.YELLOW}Why: {case['reason']}")
        print(f"   {Fore.GREEN}Examples: {case['example']}\n")


def demo_6_parameter_combinations():
    """Demo 6: Combining parameters for best results."""
    print_header("Demo 6: Parameter Combinations", 2)
    
    print(f"{Fore.WHITE}Key API parameters and their effects:\n")
    
    parameters = {
        "Temperature": {
            "range": "0.0 - 2.0",
            "default": "1.0",
            "effect": "Controls randomness/creativity",
            "tips": "Lower = deterministic, Higher = creative"
        },
        "Top-P (Nucleus Sampling)": {
            "range": "0.0 - 1.0",
            "default": "1.0",
            "effect": "Cumulative probability for token selection",
            "tips": "0.9 = 90% most likely tokens, good for balance"
        },
        "Top-K": {
            "range": "0 - n",
            "default": "-1 (disabled)",
            "effect": "Selects from K most likely tokens",
            "tips": "40 = only top 40 tokens considered"
        },
        "Max Tokens": {
            "range": "1 - context limit",
            "default": "inf",
            "effect": "Maximum response length",
            "tips": "Set based on desired response length"
        },
        "Frequency Penalty": {
            "range": "-2.0 - 2.0",
            "default": "0.0",
            "effect": "Reduces repetition of tokens",
            "tips": "1.0 = less repetition, 0 = default"
        },
    }
    
    for param, info in parameters.items():
        print(f"{Fore.CYAN}★ {param}")
        print(f"  {Fore.MAGENTA}Range: {Fore.WHITE}{info['range']}")
        print(f"  {Fore.MAGENTA}Default: {Fore.WHITE}{info['default']}")
        print(f"  {Fore.MAGENTA}Effect: {Fore.WHITE}{info['effect']}")
        print(f"  {Fore.MAGENTA}Tips: {Fore.WHITE}{info['tips']}\n")
    
    print(f"{Fore.GREEN}Pro Combinations:\n")
    
    combos = [
        {
            "name": "Deterministic",
            "temps": {"temperature": 0.0, "top_p": 1.0},
            "use": "Factual answers"
        },
        {
            "name": "Balanced",
            "temps": {"temperature": 0.7, "top_p": 0.9},
            "use": "General conversation"
        },
        {
            "name": "Creative",
            "temps": {"temperature": 1.0, "top_p": 0.95},
            "use": "Creative writing"
        },
        {
            "name": "Diverse",
            "temps": {"temperature": 1.2, "top_p": 0.99},
            "use": "Brainstorming"
        },
    ]
    
    for combo in combos:
        print(f"  {Fore.CYAN}{combo['name']}: {combo['use']}")
        params_str = ", ".join(f"{k}={v}" for k, v in combo['temps'].items())
        print(f"    {Fore.YELLOW}{params_str}\n")


def main():
    """Run all demonstrations."""
    print(f"\n{Fore.CYAN}{Style.BRIGHT}{'='*70}")
    print(f"API BASICS: Temperature Control & Creativity Parameters".center(70))
    print(f"{'='*70}{Style.RESET_ALL}\n")
    
    print(f"{Fore.WHITE}This demo explores how API parameters affect model behavior.")
    print(f"We'll examine temperature, top-p, top-k, and other key controls.\n")
    
    demos = [
        ("Temperature Spectrum", demo_1_temperature_spectrum),
        ("Same Prompt Different Temps", demo_2_same_prompt_different_temps),
        ("Response Variance Analysis", demo_3_response_analysis),
        ("Creativity Scale (0-2)", demo_4_creativity_scale),
        ("Use Case Recommendations", demo_5_use_case_recommendations),
        ("Parameter Combinations", demo_6_parameter_combinations),
    ]
    
    print(f"{Fore.YELLOW}Running 6 demonstrations...\n")
    
    for title, demo_func in demos:
        try:
            demo_func()
            print(f"{Fore.GREEN}✓ {title} completed\n")
        except Exception as e:
            print(f"{Fore.RED}✗ {title} failed: {e}\n")
    
    print(f"\n{Fore.CYAN}{Style.BRIGHT}{'='*70}")
    print(f"Demonstrations Complete!".center(70))
    print(f"{'='*70}{Style.RESET_ALL}\n")
    
    print(f"{Fore.GREEN}✓ Visualizations saved to: output/")
    print(f"{Fore.WHITE}Next steps:")
    print(f"  1. Review the visualizations")
    print(f"  2. Configure Azure credentials in .env")
    print(f"  3. Run with real API calls (set to mock by default)\n")


if __name__ == "__main__":
    main()
