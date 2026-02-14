"""
API parameter utilities for temperature and creativity control.
Demonstrates how API parameters affect model behavior.
"""

import numpy as np
from typing import List, Dict, Tuple
from dataclasses import dataclass


@dataclass
class TemperatureAnalysis:
    """Analysis of temperature parameter effects."""
    temperature: float
    responses: List[str]
    variance: float
    repetition_rate: float
    description: str


class APIParameters:
    """Manage and analyze API parameters."""
    
    TEMPERATURE_RANGES = {
        0.0: {
            "name": "Deterministic",
            "description": "Always same output",
            "use_case": "Fact-based, consistent answers",
            "creativity": 0,
            "reliability": 10
        },
        0.3: {
            "name": "Low (Focused)",
            "description": "Very consistent, minimal variation",
            "use_case": "Customer service, technical documentation",
            "creativity": 1,
            "reliability": 9
        },
        0.7: {
            "name": "Medium (Balanced)",
            "description": "Balanced creativity and consistency",
            "use_case": "General conversation, content creation",
            "creativity": 5,
            "reliability": 6
        },
        1.0: {
            "name": "High (Creative)",
            "description": "More varied and creative responses",
            "use_case": "Brainstorming, creative writing",
            "creativity": 7,
            "reliability": 5
        },
        1.5: {
            "name": "Very High (Chaotic)",
            "description": "Highly unpredictable and creative",
            "use_case": "Experimental, exploratory use",
            "creativity": 10,
            "reliability": 3
        }
    }
    
    @staticmethod
    def get_temperature_info(temperature: float) -> Dict:
        """Get information about a temperature value."""
        if temperature == 0.0:
            return APIParameters.TEMPERATURE_RANGES[0.0]
        elif temperature <= 0.3:
            return APIParameters.TEMPERATURE_RANGES[0.3]
        elif temperature <= 0.7:
            return APIParameters.TEMPERATURE_RANGES[0.7]
        elif temperature <= 1.0:
            return APIParameters.TEMPERATURE_RANGES[1.0]
        else:
            return APIParameters.TEMPERATURE_RANGES[1.5]
    
    @staticmethod
    def calculate_text_variance(texts: List[str]) -> float:
        """
        Calculate variance in text responses.
        Lower = more consistent, Higher = more varied.
        """
        if len(texts) < 2:
            return 0.0
        
        # Calculate unique n-grams
        bigrams = set()
        trigrams = set()
        
        for text in texts:
            words = text.lower().split()
            bigrams.update(zip(words, words[1:]))
            trigrams.update(zip(words, words[1:], words[2:]))
        
        # Variance is measured by unique phrases
        unique_phrases = len(bigrams) + len(trigrams)
        total_phrases = sum(len(text.split()) - 1 for text in texts) * 2
        
        variance = unique_phrases / max(total_phrases, 1)
        return min(variance, 1.0)  # Clamp to 0-1
    
    @staticmethod
    def calculate_repetition_rate(texts: List[str]) -> float:
        """
        Calculate how much text is repeated across responses.
        Higher = more repeated patterns.
        """
        if len(texts) < 2:
            return 0.0
        
        # Find repeated sentences
        all_sentences = []
        for text in texts:
            sentences = [s.strip() for s in text.split('.') if s.strip()]
            all_sentences.extend(sentences)
        
        repeated = 0
        for sentence in all_sentences:
            if all_sentences.count(sentence) > 1:
                repeated += 1
        
        rate = repeated / max(len(all_sentences), 1)
        return min(rate, 1.0)
    
    @staticmethod
    def analyze_responses(responses: List[str], temperature: float) -> TemperatureAnalysis:
        """Analyze a list of responses for a given temperature."""
        variance = APIParameters.calculate_text_variance(responses)
        repetition = APIParameters.calculate_repetition_rate(responses)
        
        info = APIParameters.get_temperature_info(temperature)
        
        return TemperatureAnalysis(
            temperature=temperature,
            responses=responses,
            variance=variance,
            repetition_rate=repetition,
            description=info['description']
        )
    
    @staticmethod
    def compare_temperatures(temperature_results: Dict[float, List[str]]) -> Dict:
        """Compare results across different temperatures."""
        analyses = {}
        
        for temp, responses in temperature_results.items():
            analyses[temp] = APIParameters.analyze_responses(responses, temp)
        
        return {
            'analyses': analyses,
            'best_for_consistency': min(
                analyses.items(), 
                key=lambda x: x[1].variance
            )[0],
            'best_for_creativity': max(
                analyses.items(),
                key=lambda x: x[1].variance
            )[0]
        }


class MockLLMResponses:
    """Generate mock responses at different temperatures for demonstration."""
    
    # Base responses
    RESPONSES = {
        0.0: [
            "The capital of France is Paris. Paris is known for the Eiffel Tower.",
            "The capital of France is Paris. Paris is known for the Eiffel Tower.",
            "The capital of France is Paris. Paris is known for the Eiffel Tower.",
        ],
        0.3: [
            "The capital of France is Paris, famous for its iconic Eiffel Tower.",
            "The capital of France is Paris. It's known for the Eiffel Tower.",
            "Paris is the capital of France, celebrated for the Eiffel Tower.",
        ],
        0.7: [
            "France's capital is Paris, a city renowned for the Eiffel Tower and romance.",
            "Paris serves as the capital of France and attracts millions for its charm.",
            "The French capital, Paris, draws visitors with the Eiffel Tower.",
        ],
        1.0: [
            "Ah, Paris! The City of Light and France's beating heart, home to the magnificent Eiffel Tower.",
            "France is ruled from Paris, a romantic metropolis where the Eiffel Tower pierces the sky.",
            "The enigmatic Paris claims the capital throne, its skyline punctuated by Gustave's iron masterpiece.",
        ],
        1.5: [
            "Bebop Paris! The whimsical French nexus of culture, dreams, and a certain pointy iron monument.",
            "In the realm of Gaul's governance, Paris reigns supreme with its mystical tower reaching toward destiny.",
            "Paris—that tempestuous jewel of European chaos—holds France's destiny in her passionate arms.",
        ]
    }
    
    @staticmethod
    def get_responses(temperature: float) -> List[str]:
        """Get mock responses for a temperature."""
        if temperature in MockLLMResponses.RESPONSES:
            return MockLLMResponses.RESPONSES[temperature]
        
        # Find closest temperature
        closest = min(
            MockLLMResponses.RESPONSES.keys(),
            key=lambda x: abs(x - temperature)
        )
        return MockLLMResponses.RESPONSES[closest]
