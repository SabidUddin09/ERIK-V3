import streamlit as st
import sympy as sp
from sympy.integrals.manualintegrate import integral_steps
import matplotlib.pyplot as plt
import numpy as np
from scholarly import scholarly

# ------------------------------
# APP CONFIG
# ------------------------------
st.set_page_config(page_title="ERIK", layout="wide")
st.title("🤖 ERIK: Exceptional Resources & Intelligence Kernel")
st.caption("Developed by **Sabid Uddin Nahian**")

# ------------------------------
# MATH SOLVER
# ------------------------------
st.header("📐 Math Solver (Step-by-Step with LaTeX)")

expr_input = st.text_input("Enter a math expression (e.g. integrate(sin(x), x), solve(x**2-4, x)):")

if expr_input:
    try:
        x = sp.Symbol('x')
        expr = sp.sympify(expr_input)
        result = None
        steps = None

        # Detect type of operation
        if "integrate" in expr_input:
            integrand = expr.args[0]
            var = expr.args[1]
            steps = integral_steps(integrand, var)
            result = sp.integrate(integrand, var)
        elif "diff" in expr_input or "derivative" in expr_input:
            result = sp.diff(expr)
        elif "limit" in expr_input:
            result = sp.limit(*expr.args)
        elif "solve" in expr_input:
            result = sp.solve(expr.args[0], expr.args[1])
        else:
            result = expr

        st.latex(sp.latex(result))

        if steps:
            st.write("**Step-by-step integration:**")
            st.text(str(steps))

    except Exception as e:
        st.error(f"Error: {e}")

# ------------------------------
# PLOTTER
# ------------------------------
st.header("📊 Function Plotter")

func_input = st.text_input("Enter function to plot (e.g. sin(x), x**2, exp(x)):")

if func_input:
    try:
        x = sp.Symbol('x')
        func = sp.lambdify(x, sp.sympify(func_input), 'numpy')
        X = np.linspace(-10, 10, 400)
        Y = func(X)

        fig, ax = plt.subplots()
        ax.plot(X, Y)
        ax.set_title(f"y = {func_input}")
        st.pyplot(fig)

    except Exception as e:
        st.error(f"Plotting error: {e}")

# ------------------------------
# RESEARCH ASSISTANT (Google Scholar)
# ------------------------------
st.header("🔎 Research Assistant (Google Scholar)")

query = st.text_input("Enter a research topic (e.g. quantum computing):")

if query:
    try:
        search_query = scholarly.search_pubs(query)
        st.write("### Top 3 Results from Google Scholar:")
        for i in range(3):
            pub = next(search_query)
            st.markdown(f"**{pub['bib']['title']}**")
            st.write(f"Authors: {pub['bib'].get('author','N/A')}")
            st.write(f"Year: {pub['bib'].get('pub_year','N/A')}")
            st.write(f"Abstract: {pub['bib'].get('abstract','No abstract available')}")
            if 'eprint_url' in pub:
                st.write(f"[Read Paper]({pub['eprint_url']})")
            st.markdown("---")
    except Exception as e:
        st.error(f"Google Scholar error: {e}")

# ------------------------------
# FOOTER
# ------------------------------
st.markdown("<hr>", unsafe_allow_html=True)
st.caption("🚀 Developed by **Sabid Uddin Nahian**")
