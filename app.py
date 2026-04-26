# # import streamlit as st
# # from lexer import tokenize
# # from parser_ast import Parser
# # from icg import generate_code
# # from optimizer import optimize
# # from visualize_ast import visualize
# # from Symbol_table import add_symbol, print_symbol_table, symbol_table
# # import os

# # st.title("Mini Compiler with Optimization & AST Visualization")

# # uploaded_file = st.file_uploader("Upload .txt or .java file", type=["txt", "java"])

# # if uploaded_file is not None:

# #     code = uploaded_file.read().decode("utf-8")

# #     st.subheader("📄 Source Code")
# #     st.code(code)

# #     lines = code.split("\n")

# #     all_outputs = []

# #     for line in lines:
# #         line = line.strip()

# #         if not line:
# #             continue

# #         # Handle variable declaration
# #         if line.startswith("int"):
# #             parts = line.replace(";", "").split()
# #             if len(parts) >= 2:
# #                 add_symbol(parts[1], "int")

# #         # Handle expressions
# #         if "=" in line:
# #             expr = line.split("=")[1]
# #             expr = expr.replace(";", "").strip()

# #             st.subheader(f"⚙️ Processing: {expr}")

# #             tokens = tokenize(expr)
# #             st.write("🔹 Tokens:", tokens)

# #             parser = Parser(tokens)
# #             ast = parser.parse()

# #             # Save AST image
# #             visualize(ast)

# #             if os.path.exists("ast_tree.png"):
# #                 st.image("ast_tree.png")

# #             intermediate_code = []
# #             generate_code(ast, intermediate_code)

# #             st.write("🔹 Intermediate Code:")
# #             for line in intermediate_code:
# #                 st.code(line)

# #             optimized = optimize(intermediate_code)

# #             st.write("🔹 Optimized Code:")
# #             for line in optimized:
# #                 st.code(line)

# #     st.subheader(" Symbol Table")
# #     st.write(symbol_table)



# """
# Mini Compiler — Streamlit GUI (Improved)
# ----------------------------------------
# A polished Streamlit interface for the mini compiler pipeline:
#   Source ➜ Lexer ➜ Parser/AST ➜ Intermediate Code ➜ Optimizer ➜ Symbol Table

# Drop-in replacement for the original app.py. Keeps the same imports
# (lexer, parser_ast, icg, optimizer, visualize_ast, Symbol_table) so it
# plugs into your existing project unchanged.

# Run:
#     streamlit run app.py
# """

# import os
# import io
# import time
# import contextlib
# import streamlit as st

# from lexer import tokenize
# from parser_ast import Parser
# from icg import generate_code
# from optimizer import optimize
# from visualize_ast import visualize
# from Symbol_table import add_symbol, print_symbol_table, symbol_table


# # ---------------------------------------------------------------------------
# # Page config & global styles
# # ---------------------------------------------------------------------------
# st.set_page_config(
#     page_title="Mini Compiler Studio",
#     page_icon="🛠️",
#     layout="wide",
#     initial_sidebar_state="expanded",
# )

# CUSTOM_CSS = """
# <style>
#     /* Hide default Streamlit chrome for a cleaner look */
#     #MainMenu {visibility: hidden;}
#     footer {visibility: hidden;}

#     /* Hero header */
#     .hero {
#         background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 50%, #ec4899 100%);
#         padding: 1.75rem 2rem;
#         border-radius: 16px;
#         color: white;
#         margin-bottom: 1.5rem;
#         box-shadow: 0 10px 30px -10px rgba(79, 70, 229, 0.45);
#     }
#     .hero h1 {
#         margin: 0;
#         font-size: 1.9rem;
#         font-weight: 700;
#         letter-spacing: -0.02em;
#     }
#     .hero p {
#         margin: 0.35rem 0 0 0;
#         opacity: 0.92;
#         font-size: 0.98rem;
#     }

