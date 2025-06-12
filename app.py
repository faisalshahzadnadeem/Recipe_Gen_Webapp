# Professional Streamlit App for Recipe Generation + RAG Chatbot (LOCAL VERSION)

import streamlit as st
import os
import re
import tempfile
import cohere
from PyPDF2 import PdfReader
import numpy as np

# === CONFIG ===
COHERE_API_KEY = "TjRlGT2z3C8nqBlNysvvtWYFBw3ynV2ylYDobuUA"
co = cohere.Client(COHERE_API_KEY)

# ===========================
# --- RECIPE GENERATOR ------
# ===========================
def is_valid_ingredients(text):
    items = [i.strip() for i in text.split(",")]
    return len(items) >= 2 and all(re.match("^[a-zA-Z\s\-]+$", i) for i in items)

def is_valid_cuisine(text):
    return bool(re.match("^[a-zA-Z\s]+$", text)) and len(text) >= 3

def generate_recipe(ingredients, cuisine):
    prompt = (
        f"You are a professional chef. Using the following ingredients, write a detailed "
        f"{cuisine} recipe.\n\n"
        f"Ingredients: {ingredients}\n\n"
        f"Write clear, numbered, step-by-step cooking instructions only.\n"
        f"Include at least 8 detailed steps.\n\n"
        f"Steps:"
    )
    response = co.generate(
        model="command-r-plus",
        prompt=prompt,
        max_tokens=750,
        temperature=0.4,
    )
    return response.generations[0].text.strip()

# ===========================
# --- RAG CHATBOT -----------
# ===========================
def load_pdf_chunks(pdf_path: str, chunk_size: int = 300):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

def embed_chunks(chunks):
    response = co.embed(
        texts=chunks,
        model="embed-english-v3.0",
        input_type="search_document"
    )
    return response.embeddings

def retrieve_chunks(query, chunks, embeddings, top_k=3):
    query_emb = co.embed(
        texts=[query],
        model="embed-english-v3.0",
        input_type="search_query"
    ).embeddings[0]
    similarities = [
        np.dot(query_emb, emb) / (np.linalg.norm(query_emb) * np.linalg.norm(emb))
        for emb in embeddings
    ]
    top_indices = sorted(range(len(similarities)), key=lambda i: similarities[i], reverse=True)[:top_k]
    return [chunks[i] for i in top_indices]

def generate_answer(query, context):
    prompt = (
        f"You are a culinary assistant. Use the following context from a recipe book to answer the user's question. "
        f"If the context does not contain the answer, use your own knowledge to help.\n\n"
        f"Context:\n{context}\n\n"
        f"User's Question: {query}\n\n"
        f"Answer:"
    )
    response = co.generate(
        model="command-r-plus",
        prompt=prompt,
        max_tokens=500,
        temperature=0.4,
    )
    return response.generations[0].text.strip()

# ===========================
# --- STREAMLIT UI ----------
# ===========================
st.set_page_config(page_title="Recipe AI & RAG Bot", layout="wide")

# Custom CSS for floating chat widget
st.markdown("""
    <style>
    .bot-float {
        position: fixed;
        bottom: 20px;
        right: 30px;
        width: 350px;
        z-index: 1001;
        background: white;
        box-shadow: 0 0 16px rgba(0,0,0,0.2);
        border-radius: 16px;
        border: 1px solid #eee;
        padding-bottom: 8px;
        padding-top: 0;
    }
    .bot-float-header {
        background: #00c4b4;
        color: white;
        padding: 8px 16px;
        border-top-left-radius: 16px;
        border-top-right-radius: 16px;
        font-weight: bold;
        font-size: 16px;
        margin-bottom: 0px;
    }
    .bot-float-content {
        padding: 12px 16px 0 16px;
        max-height: 260px;
        overflow-y: auto;
        font-size: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# --- Main Layout ---
col1, col2 = st.columns([2, 1])

with col1:
    st.header("🍳 AI Recipe Generator")
    with st.form("recipe_form"):
        ingredients = st.text_input("Enter ingredients (comma-separated):", value="chicken breast, olive oil, garlic, salt, pepper, lemon juice")
        cuisine = st.text_input("Cuisine type (e.g., Italian, Indian):", value="Mediterranean")
        submitted = st.form_submit_button("Generate Recipe")

        if submitted:
            if not is_valid_ingredients(ingredients):
                st.error("Please enter at least two valid ingredients, separated by commas.")
            elif not is_valid_cuisine(cuisine):
                st.error("Please enter a valid cuisine type (e.g., 'Indian', 'Italian').")
            else:
                with st.spinner("Generating recipe..."):
                    recipe_steps = generate_recipe(ingredients, cuisine)
                st.success("Here's your recipe!")
                st.markdown(f"#### {cuisine.title()} Recipe with {ingredients.title()}:")
                st.markdown(recipe_steps)

with col2:
    st.header("📄 Upload Recipe Book (PDF)")
    pdf_file = st.file_uploader("Upload PDF for RAG Chatbot:", type=["pdf"])
    if pdf_file:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tf:
            tf.write(pdf_file.read())
            pdf_path = tf.name
        st.success("PDF uploaded and processed for chatbot.")

# --- Chatbot Widget ---
with st.container():
    st.markdown('<div class="bot-float">', unsafe_allow_html=True)
    st.markdown('<div class="bot-float-header">🤖 Recipe Chatbot</div>', unsafe_allow_html=True)
    st.markdown('<div class="bot-float-content">', unsafe_allow_html=True)

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if not pdf_file:
        st.info("Upload a PDF to enable chat.")
    else:
        if "rag_chunks" not in st.session_state or st.session_state.get("rag_pdf_path") != pdf_path:
            with st.spinner("Processing PDF and generating embeddings..."):
                chunks = load_pdf_chunks(pdf_path)
                embeddings = embed_chunks(chunks)
                st.session_state["rag_chunks"] = chunks
                st.session_state["rag_embeddings"] = embeddings
                st.session_state["rag_pdf_path"] = pdf_path

        prompt = st.text_input("Ask the RAG bot (about your PDF):", key="chatbot_input")
        if st.button("Send", key="chatbot_send") and prompt:
            chunks = st.session_state["rag_chunks"]
            embeddings = st.session_state["rag_embeddings"]
            top_chunks = retrieve_chunks(prompt, chunks, embeddings)
            context = "\n".join(top_chunks)
            answer = generate_answer(prompt, context)
            st.session_state.chat_history.append(("user", prompt))
            st.session_state.chat_history.append(("bot", answer))

        for who, msg in st.session_state.chat_history[-6:]:
            align = "right" if who == "user" else "left"
            color = "#006" if who == "user" else "#00c4b4"
            st.markdown(f"<div style='text-align:{align}; color:{color}; margin-bottom:8px;'><b>{'You' if who=='user' else 'Bot'}:</b> {msg}</div>", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

