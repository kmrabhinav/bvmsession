"""
PDF Ingestion and Processing Module
Loads and processes PDF documents for RAG pipeline
"""

from typing import List, Tuple
from pathlib import Path
import re


class PDFIngestion:
    """Load and ingest PDF documents."""
    
    def __init__(self):
        """Initialize PDF ingestion (pypdf will be imported on demand)."""
        self.pdf_path = None
        self.raw_text = None
        self.pages = []
    
    def load_pdf(self, file_path: str) -> str:
        """
        Load PDF and extract text.
        
        Args:
            file_path: Path to PDF file
            
        Returns:
            Extracted text from PDF
        """
        try:
            from PyPDF2 import PdfReader
        except ImportError:
            raise ImportError("PyPDF2 not installed. Run: pip install PyPDF2")
        
        self.pdf_path = file_path
        pdf_reader = PdfReader(file_path)
        
        full_text = ""
        page_texts = []
        
        for page_num, page in enumerate(pdf_reader.pages):
            text = page.extract_text()
            page_texts.append({
                'page': page_num + 1,
                'text': text,
                'length': len(text)
            })
            full_text += f"\n[Page {page_num + 1}]\n{text}\n"
        
        self.raw_text = full_text
        self.pages = page_texts
        
        return full_text
    
    def get_text_stats(self) -> dict:
        """Get statistics about loaded text."""
        if not self.raw_text:
            return {}
        
        lines = self.raw_text.split('\n')
        words = self.raw_text.split()
        paragraphs = [p for p in self.raw_text.split('\n\n') if p.strip()]
        
        return {
            'total_characters': len(self.raw_text),
            'total_words': len(words),
            'total_lines': len(lines),
            'total_paragraphs': len(paragraphs),
            'average_word_length': sum(len(w) for w in words) / len(words) if words else 0,
            'pages': len(self.pages)
        }
    
    def clean_text(self, text: str) -> str:
        """
        Clean extracted text.
        
        Args:
            text: Raw text to clean
            
        Returns:
            Cleaned text
        """
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove page markers
        text = re.sub(r'\[Page \d+\]', '', text)
        
        # Remove excessive newlines
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        return text.strip()
    
    def get_page_content(self, page_num: int) -> str:
        """Get content from specific page."""
        if page_num < 1 or page_num > len(self.pages):
            return ""
        
        return self.pages[page_num - 1]['text']
    
    def extract_metadata(self) -> dict:
        """Extract metadata from PDF."""
        try:
            from PyPDF2 import PdfReader
        except ImportError:
            return {}
        
        if not self.pdf_path:
            return {}
        
        pdf_reader = PdfReader(self.pdf_path)
        metadata = pdf_reader.metadata or {}
        
        return {
            'title': metadata.get('/Title', 'Unknown'),
            'author': metadata.get('/Author', 'Unknown'),
            'subject': metadata.get('/Subject', 'Unknown'),
            'pages': len(pdf_reader.pages),
            'created': str(metadata.get('/CreationDate', 'Unknown')),
        }
