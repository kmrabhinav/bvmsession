#!/usr/bin/env python3
"""
Chat with PDF - Retrieval Augmented Generation Demo
====================================================

Demonstrates the complete RAG pipeline:
1. Ingestion: Loading and extracting text from PDF
2. Chunking & Embedding: Breaking text into chunks and creating vectors
3. Retrieval: Finding relevant chunks for a query
4. Synthesis: Generating factual answers from context

This demo uses the BVM.pdf document to show how to chat with your PDFs.
"""

import sys
from pathlib import Path
import numpy as np

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from colorama import Fore, Back, Style, init
from ingestion import PDFIngestion
from chunking import TextChunker, EmbeddingGenerator
from retrieval import VectorStore, RAGSynthesizer
from visualizer import RAGVisualizer

# Initialize colorama
init(autoreset=True)


def print_header(text: str, level: int = 1):
    """Print formatted header."""
    if level == 1:
        print(f"\n{Fore.CYAN}{Style.BRIGHT}{'='*70}")
        print(f"{text.center(70)}")
        print(f"{'='*70}{Style.RESET_ALL}\n")
    elif level == 2:
        print(f"\n{Fore.GREEN}{Style.BRIGHT}▶ {text}{Style.RESET_ALL}\n")
    else:
        print(f"{Fore.YELLOW}{Style.BRIGHT}  • {text}{Style.RESET_ALL}")


def demo_1_ingestion():
    """Demo 1: PDF Ingestion - Load and extract text."""
    print_header("Demo 1: Ingestion - Loading PDF", 2)
    
    print(f"{Fore.WHITE}Step 1: Loading PDF document...")
    
    pdf_path = Path(__file__).parent / "bvm.pdf"
    
    if not pdf_path.exists():
        print(f"{Fore.RED}✗ PDF file not found at {pdf_path}")
        return None, None
    
    ingestion = PDFIngestion()
    raw_text = ingestion.load_pdf(str(pdf_path))
    
    print(f"{Fore.GREEN}✓ PDF loaded successfully!\n")
    
    # Get metadata
    metadata = ingestion.extract_metadata()
    print(f"{Fore.CYAN}Document Metadata:")
    for key, value in metadata.items():
        print(f"  {Fore.MAGENTA}{key}: {Fore.WHITE}{value}")
    
    # Get text statistics
    stats = ingestion.get_text_stats()
    print(f"\n{Fore.CYAN}Text Statistics:")
    print(f"  {Fore.MAGENTA}Total characters: {Fore.WHITE}{stats['total_characters']:,}")
    print(f"  {Fore.MAGENTA}Total words: {Fore.WHITE}{stats['total_words']:,}")
    print(f"  {Fore.MAGENTA}Total lines: {Fore.WHITE}{stats['total_lines']:,}")
    print(f"  {Fore.MAGENTA}Total paragraphs: {Fore.WHITE}{stats['total_paragraphs']:,}")
    print(f"  {Fore.MAGENTA}Number of pages: {Fore.WHITE}{stats['pages']}")
    print(f"  {Fore.MAGENTA}Average word length: {Fore.WHITE}{stats['average_word_length']:.1f} chars")
    
    print(f"\n{Fore.YELLOW}Text Preview (first 300 chars):")
    print(f"{Fore.WHITE}{raw_text[:300]}...")
    
    return ingestion, raw_text


def demo_2_chunking_and_embedding(raw_text):
    """Demo 2: Chunking and Embedding - Prepare for vector search."""
    print_header("Demo 2: Chunking & Embedding - Creating Vector Store", 2)
    
    print(f"{Fore.WHITE}Step 1: Chunking text into overlapping segments...")
    
    chunker = TextChunker(chunk_size=500, overlap=50)
    chunks = chunker.chunk_text(raw_text, page=1)
    
    print(f"{Fore.GREEN}✓ Text chunked into {len(chunks)} chunks!\n")
    
    # Show chunking statistics
    chunk_stats = chunker.get_chunk_stats()
    print(f"{Fore.CYAN}Chunking Statistics:")
    print(f"  {Fore.MAGENTA}Total chunks: {Fore.WHITE}{chunk_stats['total_chunks']}")
    print(f"  {Fore.MAGENTA}Avg chunk size: {Fore.WHITE}{chunk_stats['avg_chunk_size']:.0f} characters")
    print(f"  {Fore.MAGENTA}Min chunk size: {Fore.WHITE}{chunk_stats['min_chunk_size']:.0f} characters")
    print(f"  {Fore.MAGENTA}Max chunk size: {Fore.WHITE}{chunk_stats['max_chunk_size']:.0f} characters")
    print(f"  {Fore.MAGENTA}Total chunked text: {Fore.WHITE}{chunk_stats['total_text_length']:,} characters")
    
    print(f"\n{Fore.WHITE}Step 2: Generating embeddings for each chunk...")
    
    embedding_gen = EmbeddingGenerator(embedding_dim=100)
    embeddings = embedding_gen.embed_chunks(chunks)
    
    print(f"{Fore.GREEN}✓ Generated {len(embeddings)} embeddings!\n")
    
    print(f"{Fore.CYAN}Embedding Statistics:")
    print(f"  {Fore.MAGENTA}Embedding dimension: {Fore.WHITE}100 (100-dimensional vectors)")
    print(f"  {Fore.MAGENTA}Total embeddings: {Fore.WHITE}{len(embeddings)}")
    
    embeddings_array = np.array(list(embeddings.values()))
    print(f"  {Fore.MAGENTA}Embedding shape: {Fore.WHITE}{embeddings_array.shape}")
    print(f"  {Fore.MAGENTA}Mean norm: {Fore.WHITE}{np.mean([np.linalg.norm(e) for e in embeddings.values()]):.4f}")
    
    print(f"\n{Fore.YELLOW}Sample Chunks (first 3):")
    for i, chunk in enumerate(chunks[:3]):
        preview = chunk.text[:80].replace('\n', ' ')
        print(f"  {Fore.CYAN}Chunk {chunk.id}: {Fore.WHITE}{preview}...")
    
    return chunks, embedding_gen


