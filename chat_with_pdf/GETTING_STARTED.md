# Getting Started - Chat with PDF Demo

## Quick Start (2 minutes)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the demo
python main_demo.py

# 3. View results
# - PNG visualizations: output/
# - Interactive HTML: output/embedding_space_interactive.html
```

## Installation Details

### Prerequisites
- Python 3.10 or higher
- pip package manager

### Step 1: Install Packages

```bash
pip install -r requirements.txt
```

**What gets installed:**
- `PyPDF2` - PDF text extraction
- `numpy` & `scikit-learn` - Vector operations & PCA
- `matplotlib` & `plotly` - Visualizations (Plotly for interactive)
- `colorama` - Colored terminal output

### Step 2: Verify Installation

```bash
# Test imports
python -c "import PyPDF2, numpy, matplotlib, plotly; print('✓ All dependencies installed!')"
```

## Running the Demo

### Full Demo (All 6 Demonstrations)

```bash
python main_demo.py
```

**Output:**
```
====================================================================
       CHAT WITH YOUR PDF - Retrieval Augmented Generation Demo
====================================================================

This demo demonstrates the complete RAG pipeline:
  1. Ingestion: Loading and extracting PDF content
  2. Chunking & Embedding: Creating vector representations
  3. Retrieval: Finding relevant context for queries
  4. Synthesis: Generating factual answers

Running 6 comprehensive demonstrations...

▶ Demo 1: Ingestion - Loading PDF
[Output showing document stats...]

... (5 more demos)

Demonstrations Complete!
✓ All demos executed successfully!
Next steps:
  1. Review PNG charts in: output/
  2. Open interactive embedding visualization: output/embedding_space_interactive.html
```

## Understanding the Output

### Text Output (Terminal)
- **Demo 1**: Document statistics and metadata
- **Demo 2**: Chunking and embedding statistics
- **Demo 3**: Vector store information
- **Demo 4**: Retrieval results with similarity scores
- **Demo 5**: Generated answers from context
- **Demo 6**: Visualization generation status

### Generated Files

#### PNG Visualizations
Located in `output/`:

1. **rag_pipeline_overview.png** (1,200x1,000px)
   - Visual diagram of the 4 RAG stages
   - Color-coded for easy understanding

2. **chunking_visualization.png** (1,400x600px)
   - Bar chart: chunk size distribution
   - Line chart: cumulative text coverage

3. **rag_statistics.png** (1,200x1,000px)
   - 4-panel statistics dashboard
   - Chunks, embedding dimension, etc.

4. **retrieval_process_1.png**, **_2.png**, **_3.png** (1,400x600px each)
   - Relevance scores for retrieved chunks
   - Text preview of selected context

#### Interactive HTML

**embedding_space_interactive.html** (NEW!)
- Open with any web browser
- 2D interactive plot of embeddings
- **Features:**
  - Hover over chunks for details
  - Query point highlighted in red
  - Retrieved chunks in orange
  - Zoom and pan capabilities
  - Legend for chunk types

## Project Structure

```
chat_with_pdf/
├── bvm.pdf                          # Input document
├── main_demo.py                     # Run this! ▶
├── requirements.txt                 # Dependencies
├── README.md                        # Full documentation
├── GETTING_STARTED.md               # You are here
│
├── src/                             # Source code modules
│   ├── ingestion.py                # PDF loading
│   ├── chunking.py                 # Text chunking & embeddings
│   ├── retrieval.py                # Vector store & RAG
│   ├── visualizer.py               # All visualizations
│   └── __init__.py
│
├── output/                          # Generated outputs
│   ├── rag_pipeline_overview.png
│   ├── chunking_visualization.png
│   ├── rag_statistics.png
│   ├── embedding_space_interactive.html    ← Open in browser!
│   ├── retrieval_process_1.png
│   ├── retrieval_process_2.png
│   └── retrieval_process_3.png
│
└── data/                           # Supporting data (if any)
```

## Key Concepts Quick Reference

### RAG = Retrieval Augmented Generation

1. **Retrieval**: Find relevant document chunks using vector similarity
2. **Augmentation**: Add chunks as context to query
3. **Generation**: Ask LLM to answer based on context

### Vector Embeddings
- Text → 100-dimensional vector
- Similar text = similar vectors (small distance)
- Distance measured by cosine similarity (0 = different, 1 = identical)

### Chunking
- Split documents into ~500 character chunks
- Overlap between chunks maintains context
- Each chunk gets its own embedding

### Similarity Score
- **0.0 - 0.3**: Low similarity (not relevant)
- **0.3 - 0.6**: Medium similarity (somewhat relevant)
- **0.6 - 1.0**: High similarity (very relevant)

## Typical Workflow

```
1. Load PDF (ingestion.py)
   └─ Extract raw text from bvm.pdf

