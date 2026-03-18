"""
Azure OpenAI Integration Module
Uses Azure OpenAI services for embeddings and chat completion
"""

import os
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import numpy as np
from dotenv import load_dotenv

try:
    from openai import AzureOpenAI
    AZURE_AVAILABLE = True
except ImportError:
    AZURE_AVAILABLE = False


class AzureOpenAIIntegration:
    """Integrate with Azure OpenAI for embeddings and chat."""
    print("A02")
    def __init__(self):
        print("A1")
        """Initialize Azure OpenAI client from Windows OS or environment variables."""
        # Load .env file from the parent directory (where main_demo.py is)
        env_path = Path(__file__).parent.parent / ".env"
        
        # Debug: Check if .env file exists
        env_exists = env_path.exists()
        if not env_exists:
            print(f"AAAA⚠ .env file not found at: {env_path}")
        
        load_dotenv(str(env_path))
        
        # Check Windows OS environment variables first, then fall back to .env
        self.api_key = os.getenv("AZURE_OPENAI_API_KEY")
        print (self.api_key)
        self.endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        print(self.endpoint)
        self.embedding_deployment = os.getenv("AZURE_EMBEDDING_DEPLOYMENT")
        print(self.embedding_deployment)
        self.chat_deployment = os.getenv("AZURE_CHAT_DEPLOYMENT")
        print(self.chat_deployment)
        self.api_version = os.getenv("OPENAI_API_VERSION", "2024-02-15-preview")
        print(self.api_version)
        print("A03")
        # Log source of configuration (Windows OS vars or .env file)
        self._log_config_source()
        print("A04")
        # Debug: Check which variables are missing
        missing = []
        if not self.api_key:
            missing.append("AZURE_OPENAI_API_KEY")
        if not self.endpoint:
            missing.append("AZURE_OPENAI_ENDPOINT")
        if not self.embedding_deployment:
            missing.append("AZURE_EMBEDDING_DEPLOYMENT")
        if not self.chat_deployment:
            missing.append("AZURE_CHAT_DEPLOYMENT")
        if not AZURE_AVAILABLE:
            missing.append("azure.openai package not installed")
        
        if missing:
            print(f"BBB⚠ Missing configuration: {', '.join(missing)}")
        print("A05")
        self.configured = all([
            self.api_key,
            self.endpoint,
            self.embedding_deployment,
            self.chat_deployment,
            AZURE_AVAILABLE
        ])
        print("A06")
        
        self.client = None
        print("A07")
        if self.configured:
            try:
                self.client = AzureOpenAI(
                    api_key=self.api_key,
                    azure_endpoint=self.endpoint,
                    api_version=self.api_version
                )
                print("A08")
            except Exception as e:
                print(f"TTTError initializing Azure OpenAI: {e}")
                self.configured = False
    
    def _log_config_source(self):
        """Log whether configuration came from Windows OS vars or .env file."""
        # Check if vars exist in Windows OS environment
        import subprocess
        try:
            # Query Windows environment variables
            result = subprocess.run(
                ['powershell', '-Command', 
                 '$env:AZURE_OPENAI_API_KEY'],
                capture_output=True,
                text=True,
                timeout=2
            )
            os_var_exists = bool(result.stdout.strip())
            
            if os_var_exists and self.api_key:
                print("✓ Azure configuration loaded from Windows OS environment variables")
            elif self.api_key:
                print("✓ Azure configuration loaded from .env file (fallback)")
        except:
            # If we can't check OS vars, just continue
            pass
    
    def is_configured(self) -> bool:
        """Check if Azure OpenAI is properly configured."""
        return self.configured
    
    def get_embedding(self, text: str) -> Optional[np.ndarray]:
        """
        Get embedding for text from Azure OpenAI.
        
        Args:
            text: Text to embed
            
        Returns:
            Embedding vector or None if not configured
        """
        if not self.configured:
            return None
        
        try:
            response = self.client.embeddings.create(
                input=text,
                model=self.embedding_deployment
            )
            
            embedding = response.data[0].embedding
            return np.array(embedding)
        
        except Exception as e:
            print(f"Error getting embedding: {e}")
            return None
    
    def get_embeddings_batch(self, texts: List[str]) -> Optional[List[np.ndarray]]:
        """
        Get embeddings for multiple texts.
        
        Args:
            texts: List of texts to embed
            
        Returns:
            List of embedding vectors or None if not configured
        """
        if not self.configured or not texts:
            return None
        
        try:
            response = self.client.embeddings.create(
                input=texts,
                model=self.embedding_deployment
            )
            
            # Sort by index to maintain order
            embeddings_dict = {item.index: np.array(item.embedding) for item in response.data}
            embeddings = [embeddings_dict[i] for i in range(len(texts))]
            
            return embeddings
        
        except Exception as e:
            print(f"Error getting batch embeddings: {e}")
            return None
    
    def generate_answer(
        self,
        query: str,
        context_chunks: List[str],
        system_prompt: Optional[str] = None
    ) -> Tuple[str, Optional[str]]:
        """
        Generate answer using Azure OpenAI Chat with retrieved context.
        
        Args:
            query: User query
            context_chunks: Retrieved context chunks
            system_prompt: Optional system prompt override
            
        Returns:
            Tuple of (answer, model_info) or (None, error_message) if not configured
        """
        if not self.configured:
            return None, "Azure OpenAI not configured"
        
        try:
            # Build context
            context = "\n\n".join([f"[{i+1}] {chunk}" for i, chunk in enumerate(context_chunks)])
            
            # Default system prompt if not provided
            if system_prompt is None:
                system_prompt = (
                    "You are a helpful assistant answering questions based on provided documents. "
                    "Always ground your answers in the provided context. "
                    "If information is not in the context, clearly state that. "
                    "Cite the source sections when applicable."
                )
            
            # Create messages
            messages = [
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": f"Context from document:\n{context}\n\nQuestion: {query}"
                }
            ]
            
            # Call Azure OpenAI Chat
            response = self.client.chat.completions.create(
                model=self.chat_deployment,
                messages=messages,
                temperature=0.7,
                max_tokens=500
            )
            
            answer = response.choices[0].message.content
            model_info = f"Model: {self.chat_deployment}, Tokens: {response.usage.total_tokens}"
            
            return answer, model_info
        
        except Exception as e:
            return None, f"Error generating answer: {e}"
    
    def get_config_info(self) -> Dict:
        """Get configuration information."""
        return {
            'configured': self.configured,
            'endpoint': self.endpoint if self.configured else 'Not set',
            'embedding_model': self.embedding_deployment if self.configured else 'Not set',
            'chat_model': self.chat_deployment if self.configured else 'Not set',
            'api_version': self.api_version if self.configured else 'Not set',
            'config_source': self._get_config_source()
        }
    
    def _get_config_source(self) -> str:
        """Determine if configuration comes from Windows OS vars or .env file."""
        import subprocess
        try:
            result = subprocess.run(
                ['powershell', '-Command', 
                 '$env:AZURE_OPENAI_API_KEY'],
                capture_output=True,
                text=True,
                timeout=2
            )
            if result.stdout.strip():
                return "Windows OS Environment Variables"
        except:
            pass
        
        return ".env file (fallback)" if self.configured else "Not configured"
    
    @staticmethod
    def setup_windows_env_vars():
        """
        Display instructions for setting up Windows OS environment variables.
        
        Usage: 
            from azure_integration import AzureOpenAIIntegration
            AzureOpenAIIntegration.setup_windows_env_vars()
        """
        print("\n" + "="*70)
        print("SETTING UP WINDOWS OS ENVIRONMENT VARIABLES FOR AZURE OPENAI")
        print("="*70 + "\n")
        
        print("Option 1: Set Variables via PowerShell (Current Session Only)")
        print("-" * 70)
        print("""
$env:AZURE_OPENAI_API_KEY = "your-api-key-here"
$env:AZURE_OPENAI_ENDPOINT = "https://your-resource.openai.azure.com/"
$env:OPENAI_API_VERSION = "2024-02-15-preview"
$env:AZURE_EMBEDDING_DEPLOYMENT = "text-embedding-3-small"
$env:AZURE_CHAT_DEPLOYMENT = "gpt-4-turbo"
        """)
        
        print("\nOption 2: Set Variables Permanently via System Properties")
        print("-" * 70)
        print("""
1. Open Settings > System > Advanced system settings
2. Click "Environment Variables" button
3. Under "User variables", click "New"
4. Add each variable:
   - Variable name: AZURE_OPENAI_API_KEY
   - Variable value: your-api-key-here
   (Repeat for other variables)
5. Click OK and restart your terminal/IDE
        """)
        
        print("\nOption 3: Set Variables via PowerShell (Permanent)")
        print("-" * 70)
        print("""
[System.Environment]::SetEnvironmentVariable(
    'AZURE_OPENAI_API_KEY',
    'your-api-key-here',
    [System.EnvironmentVariableTarget]::User
)
        """)
        
        print("\nVerify Configuration:")
        print("-" * 70)
        print("Run this to verify:")
        print("""
python -c "from src.azure_integration import AzureOpenAIIntegration; \\
client = AzureOpenAIIntegration(); \\
print(client.get_config_info())"
        """)
        print("="*70 + "\n")
