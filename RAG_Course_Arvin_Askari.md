# Week 1 — RAG Mini-Course Notes (LLMWare 2024)

> **Name:** Arvin Askari  
> **File name:** `RAG_Course_Arvin_Askari.md`  
> **Course:** https://www.udemy.com/course/learn-rag-with-llmware-2024/  

---
## Pipeline Map — what & why (1–2 bullets per step)

### 1) Ingest
- **What:** Collect and load raw data sources such as PDFs, websites, or text files into the RAG system.  
- **Why:** Ensures all relevant information is accessible for later processing and retrieval.

### 2) Chunk
- **What:** Split large documents into smaller, overlapping text chunks (e.g., 500–1,000 tokens each).  
- **Why:** Improves retrieval precision by allowing the model to search smaller, context-rich passages instead of entire documents.

### 3) Embed & Index
- **What:** Convert each chunk into a numerical vector (embedding) using a pre-trained model, then store them in a vector database or index.  
- **Why:** Enables semantic search based on meaning rather than exact keyword matches, improving accuracy and recall.

### 4) Retrieve (top-k)
- **What:** Use the user’s query to find and return the *k* most semantically similar chunks from the vector index.  
- **Why:** Provides the model with the most relevant context to ground its response in factual source material.

### 5) Generate
- **What:** Combine the user’s query with the retrieved chunks and pass them to the LLM for final answer generation.  
- **Why:** Reduces hallucinations and ensures the response is contextually accurate and supported by real data.

---

## Glossary — 5 terms (one sentence each)
- **Library:** Parses, chunks, and indexes documents to convert a “pile of files” into an AI-ready knowledge base.  
- **Embedding:** Transforms text into numerical vectors that capture semantic meaning, enabling similarity search.  
- **Chunking:** The process of splitting large documents into smaller, overlapping text sections for better retrieval accuracy.  
- **Retrieval:** The step where the system finds the most relevant chunks based on vector similarity.  
- **Context Window:** The portion of text the LLM can “see” and use when generating an answer.