#     /* Stat cards */
#     .stat-card {
#         background: white;
#         border: 1px solid #e5e7eb;
#         border-radius: 12px;
#         padding: 1rem 1.1rem;
#         box-shadow: 0 1px 2px rgba(0,0,0,0.04);
#     }
#     .stat-card .label {
#         font-size: 0.78rem;
#         text-transform: uppercase;
#         letter-spacing: 0.06em;
#         color: #6b7280;
#         font-weight: 600;
#     }
#     .stat-card .value {
#         font-size: 1.6rem;
#         font-weight: 700;
#         color: #111827;
#         margin-top: 0.15rem;
#     }
#     .stat-card .delta {
#         font-size: 0.8rem;
#         color: #10b981;
#         margin-top: 0.1rem;
#     }

#     /* Step pill */
#     .step-pill {
#         display: inline-block;
#         padding: 0.25rem 0.7rem;
#         border-radius: 999px;
#         background: #eef2ff;
#         color: #4338ca;
#         font-size: 0.78rem;
#         font-weight: 600;
#         margin-bottom: 0.5rem;
#     }

#     /* Section card */
#     .section-card {
#         background: white;
#         border: 1px solid #e5e7eb;
#         border-radius: 14px;
#         padding: 1.25rem 1.4rem;
#         margin-bottom: 1rem;
#     }

#     /* Code blocks slightly darker */
#     .stCodeBlock, pre {
#         border-radius: 10px !important;
#     }

#     /* Sidebar polish */
#     section[data-testid="stSidebar"] {
#         background: #f9fafb;
#         border-right: 1px solid #e5e7eb;
#     }
# </style>
# """
# st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# # ---------------------------------------------------------------------------
# # Helpers
# # ---------------------------------------------------------------------------
# SAMPLE_CODE = """int a;
# int b;
# int c;
# a = 5 + 3 * 2;
# b = a + 10;
# c = b * 0 + a;
# """


# def stat_card(label: str, value, delta: str | None = None):
#     delta_html = f'<div class="delta">{delta}</div>' if delta else ""
#     st.markdown(
#         f"""
#         <div class="stat-card">
#             <div class="label">{label}</div>
#             <div class="value">{value}</div>
#             {delta_html}
#         </div>
#         """,
#         unsafe_allow_html=True,
#     )


# def parse_lines(code: str):
#     """Yield non-empty, stripped lines."""
#     for raw in code.split("\n"):
#         line = raw.strip()
#         if line:
#             yield line


# def capture_symbol_table_text() -> str:
#     buf = io.StringIO()
#     with contextlib.redirect_stdout(buf):
#         try:
#             print_symbol_table()
#         except Exception as e:  # pragma: no cover
#             print(f"<error printing symbol table: {e}>")
#     return buf.getvalue().strip() or "(empty)"


# def reset_symbol_table():
#     """Best-effort reset of the shared symbol table between runs."""
#     try:
#         if isinstance(symbol_table, dict):
#             symbol_table.clear()
#         elif isinstance(symbol_table, list):
#             del symbol_table[:]
#     except Exception:
#         pass


# # ---------------------------------------------------------------------------
# # Sidebar — controls
# # ---------------------------------------------------------------------------
# with st.sidebar:
#     st.markdown("### ⚙️ Compiler Controls")

#     input_mode = st.radio(
#         "Input mode",
#         ["Upload file", "Paste code", "Use sample"],
#         index=2,
#         help="Choose how you'd like to provide source code.",
#     )

#     st.markdown("---")
#     st.markdown("### 🧪 Pipeline stages")
#     show_tokens = st.checkbox("Show tokens", value=True)
#     show_ast = st.checkbox("Show AST diagram", value=True)
#     show_icg = st.checkbox("Show intermediate code", value=True)
#     show_opt = st.checkbox("Show optimized code", value=True)
#     show_symbols = st.checkbox("Show symbol table", value=True)

#     st.markdown("---")
#     st.markdown("### ℹ️ About")
#     st.caption(
#         "A teaching mini-compiler: lexical analysis, parsing, AST "
#         "visualization, intermediate code generation and optimization."
#     )


# # ---------------------------------------------------------------------------
# # Hero header
# # ---------------------------------------------------------------------------
# st.markdown(
#     """
#     <div class="hero">
#         <h1>🛠️ Mini Compiler Studio</h1>
#         <p>Lex • Parse • Visualize • Generate IR • Optimize — all in one place.</p>
#     </div>
#     """,
#     unsafe_allow_html=True,
# )


