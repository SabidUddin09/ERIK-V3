import streamlit as st
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import PyPDF2
import docx
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

translator = Translator()

# ------------------------------
# SESSION STATE FOR CHAT HISTORY
# ------------------------------
if "history" not in st.session_state:
    st.session_state.history = []

def add_history(q, a):
    st.session_state.history.append({"q": q, "a": a})

# ------------------------------
# SIDEBAR CHAT HISTORY
# ------------------------------
st.sidebar.header("💬 Chat History")
for i, msg in enumerate(st.session_state.history):
    st.sidebar.write(f"**Q{i+1}:** {msg['q']}")
    st.sidebar.write(f"**A:** {msg['a']}")
    st.sidebar.markdown("---")

# ------------------------------
# MENU
# ------------------------------
menu = st.sidebar.selectbox("📌 Choose Feature", [
    "Doubt Solver", "Topic Analyzer", "Document Upload",
    "Quiz Generator", "Flashcards", "Math Solver",
    "Graph Generator (2D)", "3D Diagram Generator", "Research Assistant"
])

# ------------------------------
# DOUBT SOLVER
# ------------------------------
if menu == "Doubt Solver":
    st.header("❓ Doubt Solver (Google Search)")
    query = st.text_input("Enter your question (Bangla/English):")
    answer_format = st.selectbox("Answer Format", ["Short (≤75 words)", "Long (≤350 words)"])
    
    if query:
        translated = translator.translate(query, dest="en").text
        st.write(f"🔎 Searching for: **{translated}**")
        try:
            results = list(search(translated, num=3, stop=3))
            final_answer = ""
            for r in results:
                final_answer += r + " "
            # Short vs Long formatting
            if answer_format.startswith("Short"):
                final_answer = " ".join(final_answer.split()[:75])
            else:
                final_answer = " ".join(final_answer.split()[:350])
            st.write(final_answer)
            add_history(query, final_answer)
        except Exception as e:
            st.error(f"Search error: {e}")

# ------------------------------
# TOPIC ANALYZER
# ------------------------------
elif menu == "Topic Analyzer":
    st.header("📘 Topic Analyzer")
    topic_text = st.text_area("Enter topic/text:")
    if topic_text:
        translated_text = translator.translate(topic_text, dest="en").text
        words = translated_text.split()
        summary = " ".join(words[:50]) + "..." if len(words) > 50 else translated_text
        keywords = list(set([w for w in words if len(w) > 5]))[:8]
        st.subheader("Summary:")
        st.write(summary)
        st.subheader("Keywords:")
        st.write(", ".join(keywords))
        st.subheader("Example Questions:")
        for i, kw in enumerate(keywords):
            st.write(f"{i+1}. Explain {kw} in short.")

# ------------------------------
# DOCUMENT UPLOAD
# ------------------------------
elif menu == "Document Upload":
    st.header("📂 Document Upload")
    uploaded = st.file_uploader("Upload PDF, DOCX, TXT", type=["pdf", "docx", "txt"])
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
        st.subheader("Extracted Text (preview):")
        st.write(text[:500] + "...")

# ------------------------------
# QUIZ GENERATOR
# ------------------------------
elif menu == "Quiz Generator":
    st.header("📝 Quiz Generator")
    quiz_topic = st.text_input("Enter topic for quiz:")
    num_q = st.slider("Number of Questions:", 3, 10, 5)
    if quiz_topic:
        st.subheader("MCQs:")
        for i in range(num_q):
            st.write(f"Q{i+1}: Example question on {quiz_topic}?")
            st.radio("Options:", ["A", "B", "C", "D"])
        st.subheader("Short Questions:")
        for i in range(num_q):
            st.write(f"Q{i+1}: Explain {quiz_topic} briefly.")
        st.subheader("Long Questions:")
        for i in range(num_q):
            st.write(f"Q{i+1}: Discuss {quiz_topic} in detail.")

# ------------------------------
# FLASHCARDS
# ------------------------------
elif menu == "Flashcards":
    st.header("🎴 Flashcards")
    flash_topic = st.text_input("Enter topic for flashcards:")
    num_cards = st.slider("Number of flashcards:", 3, 10, 5)
    if flash_topic:
        for i in range(1, num_cards+1):
            st.write(f"**Front:** Concept {i} on {flash_topic}")
            st.write(f"**Back:** Explanation {i} on {flash_topic}")

# ------------------------------
# QUICKMATH SOLVER
# ------------------------------
elif menu == "Math Solver":
    st.header("📐 QuickMath Solver (Step-by-Step)")
    expr_input = st.text_input("Enter math expression (e.g., integrate(sin(x), x)):")
    if expr_input:
        try:
            x, y, z = sp.symbols("x y z")
            expr = sp.sympify(expr_input)
            simplified = sp.simplify(expr)
            derivative = sp.diff(expr)
            integral = sp.integrate(expr)
            st.subheader("Simplified:")
            st.latex(sp.latex(simplified))
            st.subheader("Derivative:")
            st.latex(sp.latex(derivative))
            st.subheader("Integral:")
            st.latex(sp.latex(integral))
            add_history(expr_input, str(simplified))
        except Exception as e:
            st.error(f"Math error: {e}")

# ------------------------------
# 2D GRAPH GENERATOR
# ------------------------------
elif menu == "Graph Generator (2D)":
    st.header("📊 2D Graph Generator")
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
elif menu == "3D Diagram Generator":
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
# RESEARCH ASSISTANT
# ------------------------------
elif menu == "Research Assistant":
    st.header("🔎 Research Assistant (Google Scholar)")
    topic = st.text_input("Enter research topic:")
    answer_format = st.selectbox("Answer Format", ["Short (≤75 words)", "Long (≤350 words)"])
    if topic:
        try:
            search_query = scholarly.search_pubs(topic)
            results_text = ""
            st.write("### Top 3 Papers:")
            for i in range(3):
                pub = next(search_query)
                st.markdown(f"**{pub['bib']['title']}**")
                st.write(f"Authors: {pub['bib'].get('author','N/A')}")
                st.write(f"Year: {pub['bib'].get('pub_year','N/A')}")
                st.write(f"Abstract: {pub['bib'].get('abstract','No abstract')}")
                if 'eprint_url' in pub:
                    st.write(f"[Read Paper]({pub['eprint_url']})")
                results_text += pub['bib'].get('abstract','') + " "
            # Format answer length
            if answer_format.startswith("Short"):
                results_text = " ".join(results_text.split()[:75])
            else:
                results_text = " ".join(results_text.split()[:350])
            add_history(topic, results_text)
        except Exception as e:
            st.error(f"Research error: {e}")

# ------------------------------
# FOOTER
# ------------------------------
st.markdown("<hr>", unsafe_allow_html=True)
st.caption("🚀 Developed by **Sabid Uddin Nahian**")
