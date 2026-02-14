"""
Quick start script to verify the project is set up correctly.
Run this to test if all dependencies are installed and working.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))


def check_dependencies():
    """Check if all required dependencies are installed."""
    dependencies = {
        'tiktoken': 'Token encoding/decoding',
        'matplotlib': 'Visualization',
        'numpy': 'Numerical computation',
        'pandas': 'Data manipulation',
        'colorama': 'Colored terminal output',
    }
    
    print("Checking dependencies...\n")
    all_ok = True
    
    for package, description in dependencies.items():
        try:
            __import__(package)
            print(f"✓ {package:15} - {description}")
        except ImportError:
            print(f"✗ {package:15} - {description} [MISSING]")
            all_ok = False
    
    return all_ok


def test_tokenizer():
    """Test basic tokenization functionality."""
    print("\nTesting tokenizer...\n")
    
    try:
        from tokenizer_utils import TextTokenizer
        
        tokenizer = TextTokenizer(model="gpt-3.5-turbo")
        text = "Hello, tokenization! 🚀"
        
        tokens = tokenizer.tokenize(text)
        analysis = tokenizer.analyze_text(text)
        
        print(f"Text: \"{text}\"")
        print(f"Characters: {analysis['character_count']}")
        print(f"Tokens: {analysis['token_count']}")
        print(f"Token IDs: {tokens}")
        print(f"\n✓ Tokenizer working correctly!")
        
        return True
    except Exception as e:
        print(f"✗ Tokenizer test failed: {e}")
        return False


def test_visualization():
    """Test visualization functionality."""
    print("\nTesting visualization...\n")
    
    try:
        from visualizer import TokenizationVisualizer
        print("✓ Visualization module imported successfully!")
        return True
    except Exception as e:
        print(f"✗ Visualization test failed: {e}")
        return False


def main():
    print("=" * 60)
    print("TOKENIZATION DEMO - Quick Start Check")
    print("=" * 60 + "\n")
    
    deps_ok = check_dependencies()
    tokenizer_ok = test_tokenizer()
    viz_ok = test_visualization()
    
    print("\n" + "=" * 60)
    
    if deps_ok and tokenizer_ok and viz_ok:
        print("✓ All checks passed! Ready to run demos.\n")
        print("Quick start commands:")
        print("  • python main_demo.py       - Run basic tokenization demos")
        print("  • python azure_demo.py      - Run Azure OpenAI demo (needs .env)")
        print("=" * 60 + "\n")
        return 0
    else:
        print("✗ Some checks failed. Please run:")
        print("  pip install -r requirements.txt\n")
        print("=" * 60 + "\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
