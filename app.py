import streamlit as st
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from googlesearch import search
import requests
from bs4 import BeautifulSoup
import fitz  # PyMuPDF
import docx

# ---------------------------
# APP TITLE & INTRO
# ---------------------------
st.set_page_config(page_title="ERIK - AI Study Assistant", layout="wide")
st.title("📘 ERIK - Exceptional Resources & Intelligence Kernal")
st.write("Welcome to **ERIK**, your AI-powered study and research assistant. 🚀")
st.write("👉 Features: Doubt Solver | Topic Analyzer | Quiz Generator | Flashcards | Document Upload | Math Solver | Graphing | Research Assistant | 3D Diagrams")

# ---------------------------
# CHAT HISTORY
# ---------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

def add_chat(role, text):
    st.session_state.chat_history.append({"role": role, "text": text})

# ---------------------------
# DOCUMENT UPLOAD
# ---------------------------
def extract_text_from_file(uploaded_file):
    if uploaded_file.type == "application/pdf":
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = docx.Document(uploaded_file)
        return " ".join([para.text for para in doc.paragraphs])
    else:
        return uploaded_file.read().decode("utf-8")

# ---------------------------
# DOUBT SOLVER
# ---------------------------
def doubt_solver(question):
    # Simple Google-based answer fetch
    query = question
    try:
        for j in search(query, num=1, stop=1, lang="en"):
            res = requests.get(j)
            soup = BeautifulSoup(res.text, "html.parser")
            return soup.get_text()[:500]
    except:
        return "Couldn't fetch an answer. Please try rephrasing."

# ---------------------------
# QUIZ GENERATOR
# ---------------------------
def generate_quiz(text, q_type="MCQ"):
    sentences = text.split(".")
    questions = []
    for i, sentence in enumerate(sentences[:5]):
        if q_type == "MCQ":
            questions.append(f"Q{i+1}: {sentence.strip()}?")
        elif q_type == "Short":
            questions.append(f"Q{i+1}: Explain briefly → {sentence.strip()}")
        else:
            questions.append(f"Q{i+1}: Write in detail → {sentence.strip()}")
    return questions

# ---------------------------
# FLASHCARDS
# ---------------------------
def generate_flashcards(text):
    key_points = text.split(".")[:5]
    return [{"front": f"Concept {i+1}", "back": kp.strip()} for i, kp in enumerate(key_points)]

# ---------------------------
# ADVANCED MATH SOLVER
# ---------------------------
def solve_math(expression):
    try:
        expr = sp.sympify(expression)
        simplified = sp.simplify(expr)
        derivative = sp.diff(expr)
        integral = sp.integrate(expr)
        return {
            "Simplified": str(simplified),
            "Derivative": str(derivative),
            "Integral": str(integral)
        }
    except Exception as e:
        return {"Error": str(e)}

# ---------------------------
# GRAPH GENERATOR (2D & 3D)
# ---------------------------
def plot_function(expr):
    x = sp.symbols('x')
    f = sp.lambdify(x, sp.sympify(expr), "numpy")
    X = np.linspace(-10, 10, 400)
    Y = f(X)
    fig, ax = plt.subplots()
    ax.plot(X, Y)
    ax.set_title(f"Graph of {expr}")
    st.pyplot(fig)

def plot_3d(expr):
    x, y = sp.symbols('x y')
    f = sp.lambdify((x,y), sp.sympify(expr), "numpy")
    X = np.linspace(-5, 5, 50)
    Y = np.linspace(-5, 5, 50)
    X, Y = np.meshgrid(X, Y)
    Z = f(X, Y)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(X, Y, Z, cmap="viridis")
    ax.set_title(f"3D Surface of {expr}")
    st.pyplot(fig)

# ---------------------------
# RESEARCH ASSISTANT
# ---------------------------
def research_assistant(topic):
    st.write(f"🔍 Researching: {topic}")
    results = []
    try:
        for j in search(topic, num=3, stop=3, lang="en"):
            results.append(j)
    except:
        results.append("No results found")
    return results

# ---------------------------
# SIDEBAR MENU
# ---------------------------
menu = st.sidebar.selectbox("📌 Choose Feature", 
    ["Doubt Solver", "Topic Analyzer", "Document Upload", 
     "Quiz Generator", "Flashcards", "Math Solver", 
     "Graph Generator", "3D Diagram Generator", "Research Assistant"])

# ---------------------------
# MAIN APP LOGIC
# ---------------------------
if menu == "Doubt Solver":
    q = st.text_input("Ask your academic question:")
    if q:
        ans = doubt_solver(q)
        add_chat("User", q)
        add_chat("ERIK", ans)
        st.write("**Answer:**", ans)

elif menu == "Topic Analyzer":
    topic = st.text_area("Enter a topic:")
    if topic:
        st.subheader("🔑 Key Concepts")
        st.write(topic.split()[:10])
        st.subheader("📘 Example Questions")
        st.write(generate_quiz(topic, "Short"))

elif menu == "Document Upload":
    uploaded = st.file_uploader("Upload study material", type=["pdf","docx","txt"])
    if uploaded:
        content = extract_text_from_file(uploaded)
        st.write(content[:1000])

elif menu == "Quiz Generator":
    notes = st.text_area("Paste your notes:")
    if notes:
        st.write(generate_quiz(notes, "MCQ"))

elif menu == "Flashcards":
    notes = st.text_area("Paste notes for flashcards:")
    if notes:
        for card in generate_flashcards(notes):
            st.write(f"🃏 **{card['front']}** → {card['back']}")

elif menu == "Math Solver":
    expr = st.text_input("Enter math expression (e.g., sin(x)^2 + cos(x)^2):")
    if expr:
        results = solve_math(expr)
        st.json(results)

elif menu == "Graph Generator":
    expr = st.text_input("Enter function in x (e.g., sin(x)):")
    if expr:
        plot_function(expr)

elif menu == "3D Diagram Generator":
    expr = st.text_input("Enter function in x,y (e.g., sin(x)*cos(y)):")
    if expr:
        plot_3d(expr)

elif menu == "Research Assistant":
    topic = st.text_input("Enter research topic:")
    if topic:
        results = research_assistant(topic)
        for r in results:
            st.write("🔗", r)

# ---------------------------
# SHOW CHAT HISTORY
# ---------------------------
st.sidebar.subheader("💬 Chat History")
for chat in st.session_state.chat_history:
    st.sidebar.write(f"**{chat['role']}**: {chat['text']}")
