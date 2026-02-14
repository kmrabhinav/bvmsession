# Getting Started with API Basics Demo

## Prerequisites

- Python 3.10 or higher
- pip package manager
- Virtual environment (recommended)

## Installation Steps

### 1. Set Up Virtual Environment

```bash
# Navigate to the project directory
cd c:\Demo\api_basics_demo

# Create virtual environment (or use shared one)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
```

### 2. Install Dependencies

```bash
# Install all required packages
pip install -r requirements.txt
```

### 3. Verify Installation

```bash
# Test imports
python -c "import openai, matplotlib, numpy; print('All dependencies installed!')"
```

## Running the Demo

### Run Main Demo

```bash
# Run all demonstrations
python main_demo.py
```

This will:
1. Display temperature spectrum information
2. Show responses at different temperatures
3. Analyze response variance
4. Show creativity scale
5. Display use case recommendations
6. Explain parameter combinations
7. Generate PNG visualizations

### Generated Output

Visualizations will be saved to `output/`:
- `temperature_spectrum.png` - Temperature effects chart
- `response_variance.png` - Variance analysis chart

## Configuration

### Using Mock Data (Default)

The demo uses mock LLM responses by default. No configuration needed!

### Using Real Azure OpenAI (Optional)

1. **Create `.env` file** in project root:

```env
AZURE_OPENAI_API_KEY=your_api_key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_DEPLOYMENT_NAME=your_deployment_name
AZURE_MODEL_NAME=gpt-35-turbo
```

2. **Update main_demo.py** to use real API calls (lines marked with "TODO")

## File Structure

```
api_basics_demo/
├── main_demo.py              # Main script - run this!
├── requirements.txt          # Dependencies
├── .env                       # API secrets (optional)
├── README.md                  # This file
├── GETTING_STARTED.md         # You are here
├── PROJECT_SUMMARY.md         # Architecture overview
├── VISUAL_GUIDE.md            # Visual explanations
├── src/
│   ├── __init__.py
│   ├── api_parameters.py      # Temperature analysis
│   ├── api_client.py          # API integration
│   └── visualizer.py          # Chart generation
├── output/                    # Generated visualizations
└── data/                      # Sample data (if any)
```

## Quick Reference

### Temperature Settings

| Temperature | Use Case | Example |
|-------------|----------|---------|
| 0.0 | Deterministic | Support bot, factual Q&A |
| 0.3 | Focused | Email templates |
| 0.7 | Balanced | **← Recommended** |
| 1.0 | Creative | Story writing |
| 1.5+ | Chaotic | Brainstorming |

### Basic Python Usage

```python
from src.api_parameters import APIParameters
from src.api_client import APIClient

# Get temperature info
info = APIParameters.get_temperature_info(0.7)
print(info['description'])

# Analyze mock responses
responses = [
    "Paris is the capital of France.",
    "The capital of France is Paris.",
    "France's capital: Paris."
]
analysis = APIParameters.analyze_responses(responses, temperature=0.7)
print(f"Variance: {analysis.variance}")
print(f"Repetition: {analysis.repetition_rate}")
```

## Troubleshooting

### ModuleNotFoundError

```bash
# Make sure virtual environment is activated
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Matplotlib Issues

```bash
# Reinstall matplotlib
pip install --upgrade matplotlib

# Try interactive backend
python -c "import matplotlib; matplotlib.use('TkAgg')"
```

### API Connection Issues

- Verify `.env` file exists with correct credentials
- Check Azure OpenAI endpoint format
- Ensure API key is valid and not expired
- Test with `APIClient().is_configured()`

## Next Steps

1. **Run the demo**: `python main_demo.py`
2. **Review visualizations** in `output/` folder
3. **Read PROJECT_SUMMARY.md** for architecture details
4. **Check VISUAL_GUIDE.md** for visual explanations
5. **Experiment** with different temperatures in your own code

## Learning Path

1. Start with Demo 1 (Temperature Spectrum) - understand the concept
2. Move to Demo 2 (Same Prompt Different Temps) - see it in action
3. Study Demo 3 (Response Variance) - understand metrics
4. Learn Demo 4 (Creativity Scale) - visualize the range
5. Review Demo 5 (Use Case Recommendations) - match to your needs
6. Master Demo 6 (Parameter Combinations) - advanced tuning

## Common Commands

```bash
# Run full demo
python main_demo.py

# Run specific demo (modify main_demo.py to call directly)
python -c "from main_demo import demo_1_temperature_spectrum; demo_1_temperature_spectrum()"

# Test API connection
python -c "from src.api_client import APIClient; print(APIClient().is_configured())"

# Check installed packages
pip list

# Update dependencies
pip install --upgrade -r requirements.txt
```

## Performance Tips

- First run will generate visualizations (matplotlib startup)
- Subsequent runs will be faster
- Mock responses are instantaneous (no API calls)
- Real API calls may take a few seconds per request

## Getting Help

- Check the error message carefully
- Review `README.md` for detailed explanations
- Look at `VISUAL_GUIDE.md` for graphical help
- Verify all dependencies with `pip list`
- Ensure Python 3.10+ is being used

## Ready to Explore?

```bash
python main_demo.py
```

Enjoy learning about API parameters! 🚀
