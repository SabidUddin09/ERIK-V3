import streamlit as st
import requests
from bs4 import BeautifulSoup
import sympy as sp
import matplotlib.pyplot as plt
import random
import urllib.parse

# ------------------ ERIK Intro ------------------
st.set_page_config(page_title="ERIK - Exceptional Resources & Intelligence Kernal", layout="wide")
st.title("🤖 ERIK - Exceptional Resources & Intelligence Kernal")
st.write("Welcome to **ERIK**! 🚀\n\nYour AI-powered study buddy for solving doubts, generating quizzes, analyzing topics, and more. Supports **Bangla + English** automatically.")

# ------------------ Session State ------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ------------------ Utility Functions ------------------
def google_search_answer(query):
    """Search Google and return first paragraph from Wikipedia or top result"""
    try:
        search_url = "https://www.google.com/search?q=" + urllib.parse.quote(query)
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        # Try to get snippet from Google
        snippet = soup.find("div", class_="BNeawe s3v9rd AP7Wnd")
        if snippet:
            return snippet.text
        # Fallback to Wikipedia
        wiki_url = f"https://en.wikipedia.org/wiki/{query.replace(' ', '_')}"
        wiki_page = requests.get(wiki_url, headers=headers)
        wiki_soup = BeautifulSoup(wiki_page.text, "html.parser")
        paragraphs = wiki_soup.find_all("p")
        for p in paragraphs:
            if len(p.text) > 50:
                return p.text
        return "No good answer found."
    except Exception as e:
        return f"Error fetching answer: {e}"

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
    ["💬 Doubt Solver", "📑 Topic Analyzer", "📝 Quiz Generator", "🎴 Flashcards"])

# ---- Doubt Solver ----
if menu == "💬 Doubt Solver":
    query = st.text_input("Ask your question (Bangla or English):")
    response_type = st.radio("Response format:", ["Short", "Long"])

    if st.button("Get Answer"):
        if any(op in query for op in ["+", "-", "*", "/", "x^2", "integrate", "diff"]):
            answer = solve_math(query)
        else:
            answer = google_search_answer(query)

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
