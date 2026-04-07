import streamlit as st
from groq import Groq
import os
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
from pypdf import PdfReader

# ------------------ SETUP ------------------
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.set_page_config(page_title="TechRAG Chatbot", page_icon="🤖")
st.title("TechRAG Chatbot")

# ------------------ SYSTEM PROMPT ------------------
SYSTEM_PROMPT = """
You are an intelligent AI assistant.

Rules:
1. If user uploads a PDF, answer using ONLY that PDF.
   - If the PDF is empty or contains no relevant information, politely inform the user and answer using general AI knowledge.
2. If no PDF is provided, answer generally with helpful and accurate tech explanations.
3. Keep answers clear, structured, and beginner-friendly.
4. Do not hallucinate or make up facts.
"""

# ------------------ LOAD EMBEDDING MODEL ------------------
@st.cache_resource
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

model = load_model()

# ------------------ PDF UPLOAD ------------------
uploaded_file = st.file_uploader("Upload a PDF for context", type=["pdf"])
pdf_text = ""

if uploaded_file:
    reader = PdfReader(uploaded_file)
    for page in reader.pages:
        text = page.extract_text()
        if text:
            pdf_text += text + "\n"

# ------------------ CHUNK PDF & CREATE FAISS INDEX ------------------
@st.cache_resource
def create_faiss_index(text):
    if not text:
        return None, None
    words = text.split()
    chunks = [" ".join(words[i:i+50]) for i in range(0, len(words), 50)]
    embeddings = model.encode(chunks, convert_to_numpy=True)
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    return index, chunks

index, chunks = create_faiss_index(pdf_text)

# ------------------ RETRIEVE FROM PDF ------------------
def retrieve_from_pdf(query, k=2):
    if not index or not chunks:
        return None
    query_vector = model.encode([query], convert_to_numpy=True)
    distances, indices = index.search(query_vector, k)
    results = [chunks[i] for i in indices[0] if chunks[i].strip()]
    if not results:
        return None  # No relevant content found
    return "\n".join(results)

# ------------------ SESSION STATE ------------------
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

# ------------------ DISPLAY CHAT ------------------
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ------------------ USER INPUT ------------------
user_input = st.chat_input("Ask a tech question...")

if user_input:
    st.chat_message("user").markdown(user_input)

    # PDF retrieval takes priority
    context = retrieve_from_pdf(user_input) if uploaded_file else None

    if uploaded_file and not context:
        # PDF uploaded but empty / no relevant content
        final_prompt = f"PDF is empty or contains no relevant information.\nQuestion:\n{user_input}"
    elif context:
        # PDF uploaded and has relevant content
        final_prompt = f"Context from PDF:\n{context}\n\nQuestion:\n{user_input}"
    else:
        # No PDF uploaded
        final_prompt = f"Question:\n{user_input}"

    # Add user message
    st.session_state.messages.append({"role": "user", "content": final_prompt})

    # Fetch response from Groq
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=st.session_state.messages,
            temperature=0.3
        )
        bot_reply = response.choices[0].message.content
    except Exception as e:
        bot_reply = f"Error fetching response: {e}"

    # Display & save response
    st.chat_message("assistant").markdown(bot_reply)
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})