2. Process Text (chunking.py)
   ├─ Split into chunks (500 chars each)
   └─ Create embeddings (100D vectors)

3. Setup Search (retrieval.py)
   ├─ Store embeddings in vector database
   └─ Ready for queries

4. Query (retrieval.py)
   ├─ Embed query: "What is this about?"
   ├─ Find top-3 similar chunks
   └─ Get scores (confidence: 75%, 62%, 51%)

5. Answer (synthesis)
   ├─ Use retrieved chunks as context
   ├─ Ask LLM to answer
   └─ Output: "Based on the document: ..."

6. Visualize (visualizer.py)
   ├─ Create PNG charts
   ├─ Generate interactive HTML
   └─ Show retrieval process
```

## Troubleshooting

### "ModuleNotFoundError: No module named 'PyPDF2'"

```bash
# Activate your Python environment if needed
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### "No such file or directory: 'bvm.pdf'"

- Make sure `bvm.pdf` is in the project root (same directory as `main_demo.py`)
- Check file path: `c:\Demo\chat_with_pdf\bvm.pdf`

### "Unable to open embedding_space_interactive.html"

- Check that file exists in `output/embedding_space_interactive.html`
- Try right-click → "Open with" → Select your browser
- Or drag the .html file directly into browser window

### Slow execution

- First run: ~3-5 seconds (normal - loads PDF, creates embeddings)
- Subsequent runs: faster
- Large PDFs → slower processing

## Next Steps

### 1. Understand the Visualizations
- Open `output/rag_pipeline_overview.png` to see architecture
- View `output/embedding_space_interactive.html` in browser
- Study `output/retrieval_process_*.png` to see answer selection

### 2. Experiment with the Code
- Modify chunk size in `main_demo.py` (currently 500 chars)
- Change number of retrieved chunks (currently 3)
- Adjust similarity threshold (currently 0.3)

### 3. Try Different Queries
- Edit queries in `demo_4_retrieval()` function
- Run again to see different retrieval results

### 4. Production Enhancements
- Replace simple embeddings with OpenAI embeddings
- Add more sophisticated chunking strategies
- Implement chunk reranking for better results
- Build web interface for easy querying

## Performance Tips

### Speed Optimization
- Embed queries once per session (not per request)
- Use approximate nearest neighbors for large datasets
- Cache embeddings on disk

### Quality Improvement
- Use better embedding models (OpenAI, Sentence Transformers)
- Experiment with chunk size and overlap
- Add metadata to chunks (page, date, author)
- Implement multi-stage retrieval (broad → rerank → final)

## Advanced Topics

### Understanding Embeddings
- 100 dimensions = 100-element vector
- Each dimension captures different semantic aspect
- Similar chunks have similar vectors
- Cosine similarity = dot product / (norm1 × norm2)

### Why Chunking Matters
- LLMs have token limits (4K-32K typically)
- Whole document may exceed limit
- Chunks ensure context fits in model
- Overlaps maintain continuity between chunks

### Retrieval Quality
- **Precision**: Are retrieved chunks relevant? (quality)
- **Recall**: Are all relevant chunks found? (completeness)
- Trade-off: higher threshold → higher precision, lower recall

## Learning Resources

- Read `README.md` for full documentation
- Study `PROJECT_SUMMARY.md` for architecture details
- Review source code comments in `src/`
- Check docstrings in each Python function

## Getting Help

1. Check error messages carefully
2. Review the FAQ in `README.md`
3. Look at docstring comments in code
4. Verify file paths and dependencies
5. Check that `bvm.pdf` exists and is readable

## Quick Commands Reference

```bash
# Install dependencies
pip install -r requirements.txt

# Run full demo
python main_demo.py

# Check specific demo output
# (modify main_demo.py to call individual demo functions)

# List output files
dir output\

# Open interactive visualization
start output\embedding_space_interactive.html  # Windows
open output/embedding_space_interactive.html   # Mac
xdg-open output/embedding_space_interactive.html # Linux
```

## What You'll Learn

After running this demo, you'll understand:
- ✓ How to extract text from PDFs
- ✓ Vector embeddings and semantic search
- ✓ Building RAG systems
- ✓ Query retrieval and ranking
- ✓ Grounding LLM answers in documents
- ✓ Creating interactive visualizations

---

**Ready?** Run `python main_demo.py` and explore!
