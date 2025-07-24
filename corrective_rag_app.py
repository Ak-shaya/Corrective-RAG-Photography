# ----------------------------------------
# 🔧 IMPORTS & ENV SETUP
# ----------------------------------------
import os
import streamlit as st
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.prompts import PromptTemplate
from langchain.schema import Document

# ----------------------------------------
# 🔐 LOAD ENV
# ----------------------------------------
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# ----------------------------------------
# 🧠 LLM + EMBEDDINGS SETUP
# ----------------------------------------
llm = ChatOpenAI(model="gpt-4", temperature=0, openai_api_key=openai_api_key)
embeddings = OpenAIEmbeddings()

# ----------------------------------------
# 📄 PROMPT TEMPLATE (EVALUATION)
# ----------------------------------------
corrective_prompt_template = """
You are a Corrective RAG system built to support photography learners.
Your job is to evaluate whether the context retrieved is good enough to answer the student’s query about photography concepts, techniques, or common mistakes.

Query: {user_query}
Retrieved Context: {retrieved_context}

Evaluate using the following:
1. Relevance Score (0-1)
2. Completeness Score (0-1)
3. Accuracy Score (0-1)
4. Specificity Score (0-1)

Give your evaluation:
- Relevance Score: ____
- Completeness Score: ____
- Accuracy Score: ____
- Specificity Score: ____
- Overall Quality: [EXCELLENT/GOOD/FAIR/POOR]
- Action Needed: [PROCEED_WITH_ANSWER / RETRIEVE_AGAIN]

If Action Needed is RETRIEVE_AGAIN, provide:
• NEW_QUERY: [A more focused query to retrieve better context]
• REASONING: [Why the original context was insufficient]

Respond only in this evaluation format.
"""

# ----------------------------------------
# 📦 VECTOR STORE UTILS
# ----------------------------------------
def create_vectorstore():
    loader = TextLoader("sample_photography_notes.txt")
    documents = loader.load()

    text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = text_splitter.split_documents(documents)

    vectorstore = FAISS.from_documents(docs, embeddings)
    vectorstore.save_local("faiss_index")
    return vectorstore

def load_vectorstore(path="faiss_index"):
    return FAISS.load_local(path, embeddings, allow_dangerous_deserialization=True)

# ----------------------------------------
# 🔍 CORE RAG LOGIC
# ----------------------------------------
def retrieve_context(user_query):
    retriever = load_vectorstore().as_retriever()
    return retriever.get_relevant_documents(user_query)

def evaluate_context(user_query, retrieved_context):
    prompt = PromptTemplate.from_template(corrective_prompt_template)
    eval_prompt = prompt.format(user_query=user_query, retrieved_context=retrieved_context)
    return llm.predict(eval_prompt)

def generate_new_content(user_query):
    generation_prompt = f"""
    A photography learner asked: "{user_query}"

    The current content database doesn't answer this well.

    Please write a 150-200 word educational explanation that answers the question clearly and helpfully, suitable for photography beginners. Focus on practical advice and accuracy.
    """
    return llm.predict(generation_prompt)

def add_to_vectorstore(new_text):
    vectorstore = load_vectorstore()
    doc = Document(page_content=new_text)
    vectorstore.add_documents([doc])
    vectorstore.save_local("faiss_index")

def generate_final_answer(user_query):
    docs = retrieve_context(user_query)
    combined_context = "\n".join([doc.page_content for doc in docs])
    evaluation = evaluate_context(user_query, combined_context)

    # Check if model asks to retrieve again
    if "RETRIEVE_AGAIN" in evaluation:
        new_content = generate_new_content(user_query)
        add_to_vectorstore(new_content)

        # Re-run with new content
        docs = retrieve_context(user_query)
        combined_context = "\n".join([doc.page_content for doc in docs])
        evaluation = evaluate_context(user_query, combined_context)

    return evaluation, combined_context

# ----------------------------------------
# 🎨 STREAMLIT UI
# ----------------------------------------
st.set_page_config(page_title="📸 Corrective RAG with Auto-Learning", layout="centered")

st.markdown(
    "<h2 style='color:purple;'>📸 AI Assistant for Photography Learners</h2>",
    unsafe_allow_html=True
)

st.markdown("Ask a question about photography (e.g., lighting, framing, overexposure)")

user_query = st.text_input("Your question:", placeholder="Why are my portraits too bright?")

if st.button("Submit") and user_query:
    with st.spinner("Retrieving, evaluating and learning..."):
        evaluation, context = generate_final_answer(user_query)

    st.markdown("### 🔍 Evaluation Result")
    st.code(evaluation)

    st.markdown("### 📚 Retrieved Context")
    st.code(context)

# ----------------------------------------
# ⚠️ Optional: Run Once to Create Initial Index
# ----------------------------------------
# create_vectorstore()