def demo_3_vector_store(chunks, embedding_gen):
    """Demo 3: Vector Store - Organize embeddings for retrieval."""
    print_header("Demo 3: Vector Store - Efficient Organization", 2)
    
    print(f"{Fore.WHITE}Creating vector store...")
    
    store = VectorStore()
    store.add_chunks(chunks)
    
    print(f"{Fore.GREEN}✓ Vector store created!\n")
    
    stats = store.get_stats()
    print(f"{Fore.CYAN}Vector Store Statistics:")
    print(f"  {Fore.MAGENTA}Total chunks: {Fore.WHITE}{stats['total_chunks']}")
    print(f"  {Fore.MAGENTA}Total embeddings: {Fore.WHITE}{stats['total_embeddings']}")
    print(f"  {Fore.MAGENTA}Embedding dimension: {Fore.WHITE}{stats['embedding_dim']}")
    print(f"  {Fore.MAGENTA}Average chunk size: {Fore.WHITE}{stats['avg_chunk_size']:.0f} characters")
    print(f"  {Fore.MAGENTA}Embedding sparsity: {Fore.WHITE}{stats['sparsity']:.2%}")
    
    print(f"\n{Fore.WHITE}The vector store is ready for similarity search!")
    
    return store


def demo_4_retrieval(store):
    """Demo 4: Retrieval - Find relevant chunks for queries."""
    print_header("Demo 4: Retrieval - Finding Relevant Context", 2)
    
    # Example queries
    queries = [
        "Who manages BVM",
        "When was BVM established",
        "What did N. D. Bhatt wrote about?",
        "What is the main topic of this document?",
        "key concepts and information",
        "structure and overview",
    ]
    
    print(f"{Fore.WHITE}Testing retrieval with example queries:\n")
    
    all_results = {}
    
    for query in queries:
        print(f"{Fore.CYAN}Query: {Fore.YELLOW}\"{query}\"")
        
        retrieved_chunks, scores = store.retrieve(query, top_k=3, threshold=0.3)
        
        print(f"{Fore.GREEN}✓ Retrieved {len(retrieved_chunks)} relevant chunks:\n")
        
        for i, (chunk, score) in enumerate(zip(retrieved_chunks, scores), 1):
            preview = chunk.text[:70].replace('\n', ' ')
            print(f"  {Fore.MAGENTA}[{i}] Chunk {chunk.id} - Confidence: {Fore.YELLOW}{score:.1%}")
            print(f"      {Fore.WHITE}\"{preview}...\"")
        
        all_results[query] = (retrieved_chunks, scores)
        print()
    
    return all_results


def demo_5_synthesis(store, all_results):
    """Demo 5: Synthesis - Generate answers from retrieved context."""
    print_header("Demo 5: Synthesis - Generating Factual Answers", 2)
    
    print(f"{Fore.WHITE}Generating answers using retrieved context:\n")
    
    synthesizer = RAGSynthesizer()
    
    for query, (retrieved_chunks, scores) in all_results.items():
        print(f"{Fore.CYAN}{'='*70}")
        print(f"Query: {Fore.YELLOW}\"{query}\"")
        print(f"{Fore.CYAN}{'='*70}")
        
        answer = synthesizer.synthesize_answer(query, retrieved_chunks, scores)
        print(f"{Fore.WHITE}{answer}\n")
        
        # Show sources
        sources = synthesizer.get_answer_sources(retrieved_chunks, scores)
        print(f"{Fore.MAGENTA}Sources Used:")
        for i, source in enumerate(sources, 1):
            print(f"  [{i}] Page {source['page']}, Chunk {source['chunk_id']} "
                  f"(Confidence: {source['confidence']:.1%})")


