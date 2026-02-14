"""
Azure OpenAI API client with parameter control.
"""

import os
from typing import Optional, Dict, Any
from dotenv import load_dotenv

try:
    from azure.openai import AzureOpenAI
    AZURE_AVAILABLE = True
except ImportError:
    AZURE_AVAILABLE = False


class APIClient:
    """Manages API calls with various parameters."""
    
    def __init__(self):
        """Initialize API client from environment variables."""
        load_dotenv()
        
        self.api_key = os.getenv("AZURE_OPENAI_API_KEY")
        self.endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        self.deployment = os.getenv("AZURE_DEPLOYMENT_NAME")
        self.model_name = os.getenv("AZURE_MODEL_NAME", "gpt-35-turbo")
        
        self.configured = all([self.api_key, self.endpoint, self.deployment]) and AZURE_AVAILABLE
        self.client = None
        
        if self.configured:
            try:
                self.client = AzureOpenAI(
                    api_key=self.api_key,
                    azure_endpoint=self.endpoint,
                    api_version="2024-02-15-preview"
                )
            except Exception as e:
                self.configured = False
                self.client = None
    
    def is_configured(self) -> bool:
        """Check if API is properly configured."""
        return self.configured
    
    def call_api(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 200,
        top_p: float = 1.0
    ) -> Optional[str]:
        """
        Make an API call with specified parameters.
        
        Args:
            prompt: The prompt to send
            temperature: Creativity level (0.0 to 2.0)
            max_tokens: Maximum response length
            top_p: Nucleus sampling parameter
            
        Returns:
            Response text or None if not configured
        """
        if not self.configured:
            return None
        
        try:
            response = self.client.chat.completions.create(
                model=self.deployment,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=top_p
            )
            
            return response.choices[0].message.content
        except Exception as e:
            print(f"API Error: {e}")
            return None
    
    def batch_call(
        self,
        prompt: str,
        temperatures: list,
        num_calls_per_temp: int = 3,
        max_tokens: int = 200
    ) -> Dict[float, list]:
        """
        Make multiple API calls at different temperatures.
        
        Args:
            prompt: The prompt to send
            temperatures: List of temperature values to test
            num_calls_per_temp: How many times to call each temperature
            max_tokens: Maximum response length
            
        Returns:
            Dictionary mapping temperature to list of responses
        """
        if not self.configured:
            return {}
        
        results = {}
        
        for temp in temperatures:
            results[temp] = []
            for _ in range(num_calls_per_temp):
                response = self.call_api(prompt, temperature=temp, max_tokens=max_tokens)
                if response:
                    results[temp].append(response)
        
        return results
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the configured model."""
        return {
            "deployment_name": self.deployment,
            "model_name": self.model_name,
            "endpoint": self.endpoint,
            "configured": self.configured
        }