# # ---------------------------------------------------------------------------
# # Source acquisition
# # ---------------------------------------------------------------------------
# code: str | None = None

# if input_mode == "Upload file":
#     uploaded_file = st.file_uploader(
#         "Upload a `.txt` or `.java` source file",
#         type=["txt", "java"],
#         help="Each statement on its own line. Supports `int x;` declarations and `x = expr;` assignments.",
#     )
#     if uploaded_file is not None:
#         code = uploaded_file.read().decode("utf-8")

# elif input_mode == "Paste code":
#     code = st.text_area(
#         "Paste your source code",
#         value=SAMPLE_CODE,
#         height=200,
#         help="Edit freely — the compiler will run when you click ▶ Compile.",
#     )

# else:  # Use sample
#     code = SAMPLE_CODE
#     with st.expander("📄 Sample source (click to view)", expanded=False):
#         st.code(code, language="java")

# run = st.button("▶  Compile", type="primary", use_container_width=True)


# # ---------------------------------------------------------------------------
# # Compile pipeline
# # ---------------------------------------------------------------------------
# if run and code:
#     reset_symbol_table()

#     statements = list(parse_lines(code))
#     declarations = [s for s in statements if s.startswith("int")]
#     expressions = [s for s in statements if "=" in s and not s.startswith("int")]
#     # Some lines are both declaration + assignment (e.g. "int a = 5;"); count once below.
#     decl_and_assign = [s for s in statements if s.startswith("int") and "=" in s]

#     # Top-of-page summary stats
#     st.markdown("### 📊 Pipeline summary")
#     c1, c2, c3, c4 = st.columns(4)
#     with c1:
#         stat_card("Statements", len(statements))
#     with c2:
#         stat_card("Declarations", len(declarations))
#     with c3:
#         stat_card("Expressions", len(expressions) + len(decl_and_assign))
#     with c4:
#         stat_card("Symbols", len(symbol_table) if hasattr(symbol_table, "__len__") else "—")

#     st.markdown("")

#     # Source preview
#     with st.expander("📄 Source code", expanded=True):
#         st.code(code, language="java")

#     # Process declarations first (so symbol table is populated)
#     for line in statements:
#         if line.startswith("int"):
#             parts = line.replace(";", "").split()
#             if len(parts) >= 2:
#                 # Strip any trailing assignment from the declared name
#                 name = parts[1].split("=")[0].strip()
#                 if name:
#                     add_symbol(name, "int")

#     # Process expressions with a progress bar + per-step UI
#     expr_lines = [s for s in statements if "=" in s]
#     progress = st.progress(0.0, text="Compiling…")
#     total = max(len(expr_lines), 1)

#     for idx, line in enumerate(expr_lines, start=1):
#         rhs = line.split("=", 1)[1].replace(";", "").strip()
#         lhs = line.split("=", 1)[0].replace("int", "").strip()

#         st.markdown(
#             f"""
#             <div class="section-card">
#                 <span class="step-pill">Statement {idx} of {len(expr_lines)}</span>
#                 <h4 style="margin:0.2rem 0 0.6rem 0;">⚙️ <code>{lhs} = {rhs}</code></h4>
#             </div>
#             """,
#             unsafe_allow_html=True,
#         )

#         tabs_labels = []
#         if show_tokens: tabs_labels.append("🔤 Tokens")
#         if show_ast: tabs_labels.append("🌳 AST")
#         if show_icg: tabs_labels.append("📜 Intermediate")
#         if show_opt: tabs_labels.append("✨ Optimized")

#         if not tabs_labels:
#             st.info("Enable at least one stage from the sidebar to see output.")
#         else:
#             tabs = st.tabs(tabs_labels)
#             tab_iter = iter(tabs)

#             tokens = tokenize(rhs)
#             parser = Parser(tokens)
#             ast = parser.parse()

#             intermediate_code: list[str] = []
#             generate_code(ast, intermediate_code)
#             optimized = optimize(intermediate_code)

