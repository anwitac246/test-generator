#  AI-Powered Test Generator

This project is an AI-based test paper generator designed to create practice questions for competitive exams like **JEE Mains**, **NEET**, and **UPSC**. It uses a Retrieval-Augmented Generation (RAG) pipeline to extract questions from subject-specific input PDFs, including both text and diagrams.

##  Features

-  Converts reference material into practice questions  
-  Uses RAG to generate high-quality questions and options  
-  Handles diagrams and formulas from PDFs (non-OCR based)  
-  Supports JEE Mains, NEET, and UPSC syllabus  

##  Tech Stack

- Python  
- LangChain  
- FAISS / ChromaDB (Vector Store)  
- PyMuPDF / pdf2image for PDF parsing  
- Hugging Face Transformers (for generation)

##  Getting Started

```bash
git clone https://github.com/yourusername/ai-test-generator.git
cd ai-test-generator
pip install -r requirements.txt
python app.py
