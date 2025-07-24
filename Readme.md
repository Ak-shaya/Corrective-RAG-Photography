# 📸 Corrective RAG for Photography Learners

This is a self-improving AI system that helps photography learners get better answers to their questions.

It uses:
- 🧠 **LangChain + FAISS** for document retrieval
- 🤖 **GPT-4** to evaluate context and generate missing information
- 🎯 Automatically improves its knowledge base over time
- 🖥️ A simple **Streamlit interface** for instant Q&A

---

## 🧠 What It Does

1. You ask a photography question (e.g., "Why are my portraits too bright?")
2. The app retrieves relevant content from your notes
3. GPT-4 evaluates whether the content is:
   - Relevant
   - Complete
   - Accurate
   - Specific
4. If the content is **poor**, it will:
   - Ask GPT-4 to generate a correct explanation
   - Store that new content back into your FAISS index
5. Next time someone asks a similar question — it will already have the answer ✅

---

## 🚀 Quick Start
## 🚀 Getting Started

### 🔧 1. Clone the Repo

```bash
git clone https://github.com/Ak-shaya/Corrective-RAG-Photography.git
cd Corrective-RAG-Photography
```

---

### 🛠️ 2. Set Up the Environment

Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install all required packages:

```bash
pip install -r requirements.txt
```

Create a `.env` file and paste your OpenAI API key:

```env
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

---

### 🧠 3. (One-Time) Create the FAISS Index

1. Open the file `corrective_rag_app.py`  
2. Scroll to the bottom and **uncomment** this line:

```python
create_vectorstore()
```

3. Run the app once to generate the vector index:

```bash
streamlit run corrective_rag_app.py
```

4. After the index is created, **comment the line again** to avoid overwriting:

```python
# create_vectorstore()
```

---

### ▶️ 4. Use the App

```bash
streamlit run corrective_rag_app.py
```

Ask any photography question. The AI assistant will retrieve context, evaluate its quality, and learn if needed!

---

## 🧰 Tech Stack

| Tool           | Purpose                            |
|----------------|-------------------------------------|
| Streamlit      | UI interface                        |
| LangChain      | Retrieval + orchestration           |
| FAISS          | Local vectorstore                   |
| OpenAI GPT-4   | Evaluation + content generation     |
| Python         | Core programming language           |

---

## 🛡️ Security & Clean Repo

- ✅ `.env` is excluded via `.gitignore` to protect your API key  
- ✅ `faiss_index/` is excluded to avoid pushing large vector files  
- ✅ `.DS_Store` and `__pycache__/` are excluded for cleanliness  

---

## 🧩 Future Enhancements

- Support PDFs, YouTube transcripts, and Notion docs  
- User-specific indexes with login  
- Track learning growth and content history  
- SaaS-ready frontend and admin panel  

---

## 🤝 Contributing

Want to use this for fitness, finance, or any other niche?  
Fork it, build on it, and let's grow together!

---

Made with ❤️ by [Akshaya](https://github.com/Ak-shaya)
