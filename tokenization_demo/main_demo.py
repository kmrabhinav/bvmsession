"""
Main demonstration of text tokenization with Azure OpenAI.
Visualizes how text is converted into tokens and how tokens become numbers.
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from tokenizer_utils import TextTokenizer
from visualizer import TokenizationVisualizer
from colorama import Fore, Style, init

# Initialize colorama for colored output
init(autoreset=True)


def print_header(title: str):
    """Print a formatted section header."""
    print(f"\n{Fore.CYAN}{'='*70}")
    print(f"{Fore.CYAN}{title.center(70)}")
    print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")


def demo_basic_tokenization():
    """Demonstrate basic text to token conversion."""
    print_header("DEMO 1: Basic Text-to-Token Conversion")
    
    tokenizer = TextTokenizer(model="gpt-3.5-turbo")
    
    # Example 1: Simple sentence
    text1 = "Hello, World!"
    print(f"{Fore.YELLOW}Input Text:{Style.RESET_ALL} \"{text1}\"")
    print(f"{Fore.YELLOW}Character Count:{Style.RESET_ALL} {len(text1)}")
    
    tokens = tokenizer.tokenize(text1)
    print(f"{Fore.YELLOW}Tokens (IDs):{Style.RESET_ALL} {tokens}")
    print(f"{Fore.YELLOW}Token Count:{Style.RESET_ALL} {len(tokens)}")
    
    # Show detailed token breakdown
    print(f"\n{Fore.GREEN}Token Breakdown:{Style.RESET_ALL}")
    print(f"{Fore.GREEN}{'-'*50}{Style.RESET_ALL}")
    
    token_details = tokenizer.tokenize_with_details(text1)
    for i, (token_id, token_str) in enumerate(token_details):
        # Display token string with visible spaces
        display_str = repr(token_str)[1:-1]
        print(f"  Token {i}: ID={Fore.MAGENTA}{token_id:5d}{Style.RESET_ALL} | " 
              f"String={Fore.CYAN}\"{display_str}\"{Style.RESET_ALL}")
    
    return tokenizer, text1


def demo_detailed_analysis():
    """Demonstrate detailed tokenization analysis."""
    print_header("DEMO 2: Detailed Tokenization Analysis")
    
    tokenizer = TextTokenizer(model="gpt-3.5-turbo")
    
    texts = [
        "Hello, World!",
        "Python is great for AI and machine learning.",
        "🚀 Tokens 123 #hashtag email@example.com",
    ]
    
    for i, text in enumerate(texts, 1):
        print(f"{Fore.YELLOW}Text {i}:{Style.RESET_ALL} \"{text}\"")
        analysis = tokenizer.analyze_text(text)
        
        print(f"  {Fore.GREEN}Characters:{Style.RESET_ALL} {analysis['character_count']}")
        print(f"  {Fore.GREEN}Words:{Style.RESET_ALL} {analysis['word_count']}")
        print(f"  {Fore.GREEN}Tokens:{Style.RESET_ALL} {analysis['token_count']}")
        print(f"  {Fore.GREEN}Avg Chars/Token:{Style.RESET_ALL} {analysis['avg_chars_per_token']:.2f}")
        print()


def demo_special_characters():
    """Demonstrate how special characters and Unicode are tokenized."""
    print_header("DEMO 3: Special Characters & Unicode Tokenization")
    
    tokenizer = TextTokenizer(model="gpt-3.5-turbo")
    
    examples = [
        ("Numbers", "The year is 2024"),
        ("Punctuation", "What?! Really... yes!!!"),
        ("Code", "def hello(): return 'world'"),
        ("Mixed", "Email: john@example.com | Phone: +1-555-1234"),
        ("Unicode", "Hello 世界 🌍 Привет"),
    ]
    
    for category, text in examples:
        print(f"{Fore.YELLOW}{category}:{Style.RESET_ALL}")
        print(f"  Text: {text}")
        
        tokens = tokenizer.tokenize(text)
        token_details = tokenizer.tokenize_with_details(text)
        
        print(f"  Token Count: {len(tokens)}")
        print(f"  Tokens: {token_details[0:5]}", end="")
        if len(token_details) > 5:
            print(f" ... (+{len(token_details) - 5} more)")
        else:
            print()
        print()


def demo_encoding_differences():
    """Show how different texts can have different compression ratios."""
    print_header("DEMO 4: Encoding Efficiency Comparison")
    
    tokenizer = TextTokenizer(model="gpt-3.5-turbo")
    
    texts = {
        "English": "The quick brown fox jumps over the lazy dog.",
        "Numbers": "1 2 3 4 5 6 7 8 9 0 1234567890",
        "Code": "function calculate(a, b) { return a + b * 2; }",
        "Repetitive": "buffalo buffalo buffalo buffalo buffalo buffalo",
    }
    
    analyses = []
    for category, text in texts.items():
        analysis = tokenizer.analyze_text(text)
        analyses.append(analysis)
        
        ratio = analysis['character_count'] / analysis['token_count']
        print(f"{Fore.YELLOW}{category}:{Style.RESET_ALL}")
        print(f"  Text: {text}")
        print(f"  {Fore.GREEN}Chars: {analysis['character_count']:3d} | "
              f"Tokens: {analysis['token_count']:2d} | "
              f"Ratio: {ratio:.2f} chars/token{Style.RESET_ALL}\n")
    
    # Create visualization
    print(f"\n{Fore.CYAN}Creating comparison visualization...{Style.RESET_ALL}")
    output_path = Path(__file__).parent / "output" / "tokenization_comparison.png"
    output_path.parent.mkdir(exist_ok=True)
    
    TokenizationVisualizer.compare_texts_tokenization(analyses, save_path=str(output_path))
    print(f"{Fore.GREEN}✓ Visualization saved to: {output_path}{Style.RESET_ALL}")


def demo_token_reconstruction():
    """Demonstrate converting tokens back to text."""
    print_header("DEMO 5: Token Reconstruction (Numbers Back to Text)")
    
    tokenizer = TextTokenizer(model="gpt-3.5-turbo")
    
    original_text = "Tokenization is fascinating!"
    print(f"{Fore.YELLOW}Original Text:{Style.RESET_ALL} \"{original_text}\"")
    
    # Convert to tokens
    tokens = tokenizer.tokenize(original_text)
    print(f"\n{Fore.YELLOW}Step 1 - Convert Text to Token IDs:{Style.RESET_ALL}")
    print(f"  {tokens}\n")
    
    # Show the tokens
    token_details = tokenizer.tokenize_with_details(original_text)
    print(f"{Fore.YELLOW}Step 2 - Tokens with Details:{Style.RESET_ALL}")
    for i, (token_id, token_str) in enumerate(token_details):
        display_str = repr(token_str)[1:-1]
        print(f"  Token {i}: {Fore.MAGENTA}{token_id}{Style.RESET_ALL} → {Fore.CYAN}\"{display_str}\"{Style.RESET_ALL}")
    
    # Reconstruct back
    reconstructed = tokenizer.decode_tokens(tokens)
    print(f"\n{Fore.YELLOW}Step 3 - Convert Token IDs Back to Text:{Style.RESET_ALL}")
    print(f"  \"{reconstructed}\"")
    
    match = original_text == reconstructed
    status = f"{Fore.GREEN}✓ Perfect match!{Style.RESET_ALL}" if match else f"{Fore.RED}✗ Mismatch!{Style.RESET_ALL}"
    print(f"\n{Fore.YELLOW}Result:{Style.RESET_ALL} {status}")


def demo_token_visualization():
    """Create detailed visualization of token breakdown."""
    print_header("DEMO 6: Visual Token Breakdown")
    
    tokenizer = TextTokenizer(model="gpt-3.5-turbo")
    text = "AI is transforming technology!"
    
    print(f"{Fore.YELLOW}Text:{Style.RESET_ALL} \"{text}\"")
    analysis = tokenizer.analyze_text(text)
    
    print(f"{Fore.GREEN}Analysis:{Style.RESET_ALL}")
    print(f"  Characters: {analysis['character_count']}")
    print(f"  Tokens: {analysis['token_count']}")
    print(f"  Average: {analysis['avg_chars_per_token']:.2f} chars per token")
    
    # Create visualization
    print(f"\n{Fore.CYAN}Creating token breakdown visualization...{Style.RESET_ALL}")
    output_path = Path(__file__).parent / "output" / "token_breakdown.png"
    output_path.parent.mkdir(exist_ok=True)
    
    TokenizationVisualizer.visualize_tokens_breakdown(
        text, 
        analysis['token_details'],
        save_path=str(output_path)
    )
    print(f"{Fore.GREEN}✓ Visualization saved to: {output_path}{Style.RESET_ALL}")


def main():
    """Run all tokenization demonstrations."""
    print(f"\n{Fore.CYAN}")
    print("╔" + "═"*68 + "╗")
    print("║" + "TOKENIZATION DEMO: How Text Becomes Numbers".center(68) + "║")
    print("║" + "Using Azure OpenAI & tiktoken".center(68) + "║")
    print("╚" + "═"*68 + "╝")
    print(f"{Style.RESET_ALL}")
    
    try:
        # Run demonstrations
        demo_basic_tokenization()
        demo_detailed_analysis()
        demo_special_characters()
        demo_encoding_differences()
        demo_token_reconstruction()
        demo_token_visualization()
        
        # Summary
        print_header("SUMMARY")
        print(f"{Fore.CYAN}Key Takeaways:{Style.RESET_ALL}\n")
        print("1. {:<50} Text is converted to token IDs".format("✓ TOKENIZATION:"))
        print("2. {:<50} Each token is a number".format("✓ NUMERICAL REPRESENTATION:"))
        print("3. {:<50} Tokens are not 1:1 with characters".format("✓ VARIABLE LENGTH:"))
        print("4. {:<50} Special chars/spaces affect tokenization".format("✓ ENCODING:"))
        print("5. {:<50} Tokens can be reconstructed to text".format("✓ REVERSIBILITY:"))
        
        print(f"\n{Fore.GREEN}✓ All demonstrations completed successfully!{Style.RESET_ALL}\n")
        print(f"{Fore.YELLOW}Generated visualizations are in: output/{Style.RESET_ALL}\n")
        
    except FileNotFoundError as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Make sure all dependencies are installed:{Style.RESET_ALL}")
        print("  pip install -r requirements.txt")
    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