def demo_6_visualizations(chunks, store, all_results):
    """Demo 6: Visualizations - Create comprehensive charts."""
    print_header("Demo 6: Visualizations - Interactive Charts & Plots", 2)
    
    output_dir = Path(__file__).parent / 'output'
    output_dir.mkdir(exist_ok=True)
    
    print(f"{Fore.WHITE}Generating visualizations...\n")
    
    # 1. Pipeline overview
    print(f"{Fore.CYAN}Creating RAG pipeline overview...")
    RAGVisualizer.plot_pipeline_overview(
        save_path=str(output_dir / 'rag_pipeline_overview.png')
    )
    print(f"{Fore.GREEN}✓ Saved: rag_pipeline_overview.png")
    
    # 2. Chunking visualization
    print(f"{Fore.CYAN}Creating chunking visualization...")
    RAGVisualizer.plot_chunking_visualization(
        chunks,
        save_path=str(output_dir / 'chunking_visualization.png')
    )
    print(f"{Fore.GREEN}✓ Saved: chunking_visualization.png")
    
    # 3. Statistics
    stats = store.get_stats()
    embedding_dim = 100
    avg_chunk_size = stats['avg_chunk_size'] if stats else 0
    total_text = sum(len(c.text) for c in chunks)
    
    print(f"{Fore.CYAN}Creating RAG statistics...")
    RAGVisualizer.plot_rag_statistics(
        num_chunks=len(chunks),
        embedding_dim=embedding_dim,
        avg_chunk_size=avg_chunk_size,
        total_text=total_text,
        save_path=str(output_dir / 'rag_statistics.png')
    )
    print(f"{Fore.GREEN}✓ Saved: rag_statistics.png")
    
    # 4. Embedding space (interactive HTML)
    print(f"{Fore.CYAN}Creating interactive embedding space visualization...")
    first_query, first_results = list(all_results.items())[0]
    retrieved_chunks, _ = first_results
    query_embedding = store.get_query_embedding(first_query)
    
    RAGVisualizer.plot_embedding_space_interactive(
        chunks=chunks,
        query_embedding=query_embedding,
        retrieved_chunks=retrieved_chunks,
        save_path=str(output_dir / 'embedding_space_interactive.html')
    )
    print(f"{Fore.GREEN}✓ Saved: embedding_space_interactive.html")
    print(f"  {Fore.YELLOW}→ Open in browser to explore the vector space interactively!")
    
    # 5. Retrieval process visualization
    print(f"{Fore.CYAN}Creating retrieval process visualization...")
    for i, (query, (retrieved_chunks, scores)) in enumerate(all_results.items(), 1):
        RAGVisualizer.plot_retrieval_process(
            query=query,
            retrieved_chunks=retrieved_chunks,
            scores=scores,
            save_path=str(output_dir / f'retrieval_process_{i}.png')
        )
        print(f"{Fore.GREEN}✓ Saved: retrieval_process_{i}.png")
    
    print(f"\n{Fore.CYAN}Output directory: {output_dir}")


def main():
    """Run complete RAG demonstration."""
    print(f"\n{Fore.CYAN}{Style.BRIGHT}{'='*70}")
    print(f"CHAT WITH YOUR PDF - Retrieval Augmented Generation Demo".center(70))
    print(f"{'='*70}{Style.RESET_ALL}\n")
    
    print(f"{Fore.WHITE}This demo demonstrates the complete RAG pipeline:")
    print(f"  1. {Fore.YELLOW}Ingestion{Fore.WHITE}: Loading and extracting PDF content")
    print(f"  2. {Fore.YELLOW}Chunking & Embedding{Fore.WHITE}: Creating vector representations")
    print(f"  3. {Fore.YELLOW}Retrieval{Fore.WHITE}: Finding relevant context for queries")
    print(f"  4. {Fore.YELLOW}Synthesis{Fore.WHITE}: Generating factual answers\n")
    
    print(f"{Fore.MAGENTA}Running 6 comprehensive demonstrations...\n")
    
    try:
        # Demo 1: Ingestion
        ingestion, raw_text = demo_1_ingestion()
        if ingestion is None:
            return
        
        # Demo 2: Chunking & Embedding
        chunks, embedding_gen = demo_2_chunking_and_embedding(raw_text)
        
        # Demo 3: Vector Store
        store = demo_3_vector_store(chunks, embedding_gen)
        
        # Demo 4: Retrieval
        all_results = demo_4_retrieval(store)
        
        # Demo 5: Synthesis
        demo_5_synthesis(store, all_results)
        
        # Demo 6: Visualizations
        demo_6_visualizations(chunks, store, all_results)
        
        print(f"\n{Fore.CYAN}{Style.BRIGHT}{'='*70}")
        print(f"Demonstrations Complete!".center(70))
        print(f"{'='*70}{Style.RESET_ALL}\n")
        
        print(f"{Fore.GREEN}✓ All demos executed successfully!")
        print(f"{Fore.WHITE}Next steps:")
        print(f"  1. Review PNG charts in: output/")
        print(f"  2. Open interactive embedding visualization: output/embedding_space_interactive.html")
        print(f"  3. Explore how RAG connects queries to document content\n")
        
    except Exception as e:
        print(f"\n{Fore.RED}✗ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
