# Vector Algebra Demo - Getting Started

## ✓ Demo Created!

Your Vector Algebra demo is ready at `C:\Demo\vector_algebra_demo\`

This project demonstrates how word embeddings enable semantic arithmetic using the famous example: **King - Man + Woman = Queen**

## Quick Start

### Run the Demo (Easiest)
```powershell
cd C:\Demo\vector_algebra_demo
C:/Demo/.venv/Scripts/python.exe main_demo.py
```

The demo will:
1. Load pre-trained GloVe word embeddings (100-dimensional)
2. Show basic vector operations
3. Calculate word similarities
4. Perform the King-Man+Woman=Queen analogy
5. Test other semantic analogies
6. Generate 3 visualization charts

## What You'll Learn

### The Famous Analogy
```
King - Man + Woman ≈ Queen

This demonstrates that:
- King word vector
- Minus Man word vector (removes "male" features)
- Plus Woman word vector (adds "female" features)
- Approximately equals Queen word vector!
```

### Why It Works

Word embeddings capture semantic relationships:
- **Gender dimension**: distinguishes male vs female concepts
- **Royalty dimension**: distinguishes royal vs common
- **Vector arithmetic**: manipulating these dimensions gives meaningful results

## 6 Demonstrations Included

### 1️⃣ Understanding Word Vectors
- Shows vector dimensions (100)
- Displays vocabulary size (1M+ words)
- Shows actual vector values

### 2️⃣ Word Similarity
- Calculates cosine similarity between words
- Demonstrates proximity in vector space
- Shows king↔queen is similar, king↔car is not

### 3️⃣ King - Man + Woman = Queen
- The famous word analogy
- Finds nearest words to the result
- Compares to actual "queen" embedding

### 4️⃣ More Analogies
- France is to Paris as Germany is to...
- Bad is to Worse as Good is to...
- Gender analogies (actor → actress)

### 5️⃣ Vector Space Analysis
- Analyzes relationships between words
- Calculates magnitudes
- Shows pairwise similarities

### 6️⃣ Visualizations
- Vector arithmetic in 2D space
- Word embeddings plotted by semantic features
- Similarity heatmap of word pairs

## Project Structure

```
vector_algebra_demo/
├── main_demo.py              ← Run this!
├── requirements.txt          ← Dependencies
├── README.md                 ← Full documentation
├── GETTING_STARTED.md        ← This file
├── src/
│   ├── embeddings.py         ← Word embedding utilities
│   ├── vector_algebra.py     ← Vector operations
│   └── visualizer.py         ← Visualization tools
├── data/
│   └── examples.md           ← Example analogies
└── output/
    ├── vector_arithmetic.png ← Generated charts
    ├── word_space.png
    └── similarity_heatmap.png
```

## Example Output

```
=== Vector Arithmetic ===
King vector magnitude: 5.4321
Subtract Man vector...
Add Woman vector...
Result vector: [0.123, -0.456, 0.789, ...]

Top words similar to result:
1. QUEEN          (similarity: 0.8934)
2. PRINCESS       (similarity: 0.7821)
3. LADY           (similarity: 0.7456)
...
```

## Generated Visualizations

1. **vector_arithmetic.png**
   - Shows King, Man, Woman vectors
   - Shows resulting vector
   - Plotted in 2D using PCA

2. **word_space.png**
   - Multiple words plotted in 2D space
   - Color-coded by gender and royalty
   - Shows semantic clusters

3. **similarity_heatmap.png**
   - Bar chart of word pair similarities
   - Shows which words are most similar

## More Analogies You Can Try

By modifying `main_demo.py`:

```python
embeddings.analogy("france", "paris", "germany")
# Result: berlin

embeddings.analogy("bad", "worse", "good")
# Result: better

embeddings.analogy("actor", "actress", "prince")
# Result: princess
```

## Key Concepts

### Cosine Similarity
- Measures angle between vectors
- Range: -1 to 1 (or 0 to 1 for normalized)
- 1.0 = identical direction, 0.0 = perpendicular

### Vector Magnitude
- Length of the vector
- Larger = stronger concept representation

### PCA (Principal Component Analysis)
- Reduces 100D vectors to 2D for visualization
- Preserves most important variance
- Shows relationship structure

### GloVe Embeddings
- Pre-trained on Wikipedia and web text
- 100-dimensional vectors
- ~1 million word vocabulary
- Captures semantic and syntactic relationships

## Troubleshooting

### "ModuleNotFoundError"
```powershell
pip install -r requirements.txt
```

### Model taking too long to load
- GloVe model is ~100MB
- First run downloads and caches it
- Subsequent runs are instant

### Out of memory
- The demo uses ~500MB of RAM
- Should work on most modern machines

## Advanced Usage

### Use embeddings in your code
```python
from src.embeddings import WordEmbeddings

embeddings = WordEmbeddings()
vec = embeddings.get_vector("king")
similarity = embeddings.get_similarity("king", "queen")
```

### Get specific analogies
```python
results = embeddings.analogy("france", "paris", "italy")
# Returns [(word, score), ...]
```

### Create custom visualizations
```python
from src.visualizer import Vector2DVisualizer

Vector2DVisualizer.plot_word_relationships(
    {"word1": vec1, "word2": vec2},
    save_path="chart.png"
)
```

## Resources

- [Word2Vec Paper](https://arxiv.org/abs/1310.4546)
- [GloVe Paper](https://aclanthology.org/P14-1146/)
- [Gensim Documentation](https://radimrehurek.com/gensim/)
- [Semantic Analogies](https://www.google.com/url?q=https://aclanthology.org/D13-1090)

## Next Steps

1. Run the demo: `python main_demo.py`
2. View the visualizations in `output/` folder
3. Read the full README.md for advanced usage
4. Experiment with custom analogies
5. Integrate into your own projects

---

**Ready?** Jump to the quick start at the top! 🚀
