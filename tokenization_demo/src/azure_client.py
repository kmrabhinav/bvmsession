"""
Azure OpenAI client for making API calls.
"""

import os
from typing import Optional
from azure.openai import AzureOpenAI
from dotenv import load_dotenv


class AzureOpenAIClient:
    """Manages Azure OpenAI API connections and calls."""
    
    def __init__(self):
        """Initialize Azure OpenAI client from environment variables."""
        load_dotenv()
        
        self.api_key = os.getenv("AZURE_OPENAI_API_KEY")
        self.endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        self.deployment = os.getenv("AZURE_DEPLOYMENT_NAME")
        self.model_name = os.getenv("AZURE_MODEL_NAME", "gpt-35-turbo")
        
        if not all([self.api_key, self.endpoint, self.deployment]):
            raise ValueError(
                "Missing Azure OpenAI configuration. "
                "Please set AZURE_OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT, "
                "and AZURE_DEPLOYMENT_NAME environment variables."
            )
        
        self.client = AzureOpenAI(
            api_key=self.api_key,
            azure_endpoint=self.endpoint,
            api_version="2024-02-15-preview"
        )
    
    def chat_completion(self, messages: list, temperature: float = 0.7) -> str:
        """
        Get a chat completion from Azure OpenAI.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            temperature: Temperature for response generation
            
        Returns:
            The assistant's response text
        """
        response = self.client.chat.completions.create(
            model=self.deployment,
            messages=messages,
            temperature=temperature,
            max_tokens=500
        )
        
        return response.choices[0].message.content
    
    def get_model_info(self) -> dict:
        """Get information about the configured model."""
        return {
            "deployment_name": self.deployment,
            "model_name": self.model_name,
            "endpoint": self.endpoint
        }
