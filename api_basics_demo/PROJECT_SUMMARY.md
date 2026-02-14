# API Basics Demo - Project Architecture

## Overview

This project demonstrates how API parameters (especially temperature) control model behavior, consistency, and creativity.

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Main Application                         │
│               (main_demo.py - 6 Demonstrations)             │
└────────┬────────────────────────────────────────────────────┘
         │
    ┌────┴────────────────────────────────────────┬──────────┐
    │                                              │          │
┌───▼──────────────┐  ┌──────────────────────┐  │  │       │
│ API Parameters   │  │ Mock LLM Responses   │  │  │       │
│ Module           │  │ (Default Mode)       │  │  │       │
├──────────────────┤  ├──────────────────────┤  │  │       │
│ • Temperature    │  │ • Pre-built responses│  │  │       │
│   Analysis       │  │ • Different temps    │  │  │       │
│ • Variance       │  │ • Various creativity │  │  │       │
│   Calculation    │  │   levels             │  │  │       │
│ • Repetition     │  ├──────────────────────┤  │  │       │
│   Rate Analysis  │  │ Features:            │  │  │       │
│ • Zone Matching  │  │ • No API call needed │  │  │       │
└───────────────────┘  │ • Fast execution    │  │  │       │
                       └──────────────────────┘  │  │       │
                       ┌────────────────────────┐│  │       │
                       │ Azure OpenAI API Client││  │       │
                       ├────────────────────────┤│  │       │
                       │ • Real API integration ││  │       │
                       │ • Parameter control    │└──┘       │
                       │ • .env configuration   │            │
                       │ • Credential handling  │            │
                       └────────────────────────┘            │
                                              ┌──────────┐
                                              │ Optional │
                                              │ Real API │
                                              │ Calls    │
                                              └──────────┘
             ┌──────────────────────────────────────┐
             │    Visualization Generation          │
             ├──────────────────────────────────────┤
             │ • Temperature spectrum chart         │
             │ • Response variance analysis         │
             │ • Parameter comparison plots         │
             │ • Saves to PNG files (output/)       │
             └──────────────────────────────────────┘
```

## Module Breakdown

### 1. **main_demo.py** - Main Application
**Line Count**: ~350 lines  
**Purpose**: Orchestrates all demonstrations

#### Six Demonstrations:
```
Demo 1: Temperature Spectrum
 └─ Shows full temperature range and effects
 └─ Output: console display + chart

Demo 2: Same Prompt Different Temps
 └─ Runs one prompt at 5 different temperatures
 └─ Shows response variation based on temperature

Demo 3: Response Variance Analysis
 └─ Measures variance and repetition rates
 └─ Identifies best for consistency vs creativity
 └─ Output: statistical analysis + chart

Demo 4: Creativity Scale (0-2)
 └─ Visual representation of temperature scale
 └─ Shows progression from deterministic to chaotic

Demo 5: Use Case Recommendations
 └─ Matches temperatures to specific tasks
 └─ Examples: support (0.0), chat (0.7), creative (1.0+)

Demo 6: Parameter Combinations
 └─ Explains temperature, top-p, top-k, frequency penalty
 └─ Shows recommended combinations for different tasks
```

**Key Functions**:
- `print_header()` - Colored console output
- `demo_X()` - Individual demonstration functions
- `main()` - Orchestrates all demos

### 2. **api_parameters.py** - Parameter Analysis & Mock Responses
**Line Count**: ~250 lines  
**Purpose**: Core logic for temperature analysis

#### Classes:

**APIParameters**
- Static methods for temperature analysis
- `TEMPERATURE_RANGES` - Predefined temperature zones
- `get_temperature_info()` - Returns zone info for any temp
- `calculate_text_variance()` - Measures response diversity
- `calculate_repetition_rate()` - Measures pattern repetition
- `analyze_responses()` - Comprehensive response analysis
- `compare_temperatures()` - Cross-temperature comparison

**TemperatureAnalysis**
- Data class for analysis results
- Stores variance, repetition_rate, responses
- Includes descriptive information

**MockLLMResponses**
- Pre-built responses at different temperatures
- `RESPONSES` - Dictionary keyed by temperature
- `get_responses()` - Retrieves responses with fallback

#### Temperature Zones:
```
0.0     → Deterministic (100% identical outputs)
0.3     → Low/Focused (very consistent)
0.7     → Medium/Balanced (recommended general use)
1.0     → High/Creative (varied responses)
1.5+    → Very High/Chaotic (highly unpredictable)
```

### 3. **api_client.py** - Azure OpenAI Integration
**Line Count**: ~110 lines  
**Purpose**: Real API integration (optional)

#### Class: APIClient
- Initializes from `.env` configuration
- `is_configured()` - Checks if credentials provided
- `call_api()` - Single API call with parameters
- `batch_call()` - Multiple calls at different temperatures
- `get_model_info()` - Returns deployment information

**Key Parameters Supported**:
- Temperature (0.0 - 2.0)
- Top-P (0.0 - 1.0)
- Max Tokens
- Custom system messages

### 4. **visualizer.py** - Chart Generation
**Line Count**: ~200 lines  
**Purpose**: Create matplotlib visualizations

#### Class: ParameterVisualizer

**Methods**:
- `plot_temperature_spectrum()` - 4-panel temperature visualization
  - Creativity vs Temperature
  - Consistency vs Temperature
  - Trade-off comparison
  - Temperature operating zones
  
- `plot_response_variance()` - 2-panel variance analysis
  - Response variance by temperature
  - Repetition rate by temperature
  
- `plot_parameter_comparison()` - Flexible multi-parameter charts
  - Generic comparison tool
  - Configurable parameter displays

**Output**: PNG files saved to `output/` directory

## Data Flow

### Demonstration Workflow

```
Start Demo
    │
    ├─→ Load mock responses (or real API)
    │
    ├─→ For each temperature:
    │   ├─ Get responses
    │   ├─ Calculate variance
    │   ├─ Calculate repetition rate
    │   └─ Display results
    │
    ├─→ Compare temperatures
    │
    ├─→ Generate visualizations
    │
    └─→ Save charts to output/