#             if show_tokens:
#                 with next(tab_iter):
#                     st.caption("Lexical analysis output")
#                     if isinstance(tokens, (list, tuple)):
#                         # Render tokens as a clean table when possible
#                         try:
#                             rows = []
#                             for t in tokens:
#                                 if isinstance(t, (list, tuple)) and len(t) >= 2:
#                                     rows.append({"type": str(t[0]), "value": str(t[1])})
#                                 else:
#                                     rows.append({"token": str(t)})
#                             st.table(rows)
#                         except Exception:
#                             st.write(tokens)
#                     else:
#                         st.write(tokens)

#             if show_ast:
#                 with next(tab_iter):
#                     st.caption("Abstract Syntax Tree")
#                     try:
#                         visualize(ast)
#                         if os.path.exists("ast_tree.png"):
#                             st.image("ast_tree.png", use_column_width=True)
#                         else:
#                             st.warning("AST image was not generated.")
#                     except Exception as e:
#                         st.error(f"Could not render AST: {e}")

#             if show_icg:
#                 with next(tab_iter):
#                     st.caption(f"Three-address code · {len(intermediate_code)} instruction(s)")
#                     st.code("\n".join(intermediate_code) or "(none)", language="text")

#             if show_opt:
#                 with next(tab_iter):
#                     saved = max(len(intermediate_code) - len(optimized), 0)
#                     st.caption(
#                         f"After optimization · {len(optimized)} instruction(s) "
#                         f"· {saved} removed"
#                     )
#                     st.code("\n".join(optimized) or "(none)", language="text")

#         progress.progress(idx / total, text=f"Compiled {idx} / {total}")
#         time.sleep(0.05)  # tiny pause so the progress bar feels alive

#     progress.empty()

#     # Symbol table
#     if show_symbols:
#         st.markdown("### 🗂️ Symbol Table")
#         col_a, col_b = st.columns([1, 1])
#         with col_a:
#             st.markdown("**Structured view**")
#             try:
#                 if isinstance(symbol_table, dict):
#                     rows = [{"name": k, **(v if isinstance(v, dict) else {"type": v})}
#                             for k, v in symbol_table.items()]
#                     st.table(rows or [{"name": "(empty)"}])
#                 elif isinstance(symbol_table, list):
#                     st.table(symbol_table or [{"value": "(empty)"}])
#                 else:
#                     st.write(symbol_table)
#             except Exception as e:
#                 st.error(f"Could not render symbol table: {e}")
#                 st.write(symbol_table)
#         with col_b:
#             st.markdown("**Raw output**")
#             st.code(capture_symbol_table_text(), language="text")

#     st.success("✅ Compilation finished.")

# elif run and not code:
#     st.warning("Please provide some source code first.")

# else:
#     # Idle state — show a friendly hint
#     st.info(
#         "👈 Choose an input mode in the sidebar, then click **▶ Compile** "
#         "to run the full lexer → parser → IR → optimizer pipeline."
#     )



import os
import io
import time
import contextlib
import streamlit as st

from lexer import tokenize
from parser_ast import Parser
from icg import generate_code
from optimizer import optimize
from visualize_ast import visualize
from Symbol_table import add_symbol, print_symbol_table, symbol_table


# ---------------------------------------------------------------------------
# Page config & global styles
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Mini Compiler Studio",
    page_icon="🛠️",
    layout="wide",
    initial_sidebar_state="expanded",
)

