# API Basics Demo: Temperature Control & Creativity Parameters

## Overview

This demo explores one of the most important concepts in working with Large Language Models: **how API parameters control model behavior**.

Most importantly, it teaches **temperature and other parameters** that directly affect:
- **Consistency**: How predictable responses are
- **Creativity**: How varied and novel responses become
- **Quality**: Whether the model stays on-topic or gets random

## What You'll Learn

### 1. **Temperature Parameter** (The Big One!)
- Range: 0.0 to 2.0
- **0.0**: Completely deterministic (same output every time)
- **0.7**: Sweet spot for most applications
- **1.0+**: Creative but potentially chaotic

### 2. **Response Variance**
- How to measure consistency vs creativity
- How repeated patterns emerge at low temperatures
- Why high temperatures show more variety

### 3. **Use Case Matching**
- Customer support → Low temperature (0.0-0.3)
- General conversation → Medium temperature (0.7)
- Creative writing → High temperature (1.0-1.5)
- Brainstorming → Very high temperature (1.2+)

### 4. **Parameter Combinations**
- How to combine temperature with top-p, top-k, frequency penalties
- Real-world recommended settings for different scenarios

## Key Concepts

### Temperature (0.0 - 2.0)
Controls the randomness of responses:
- **Lower values** → More deterministic, factual, consistent
- **Higher values** → More creative, varied, sometimes chaotic

### Top-P (Nucleus Sampling) (0.0 - 1.0)
Considers only tokens with cumulative probability up to P:
- **0.9**: Uses only top 90% cumulative probability (good balance)
- **1.0**: Uses all tokens (default)

### Top-K
Selects from the K most likely next tokens:
- **40**: Only the top 40 tokens are considered
- **-1**: Disabled (uses all tokens)

### Frequency Penalty (-2.0 - 2.0)
Reduces likelihood of repeating tokens:
- **0.0**: Default (no penalty)
- **1.0**: Moderate anti-repetition
- **2.0**: Strong anti-repetition

## Demo Structure

```
main_demo.py                 # Main demonstration script
├── Demo 1: Temperature Spectrum
│   Shows the full range and effects of temperatures
│
├── Demo 2: Same Prompt Different Temps  
│   Real responses at different temperature settings
│
├── Demo 3: Response Variance Analysis
│   Measures consistency and repetition rates
│
├── Demo 4: Creativity Scale (0-2)
│   Visual representation of the temperature scale
│
├── Demo 5: Use Case Recommendations
│   Best temperatures for different scenarios
│
└── Demo 6: Parameter Combinations
    How to combine parameters effectively

src/
├── api_parameters.py        # Parameter analysis and mock responses
├── api_client.py            # Azure OpenAI API client
├── visualizer.py            # Visualization generation
└── __init__.py              # Package initialization

output/                       # Generated visualizations
├── temperature_spectrum.png
└── response_variance.png
```

## Generated Visualizations

### 1. **Temperature Spectrum Chart**
- Shows creativity vs consistency trade-off
- Displays temperature zones and their characteristics
- Helps understand when to use each temperature

### 2. **Response Variance Analysis**
- Bar charts showing variance at each temperature
- Repetition rates across different settings
- Visual comparison of consistency metrics

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the demo
python main_demo.py

# 3. View generated visualizations
# Output files saved to: output/
```

## Configuration

### Mock Mode (Default)
By default, the demo uses mock LLM responses (no API calls needed).

### Real API Mode
To use actual Azure OpenAI API:

1. Create a `.env` file in the project root:
```
AZURE_OPENAI_API_KEY=your_key_here
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_DEPLOYMENT_NAME=your_deployment
AZURE_MODEL_NAME=gpt-35-turbo
```

2. Uncomment API calls in `main_demo.py`

## Tips & Best Practices

### For Different Tasks:

**Factual Accuracy Needed?** → Use low temperature (0.0-0.3)
- Customer support
- Data retrieval
- Technical documentation

**Balance Needed?** → Use medium temperature (0.7)
- General conversation
- Email composition
- Content summarization

**Creativity Needed?** → Use high temperature (1.0-1.5)
- Creative writing
- Brainstorming
- Story generation

**Maximum Variety?** → Use very high temperature (1.5-2.0)
- Experimental exploration
- Game design
- Artistic applications

## Key Files

| File | Purpose |
|------|---------|
| `main_demo.py` | Main executable with all 6 demonstrations |
| `api_parameters.py` | Temperature analysis and mock responses |
| `api_client.py` | Azure OpenAI integration |
| `visualizer.py` | Chart generation for parameter effects |
| `requirements.txt` | Python dependencies |
| `.env` | API credentials (optional) |

## Understanding the Output

### Response Statistics
- **Variance**: How different responses are (0=identical, 1=very different)
- **Repetition Rate**: How much repeated text appears (0=none, 1=high)
- **Consistency**: Related to low variance and high repetition

### Temperature Zones
- **0.0**: Deterministic (100% reproducible)
- **0.3**: Focused (very consistent)
- **0.7**: Balanced (recommended for most uses)
- **1.0**: Creative (notable variation)
- **1.5+**: Chaotic (highly unpredictable)

## Common Questions

**Q: What's the recommended temperature for my use case?**
A: Start with 0.7 and adjust based on results. Lower for consistency, higher for creativity.

**Q: Should I use temperature or top-p?**
A: Temperature is usually sufficient. Top-p is useful for fine-tuning when temperature alone isn't enough.

**Q: Can I set temperature to 0 in production?**
A: Yes! It's actually recommended for deterministic tasks like customer support.

**Q: What happens if I set top-p and temperature both?**
A: They work together. Temperature controls randomness, top-p controls which tokens are considered. Use both for fine control.

## Further Reading

- [OpenAI Documentation on Temperature](https://platform.openai.com/docs/guides/gpt/temperature)
- [Understanding Top-K and Top-P Sampling](https://huggingface.co/blog/how-to-generate)
- [Best Practices for Prompting](https://help.openai.com/en/articles/6654000-best-practices-for-api-usage)

---

**Note**: This is an educational demonstration. For production use, always test thoroughly with your specific use cases and data.