```

### Analysis Pipeline

```
Raw Responses
    ↓
Text Processing (tokenization, n-gram extraction)
    ↓
Variance Calculation (unique bigrams/trigrams)
    ↓
Repetition Analysis (repeated sentence detection)
    ↓
TemperatureAnalysis Object
    ↓
Display + Visualization
```

## Database/Storage

### Files Structure

```
api_basics_demo/
├── src/
│   ├── __init__.py          (package init, exports)
│   ├── api_parameters.py    (analysis logic)
│   ├── api_client.py        (API integration)
│   └── visualizer.py        (chart generation)
├── output/                  (generated visualizations)
│   ├── temperature_spectrum.png
│   ├── response_variance.png
│   └── [more charts]
├── main_demo.py             (main executable)
├── requirements.txt         (dependencies)
├── .env                     (optional: API credentials)
├── README.md
├── GETTING_STARTED.md
├── PROJECT_SUMMARY.md
└── VISUAL_GUIDE.md
```

### Configuration (.env)
```
AZURE_OPENAI_API_KEY=xxxx              # API authentication
AZURE_OPENAI_ENDPOINT=https://xxxx     # Azure endpoint
AZURE_DEPLOYMENT_NAME=deployment       # Model deployment name
AZURE_MODEL_NAME=gpt-35-turbo          # Model identifier
```

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| openai | >=1.3.0 | OpenAI API client |
| azure-openai | >=1.13.0 | Azure integration |
| python-dotenv | >=1.0.0 | .env configuration |
| matplotlib | >=3.7.0 | Chart visualization |
| numpy | >=1.24.0 | Numerical operations |
| scipy | >=1.10.0 | Scientific computing |
| pandas | >=2.0.0 | Data handling |
| colorama | >=0.4.6 | Colored terminal output |

## Execution Flow

```
1. main_demo.py starts
   ├─ Import modules
   ├─ Initialize colorama for colors
   └─ Print welcome banner

2. For each demonstration:
   ├─ Print demo header
   ├─ Load mock responses (default) or real API calls
   ├─ Calculate statistics
   ├─ Display results with colored output
   ├─ Generate visualization (if applicable)
   └─ Print completion status

3. Generate output files:
   ├─ temperature_spectrum.png
   ├─ response_variance.png
   └─ [saved to output/ directory]

4. Print summary and exit
```

## Key Algorithms

### Text Variance Calculation
```
1. Extract bigrams and trigrams from all responses
2. Count unique n-grams
3. Variance = unique_phrases / total_phrases
4. Clamp result to 0-1 range
Result: Higher = more varied responses
```

### Repetition Rate Calculation
```
1. Split responses into sentences
2. Count how many sentences appear multiple times
3. Repetition rate = repeated_count / total_sentences
4. Clamp result to 0-1 range
Result: Higher = more repetitive (consistency)
```

### Temperature Zone Matching
```
- 0.0: Return Deterministic zone
- 0.3: Return Focused zone
- 0.7: Return Balanced zone
- 1.0: Return Creative zone
- 1.5+: Return Chaotic zone
```

## Performance Characteristics

| Operation | Time | Notes |
|-----------|------|-------|
| Mock responses | <100ms | Pre-calculated, instant |
| Variance calculation | ~50ms | Text processing overhead |
| Chart generation | 500-1000ms | Matplotlib rendering |
| Real API call | 1-5s | Network dependent |
| Full demo | 2-5s | Depends on mode |

## Design Patterns Used

1. **Static Class Pattern** - APIParameters (utility methods)
2. **Data Class Pattern** - TemperatureAnalysis (immutable data)
3. **Singleton-like Pattern** - APIClient (shared configuration)
4. **Strategy Pattern** - Mock vs Real API responses
5. **Factory Pattern** - ParameterVisualizer (multiple chart types)

## Extension Points

The architecture supports easy extension:

1. **Add new parameters** - Extend `APIParameters.TEMPERATURE_RANGES`
2. **Add new responses** - Extend `MockLLMResponses.RESPONSES`
3. **Add new visualizations** - Add methods to `ParameterVisualizer`
4. **Add new demonstrations** - Create `demo_X()` functions in main_demo.py

## Error Handling

- Try/catch in demo runner for graceful failure
- Fallback to mock responses if API unavailable
- File I/O errors caught when saving visualizations
- Validation of .env variables before API calls

## Testing Considerations

To test the system:
```
1. Verify mock responses work (no credentials needed)
2. Check visualization generation
3. Compare known good outputs
4. Test with real API (if credentials configured)
5. Validate statistical calculations manually
```

---

**Architecture Version**: 1.0  
**Last Updated**: 2024  
**Status**: Production Ready