CUSTOM_CSS = """
<style>
    /* Hide default Streamlit chrome for a cleaner look */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Hero header */
    .hero {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 50%, #ec4899 100%);
        padding: 1.75rem 2rem;
        border-radius: 16px;
        color: white;
        margin-bottom: 1.5rem;
        box-shadow: 0 10px 30px -10px rgba(79, 70, 229, 0.45);
    }
    .hero h1 {
        margin: 0;
        font-size: 1.9rem;
        font-weight: 700;
        letter-spacing: -0.02em;
    }
    .hero p {
        margin: 0.35rem 0 0 0;
        opacity: 0.92;
        font-size: 0.98rem;
    }

    /* Stat cards */
    .stat-card {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
        padding: 1rem 1.1rem;
        box-shadow: 0 1px 2px rgba(0,0,0,0.04);
    }
    .stat-card .label {
        font-size: 0.78rem;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: #6b7280;
        font-weight: 600;
    }
    .stat-card .value {
        font-size: 1.6rem;
        font-weight: 700;
        color: #111827;
        margin-top: 0.15rem;
    }
    .stat-card .delta {
        font-size: 0.8rem;
        color: #10b981;
        margin-top: 0.1rem;
    }

    /* Step pill */
    .step-pill {
        display: inline-block;
        padding: 0.25rem 0.7rem;
        border-radius: 999px;
        background: #eef2ff;
        color: #4338ca;
        font-size: 0.78rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }

    /* Section card */
    .section-card {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 14px;
        padding: 1.25rem 1.4rem;
        margin-bottom: 1rem;
    }

    /* Code blocks slightly darker */
    .stCodeBlock, pre {
        border-radius: 10px !important;
    }

    /* Sidebar — dark background with light text for visibility */
    section[data-testid="stSidebar"] {
        background: #1f2937 !important;
        border-right: 1px solid #374151;
    }
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] h4,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] div,
    section[data-testid="stSidebar"] li,
    section[data-testid="stSidebar"] .stMarkdown {
        color: #f9fafb !important;
    }
    /* Inputs keep light bg + dark text so typed values are legible */
    section[data-testid="stSidebar"] input,
    section[data-testid="stSidebar"] textarea,
    section[data-testid="stSidebar"] select {
        background: #ffffff !important;
        color: #111827 !important;
    }
    section[data-testid="stSidebar"] .stButton > button {
        background: #4f46e5 !important;
        color: #ffffff !important;
        border: none !important;
    }
    section[data-testid="stSidebar"] .stButton > button:hover {
        background: #4338ca !important;
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
SAMPLE_CODE = """int a;
int b;
int c;
a = 5 + 3 * 2;
b = a + 10;
c = b * 0 + a;
"""


def stat_card(label: str, value, delta: str | None = None):
    delta_html = f'<div class="delta">{delta}</div>' if delta else ""
    st.markdown(
        f"""
        <div class="stat-card">
            <div class="label">{label}</div>
            <div class="value">{value}</div>
            {delta_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def parse_lines(code: str):
    """Yield non-empty, stripped lines."""
    for raw in code.split("\n"):
        line = raw.strip()
        if line:
            yield line


def capture_symbol_table_text() -> str:
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        try:
            print_symbol_table()
        except Exception as e:  # pragma: no cover
            print(f"<error printing symbol table: {e}>")
    return buf.getvalue().strip() or "(empty)"


def reset_symbol_table():
    """Best-effort reset of the shared symbol table between runs."""
    try:
        if isinstance(symbol_table, dict):
            symbol_table.clear()
        elif isinstance(symbol_table, list):
            del symbol_table[:]
    except Exception:
        pass


# ---------------------------------------------------------------------------
# Sidebar — controls
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("###  Compiler Controls")

    input_mode = st.radio(
        "Input mode",
        ["Upload file", "Paste code", "Use sample"],
        index=2,
        help="Choose how you'd like to provide source code.",
    )

    st.markdown("---")
    st.markdown("###  Pipeline stages")
    show_tokens = st.checkbox("Show tokens", value=True)
    show_ast = st.checkbox("Show AST diagram", value=True)
    show_icg = st.checkbox("Show intermediate code", value=True)
    show_opt = st.checkbox("Show optimized code", value=True)
    show_symbols = st.checkbox("Show symbol table", value=True)

    st.markdown("---")
    st.markdown("### ℹ️ About")
    st.caption(
        "A teaching mini-compiler: lexical analysis, parsing, AST "
        "visualization, intermediate code generation and optimization."
    )


# ---------------------------------------------------------------------------
# Hero header
# ---------------------------------------------------------------------------
st.markdown(
    """
    <div class="hero">
        <h1> Mini Compiler Studio</h1>
        <p>Lex • Parse • Visualize • Generate IR • Optimize — all in one place.</p>
    </div>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------------------
# Source acquisition
# ---------------------------------------------------------------------------
code: str | None = None

if input_mode == "Upload file":
    uploaded_file = st.file_uploader(
        "Upload a `.txt` or `.java` source file",
        type=["txt", "java"],
        help="Each statement on its own line. Supports `int x;` declarations and `x = expr;` assignments.",
    )
    if uploaded_file is not None:
        code = uploaded_file.read().decode("utf-8")

elif input_mode == "Paste code":
    code = st.text_area(
        "Paste your source code",
        value=SAMPLE_CODE,
        height=200,
        help="Edit freely — the compiler will run when you click ▶ Compile.",
    )

else:  # Use sample
    code = SAMPLE_CODE
    with st.expander(" Sample source (click to view)", expanded=False):
        st.code(code, language="java")

run = st.button("  Compile", type="primary", use_container_width=True)


# ---------------------------------------------------------------------------
# Compile pipeline
# ---------------------------------------------------------------------------
if run and code:
    reset_symbol_table()

    statements = list(parse_lines(code))
    declarations = [s for s in statements if s.startswith("int")]
    expressions = [s for s in statements if "=" in s and not s.startswith("int")]
    # Some lines are both declaration + assignment (e.g. "int a = 5;"); count once below.
    decl_and_assign = [s for s in statements if s.startswith("int") and "=" in s]

    # Top-of-page summary stats
    st.markdown("###  Pipeline summary")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        stat_card("Statements", len(statements))
    with c2:
        stat_card("Declarations", len(declarations))
    with c3:
        stat_card("Expressions", len(expressions) + len(decl_and_assign))
    with c4:
        stat_card("Symbols", len(symbol_table) if hasattr(symbol_table, "__len__") else "—")

    st.markdown("")

    # Source preview
    with st.expander(" Source code", expanded=True):
        st.code(code, language="java")

    # Process declarations first (so symbol table is populated)
    for line in statements:
        if line.startswith("int"):
            parts = line.replace(";", "").split()
            if len(parts) >= 2:
                # Strip any trailing assignment from the declared name
                name = parts[1].split("=")[0].strip()
                if name:
                    add_symbol(name, "int")

    # Process expressions with a progress bar + per-step UI
    expr_lines = [s for s in statements if "=" in s]
    progress = st.progress(0.0, text="Compiling…")
    total = max(len(expr_lines), 1)

    for idx, line in enumerate(expr_lines, start=1):
        rhs = line.split("=", 1)[1].replace(";", "").strip()
        lhs = line.split("=", 1)[0].replace("int", "").strip()

        st.markdown(
            f"""
            <div class="section-card">
                <span class="step-pill">Statement {idx} of {len(expr_lines)}</span>
                <h4 style="margin:0.2rem 0 0.6rem 0;">⚙️ <code>{lhs} = {rhs}</code></h4>
            </div>
            """,
            unsafe_allow_html=True,
        )

        tabs_labels = []
        if show_tokens: tabs_labels.append(" Tokens")
        if show_ast: tabs_labels.append(" AST")
        if show_icg: tabs_labels.append(" Intermediate")
        if show_opt: tabs_labels.append(" Optimized")

        if not tabs_labels:
            st.info("Enable at least one stage from the sidebar to see output.")
        else:
            tabs = st.tabs(tabs_labels)
            tab_iter = iter(tabs)

            tokens = tokenize(rhs)
            full_stmt = f"{lhs} = {rhs};"

            parser = Parser(tokens)
            ast = parser.parse()

            intermediate_code: list[str] = []
            generate_code(ast, intermediate_code)
            optimized = optimize(intermediate_code)

            if show_tokens:
                with next(tab_iter):
                    st.caption(f"Lexical analysis output for: `{full_stmt}`")

                    import re

                    SYMBOL_NAMES = {
                        "+": "PLUS", "-": "MINUS", "*": "MULTIPLY", "/": "DIVIDE",
                        "%": "MODULO", "=": "ASSIGN", "==": "EQUAL", "!=": "NOT_EQUAL",
                        "<": "LESS", ">": "GREATER", "<=": "LESS_EQUAL", ">=": "GREATER_EQUAL",
                        "&&": "AND", "||": "OR", "!": "NOT",
                        "(": "LPAREN", ")": "RPAREN", "{": "LBRACE", "}": "RBRACE",
                        "[": "LBRACKET", "]": "RBRACKET",
                        ";": "SEMICOLON", ",": "COMMA", ".": "DOT",
                    }
                    KEYWORDS = {"int", "float", "char", "double", "if", "else",
                                "while", "for", "return", "void", "bool", "true", "false"}

                    # Robust regex-based tokenizer that always splits multi-char
                    # operators, single-char operators, numbers, identifiers and
                    # punctuation into distinct tokens.
                    TOKEN_RE = re.compile(
                        r"\s*(?:"
                        r"(==|!=|<=|>=|&&|\|\|)"          # 1: multi-char operators
                        r"|(\d+\.\d+|\d+)"                 # 2: numbers
                        r"|([A-Za-z_][A-Za-z0-9_]*)"       # 3: identifiers / keywords
                        r"|([+\-*/%=<>!(){}\[\];,.])"      # 4: single-char operators / punct
                        r"|(\S)"                           # 5: anything else
                        r")"
                    )

                    def classify(value: str) -> str:
                        v = str(value).strip()
                        if v in SYMBOL_NAMES:
                            return SYMBOL_NAMES[v]
                        if v in KEYWORDS:
                            return "KEYWORD"
                        if re.fullmatch(r"\d+\.\d+", v):
                            return "FLOAT"
                        if v.isdigit():
                            return "NUMBER"
                        if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", v):
                            return "IDENTIFIER"
                        return "SYMBOL"

                    rows = []
                    for i, m in enumerate(TOKEN_RE.finditer(full_stmt), start=1):
                        val = next(g for g in m.groups() if g is not None)
                        rows.append({"#": i, "Type": classify(val), "Value": val})

                    if rows:
                        st.table(rows)
                    else:
                        st.info("No tokens produced.")


            if show_ast:
                with next(tab_iter):
                    st.caption("Abstract Syntax Tree")
                    try:
                        visualize(ast)
                        if os.path.exists("ast_tree.png"):
                            st.image("ast_tree.png", use_column_width=True)
                        else:
                            st.warning("AST image was not generated.")
                    except Exception as e:
                        st.error(f"Could not render AST: {e}")

            if show_icg:
                with next(tab_iter):
                    st.caption(f"Three-address code · {len(intermediate_code)} instruction(s)")
                    st.code("\n".join(intermediate_code) or "(none)", language="text")

            if show_opt:
                with next(tab_iter):
                    saved = max(len(intermediate_code) - len(optimized), 0)
                    st.caption(
                        f"After optimization · {len(optimized)} instruction(s) "
                        f"· {saved} removed"
                    )
                    st.code("\n".join(optimized) or "(none)", language="text")

        progress.progress(idx / total, text=f"Compiled {idx} / {total}")
        time.sleep(0.05)  # tiny pause so the progress bar feels alive

    progress.empty()

    # Symbol table
    if show_symbols:
        st.markdown("###  Symbol Table")
        col_a, col_b = st.columns([1, 1])
        with col_a:
            st.markdown("**Structured view**")
            try:
                if isinstance(symbol_table, dict):
                    rows = [{"name": k, **(v if isinstance(v, dict) else {"type": v})}
                            for k, v in symbol_table.items()]
                    st.table(rows or [{"name": "(empty)"}])
                elif isinstance(symbol_table, list):
                    st.table(symbol_table or [{"value": "(empty)"}])
                else:
                    st.write(symbol_table)
            except Exception as e:
                st.error(f"Could not render symbol table: {e}")
                st.write(symbol_table)
        with col_b:
            st.markdown("**Raw output**")
            st.code(capture_symbol_table_text(), language="text")

    st.success(" Compilation finished.")

elif run and not code:
    st.warning("Please provide some source code first.")

else:
    # Idle state — show a friendly hint
    st.info(
        " Choose an input mode in the sidebar, then click **▶ Compile** "
        "to run the full lexer → parser → IR → optimizer pipeline."
    )
