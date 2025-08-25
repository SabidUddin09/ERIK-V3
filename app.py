import streamlit as st
from googlesearch import search
import requests
from bs4 import BeautifulSoup
import fitz  # PyMuPDF for PDF
import docx
import sympy as sp
import matplotlib.pyplot as plt
import io
import random

# ------------------ ERIK Intro ------------------
st.set_page_config(page_title="ERIK - Exceptional Resources & Intelligence Kernal", layout="wide")

st.title("🤖 ERIK - Exceptional Resources & Intelligence Kernal")
st.write("Welcome to **ERIK**! 🚀\n\nYour AI-powered study buddy for solving doubts, generating quizzes, analyzing topics, and more. Supports **Bangla + English** automatically.")

# ------------------ Session State ------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ------------------ Utility Functions ------------------
def google_answer(query):
    try:
        result_links = list(search(query, num_results=1))
        if result_links:
            url = result_links[0]
            page = requests.get(url, timeout=5)
            soup = BeautifulSoup(page.text, "html.parser")
            text = " ".join([p.text for p in soup.find_all("p")[:5]])
            return text[:800] + "...\n\n(Source: " + url + ")"
        return "No results found."
    except:
        return "Error while searching."

def solve_math(expression):
    try:
        expr = sp.sympify(expression)
        solution = sp.simplify(expr)
        return f"**Solution:** {solution}"
    except:
        return "Sorry, could not solve the math problem."

def plot_graph(expression):
    try:
        x = sp.symbols("x")
        expr = sp.sympify(expression)
        sp_expr = sp.lambdify(x, expr, "numpy")

        import numpy as np
        X = np.linspace(-10, 10, 400)
        Y = sp_expr(X)

        fig, ax = plt.subplots()
        ax.plot(X, Y)
        ax.axhline(0, color="black")
        ax.axvline(0, color="black")
        ax.set_title(f"Graph of {expression}")
        st.pyplot(fig)
    except Exception as e:
        st.write("Graph error:", e)

def generate_quiz(topic):
    qs = [
        f"What is the key concept of {topic}?",
        f"Explain {topic} in 2 lines.",
        f"Create 1 MCQ from {topic}.",
    ]
    return random.sample(qs, 2)

def generate_flashcards(topic):
    return {
        "Front": f"Definition of {topic}?",
        "Back": f"{topic} means ..."
    }

# ------------------ Features ------------------
menu = st.sidebar.radio("📚 Features", 
    ["💬 Doubt Solver", "📑 Topic Analyzer", "📂 Document Upload", "📝 Quiz Generator", "🎴 Flashcards"])

# ---- Doubt Solver ----
if menu == "💬 Doubt Solver":
    query = st.text_input("Ask your question (Bangla or English):")
    response_type = st.radio("Response format:", ["Short", "Long"])

    if st.button("Get Answer"):
        if any("০১২৩৪৫৬৭৮৯অআইঈউঊঋএঐওঔকখগঘঙচছজঝঞটঠডঢণতথদধনপফবভমযরলশষসহ" in ch for ch in query):
            lang = "bn"
        else:
            lang = "en"

        if any(op in query for op in ["+", "-", "*", "/", "x^2", "integrate", "diff"]):
            answer = solve_math(query)
        else:
            answer = google_answer(query)

        if response_type == "Short":
            answer = answer[:250] + "..."

        st.session_state.chat_history.append(("You", query))
        st.session_state.chat_history.append(("ERIK", answer))

    # Show history
    for sender, msg in st.session_state.chat_history:
        st.write(f"**{sender}:** {msg}")

    # Graph generator option
    graph_exp = st.text_input("Enter math expression to plot (e.g., x**2 + 3*x):")
    if st.button("Plot Graph"):
        plot_graph(graph_exp)

# ---- Topic Analyzer ----
elif menu == "📑 Topic Analyzer":
    topic = st.text_input("Enter exam topic:")
    if st.button("Analyze"):
        st.write(f"**Key Concepts of {topic}:**\n- Concept 1\n- Concept 2\n- Concept 3")
        st.write(f"**Example Question:** What is {topic} used for?")

# ---- Document Upload ----
elif menu == "📂 Document Upload":
    uploaded = st.file_uploader("Upload PDF, DOCX, or TXT", type=["pdf", "docx", "txt"])
    if uploaded:
        text = ""
        if uploaded.name.endswith(".pdf"):
            doc = fitz.open(stream=uploaded.read(), filetype="pdf")
            for page in doc:
                text += page.get_text()
        elif uploaded.name.endswith(".docx"):
            doc = docx.Document(uploaded)
            for para in doc.paragraphs:
                text += para.text + "\n"
        else:
            text = uploaded.read().decode("utf-8")

        st.write("📖 Extracted Content:")
        st.write(text[:1000])

# ---- Quiz Generator ----
elif menu == "📝 Quiz Generator":
    topic = st.text_input("Enter topic for quiz:")
    if st.button("Generate Quiz"):
        st.write(generate_quiz(topic))

# ---- Flashcards ----
elif menu == "🎴 Flashcards":
    topic = st.text_input("Enter topic for flashcards:")
    if st.button("Generate Flashcards"):
        flash = generate_flashcards(topic)
        st.write("**Front:**", flash["Front"])
        st.write("**Back:**", flash["Back"])
