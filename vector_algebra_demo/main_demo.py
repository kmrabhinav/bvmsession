"""
Vector Algebra Demo: King - Man + Woman = Queen
Demonstrates how word embeddings enable semantic arithmetic.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / 'src'))

from embeddings import WordEmbeddings
from vector_algebra import VectorAlgebra
from visualizer import Vector2DVisualizer
from colorama import Fore, Style, init

init(autoreset=True)


def print_header(title: str):
    """Print formatted section header."""
    print(f"\n{Fore.CYAN}{'='*70}")
    print(f"{Fore.CYAN}{title.center(70)}")
    print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")


def demo_basic_vectors():
    """Demonstrate basic vector operations."""
    print_header("DEMO 1: Understanding Word Vectors")
    
    embeddings = WordEmbeddings()
    
    # Get some vectors
    words = ["king", "queen", "man", "woman"]
    print(f"{Fore.YELLOW}Vector Dimensions: {embeddings.vector_size}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Vocabulary Size: {embeddings.vocabulary_size():,}{Style.RESET_ALL}\n")
    
    print(f"{Fore.GREEN}Sample Word Vectors:{Style.RESET_ALL}")
    print(f"{Fore.GREEN}{'-'*50}{Style.RESET_ALL}")
    
    for word in words:
        vector = embeddings.get_vector(word)
        magnitude = VectorAlgebra.magnitude(vector)
        print(f"  {word.upper():10} → Vector (dim={embeddings.vector_size}) | Magnitude: {magnitude:.4f}")
        print(f"             First 10 values: {vector[:10]}\n")


def demo_similarity():
    """Demonstrate word similarity calculations."""
    print_header("DEMO 2: Word Similarity Measurements")
    
    embeddings = WordEmbeddings()
    
    word_pairs = [
        ("king", "queen"),
        ("king", "man"),
        ("woman", "queen"),
        ("man", "woman"),
        ("king", "prince"),
        ("queen", "princess"),
        ("king", "car"),  # Unrelated
    ]
    
    print(f"{Fore.GREEN}Cosine Similarity Scores:{Style.RESET_ALL}")
    print(f"{Fore.GREEN}{'-'*50}{Style.RESET_ALL}\n")
    
    similarities = {}
    for word1, word2 in word_pairs:
        sim = embeddings.get_similarity(word1, word2)
        similarities[f"{word1} ↔ {word2}"] = sim
        
        # Visual bar
        bar_length = int(sim * 30)
        bar = "█" * bar_length
        print(f"  {word1.upper():8} ↔ {word2.upper():8}  {bar:30}  {sim:.4f}")
    
    print()


def demo_vector_arithmetic():
    """Demonstrate the famous King - Man + Woman = Queen example."""
    print_header("DEMO 3: King - Man + Woman = Queen")
    
    embeddings = WordEmbeddings()
    
    print(f"{Fore.YELLOW}The Famous Word Analogy:{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}King - Man + Woman = ?{Style.RESET_ALL}\n")
    
    # Get vectors
    king_vec = embeddings.get_vector("king")
    man_vec = embeddings.get_vector("man")
    woman_vec = embeddings.get_vector("woman")
    queen_vec = embeddings.get_vector("queen")
    
    print(f"{Fore.GREEN}Step 1: Start with 'King'{Style.RESET_ALL}")
    print(f"  Vector magnitude: {VectorAlgebra.magnitude(king_vec):.4f}")
    
    print(f"\n{Fore.GREEN}Step 2: Subtract 'Man' (remove male characteristics){Style.RESET_ALL}")
    temp = VectorAlgebra.subtract_vector(king_vec, man_vec)
    print(f"  Intermediate vector magnitude: {VectorAlgebra.magnitude(temp):.4f}")
    
    print(f"\n{Fore.GREEN}Step 3: Add 'Woman' (add female characteristics){Style.RESET_ALL}")
    print(f"  (King - Man) + Woman")
    
    result_vec, description = embeddings.vector_arithmetic(
        positive=["king", "woman"],
        negative=["man"]
    )
    print(f"  Result vector magnitude: {VectorAlgebra.magnitude(result_vec):.4f}\n")
    
    print(f"{Fore.CYAN}Finding nearest words to the result vector...{Style.RESET_ALL}\n")
    
    nearest = embeddings.find_nearest_words(
        result_vec, 
        top_n=10,
        exclude_words=["king", "man", "woman"]
    )
    
    print(f"{Fore.GREEN}Top Closest Words:{Style.RESET_ALL}")
    print(f"{Fore.GREEN}{'-'*50}{Style.RESET_ALL}")
    
    for i, (word, similarity) in enumerate(nearest, 1):
        bar_length = int(similarity * 25)
        bar = "█" * bar_length
        is_queen = "  ← QUEEN!" if word == "queen" else ""
        print(f"  {i:2}. {word.upper():12} {bar:25}  {similarity:.4f}{is_queen}")
    
    # Compare to actual queen
    queen_similarity = VectorAlgebra.cosine_similarity(result_vec, queen_vec)
    print(f"\n{Fore.YELLOW}Similarity to actual 'Queen': {queen_similarity:.4f}{Style.RESET_ALL}")


def demo_more_analogies():
    """Show more vector arithmetic examples."""
    print_header("DEMO 4: More Vector Analogies")
    
    embeddings = WordEmbeddings()
    
    analogies = [
        ("man", "king", "woman", "Woman to King is like Man to..."),
        ("France", "Paris", "Germany", "Germany is to what as France is to Paris?"),
        ("bad", "worse", "good", "Good to Worse is like Bad to..."),
        ("small", "smaller", "large", "Large to Smaller is like Small to..."),
    ]
    
    for word_a, word_b, word_c, question in analogies:
        print(f"\n{Fore.CYAN}{question}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}{word_a} : {word_b} :: {word_c} : ?{Style.RESET_ALL}\n")
        
        try:
            results = embeddings.analogy(word_a, word_b, word_c, top_n=5)
            
            print(f"{Fore.GREEN}Top Results:{Style.RESET_ALL}")
            for i, (word, score) in enumerate(results, 1):
                bar_length = int(score * 30)
                bar = "█" * bar_length
                print(f"  {i}. {word.upper():15} {bar:30}  {score:.4f}")
        except Exception as e:
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")


def demo_vector_space():
    """Show vector space relationships."""
    print_header("DEMO 5: Vector Space Analysis")
    
    embeddings = WordEmbeddings()
    
    # Related words
    words = ["king", "queen", "prince", "princess", "man", "woman"]
    
    print(f"{Fore.YELLOW}Analyzing word relationships in vector space...{Style.RESET_ALL}\n")
    
    vectors = {word: embeddings.get_vector(word) for word in words}
    analysis = VectorAlgebra.vector_space_analysis(vectors)
    
    print(f"{Fore.GREEN}Vector Space Analysis:{Style.RESET_ALL}")
    print(f"  Dimensions: {analysis['dimensions']}")
    print(f"  Words analyzed: {analysis['count']}\n")
    
    print(f"{Fore.GREEN}Vector Magnitudes:{Style.RESET_ALL}")
    for word, magnitude in analysis['magnitudes'].items():
        print(f"  {word.upper():10} → {magnitude:.4f}")
    
    print(f"\n{Fore.GREEN}Pairwise Similarities:{Style.RESET_ALL}")
    print(f"{Fore.GREEN}{'-'*50}{Style.RESET_ALL}")
    
    # Sort by similarity
    sorted_pairs = sorted(analysis['pairwise_similarities'].items(), 
                         key=lambda x: x[1], reverse=True)
    
    for pair, similarity in sorted_pairs[:10]:
        bar_length = int(similarity * 25)
        bar = "█" * bar_length
        print(f"  {pair:30} {bar:25}  {similarity:.4f}")


def demo_visualizations():
    """Create vector visualizations."""
    print_header("DEMO 6: Vector Space Visualizations")
    
    embeddings = WordEmbeddings()
    
    print(f"{Fore.CYAN}Creating visualizations (this may take a moment)...{Style.RESET_ALL}\n")
    
    # Get vectors for main analogy
    vectors = {
        "King": embeddings.get_vector("king"),
        "Man": embeddings.get_vector("man"),
        "Woman": embeddings.get_vector("woman"),
    }
    
    result_vec, _ = embeddings.vector_arithmetic(
        positive=["king", "woman"],
        negative=["man"]
    )
    
    output_path1 = Path(__file__).parent / "output" / "vector_arithmetic.png"
    output_path1.parent.mkdir(exist_ok=True)
    
    Vector2DVisualizer.plot_vector_arithmetic(
        vectors,
        result_vec,
        result_name="King - Man + Woman ≈ ?",
        save_path=str(output_path1)
    )
    print(f"{Fore.GREEN}✓ Vector arithmetic visualization saved{Style.RESET_ALL}\n")
    
    # Word relationships visualization
    word_list = ["king", "queen", "prince", "princess", "man", "woman", 
                "actor", "actress", "boy", "girl"]
    word_vectors = {word: embeddings.get_vector(word) for word in word_list}
    
    output_path2 = Path(__file__).parent / "output" / "word_space.png"
    Vector2DVisualizer.plot_word_relationships(
        word_vectors,
        save_path=str(output_path2)
    )
    print(f"{Fore.GREEN}✓ Word space visualization saved{Style.RESET_ALL}\n")
    
    # Similarity heatmap
    pairs = [
        ("king", "queen"),
        ("prince", "princess"),
        ("man", "woman"),
        ("actor", "actress"),
        ("king", "prince"),
        ("queen", "princess"),
    ]
    
    similarities = {}
    for w1, w2 in pairs:
        sim = embeddings.get_similarity(w1, w2)
        similarities[f"{w1.title()} ↔ {w2.title()}"] = sim
    
    output_path3 = Path(__file__).parent / "output" / "similarity_heatmap.png"
    Vector2DVisualizer.plot_similarity_heatmap(
        similarities,
        save_path=str(output_path3)
    )
    print(f"{Fore.GREEN}✓ Similarity heatmap saved{Style.RESET_ALL}\n")


def main():
    """Run all demonstrations."""
    print(f"\n{Fore.CYAN}")
    print("╔" + "═"*68 + "╗")
    print("║" + "VECTOR ALGEBRA DEMO: King - Man + Woman = Queen".center(68) + "║")
    print("║" + "Word Embeddings and Semantic Arithmetic".center(68) + "║")
    print("╚" + "═"*68 + "╝")
    print(f"{Style.RESET_ALL}")
    
    try:
        demo_basic_vectors()
        demo_similarity()
        demo_vector_arithmetic()
        demo_more_analogies()
        demo_vector_space()
        demo_visualizations()
        
        # Summary
        print_header("SUMMARY")
        print(f"{Fore.CYAN}Key Insights:{Style.RESET_ALL}\n")
        print("1. {:<50} Words map to high-dimensional vectors".format("✓ EMBEDDINGS:"))
        print("2. {:<50} Vector operations reveal semantic meaning".format("✓ ARITHMETIC:"))
        print("3. {:<50} Similar words are close in vector space".format("✓ SIMILARITY:"))
        print("4. {:<50} Analogies work through vector math".format("✓ ANALOGIES:"))
        print("5. {:<50} Dimensions capture multiple semantic features".format("✓ DIMENSIONS:"))
        
        print(f"\n{Fore.GREEN}✓ All demonstrations completed successfully!{Style.RESET_ALL}\n")
        print(f"{Fore.YELLOW}Generated visualizations are in: output/{Style.RESET_ALL}\n")
        
    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
