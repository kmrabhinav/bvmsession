# API Basics Demo - Visual Guide

## Temperature Parameter Explained

### Visual Scale (0.0 to 2.0)

```
Temperature 0.0         Temperature 0.5         Temperature 1.0         Temperature 1.5         Temperature 2.0
┌──────────────┐         ┌──────────────┐         ┌──────────────┐         ┌──────────────┐         ┌──────────────┐
│ IDENTICAL    │         │ VERY LOW     │         │ BALANCED     │         │ VERY HIGH    │         │ VERY HIGH    │
│ ██████████   │         │ █████░░░░░░  │         │ ████████░░░░ │         │ ██░░░░░░░░░░ │         │ █░░░░░░░░░░░ │
│ ██████████   │         │ ██████░░░░░░ │         │ ██████░░░░░░ │         │ ░██░░░░░░░░░ │         │ ██░░░░░░░░░░ │
│ ██████████   │         │ ██████░░░░░░ │         │ ████░░░░░░░░ │         │ ░░██░░░░░░░░ │         │ ░░░██░░░░░░░ │
│              │         │              │         │              │         │              │         │              │
│ Output: Same │         │ Output: Very │         │ Output: Good │         │ Output: Very │         │ Output: Very │
│ every time   │         │ Consistent   │         │ Balance      │         │ Creative     │         │ Random       │
└──────────────┘         └──────────────┘         └──────────────┘         └──────────────┘         └──────────────┘
  Reliability:10           Reliability:8            Reliability:6            Reliability:3            Reliability:1
   Creativity:0             Creativity:2             Creativity:5             Creativity:8             Creativity:10
```

## Temperature Zones & Use Cases

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                    TEMPERATURE OPERATING ZONES                                   │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                   │
│  ZONE 1: DETERMINISTIC (0.0)                                                     │
│  ████████████████████████████████████████████████████████                        │
│  • Same output every time                                                        │
│  • Best for: Factual Q&A, Customer support, Data retrieval                      │
│  • Examples: "What is the capital of France?" → Always "Paris"                  │
│                                                                                   │
│  ZONE 2: FOCUSED (0.1-0.3)                                                       │
│  ████████████████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░         │
│  • Very consistent, minimal variation                                            │
│  • Best for: Email templates, Documentation, Summaries                           │
│  • Examples: Slightly different phrasings but same content                       │
│                                                                                   │
│  ZONE 3: BALANCED (0.4-0.9) ← RECOMMENDED FOR GENERAL USE                        │
│  ████████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░         │
│  • Good mix of consistency and creativity                                        │
│  • Best for: General conversation, Chatbots, Content creation                    │
│  • Examples: Natural-sounding but still on-topic                                 │
│                                                                                   │
│  ZONE 4: CREATIVE (1.0-1.3)                                                      │
│  ██████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░          │
│  • Notably creative, more variation                                              │
│  • Best for: Creative writing, Brainstorming, Storytelling                      │
│  • Examples: Different viewpoints on same topic                                  │
│                                                                                   │
│  ZONE 5: CHAOTIC (1.4-2.0)                                                       │
│  ███░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░          │
│  • Highly unpredictable and random                                               │
│  • Best for: Experimental exploration, Unusual outputs                           │
│  • Examples: Might go off-topic, very creative to the point of chaos             │
│                                                                                   │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## Consistency vs Creativity Trade-off

```
CONSISTENCY                                              CREATIVITY
(Low Variance)                                           (High Variance)

    Perfect                                                 Perfect
    Copy                                                    Novel
     ↑                                                       ↑
     │                                                       │
  10│  ●                                                     │
     │   \                                                   │
  9 │    \                                                   │
     │     \                                                │
  8 │      \                                                ●
     │       \                                             / │
  7 │        \                                           /   │
     │         \                                       /     │ 
  6 │          \                                    /        │
     │           \                                /          │
  5 │            \★◄─ BALANCED ZONE             /           │★
     │             \                          /              │
  4 │              \                       /                 │
     │               \                   /                   │
  3 │                \               /                       │
     │                 \           /                         │
  2 │                  \       /                             │
     │                   \   /                               │
  1 │                    ▼ ▼                                 │
     │                                                       │
  0 └───────────────────────────────────────────────────────┘
     0°  0.3°  0.6°  0.9°  1.2°  1.5°  1.8°  2.0°
     Cold                                      Hot
```

## Key Parameters and Their Effects

### Temperature (0.0 - 2.0)
```
Effect on Response Variety:

Temperature 0.0:
Response 1: "Paris is the capital of France."
Response 2: "Paris is the capital of France."
Response 3: "Paris is the capital of France."
══════════════════════════════════════════════ IDENTICAL

Temperature 0.7:
Response 1: "France's hub is Paris, known for culture."
Response 2: "The capital of France is famously Paris."
Response 3: "Paris stands as the principal city of France."
══════════════════════════════════════════════ VARIED

Temperature 1.5:
Response 1: "Ah, Paris! The luminary of French dreams and destiny!"
Response 2: "In Gaul's heart sits Paris, city of infinite mystery."
Response 3: "Paris — where art, romance, and chaos intertwine eternally."
══════════════════════════════════════════════ HIGHLY VARIED
```

### Top-P (Nucleus Sampling)
```
Default: 1.0 (uses all tokens)

Top-P = 0.5: Considers only top 50% of tokens
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
█████████████ (selected)

Top-P = 0.9: Considers top 90% of tokens
░░░░░░░░░░
█████████████████████████████████████████ (selected)

Top-P = 1.0: Considers all tokens
██████████████████████████████████████████ (all selected)
```

