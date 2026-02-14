"""
Tokenization utilities for demonstrating how text becomes tokens.
Uses tiktoken to tokenize text similar to how Azure OpenAI models do it.
"""

import tiktoken
from typing import List, Tuple, Dict
import json


class TextTokenizer:
    """Handles text tokenization and analysis."""
    
    def __init__(self, model: str = "gpt-3.5-turbo"):
        """
        Initialize tokenizer for a specific model.
        
        Args:
            model: Model name (e.g., "gpt-3.5-turbo", "gpt-4")
        """
        self.model = model
        try:
            self.encoding = tiktoken.encoding_for_model(model)
        except KeyError:
            # Fallback to cl100k_base if model not found
            self.encoding = tiktoken.get_encoding("cl100k_base")
        
        self.model_name = model
    
    def tokenize(self, text: str) -> List[int]:
        """
        Tokenize text into token IDs.
        
        Args:
            text: Text to tokenize
            
        Returns:
            List of token IDs
        """
        return self.encoding.encode(text)
    
    def decode_tokens(self, tokens: List[int]) -> str:
        """
        Decode token IDs back to text.
        
        Args:
            tokens: List of token IDs
            
        Returns:
            Decoded text
        """
        return self.encoding.decode(tokens)
    
    def tokenize_with_details(self, text: str) -> List[Tuple[int, str]]:
        """
        Tokenize text and return both token IDs and their string representations.
        
        Args:
            text: Text to tokenize
            
        Returns:
            List of tuples (token_id, token_string)
        """
        tokens = self.tokenize(text)
        token_strings = []
        
        for token_id in tokens:
            token_str = self.encoding.decode_single_token_bytes(token_id).decode(
                'utf-8', errors='replace'
            )
            token_strings.append((token_id, token_str))
        
        return token_strings
    
    def get_token_count(self, text: str) -> int:
        """Get the number of tokens in text."""
        return len(self.tokenize(text))
    
    def analyze_text(self, text: str) -> Dict:
        """
        Comprehensive analysis of how text is tokenized.
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary with tokenization analysis
        """
        tokens = self.tokenize(text)
        token_details = self.tokenize_with_details(text)
        
        return {
            "text": text,
            "character_count": len(text),
            "word_count": len(text.split()),
            "token_count": len(tokens),
            "tokens": tokens,
            "token_details": token_details,
            "model": self.model_name,
            "avg_chars_per_token": len(text) / len(tokens) if tokens else 0,
            "avg_bytes_per_token": sum(len(t[1]) for t in token_details) / len(tokens) if tokens else 0
        }
    
    def compare_tokenization(self, texts: List[str]) -> List[Dict]:
        """
        Compare tokenization across multiple texts.
        
        Args:
            texts: List of texts to compare
            
        Returns:
            List of analysis dictionaries
        """
        return [self.analyze_text(text) for text in texts]
