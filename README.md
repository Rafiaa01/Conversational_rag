Task 1: Document-Based RAG Chatbot
Overview
Built a Retrieval-Augmented Generation (RAG) chatbot using LangChain, FAISS, Hugging Face embeddings, and OpenAI's GPT-4o-mini.

Features
Loads and extracts text from a PDF using PyPDFLoader.
Splits documents into chunks using RecursiveCharacterTextSplitter.
Generates 1536-dimensional embeddings using text-embedding-3-small.
Stores embeddings in a FAISS vector store.
Retrieves the top 3 relevant chunks for a user query.
Generates context-grounded answers and acknowledges unavailable information.
Displays retrieved chunks, source documents, and page numbers for debugging.
Supports interactive questions through the terminal.
Technologies
Python, LangChain, FAISS, OpenAI API, and PyPDFLoader.