### Top-K (Context Window)
```
Top-K = 40: Only the 40 most likely tokens

Probability: 1    2    3    4    5 ... 40   41   42   43   44 ...
Tokens:     ●●●• ●●●• ●●●• ●●●• ●●●•    ●●●• ○○○○ ○○○○ ○○○○ 
             ↑                         ↓
         Included                  Excluded (can't be selected)
```

## Code Structure Visualization

```
main_demo.py (Main Entry Point)
    │
    ├── Demo 1: Temperature Spectrum
    │   └─→ APIParameters.get_temperature_info()
    │   └─→ ParameterVisualizer.plot_temperature_spectrum()
    │
    ├── Demo 2: Same Prompt Different Temps
    │   └─→ MockLLMResponses.get_responses()
    │   └─→ Display responses side-by-side
    │
    ├── Demo 3: Response Variance Analysis
    │   └─→ APIParameters.analyze_responses()
    │   └─→ ParameterVisualizer.plot_response_variance()
    │
    ├── Demo 4: Creativity Scale
    │   └─→ Display bar chart of temperature scale
    │
    ├── Demo 5: Use Case Recommendations
    │   └─→ Display task-to-temperature mapping
    │
    └── Demo 6: Parameter Combinations
        └─→ Display recommended parameter sets
```

## Decision Tree: Choosing Temperature

```
                    ┌─────────────────────────────────┐
                    │  What do you need from LLM?     │
                    └──────────────┬──────────────────┘
                                   │
                ┌──────────────────┼──────────────────┐
                │                  │                  │
        ┌───────▼────────┐ ┌───────▼────────┐ ┌──────▼─────────┐
        │  CONSISTENCY   │ │  BALANCE       │ │  CREATIVITY    │
        │  (Factual)     │ │  (General)     │ │  (Novel ideas) │
        └───────┬────────┘ └───────┬────────┘ └──────┬─────────┘
                │                  │                  │
        ┌───────▼──────────┐ ┌──────▼──────────┐ ┌────▼──────────┐
        │ Temperature 0-0.3│ │ Temperature 0.7 │ │ Temperature1.0+│
        │                  │ │                 │ │                │
        │ Use cases:       │ │ Use cases:      │ │ Use cases:     │
        │ • Support chat   │ │ • Chat bots     │ │ • Story        │
        │ • Q&A systems    │ │ • Assistants    │ │   generation   │
        │ • Data retrieval │ │ • General conv  │ │ • Brainstorm   │
        │ • Email drafts   │ │ • Summaries     │ │ • Creative     │
        │                  │ │                 │ │   writing      │
        └──────────────────┘ └──────────────────┘ └────────────────┘
```

## Temperature Effects on Common Tasks

```
┌─────────────────────────────────────────────────────────────────┐
│ TASK: "Tell me about Paris"                                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│ Temperature 0.0 (Deterministic):                                │
│ "Paris is the capital of France. It is known for the Eiffel    │
│  Tower and is in the northern central part of the country."     │
│ ♦ Pros: Accurate, consistent, on-topic                         │
│ ✗ Cons: Boring, repetitive                                     │
│                                                                  │
│ Temperature 0.7 (Balanced):                                     │
│ "Paris, the capital of France, captivates visitors with its    │
│  iconic Eiffel Tower and rich cultural heritage. The city is   │
│  renowned for amazing food and romantic atmosphere."           │
│ ♦ Pros: Engaging, accurate, natural-sounding                  │
│ ✗ Cons: None - Generally recommended!                          │
│                                                                  │
│ Temperature 1.5 (Creative):                                     │
│ "Ah, Paris! A tempestuous jewel where vintage dreams pirouette │
│  beneath iron monuments, where boulevards sing with liberation │
│  and every croissant is a philosophical statement."            │
│ ♦ Pros: Highly creative, entertaining                         │
│ ✗ Cons: May drift off-topic, unpredictable                    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Performance Indicators

### Variance (Response Diversity)

```
Low Variance (0.0 - 0.3)          High Variance (0.8-1.0)
────────────────────────          ──────────────────────

Response 1: ██                    Response 1: ████
Response 2: ██                    Response 2: ████░░
Response 3: ██                    Response 3: ░░░░██
Response 4: ██                    Response 4: █░░░░░

Similarity: 95%                   Similarity: 40%
Variance: 0.05 (low)             Variance: 0.95 (high)
```

### Recommended Parameter Combinations

```
Scenario 1: Customer Support
┌─────────────────────────┐
│ temperature: 0.0        │
│ top_p: 1.0              │
│ top_k: -1 (disabled)    │
│ max_tokens: 500         │
└─────────────────────────┘

Scenario 2: General Chat
┌─────────────────────────┐
│ temperature: 0.7        │
│ top_p: 0.9              │
│ top_k: 40               │
│ max_tokens: 1000        │
└─────────────────────────┘

Scenario 3: Creative Writing
┌─────────────────────────┐
│ temperature: 1.0        │
│ top_p: 0.95             │
│ top_k: -1 (disabled)    │
│ max_tokens: 2000        │
└─────────────────────────┘
```

## Visual Algorithm Flow

```
Input: Prompt + Temperature
    ↓
[Token Generation]
    ├─ Apply temperature scaling to probabilities
    ├─ Softmax to convert to probability distribution
    └─ Sample next token based on probabilities
    ↓
[Sample from Distribution]
    ├─ Low Temperature (0.0): Choose highest probability token (always same)
    ├─ Medium Temperature (0.7): Choose from high-probability tokens with some variance
    └─ High Temperature (1.5): More uniform distribution, higher chance of unusual tokens
    ↓
Output: Response
```

---

**Visual explanations help understand API parameter behavior.** Refer to these diagrams when reading the documentation!
