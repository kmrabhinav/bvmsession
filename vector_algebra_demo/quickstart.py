"""
Quick start verification for Vector Algebra demo.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / 'src'))


def check_dependencies():
    """Check if all required dependencies are installed."""
    dependencies = {
        'gensim': 'Word embeddings',
        'numpy': 'Numerical computation',
        'scipy': 'Scientific computing',
        'matplotlib': 'Visualization',
        'sklearn': 'Machine learning utilities',
        'pandas': 'Data manipulation',
        'colorama': 'Colored output',
    }
    
    print("Checking dependencies...\n")
    all_ok = True
    
    for package, description in dependencies.items():
        try:
            __import__(package)
            print(f"✓ {package:15} - {description}")
        except ImportError:
            print(f"✗ {package:15} - {description} [MISSING]")
            all_ok = False
    
    return all_ok


def test_modules():
    """Test importing project modules."""
    print("\nTesting project modules...\n")
    
    try:
        from embeddings import WordEmbeddings
        from vector_algebra import VectorAlgebra
        from visualizer import Vector2DVisualizer
        
        print("✓ embeddings.py - Vector embeddings utilities")
        print("✓ vector_algebra.py - Vector operations")
        print("✓ visualizer.py - Visualization tools")
        
        return True
    except Exception as e:
        print(f"✗ Module import failed: {e}")
        return False


def main():
    print("=" * 60)
    print("VECTOR ALGEBRA DEMO - Quick Start Check")
    print("=" * 60 + "\n")
    
    deps_ok = check_dependencies()
    modules_ok = test_modules()
    
    print("\n" + "=" * 60)
    
    if deps_ok and modules_ok:
        print("✓ All checks passed! Ready to run demos.\n")
        print("Quick start commands:")
        print("  • python main_demo.py - Run the main demonstration")
        print("=" * 60 + "\n")
        return 0
    else:
        print("✗ Some checks failed. Please run:")
        print("  pip install -r requirements.txt\n")
        print("=" * 60 + "\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
