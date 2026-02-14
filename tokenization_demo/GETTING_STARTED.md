# Getting Started - Tokenization Demo

## ✓ Demo Successfully Created!

Your Azure OpenAI Tokenization visualization demo is ready to use. This project demonstrates how text is converted into tokens (numbers) that language models understand.

## Project Location
```
C:\Demo\tokenization_demo\
```

## Quick Start

### 1. Run the Basic Tokenization Demo (No Setup Required)
```powershell
cd C:\Demo\tokenization_demo
C:/Demo/.venv/Scripts/python.exe main_demo.py
```

This will show:
- ✓ Text converted to token IDs
- ✓ How different text types tokenize differently
- ✓ Token reconstruction (numbers back to text)
- ✓ Visualization charts (saved as PNG files)

### 2. Run the Azure OpenAI Demo (Requires Setup)
```powershell
cd C:\Demo\tokenization_demo
C:/Demo/.venv/Scripts/python.exe azure_demo.py
```

To use this, first set up Azure credentials:
```powershell
copy .env.example .env
# Edit .env with your Azure OpenAI credentials
```

## Project Contents

### Main Scripts
- **main_demo.py** - 6 interactive demonstrations of tokenization (recommended first)
- **azure_demo.py** - Azure OpenAI integration with token cost estimation  
- **quickstart.py** - Verify all dependencies are installed

### Source Modules
- **src/tokenizer_utils.py** - Core tokenization logic using tiktoken
- **src/azure_client.py** - Azure OpenAI API client
- **src/visualizer.py** - Visualization functions for charts

### Documentation
- **README.md** - Complete documentation and advanced usage
- **data/sample_texts.md** - Test texts for experimentation

### Generated Files
- **output/tokenization_comparison.png** - Multi-text comparison chart
- **output/token_breakdown.png** - Detailed token visualization

## What Gets Demonstrated

### Understanding Tokenization
A token is a chunk of text that models process. Not 1:1 with characters:

```
Input:  "Hello, World!" (13 characters)
Output: [9906, 11, 4435, 0] (4 tokens)

Mapping:
  9906  → "Hello"
  11    → ","
  4435  → " World"
  0     → "!"
```

### Key Insights
1. **Compression Ratio**: Text typically compresses to ~4 chars per token
2. **Variable Encoding**: Numbers/special chars have different ratios than English
3. **Unicode Handling**: Emoji and non-Latin text take more tokens
4. **API Cost**: Azure OpenAI charges by tokens, not characters

## Usage Examples

### Use as a Library
```python
from src.tokenizer_utils import TextTokenizer

tokenizer = TextTokenizer(model="gpt-3.5-turbo")

# Get token count
count = tokenizer.get_token_count("Your text here")

# Get detailed analysis
analysis = tokenizer.analyze_text("Your text here")
print(f"Tokens: {analysis['token_count']}")
print(f"Efficiency: {analysis['avg_chars_per_token']:.2f} chars/token")

# Tokenize and view details
details = tokenizer.tokenize_with_details("Your text here")
for token_id, token_str in details:
    print(f"  {token_id} → '{token_str}'")
```

## Key Features

✓ **No Azure Required** - Basic demo works with just tiktoken  
✓ **Visual Output** - Generates PNG charts of tokenization  
✓ **Educational** - 6 different demonstrations  
✓ **Production Ready** - Use modules in your own code  
✓ **Comprehensive Examples** - Covers text, code, emoji, numbers  
✓ **Cost Estimation** - Calculate Azure OpenAI token usage  

## Troubleshooting

### "ModuleNotFoundError"
Make sure you have run:
```powershell
pip install -r requirements.txt
```

### Visualizations not displaying
Try opening the PNG files directly:
- `C:\Demo\tokenization_demo\output\token_breakdown.png`
- `C:\Demo\tokenization_demo\output\tokenization_comparison.png`

### Azure demo fails with "Missing configuration"
1. Create `.env` file from `.env.example`
2. Fill in your Azure credentials:
   - AZURE_OPENAI_API_KEY
   - AZURE_OPENAI_ENDPOINT
   - AZURE_DEPLOYMENT_NAME

## What to Try Next

1. **Experiment with custom text:**
   - Edit `data/sample_texts.md` with your own examples
   - Run demos to see how your text tokenizes

2. **Integrate into your project:**
   - Use `TextTokenizer` class in your Python code
   - Estimate token usage before API calls
   - Visualize your own text tokenization

3. **Azure Integration:**
   - Set up credentials in `.env`
   - Run `azure_demo.py` to see real API token usage
   - Understand pricing implications

## Resources

- [OpenAI Tokenizer Tool](https://platform.openai.com/tokenizer) - Online visualization
- [Azure OpenAI Documentation](https://learn.microsoft.com/azure/ai-services/openai/)
- [Tiktoken GitHub](https://github.com/openai/tiktoken)
- [Token Pricing](https://openai.com/pricing/gpt-4-turbo) - Understanding costs

## Additional Information

- Python Version: 3.10.8
- Virtual Environment: Active at `C:/Demo/.venv/`
- All dependencies installed and verified
- Ready for production use or educational demonstration

---

**Next Steps:** Run `python main_demo.py` to start exploring how text becomes tokens!
