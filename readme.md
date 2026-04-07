# TechRAG Chatbot

**TechRAG Chatbot** is an AI assistant built using **RAG (Retrieval-Augmented Generation)**.  
It answers tech-related questions and can retrieve answers from PDFs you upload.  

---

## Features

- Upload a PDF and get answers directly from your document.  
- Ask general tech questions (Cloud Computing, DevOps, Quantum Computing, etc.) even without a PDF.  
- Beginner-friendly answers and structured responses.  
- Keeps conversation history in session.  
- Built with **Streamlit**, **Groq LLM**, **FAISS embeddings**, and **Sentence Transformers**.  

---

## How It Works

1. **PDF Upload:** The chatbot extracts text from your PDF.  
2. **Embedding & Indexing:** Converts text into vector embeddings using `SentenceTransformer` and stores them in a FAISS index.  
3. **Querying:** When a question is asked, it searches the PDF embeddings first.  
4. **Fallback:** If no PDF is uploaded, it queries the LLM (Groq) directly.  
5. **Response:** The chatbot returns the answer in a structured, clear format.  

---

## Getting Started

Clone the repository

```bash
git clone https://github.com/your-username/TechRAG-Chatbot.git
cd TechRAG-Chatbot

Install dependencies
pip install -r requirements.txt

Create a .env file in the project folder
GROQ_API_KEY=your_groq_api_key_here

Run the app locally
streamlit run app.py