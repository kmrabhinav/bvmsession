# Tokenization Demo - Complete Documentation

## Overview

This project demonstrates how text is converted into tokens (numbers) using Azure OpenAI and the tiktoken library. It's an educational tool to understand the fundamental process that language models use to process text.

## What is Tokenization?

Tokenization is the process of breaking down text into smaller units called **tokens**. These tokens are:
- The atomic units that language models understand
- Usually subword pieces (not always full words)
- Represented as numeric IDs
- Essential for calculating API costs in services like Azure OpenAI

### Why It Matters

1. **API Costs**: Azure OpenAI bills based on token count, not character count
2. **Model Understanding**: Models process tokens, not letters
3. **Efficiency**: Not all text encodes equally (e.g., "a" = 1 token, but "ae" = 1-2 tokens)
4. **Context Windows**: Models have limits on total tokens they can process

## Project Structure

```
tokenization_demo/
├── main_demo.py           # Basic tokenization demonstrations (no Azure needed)
├── azure_demo.py          # Azure OpenAI integration demo
├── requirements.txt       # Python dependencies
├── .env.example          # Configuration template
├── README.md             # This file
├── data/
│   └── sample_texts.md   # Sample texts for testing
├── src/
│   ├── tokenizer_utils.py     # Tokenization utilities
│   ├── azure_client.py        # Azure OpenAI client
│   └── visualizer.py          # Visualization tools
└── output/               # Generated visualizations
```

## Installation

### Prerequisites
- Python 3.8 or later
- pip package manager

### Steps

1. **Clone/Download the project**
   ```bash
   cd tokenization_demo
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **(Optional) Set up Azure OpenAI credentials**
   ```bash
   copy .env.example .env
   # Edit .env with your Azure credentials
   ```

## Quick Start

### Run Basic Tokenization Demo (No Azure Required)

```bash
python main_demo.py
```

This will show:
- Basic text-to-token conversion
- Detailed tokenization analysis
- Special characters and Unicode handling
- Encoding efficiency comparison
- Token reconstruction (numbers back to text)
- Visual token breakdown charts

### Run Azure OpenAI Demo (Azure Credentials Required)

```bash
python azure_demo.py
```

This will show:
- Token cost estimation
- Azure OpenAI API integration
- Prompt token analysis
- Response token analysis

## Demonstrations Explained

### Demo 1: Basic Text-to-Token Conversion
Shows how a simple sentence is broken into tokens with their numeric IDs.

**Example:**
```
Input: "Hello, World!"
Tokens: [15496, 11, 4435, 0]
```

### Demo 2: Detailed Tokenization Analysis
Analyzes character count, word count, and token count for various texts.

### Demo 3: Special Characters & Unicode
Shows how the tokenizer handles:
- Numbers
- Punctuation
- Code syntax
- Special characters and symbols
- Unicode and emojis

### Demo 4: Encoding Efficiency
Compares how efficiently different types of text are tokenized.

**Key Finding:** English text averages ~4 characters per token, but this varies by content type.

### Demo 5: Token Reconstruction
Demonstrates the reversibility of tokenization - converting tokens back to text.

### Demo 6: Visual Token Breakdown
Creates charts showing:
- How text is broken into individual tokens
- Token IDs and their string representations
- Comparison of multiple texts

## Understanding Token IDs

Each token has:
1. **Token ID** - A numeric identifier (0-100k+)
2. **Token String** - The actual text/piece it represents

Examples:
```
ID: 15496  → "Hello"
ID: 11     → ","
ID: 4435   → "World"
ID: 0      → "!"
```

## Key Insights

### Compression Ratio
Not all text compresses equally to tokens:

| Type          | Example                    | Chars | Tokens | Ratio  |
|---------------|----------------------------|-------|--------|--------|
| English       | "The quick brown fox"      | 19    | 5      | 3.8    |
| Numbers       | "1234567890"               | 10    | 4      | 2.5    |
| Code          | "return result;"           | 15    | 5      | 3.0    |
| Mixed         | "Price: $99.99!"           | 14    | 6      | 2.3    |

### Space and Whitespace
Special characters like spaces are often separate tokens:
- "hello world" = 2-3 tokens (the space might be with one word)
- "hello  world" (double space) = could be different from single space

### Emoji and Unicode
Unicode characters often take multiple tokens:
- "Hello 世界" = more tokens than "Hello World"
- Emojis like 🚀 can be 1-2 tokens each

## Azure OpenAI Cost Implications

For Azure OpenAI pricing, tokens matter:

```
Prompt tokens:   $0.0005 per 1K tokens (example rate)
Completion tokens: $0.0015 per 1K tokens (example rate)
```

So understanding tokenization helps estimate costs:
- 1000 character document ≈ 200-300 tokens
- Cost ≈ $0.10-0.15 for input processing

## Advanced Usage

### Using the Tokenizer Programmatically

```python
from src.tokenizer_utils import TextTokenizer

tokenizer = TextTokenizer(model="gpt-3.5-turbo")

# Get token count
count = tokenizer.get_token_count("Hello, World!")
print(count)  # Output: 4

# Get detailed analysis
analysis = tokenizer.analyze_text("Hello, World!")
print(analysis['token_count'])      # 4
print(analysis['avg_chars_per_token'])  # ~3.25

# Tokenize and reconstruct
text = "Hello, World!"
tokens = tokenizer.tokenize(text)
reconstructed = tokenizer.decode_tokens(tokens)
print(reconstructed == text)  # True
```

### Creating Custom Visualizations

```python
from src.tokenizer_utils import TextTokenizer
from src.visualizer import TokenizationVisualizer

tokenizer = TextTokenizer()
text = "Your text here"
analysis = tokenizer.analyze_text(text)

# Create visualization
TokenizationVisualizer.visualize_tokens_breakdown(
    text,
    analysis['token_details'],
    save_path="my_visualization.png"
)
```

## Troubleshooting

### "ModuleNotFoundError: No module named 'azure'"
**Solution:** Install dependencies
```bash
pip install -r requirements.txt
```

### "Missing Azure OpenAI configuration"
**Solution:** Set up your .env file
```bash
cp .env.example .env
# Edit .env with your credentials
```

### Visualizations not displaying
**Solution:** Make sure matplotlib is installed
```bash
pip install matplotlib
```

## Common Questions

### Q: Are tokens the same across all models?
**A:** Not exactly. Different models may tokenize slightly differently, but they're usually compatible. Azure OpenAI uses the same tiktoken tokenizer as OpenAI.

### Q: How do I know how many tokens my request will use?
**A:** Use the `get_token_count()` method or analyze before sending:
```python
tokenizer = TextTokenizer()
count = tokenizer.get_token_count(your_prompt)
```

### Q: Why does my 100-character text use 30 tokens?
**A:** Some texts compress better than others. Punctuation, numbers, and special characters often take more tokens per character.

### Q: Can I use this without Azure?
**A:** Yes! Run `main_demo.py` - it works with just tiktoken and doesn't require Azure credentials.

## Resources

- [OpenAI Tokenizer Tool](https://platform.openai.com/tokenizer) - Visualize tokenization online
- [Azure OpenAI Documentation](https://learn.microsoft.com/azure/ai-services/openai/)
- [Tiktoken GitHub](https://github.com/openai/tiktoken) - Token counting library
- [OpenAI API Documentation](https://platform.openai.com/docs/)

## License

This project is provided as an educational demonstration.

## Support

For issues or questions:
1. Check the Troubleshooting section
2. Review the documentation in README.md
3. Check Azure OpenAI documentation for API-specific issues
