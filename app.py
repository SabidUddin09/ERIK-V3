import streamlit as st
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import PyPDF2
import docx
import os
from scholarly import scholarly
from googlesearch import search
from googletrans import Translator
import random

# ------------------------------
# APP CONFIG
# ------------------------------
st.set_page_config(page_title="ERIK", layout="wide")
st.title("🤖 ERIK: Exceptional Resources & Intelligence Kernel")
st.caption("🚀 Developed by **Sabid Uddin Nahian**")

if "history" not in st.session_state:
    st.session_state.history = []

translator = Translator()

# ------------------------------
# CHAT HISTORY
# ------------------------------
st.sidebar.header("💬 Chat History")
for i, msg in enumerate(st.session_state.history):
    st.sidebar.write(f"**Q{i+1}:** {msg['q']}")
    st.sidebar.write(f"**A:** {msg['a']}")
    st.sidebar.markdown("---")

# ------------------------------
# DOUBT SOLVER (GOOGLE-BASED)
# ------------------------------
st.header("❓ Doubt Solver (Google Search)")
query = st.text_input("Ask a question (Bangla/English):")

if query:
    try:
        translated = translator.translate(query, dest="en").text
        st.write(f"🔎 Searching for: **{translated}**")

        results = list(search(translated, num=3, stop=3))
        for r in results:
            st.write(f"[Result]({r})")
        
        st.session_state.history.append({"q": query, "a": results})
    except Exception as e:
        st.error(f"Search error: {e}")

# ------------------------------
# TOPIC ANALYZER
# ------------------------------
st.header("📘 Topic Analyzer")
topic_text = st.text_area("Enter text or topic:")

if topic_text:
    translated_text = translator.translate(topic_text, dest="en").text
    words = translated_text.split()
    summary = " ".join(words[:50]) + "..." if len(words) > 50 else translated_text
    keywords = list(set([w for w in words if len(w) > 5]))[:8]

    st.subheader("Summary:")
    st.write(summary)
    st.subheader("Keywords:")
    st.write(", ".join(keywords))

# ------------------------------
# DOCUMENT UPLOAD
# ------------------------------
st.header("📂 Document Upload & Analysis")
uploaded = st.file_uploader("Upload PDF, DOCX, or TXT", type=["pdf", "docx", "txt"])

if uploaded:
    text = ""
    if uploaded.type == "application/pdf":
        reader = PyPDF2.PdfReader(uploaded)
        for page in reader.pages:
            text += page.extract_text()
    elif uploaded.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = docx.Document(uploaded)
        for para in doc.paragraphs:
            text += para.text + "\n"
    elif uploaded.type == "text/plain":
        text = uploaded.read().decode("utf-8")

    st.subheader("Extracted Text:")
    st.write(text[:500] + "...")

# ------------------------------
# QUIZ GENERATOR
# ------------------------------
st.header("📝 Quiz Generator")
quiz_topic = st.text_input("Enter topic for quiz:")

if quiz_topic:
    st.subheader("MCQ:")
    st.write(f"1. What is {quiz_topic}?")
    st.radio("Options:", ["A", "B", "C", "D"])
    st.subheader("Short Question:")
    st.write(f"Explain {quiz_topic} in 3 sentences.")
    st.subheader("Long Question:")
    st.write(f"Discuss {quiz_topic} in detail.")

# ------------------------------
# FLASHCARDS
# ------------------------------
st.header("🎴 Flashcards")
flash_topic = st.text_input("Enter topic for flashcards:")

if flash_topic:
    st.write(f"**Front:** Define {flash_topic}")
    st.write(f"**Back:** {flash_topic} is ...")

# ------------------------------
# QUICKMATH SOLVER
# ------------------------------
st.header("📐 QuickMath Solver (Step-by-Step)")
expr_input = st.text_input("Enter math expression (e.g. integrate(sin(x), x)): ")

if expr_input:
    try:
        x, y, z = sp.symbols("x y z")
        expr = sp.sympify(expr_input)
        result = sp.simplify(expr)
        st.latex(sp.latex(result))
        st.session_state.history.append({"q": expr_input, "a": str(result)})
    except Exception as e:
        st.error(f"Math error: {e}")

# ------------------------------
# 2D GRAPH GENERATOR
# ------------------------------
st.header("📊 Graph Generator (2D)")
func_input = st.text_input("Enter function f(x):")

if func_input:
    try:
        x = sp.Symbol("x")
        func = sp.lambdify(x, sp.sympify(func_input), "numpy")
        X = np.linspace(-10, 10, 400)
        Y = func(X)

        fig, ax = plt.subplots()
        ax.plot(X, Y)
        st.pyplot(fig)
    except Exception as e:
        st.error(f"Plot error: {e}")

# ------------------------------
# 3D DIAGRAM GENERATOR
# ------------------------------
st.header("🌐 3D Diagram Generator")
f3d_input = st.text_input("Enter function f(x, y):")

if f3d_input:
    try:
        x, y = sp.symbols("x y")
        func = sp.lambdify((x, y), sp.sympify(f3d_input), "numpy")
        X = np.linspace(-5, 5, 50)
        Y = np.linspace(-5, 5, 50)
        X, Y = np.meshgrid(X, Y)
        Z = func(X, Y)

        fig = plt.figure()
        ax = fig.add_subplot(111, projection="3d")
        ax.plot_surface(X, Y, Z, cmap="viridis")
        st.pyplot(fig)
    except Exception as e:
        st.error(f"3D plot error: {e}")

# ------------------------------
# FOOTER
# ------------------------------
st.markdown("<hr>", unsafe_allow_html=True)
st.caption("🚀 Developed by **Sabid Uddin Nahian**")
