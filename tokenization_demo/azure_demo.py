"""
Azure OpenAI Integration Demo - Tokenization with Azure models.
This script demonstrates how to use tokenization with Azure OpenAI API calls.

SETUP REQUIRED:
1. Create a .env file from .env.example
2. Fill in your Azure OpenAI credentials:
   - AZURE_OPENAI_API_KEY
   - AZURE_OPENAI_ENDPOINT
   - AZURE_DEPLOYMENT_NAME
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from tokenizer_utils import TextTokenizer
from azure_client import AzureOpenAIClient
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)


def print_header(title: str):
    """Print a formatted section header."""
    print(f"\n{Fore.CYAN}{'='*70}")
    print(f"{Fore.CYAN}{title.center(70)}")
    print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")


def demo_azure_openai_integration():
    """Demonstrate Azure OpenAI with tokenization awareness."""
    print_header("Azure OpenAI Integration Demo")
    
    try:
        # Initialize clients
        print(f"{Fore.YELLOW}Initializing clients...{Style.RESET_ALL}")
        azure_client = AzureOpenAIClient()
        tokenizer = TextTokenizer(model="gpt-3.5-turbo")
        
        # Get model info
        model_info = azure_client.get_model_info()
        print(f"{Fore.GREEN}✓ Connected to Azure OpenAI{Style.RESET_ALL}")
        print(f"  Deployment: {model_info['deployment_name']}")
        print(f"  Model: {model_info['model_name']}")
        print(f"  Endpoint: {model_info['endpoint']}")
        
        # Define a prompt
        system_message = "You are a helpful AI assistant that explains concepts clearly and concisely."
        user_prompt = "Explain tokenization in AI models in 2-3 sentences."
        
        print(f"\n{Fore.YELLOW}System Message:{Style.RESET_ALL}")
        print(f"  \"{system_message}\"")
        
        print(f"\n{Fore.YELLOW}User Prompt:{Style.RESET_ALL}")
        print(f"  \"{user_prompt}\"")
        
        # Analyze tokens for the prompt
        print(f"\n{Fore.CYAN}Token Analysis:{Style.RESET_ALL}")
        
        # System message tokens
        sys_tokens = tokenizer.tokenize(system_message)
        print(f"  {Fore.GREEN}System Message:{Style.RESET_ALL}")
        print(f"    Characters: {len(system_message)}")
        print(f"    Tokens: {len(sys_tokens)}")
        print(f"    Ratio: {len(system_message)/len(sys_tokens):.2f} chars/token")
        
        # User prompt tokens
        user_tokens = tokenizer.tokenize(user_prompt)
        print(f"  {Fore.GREEN}User Prompt:{Style.RESET_ALL}")
        print(f"    Characters: {len(user_prompt)}")
        print(f"    Tokens: {len(user_tokens)}")
        print(f"    Ratio: {len(user_prompt)/len(user_tokens):.2f} chars/token")
        
        # Total tokens in request
        total_request_tokens = len(sys_tokens) + len(user_tokens)
        print(f"  {Fore.YELLOW}Request Total: {total_request_tokens} tokens{Style.RESET_ALL}")
        
        # Make API call and show token costs
        print(f"\n{Fore.CYAN}Sending request to Azure OpenAI...{Style.RESET_ALL}")
        
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_prompt}
        ]
        
        response = azure_client.chat_completion(messages, temperature=0.7)
        
        print(f"\n{Fore.GREEN}✓ Received response:{Style.RESET_ALL}")
        print(f"  \"{response}\"\n")
        
        # Analyze response tokens
        response_tokens = tokenizer.tokenize(response)
        print(f"{Fore.CYAN}Response Token Analysis:{Style.RESET_ALL}")
        print(f"  Characters: {len(response)}")
        print(f"  Tokens: {len(response_tokens)}")
        print(f"  Ratio: {len(response)/len(response_tokens):.2f} chars/token")
        
        # Total conversation tokens
        total_tokens = total_request_tokens + len(response_tokens)
        print(f"\n{Fore.YELLOW}Total Conversation Tokens: {total_tokens}{Style.RESET_ALL}")
        print(f"  Request: {total_request_tokens} tokens")
        print(f"  Response: {len(response_tokens)} tokens")
        
    except ValueError as e:
        print(f"{Fore.RED}Configuration Error: {e}{Style.RESET_ALL}")
        print(f"\n{Fore.YELLOW}Please set up Azure OpenAI credentials:{Style.RESET_ALL}")
        print("  1. Copy .env.example to .env")
        print("  2. Fill in your Azure OpenAI credentials")
        print("  3. Run this script again")
    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()


def demo_token_cost_estimation():
    """Demonstrate token cost estimation for API calls."""
    print_header("Token Cost Estimation Demo")
    
    tokenizer = TextTokenizer(model="gpt-3.5-turbo")
    
    # Sample requests
    requests = [
        {
            "name": "Simple Question",
            "system": "You are helpful.",
            "user": "What is 2+2?"
        },
        {
            "name": "Document Analysis",
            "system": "You are an expert document analyst.",
            "user": "Analyze this: " + "Lorem ipsum dolor sit amet. " * 10
        },
        {
            "name": "Code Generation",
            "system": "You are a Python expert.",
            "user": "Write a function to sort a list of dictionaries by a key."
        },
    ]
    
    print(f"{Fore.CYAN}Estimating token costs for sample requests...{Style.RESET_ALL}\n")
    
    for request in requests:
        print(f"{Fore.YELLOW}{request['name']}:{Style.RESET_ALL}")
        
        sys_tokens = tokenizer.tokenize(request['system'])
        user_tokens = tokenizer.tokenize(request['user'])
        total_input_tokens = len(sys_tokens) + len(user_tokens)
        
        # Estimate response (typically 50-500 tokens depending on request)
        estimated_response_tokens = 100  # Conservative estimate
        
        total_tokens = total_input_tokens + estimated_response_tokens
        
        print(f"  System Message: {len(sys_tokens)} tokens")
        print(f"  User Input: {len(user_tokens)} tokens")
        print(f"  Estimated Response: ~{estimated_response_tokens} tokens")
        print(f"  {Fore.GREEN}Total: ~{total_tokens} tokens{Style.RESET_ALL}\n")


def main():
    """Run Azure OpenAI demonstration."""
    print(f"\n{Fore.CYAN}")
    print("╔" + "═"*68 + "╗")
    print("║" + "Azure OpenAI Tokenization Demo".center(68) + "║")
    print("║" + "Understanding API Token Usage".center(68) + "║")
    print("╚" + "═"*68 + "╝")
    print(f"{Style.RESET_ALL}")
    
    demo_token_cost_estimation()
    
    # Try Azure OpenAI demo if credentials are available
    print(f"\n{Fore.CYAN}Attempting Azure OpenAI connection...{Style.RESET_ALL}")
    demo_azure_openai_integration()
    
    print(f"\n{Fore.GREEN}✓ Azure demo completed!{Style.RESET_ALL}\n")


if __name__ == "__main__":
    main()
