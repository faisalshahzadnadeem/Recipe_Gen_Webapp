# 🍳 AI-Powered Recipe Generator & Recipe Chatbot (RAG)

A professional Streamlit application that uses **Cohere LLMs** to generate recipes from ingredients and answer questions based on uploaded recipe books (PDFs). The app combines **prompt-based generation** and **retrieval-augmented generation (RAG)** for accurate and intelligent culinary assistance.

## 🚀 Live Demo

👉 [Launch on Streamlit Cloud](https://share.streamlit.io/your-username/recipe-ai-streamlit/main/app.py)  
*(Replace with actual link after deployment)*

---

## 🔍 Features

### ✅ Recipe Generator (Ingredients → Recipe)
- Input ingredients and cuisine
- Get detailed, step-by-step recipes
- Powered by Cohere’s `command-r-plus` LLM

### ✅ Recipe Chatbot (PDF → Q&A)
- Upload a recipe book (PDF)
- Ask questions about it
- Combines Cohere embeddings + top-ranked PDF chunks + LLM generation

---

## 🧠 Tech Stack

| Component       | Details                             |
|----------------|-------------------------------------|
| 🧠 LLM          | [Cohere](https://cohere.com) - `command-r-plus`, `embed-english-v3.0` |
| 🧾 RAG          | Embedding chunks from PDF → Retrieval → Answer |
| 📊 UI           | [Streamlit](https://streamlit.io)   |
| 📄 PDF Parsing | PyPDF2                              |
| 🧪 Embeddings   | Cosine similarity with `numpy`      |

---

## 📁 Project Structure

```

📦RecipeApp/
│
├── app.py                     # Main Streamlit script
├── cohere\_recipe\_gen\_updated.py  # Recipe generation logic
├── recipe\_rag\_bot.py          # RAG bot logic
├── requirements.txt           # Project dependencies
└── .streamlit/
└── config.toml            # (Optional) Custom theming

````

---

## 🛠️ Installation (Local)

```bash
# Clone the repo
git clone https://github.com/your-username/recipe-ai-streamlit.git
cd recipe-ai-streamlit

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate   # On Windows
# source venv/bin/activate  # On macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
````

---

## 🔐 API Key

This app uses **Cohere API**. Get your key from: [https://dashboard.cohere.com/](https://dashboard.cohere.com/)

Set it directly in `app.py` or use environment variables.

```python
COHERE_API_KEY = "your-api-key-here"
```

---

## 🎨 Custom Theme (Optional)

Configure theme in `.streamlit/config.toml`:

```toml
[theme]
primaryColor="#FFD700"             # Yellow
backgroundColor="#1C1C1C"          # Charcoal
secondaryBackgroundColor="#000000" # Black
textColor="#FFFFFF"
font="sans serif"
```

---

## 🧠 Sample Prompts

### 🍽 Recipe Generator

> **Ingredients:** chicken breast, garlic, lemon
> **Cuisine:** Mediterranean
> **Prompt to LLM:**
> “You are a professional chef. Using the following ingredients, write a detailed Mediterranean recipe…”

### 🤖 Chatbot Prompt

> “Use the following context from a recipe book to answer the user's question. If not found, use your own knowledge…”

---

## 📌 To-Do / Future Enhancements

* Upload multiple PDFs
* Export recipes to PDF/Word
* Save chat history
* Speech-to-text for voice recipe queries

---

## 🙌 Acknowledgments

* [Cohere](https://cohere.com) for APIs
* [Streamlit](https://streamlit.io) for fast app development
* [HEC Microsoft Azure for Students](https://azure.microsoft.com/en-us/free/students/) for deployment resources

---

## 📄 License

MIT License. Use it for educational and non-commercial purposes.

```

---

Let me know if you want this saved as a downloadable `README.md` file or tailored to a specific GitHub repo name or author.
```
