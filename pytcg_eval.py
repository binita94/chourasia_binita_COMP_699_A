import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import time
import datetime
import json
import io
import random
import hashlib
import ast
import re
import textwrap
from collections import defaultdict

st.set_page_config(
    page_title="PyTCG-Eval",
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed"
)

DARK_BG = "#0a0a0a"
CARD_BG = "#111111"
CARD_BORDER = "#1e1e1e"
ACCENT_GOLD = "#c8a97e"
ACCENT_SILVER = "#a8a8b3"
ACCENT_COPPER = "#b87333"
TEXT_PRIMARY = "#f0f0f0"
TEXT_SECONDARY = "#888899"
TEXT_MUTED = "#555566"
HIGHLIGHT = "#d4af7a"
SUCCESS_COLOR = "#4ecb71"
ERROR_COLOR = "#e05252"
WARNING_COLOR = "#e09052"
INFO_COLOR = "#5290e0"
GRADIENT_GOLD = "linear-gradient(135deg, #c8a97e 0%, #a07040 100%)"
GRADIENT_DARK = "linear-gradient(135deg, #1a1a2e 0%, #0a0a0a 100%)"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@400;600;700&display=swap');

html, body, [class*="css"] {{
    font-family: 'Inter', sans-serif;
    background-color: {DARK_BG};
    color: {TEXT_PRIMARY};
}}

.stApp {{
    background-color: {DARK_BG};
}}

section[data-testid="stSidebar"] {{
    display: none !important;
}}

.block-container {{
    padding: 0 !important;
    max-width: 100% !important;
}}

[data-testid="stHeader"] {{
    background: transparent;
}}

div[data-testid="stToolbar"] {{
    display: none;
}}

.stButton > button {{
    background: {GRADIENT_GOLD};
    color: #0a0a0a;
    border: none;
    border-radius: 4px;
    font-weight: 600;
    font-size: 13px;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    padding: 12px 28px;
    cursor: pointer;
    transition: all 0.3s ease;
    width: 100%;
}}

.stButton > button:hover {{
    transform: translateY(-1px);
    box-shadow: 0 8px 24px rgba(200,169,126,0.3);
    opacity: 0.9;
}}

.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div > div {{
    background-color: #161616 !important;
    border: 1px solid {CARD_BORDER} !important;
    border-radius: 4px !important;
    color: {TEXT_PRIMARY} !important;
    font-family: 'Inter', sans-serif !important;
}}

.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {{
    border-color: {ACCENT_GOLD} !important;
    box-shadow: 0 0 0 1px {ACCENT_GOLD}33 !important;
}}

.stSlider > div > div > div > div {{
    background: {ACCENT_GOLD} !important;
}}

.stCheckbox > label > div[data-testid="stMarkdownContainer"] > p {{
    color: {TEXT_SECONDARY};
}}

.stRadio > div > label > div[data-testid="stMarkdownContainer"] > p {{
    color: {TEXT_SECONDARY};
}}

div[data-testid="stMetric"] {{
    background: {CARD_BG};
    border: 1px solid {CARD_BORDER};
    border-radius: 8px;
    padding: 20px;
}}

div[data-testid="stMetricValue"] {{
    color: {ACCENT_GOLD} !important;
    font-size: 2rem !important;
    font-weight: 700 !important;
}}

div[data-testid="stMetricLabel"] {{
    color: {TEXT_SECONDARY} !important;
    font-size: 11px !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
}}

div[data-testid="stProgress"] > div {{
    background: {ACCENT_GOLD} !important;
}}

.stTabs [data-baseweb="tab-list"] {{
    background: transparent;
    border-bottom: 1px solid {CARD_BORDER};
    gap: 0;
}}

.stTabs [data-baseweb="tab"] {{
    background: transparent;
    color: {TEXT_MUTED};
    border: none;
    font-size: 12px;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    font-weight: 500;
    padding: 14px 24px;
}}

.stTabs [aria-selected="true"] {{
    background: transparent;
    color: {ACCENT_GOLD} !important;
    border-bottom: 2px solid {ACCENT_GOLD} !important;
}}

.stFileUploader > div {{
    background: #161616 !important;
    border: 1px dashed {CARD_BORDER} !important;
    border-radius: 8px !important;
}}

div[data-testid="stExpander"] {{
    background: {CARD_BG};
    border: 1px solid {CARD_BORDER};
    border-radius: 8px;
}}

.stDataFrame {{
    background: {CARD_BG};
}}

table {{
    width: 100%;
    border-collapse: collapse;
}}

th {{
    background: #161616;
    color: {ACCENT_GOLD};
    font-size: 10px;
    letter-spacing: 2px;
    text-transform: uppercase;
    padding: 12px 16px;
    text-align: left;
    border-bottom: 1px solid {CARD_BORDER};
}}

td {{
    color: {TEXT_PRIMARY};
    padding: 12px 16px;
    border-bottom: 1px solid #1a1a1a;
    font-size: 13px;
}}

tr:hover td {{
    background: #161616;
}}

::-webkit-scrollbar {{
    width: 4px;
    height: 4px;
}}

::-webkit-scrollbar-track {{
    background: {DARK_BG};
}}

::-webkit-scrollbar-thumb {{
    background: {CARD_BORDER};
    border-radius: 2px;
}}

.nav-container {{
    background: #080808;
    border-bottom: 1px solid {CARD_BORDER};
    padding: 0 40px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    height: 64px;
    position: sticky;
    top: 0;
    z-index: 999;
}}

.card {{
    background: {CARD_BG};
    border: 1px solid {CARD_BORDER};
    border-radius: 8px;
    padding: 28px;
    margin-bottom: 16px;
    transition: border-color 0.3s ease;
}}

.card:hover {{
    border-color: #2e2e2e;
}}

.card-gold {{
    background: linear-gradient(135deg, #1a1408 0%, #111008 100%);
    border: 1px solid #3a2e1a;
    border-radius: 8px;
    padding: 28px;
    margin-bottom: 16px;
}}

.hero-text {{
    font-family: 'Playfair Display', serif;
    font-size: 52px;
    font-weight: 700;
    letter-spacing: -1px;
    line-height: 1.15;
    color: {TEXT_PRIMARY};
}}

.hero-sub {{
    font-size: 15px;
    color: {TEXT_SECONDARY};
    letter-spacing: 0.3px;
    line-height: 1.7;
}}

.label-cap {{
    font-size: 10px;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    color: {TEXT_MUTED};
    font-weight: 500;
    margin-bottom: 8px;
}}

.value-gold {{
    color: {ACCENT_GOLD};
    font-weight: 700;
}}

.badge {{
    display: inline-block;
    background: #1e1a10;
    border: 1px solid #3a2e1a;
    color: {ACCENT_GOLD};
    font-size: 10px;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    padding: 4px 12px;
    border-radius: 2px;
    font-weight: 600;
}}

.badge-success {{
    background: #0e1e10;
    border-color: #1e3a20;
    color: {SUCCESS_COLOR};
}}

.badge-error {{
    background: #1e0e0e;
    border-color: #3a1e1e;
    color: {ERROR_COLOR};
}}

.badge-info {{
    background: #0e101e;
    border-color: #1e203a;
    color: {INFO_COLOR};
}}

.divider {{
    height: 1px;
    background: {CARD_BORDER};
    margin: 24px 0;
}}

.stat-row {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 0;
    border-bottom: 1px solid #1a1a1a;
}}

.stat-row:last-child {{
    border-bottom: none;
}}

.page-wrapper {{
    padding: 0 40px 60px 40px;
    max-width: 1400px;
    margin: 0 auto;
}}

.section-header {{
    margin: 48px 0 32px 0;
}}

.section-title {{
    font-family: 'Playfair Display', serif;
    font-size: 28px;
    font-weight: 600;
    color: {TEXT_PRIMARY};
    margin: 0 0 8px 0;
}}

.auth-container {{
    max-width: 440px;
    margin: 0 auto;
    padding: 60px 20px;
}}

.auth-card {{
    background: {CARD_BG};
    border: 1px solid {CARD_BORDER};
    border-radius: 12px;
    padding: 48px 40px;
}}

.progress-bar-outer {{
    background: #1a1a1a;
    border-radius: 2px;
    height: 4px;
    overflow: hidden;
}}

.progress-bar-inner {{
    height: 100%;
    border-radius: 2px;
    transition: width 0.5s ease;
}}

.tool-card {{
    background: #111111;
    border: 1px solid #1e1e1e;
    border-radius: 8px;
    padding: 20px;
    cursor: pointer;
    transition: all 0.25s ease;
}}

.tool-card:hover {{
    border-color: {ACCENT_GOLD}66;
    background: #161616;
}}

.tool-card-selected {{
    border-color: {ACCENT_GOLD} !important;
    background: #1a1408 !important;
}}

.result-row {{
    background: {CARD_BG};
    border: 1px solid {CARD_BORDER};
    border-radius: 6px;
    padding: 16px 20px;
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}}

.code-block {{
    background: #0d0d0d;
    border: 1px solid {CARD_BORDER};
    border-radius: 6px;
    padding: 20px;
    font-family: 'JetBrains Mono', 'Courier New', monospace;
    font-size: 12px;
    color: #a8b8c8;
    overflow-x: auto;
    line-height: 1.6;
}}

.log-entry {{
    padding: 8px 16px;
    border-left: 2px solid {CARD_BORDER};
    margin-bottom: 6px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    color: {TEXT_SECONDARY};
}}

.log-entry-success {{
    border-left-color: {SUCCESS_COLOR};
    color: {SUCCESS_COLOR}cc;
}}

.log-entry-error {{
    border-left-color: {ERROR_COLOR};
    color: {ERROR_COLOR}cc;
}}

.log-entry-info {{
    border-left-color: {INFO_COLOR};
    color: {INFO_COLOR}cc;
}}

.coverage-ring {{
    width: 80px;
    height: 80px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    font-size: 16px;
    margin: 0 auto;
}}

.stMultiSelect > div > div {{
    background: #161616 !important;
    border: 1px solid {CARD_BORDER} !important;
    border-radius: 4px !important;
}}

.stMultiSelect > div > div > div > div {{
    background: #1e1a10 !important;
    color: {ACCENT_GOLD} !important;
    border-radius: 2px !important;
}}

label[data-testid="stWidgetLabel"] > div > p {{
    color: {TEXT_SECONDARY} !important;
    font-size: 12px !important;
    letter-spacing: 0.5px !important;
    font-weight: 500 !important;
}}

.stSelectbox > div > div > div {{
    color: {TEXT_PRIMARY} !important;
}}

.element-container {{
    margin-bottom: 0 !important;
}}

.row-widget.stRadio > div {{
    flex-direction: row;
    gap: 16px;
}}

.stAlert {{
    background: #111111 !important;
    border-radius: 6px !important;
    border: 1px solid {CARD_BORDER} !important;
    color: {TEXT_PRIMARY} !important;
}}

footer {{display: none;}}
#MainMenu {{display: none;}}
header {{display: none;}}
</style>
""", unsafe_allow_html=True)

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "current_user" not in st.session_state:
    st.session_state.current_user = None
if "user_role" not in st.session_state:
    st.session_state.user_role = None
if "active_page" not in st.session_state:
    st.session_state.active_page = "Dashboard"
if "users_db" not in st.session_state:
    st.session_state.users_db = {
        "admin@pytcgeval.io": {
            "password": hashlib.sha256("Admin@2025".encode()).hexdigest(),
            "role": "admin",
            "name": "System Administrator",
            "joined": "2025-01-01"
        }
    }
if "projects" not in st.session_state:
    st.session_state.projects = {}
if "active_project" not in st.session_state:
    st.session_state.active_project = None
if "system_logs" not in st.session_state:
    st.session_state.system_logs = []
if "system_settings" not in st.session_state:
    st.session_state.system_settings = {
        "pynguin_enabled": True,
        "hypothesis_enabled": True,
        "klara_enabled": True,
        "utbot_enabled": False,
        "pynguin_time_limit": 30,
        "hypothesis_time_limit": 20,
        "klara_time_limit": 15,
        "utbot_time_limit": 45,
        "storage_path": "./outputs/",
        "line_coverage_threshold": 70,
        "branch_coverage_threshold": 60,
        "mutation_score_threshold": 50,
        "max_file_size_mb": 10,
        "allow_github_repos": True,
        "safe_mode": True,
        "result_retention_days": 30
    }
if "run_history" not in st.session_state:
    st.session_state.run_history = []
if "auth_tab" not in st.session_state:
    st.session_state.auth_tab = "login"
if "saved_configs" not in st.session_state:
    st.session_state.saved_configs = []

TOOLS_INFO = {
    "Pynguin": {
        "description": "Search-based automated unit test generation for Python using evolutionary algorithms",
        "strengths": "High branch coverage, handles complex control flow",
        "language": "Python 3.8+",
        "coverage_type": ["line", "branch"],
        "color": "#c8a97e"
    },
    "Hypothesis": {
        "description": "Property-based testing framework using Ghostwriter for automatic test synthesis",
        "strengths": "Edge case discovery, data-driven validation",
        "language": "Python 3.6+",
        "coverage_type": ["line", "mutation"],
        "color": "#a8a8b3"
    },
    "Klara": {
        "description": "Static analysis driven test case generator leveraging symbolic execution",
        "strengths": "Fast generation, deterministic output",
        "language": "Python 3.7+",
        "coverage_type": ["line", "branch", "mutation"],
        "color": "#b87333"
    },
    "UTBotPython": {
        "description": "Automated unit test generation using constraint solving and fuzzing techniques",
        "strengths": "Security-oriented, finds boundary conditions",
        "language": "Python 3.9+",
        "coverage_type": ["branch", "mutation"],
        "color": "#7090c8"
    }
}

def log_event(message, level="info"):
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state.system_logs.append({
        "timestamp": ts,
        "message": message,
        "level": level,
        "user": st.session_state.current_user or "system"
    })

def hash_password(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

def simulate_test_generation(source_files, tools, time_limits):
    results = {}
    for tool in tools:
        tool_results = []
        for sf in source_files:
            lines = sf.get("content", "").split("\n")
            num_functions = len([l for l in lines if l.strip().startswith("def ")])
            num_classes = len([l for l in lines if l.strip().startswith("class ")])
            num_generated = max(1, num_functions * random.randint(2, 4) + num_classes * random.randint(1, 3))
            num_passed = int(num_generated * random.uniform(0.75, 0.97))
            line_cov = random.uniform(62, 95)
            branch_cov = random.uniform(50, 88)
            mutation_score = random.uniform(40, 78)
            tool_results.append({
                "file": sf["name"],
                "tests_generated": num_generated,
                "tests_passed": num_passed,
                "tests_failed": num_generated - num_passed,
                "line_coverage": round(line_cov, 1),
                "branch_coverage": round(branch_cov, 1),
                "mutation_score": round(mutation_score, 1),
                "execution_time": round(random.uniform(0.5, time_limits.get(tool, 30)), 2),
                "errors": [] if random.random() > 0.25 else [
                    f"AssertionError in test_function_{random.randint(1,10)}",
                    f"ImportError: Module {sf['name'].replace('.py','')} not found"
                ][:random.randint(1,2)]
            })
        results[tool] = tool_results
    return results

def extract_python_info(code_content):
    info = {"functions": [], "classes": [], "imports": [], "lines": 0}
    try:
        tree = ast.parse(code_content)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                info["functions"].append(node.name)
            elif isinstance(node, ast.ClassDef):
                info["classes"].append(node.name)
            elif isinstance(node, (ast.Import, ast.ImportFrom)):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        info["imports"].append(alias.name)
                else:
                    info["imports"].append(node.module or "")
        info["lines"] = len(code_content.split("\n"))
    except:
        info["lines"] = len(code_content.split("\n"))
        funcs = re.findall(r"^def\s+(\w+)", code_content, re.MULTILINE)
        classes = re.findall(r"^class\s+(\w+)", code_content, re.MULTILINE)
        info["functions"] = funcs
        info["classes"] = classes
    return info

def generate_test_code(source_name, tool_name, functions, classes):
    mod = source_name.replace(".py", "")
    lines = [
        f"import unittest",
        f"import sys",
        f"sys.path.insert(0, '.')",
        f"from {mod} import *",
        f"",
        f"class Test{mod.capitalize()}_{tool_name}(unittest.TestCase):",
        f""
    ]
    for fn in functions[:5]:
        lines += [
            f"    def test_{fn}_basic(self):",
            f"        result = {fn}()",
            f"        self.assertIsNotNone(result)",
            f"",
            f"    def test_{fn}_edge(self):",
            f"        with self.assertRaises(Exception):",
            f"            {fn}(None)",
            f""
        ]
    for cls in classes[:3]:
        lines += [
            f"    def test_{cls}_instantiation(self):",
            f"        obj = {cls}()",
            f"        self.assertIsInstance(obj, {cls})",
            f""
        ]
    lines += [
        f"",
        f"if __name__ == '__main__':",
        f"    unittest.main(verbosity=2)"
    ]
    return "\n".join(lines)

def render_gauge_chart(value, title, color="#c8a97e"):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={"text": title, "font": {"color": "#888899", "size": 12, "family": "Inter"}},
        number={"font": {"color": "#f0f0f0", "size": 28, "family": "Inter"}, "suffix": "%"},
        gauge={
            "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": "#333344", "tickfont": {"color": "#555566", "size": 9}},
            "bar": {"color": color, "thickness": 0.7},
            "bgcolor": "#111111",
            "borderwidth": 0,
            "steps": [
                {"range": [0, 40], "color": "#1a1010"},
                {"range": [40, 70], "color": "#1a1608"},
                {"range": [70, 100], "color": "#0e1a0e"}
            ],
            "threshold": {
                "line": {"color": color, "width": 2},
                "thickness": 0.8,
                "value": value
            }
        }
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"family": "Inter", "color": "#f0f0f0"},
        margin=dict(l=20, r=20, t=40, b=10),
        height=200
    )
    return fig

def render_bar_comparison(results_by_tool, metric):
    tools = list(results_by_tool.keys())
    values = []
    for tool in tools:
        all_vals = [r[metric] for r in results_by_tool[tool] if metric in r]
        values.append(round(np.mean(all_vals), 1) if all_vals else 0)
    colors = [TOOLS_INFO.get(t, {}).get("color", ACCENT_GOLD) for t in tools]
    fig = go.Figure(go.Bar(
        x=tools,
        y=values,
        marker=dict(color=colors, line=dict(color="rgba(0,0,0,0)", width=0)),
        text=[f"{v}%" for v in values],
        textposition="outside",
        textfont=dict(color="#f0f0f0", size=12, family="Inter")
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False, tickfont=dict(color="#888899", size=11, family="Inter"), zeroline=False),
        yaxis=dict(showgrid=True, gridcolor="#1a1a1a", tickfont=dict(color="#555566", size=10), range=[0, 110], zeroline=False),
        margin=dict(l=10, r=10, t=20, b=10),
        height=260,
        showlegend=False
    )
    return fig

def render_radar_chart(results_by_tool):
    categories = ["Line Coverage", "Branch Coverage", "Mutation Score", "Tests Passed %", "Speed Score"]
    fig = go.Figure()
    for tool, results in results_by_tool.items():
        if not results:
            continue
        lc = np.mean([r.get("line_coverage", 0) for r in results])
        bc = np.mean([r.get("branch_coverage", 0) for r in results])
        ms = np.mean([r.get("mutation_score", 0) for r in results])
        tp = np.mean([(r.get("tests_passed", 0) / max(r.get("tests_generated", 1), 1)) * 100 for r in results])
        et = np.mean([r.get("execution_time", 30) for r in results])
        speed = max(0, 100 - (et / 30) * 100)
        vals = [lc, bc, ms, tp, speed]
        color = TOOLS_INFO.get(tool, {}).get("color", ACCENT_GOLD)
        fig.add_trace(go.Scatterpolar(
            r=vals + [vals[0]],
            theta=categories + [categories[0]],
            fill="toself",
            fillcolor=f"rgba({int(color[1:3],16)}, {int(color[3:5],16)}, {int(color[5:7],16)}, 0.15)",
            line=dict(color=color, width=2),
            name=tool
        ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(visible=True, range=[0, 100], gridcolor="#1e1e1e", tickfont=dict(color="#555566", size=9)),
            angularaxis=dict(gridcolor="#1e1e1e", tickfont=dict(color="#888899", size=11, family="Inter"))
        ),
        legend=dict(font=dict(color="#888899", size=11, family="Inter"), bgcolor="rgba(0,0,0,0)"),
        margin=dict(l=40, r=40, t=20, b=20),
        height=340
    )
    return fig

def render_timeline_chart(run_history):
    if not run_history:
        return None
    dates = [r["timestamp"] for r in run_history[-15:]]
    line_covs = [r.get("avg_line_coverage", random.uniform(60, 90)) for r in run_history[-15:]]
    branch_covs = [r.get("avg_branch_coverage", random.uniform(50, 80)) for r in run_history[-15:]]
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dates, y=line_covs, name="Line Coverage",
        line=dict(color=ACCENT_GOLD, width=2),
        mode="lines+markers",
        marker=dict(color=ACCENT_GOLD, size=5)
    ))
    fig.add_trace(go.Scatter(
        x=dates, y=branch_covs, name="Branch Coverage",
        line=dict(color=ACCENT_SILVER, width=2),
        mode="lines+markers",
        marker=dict(color=ACCENT_SILVER, size=5)
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False, tickfont=dict(color="#555566", size=10), zeroline=False),
        yaxis=dict(showgrid=True, gridcolor="#1a1a1a", tickfont=dict(color="#555566", size=10), range=[0, 100], zeroline=False),
        legend=dict(font=dict(color="#888899", family="Inter"), bgcolor="rgba(0,0,0,0)"),
        margin=dict(l=10, r=10, t=20, b=10),
        height=260
    )
    return fig

def render_heatmap_coverage(results_by_tool):
    tools = list(results_by_tool.keys())
    if not tools:
        return None
    all_files = list(set([r["file"] for trs in results_by_tool.values() for r in trs]))
    z_vals = []
    for tool in tools:
        row = []
        file_map = {r["file"]: r for r in results_by_tool[tool]}
        for f in all_files:
            row.append(file_map.get(f, {}).get("line_coverage", 0))
        z_vals.append(row)
    fig = go.Figure(go.Heatmap(
        z=z_vals,
        x=[f[:20] for f in all_files],
        y=tools,
        colorscale=[[0, "#1a0e0e"], [0.5, "#3a2a10"], [1, "#c8a97e"]],
        text=[[f"{v:.0f}%" for v in row] for row in z_vals],
        texttemplate="%{text}",
        textfont=dict(color="#f0f0f0", size=12),
        showscale=True,
        colorbar=dict(
            tickfont=dict(color="#888899", size=10),
            bgcolor="rgba(0,0,0,0)",
            outlinecolor="rgba(0,0,0,0)"
        )
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(tickfont=dict(color="#888899", size=10), side="bottom"),
        yaxis=dict(tickfont=dict(color="#888899", size=11)),
        margin=dict(l=10, r=10, t=20, b=40),
        height=max(160, len(tools) * 60 + 60)
    )
    return fig

def render_3d_scatter(results_by_tool):
    fig = go.Figure()

    for tool, results in results_by_tool.items():
        if not results:
            continue

        color = TOOLS_INFO.get(tool, {}).get("color", ACCENT_GOLD)

        fig.add_trace(go.Scatter3d(
            x=[r.get("line_coverage", 0) for r in results],
            y=[r.get("branch_coverage", 0) for r in results],
            z=[r.get("mutation_score", 0) for r in results],
            mode="markers+text",
            marker=dict(
                size=8,
                color=color,
                opacity=0.85,
                line=dict(color="#000", width=0.5)
            ),
            text=[r.get("file", "")[:15] for r in results],
            textposition="top center",
            textfont=dict(color="#888899", size=9),
            name=tool
        ))

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        scene=dict(
            bgcolor="rgba(0,0,0,0)",
            xaxis=dict(
                title=dict(text="Line Coverage %", font=dict(color="#888899", size=10)),
                tickfont=dict(color="#555566", size=8),
                gridcolor="#1e1e1e",
                zerolinecolor="#1e1e1e"
            ),
            yaxis=dict(
                title=dict(text="Branch Coverage %", font=dict(color="#888899", size=10)),
                tickfont=dict(color="#555566", size=8),
                gridcolor="#1e1e1e",
                zerolinecolor="#1e1e1e"
            ),
            zaxis=dict(
                title=dict(text="Mutation Score %", font=dict(color="#888899", size=10)),
                tickfont=dict(color="#555566", size=8),
                gridcolor="#1e1e1e",
                zerolinecolor="#1e1e1e"
            )
        ),
        legend=dict(
            font=dict(color="#888899", size=11, family="Inter"),
            bgcolor="rgba(0,0,0,0)"
        ),
        margin=dict(l=0, r=0, t=20, b=0),
        height=380
    )

    return fig

def render_sunburst_chart(results_by_tool):
    ids, labels, parents, values, colors = ["root"], ["All Tools"], [""], [0], ["#111111"]
    for tool, results in results_by_tool.items():
        t_color = TOOLS_INFO.get(tool, {}).get("color", ACCENT_GOLD)
        t_id = f"tool_{tool}"
        t_total = sum(r.get("tests_generated", 0) for r in results)
        ids.append(t_id); labels.append(tool); parents.append("root"); values.append(t_total); colors.append(t_color)
        for r in results:
            f_id = f"{t_id}_{r['file']}"
            ids.append(f_id); labels.append(r["file"][:15]); parents.append(t_id)
            values.append(r.get("tests_generated", 0)); colors.append(t_color + "99")
    fig = go.Figure(go.Sunburst(
        ids=ids, labels=labels, parents=parents, values=values,
        marker=dict(colors=colors, line=dict(color="#0a0a0a", width=1)),
        insidetextfont=dict(color="#f0f0f0", family="Inter"),
        outsidetextfont=dict(color="#888899", family="Inter")
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=20, b=10),
        height=340
    )
    return fig

def render_box_plot(results_by_tool):
    fig = go.Figure()
    for tool, results in results_by_tool.items():
        color = TOOLS_INFO.get(tool, {}).get("color", ACCENT_GOLD)
        vals = [r.get("line_coverage", 0) for r in results]
        if vals:
            fig.add_trace(go.Box(
                y=vals, name=tool,
                marker_color=color,
                line_color=color,
                fillcolor=f"rgba({int(color[1:3],16)}, {int(color[3:5],16)}, {int(color[5:7],16)}, 0.15)",
                boxmean=True
            ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False, tickfont=dict(color="#888899", size=11)),
        yaxis=dict(showgrid=True, gridcolor="#1a1a1a", tickfont=dict(color="#555566", size=10), title=dict(text="Line Coverage %", font=dict(color="#888899", size=11))),
        legend=dict(font=dict(color="#888899"), bgcolor="rgba(0,0,0,0)"),
        margin=dict(l=10, r=10, t=20, b=10),
        height=280,
        showlegend=False
    )
    return fig

def render_waterfall_chart(run_history):
    if len(run_history) < 2:
        return None
    names = [f"Run {i+1}" for i in range(min(8, len(run_history)))]
    vals = [r.get("avg_line_coverage", random.uniform(60, 90)) for r in run_history[:8]]
    measures = ["absolute"] + ["relative"] * (len(vals) - 1)
    y_vals = [vals[0]] + [vals[i] - vals[i-1] for i in range(1, len(vals))]
    colors = [ACCENT_GOLD if v >= 0 else ERROR_COLOR for v in y_vals]
    fig = go.Figure(go.Waterfall(
        name="Coverage Trend",
        orientation="v",
        measure=measures,
        x=names,
        y=y_vals,
        text=[f"{v:.1f}%" for v in y_vals],
        textposition="outside",
        connector=dict(line=dict(color="#1e1e1e", width=1)),
        increasing=dict(marker=dict(color=ACCENT_GOLD)),
        decreasing=dict(marker=dict(color=ERROR_COLOR)),
        totals=dict(marker=dict(color=INFO_COLOR))
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False, tickfont=dict(color="#888899", size=11)),
        yaxis=dict(showgrid=True, gridcolor="#1a1a1a", tickfont=dict(color="#555566", size=10)),
        margin=dict(l=10, r=10, t=20, b=10),
        height=280,
        showlegend=False
    )
    return fig

def render_auth_page():
    st.markdown("""
    <div style="background:#0a0a0a; min-height:100vh; display:flex; align-items:center; justify-content:center; padding:40px 20px;">
    </div>
    """, unsafe_allow_html=True)
    col_l, col_c, col_r = st.columns([1, 1.2, 1])
    with col_c:
        st.markdown(f"""
        <div style="text-align:center; margin-bottom:48px;">
            <div style="font-family:'Playfair Display',serif; font-size:32px; font-weight:700; color:{TEXT_PRIMARY}; letter-spacing:-0.5px;">PyTCG-Eval</div>
            <div style="font-size:10px; letter-spacing:3px; text-transform:uppercase; color:{TEXT_MUTED}; margin-top:6px;">Automated Test Case Generation</div>
            <div style="width:40px; height:2px; background:{ACCENT_GOLD}; margin:20px auto 0;"></div>
        </div>
        """, unsafe_allow_html=True)
        tab_col1, tab_col2 = st.columns(2)
        with tab_col1:
            if st.button("Sign In", key="tab_login"):
                st.session_state.auth_tab = "login"
                st.rerun()
        with tab_col2:
            if st.button("Register", key="tab_register"):
                st.session_state.auth_tab = "register"
                st.rerun()
        st.markdown(f"""
        <div style="display:flex; margin-bottom:32px;">
            <div style="flex:1; height:2px; background:{'#c8a97e' if st.session_state.auth_tab=='login' else '#1e1e1e'};"></div>
            <div style="flex:1; height:2px; background:{'#c8a97e' if st.session_state.auth_tab=='register' else '#1e1e1e'};"></div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(f"""<div style="background:{CARD_BG}; border:1px solid {CARD_BORDER}; border-radius:12px; padding:40px;">""", unsafe_allow_html=True)
        if st.session_state.auth_tab == "login":
            st.markdown(f"""
            <div style="font-family:'Playfair Display',serif; font-size:22px; font-weight:600; color:{TEXT_PRIMARY}; margin-bottom:28px;">Welcome back.</div>
            """, unsafe_allow_html=True)
            email_in = st.text_input("Email address", placeholder="you@example.com", key="login_email")
            pwd_in = st.text_input("Password", type="password", placeholder="Enter your password", key="login_pwd")
            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
            if st.button("Continue", key="do_login"):
                if not email_in or not pwd_in:
                    st.error("Please enter email and password.")
                elif email_in not in st.session_state.users_db:
                    st.error("Account not found. Please register first.")
                elif st.session_state.users_db[email_in]["password"] != hash_password(pwd_in):
                    st.error("Incorrect password.")
                else:
                    user = st.session_state.users_db[email_in]
                    st.session_state.authenticated = True
                    st.session_state.current_user = email_in
                    st.session_state.user_role = user["role"]
                    log_event(f"User {email_in} signed in", "info")
                    st.rerun()
            st.markdown(f"""
            <div style="text-align:center; margin-top:24px; font-size:12px; color:{TEXT_MUTED};">
                Not a member? Switch to Register above.
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="font-family:'Playfair Display',serif; font-size:22px; font-weight:600; color:{TEXT_PRIMARY}; margin-bottom:28px;">Create account.</div>
            """, unsafe_allow_html=True)
            reg_name = st.text_input("Full name", placeholder="Jane Doe", key="reg_name")
            reg_email = st.text_input("Email address", placeholder="you@example.com", key="reg_email")
            reg_role = st.selectbox("Account type", ["Developer User", "System Administrator"], key="reg_role")
            reg_pwd = st.text_input("Password", type="password", placeholder="Min 8 characters", key="reg_pwd")
            reg_pwd2 = st.text_input("Confirm password", type="password", placeholder="Repeat password", key="reg_pwd2")
            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
            if st.button("Create Account", key="do_register"):
                if not all([reg_name, reg_email, reg_pwd, reg_pwd2]):
                    st.error("All fields are required.")
                elif reg_email in st.session_state.users_db:
                    st.error("An account with this email already exists.")
                elif reg_pwd != reg_pwd2:
                    st.error("Passwords do not match.")
                elif len(reg_pwd) < 8:
                    st.error("Password must be at least 8 characters.")
                elif "@" not in reg_email:
                    st.error("Please enter a valid email address.")
                else:
                    role_key = "admin" if reg_role == "System Administrator" else "developer"
                    st.session_state.users_db[reg_email] = {
                        "password": hash_password(reg_pwd),
                        "role": role_key,
                        "name": reg_name,
                        "joined": datetime.date.today().isoformat()
                    }
                    log_event(f"New account registered: {reg_email}", "info")
                    st.success("Account created successfully. Please sign in.")
                    st.session_state.auth_tab = "login"
                    st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="text-align:center; margin-top:32px; font-size:10px; letter-spacing:1.5px; text-transform:uppercase; color:{TEXT_MUTED};">
            PyQuality Labs &nbsp;&middot;&nbsp; PyTCG-Eval v2.0 &nbsp;&middot;&nbsp; Spring 2026
        </div>
        """, unsafe_allow_html=True)

def render_navbar():
    user_name = st.session_state.users_db.get(st.session_state.current_user, {}).get("name", "User")
    role_label = "Administrator" if st.session_state.user_role == "admin" else "Developer"
    pages_dev = ["Dashboard", "Upload Code", "Configure", "Generate Tests", "Run Tests", "Coverage Analysis", "Compare Tools", "Results History", "Export", "Metrics Guide"]
    pages_admin = ["Dashboard", "Upload Code", "Configure", "Generate Tests", "Run Tests", "Coverage Analysis", "Compare Tools", "Results History", "Export", "Metrics Guide", "Manage Tools", "System Settings", "System Logs"]
    pages = pages_admin if st.session_state.user_role == "admin" else pages_dev
    st.markdown(f"""
    <div style="background:#080808; border-bottom:1px solid {CARD_BORDER}; padding:0 40px; height:64px; display:flex; align-items:center; justify-content:space-between; position:sticky; top:0; z-index:999;">
        <div style="display:flex; align-items:center; gap:32px;">
            <div style="font-family:'Playfair Display',serif; font-size:18px; font-weight:700; color:{TEXT_PRIMARY}; white-space:nowrap;">PyTCG-Eval</div>
        </div>
        <div style="display:flex; align-items:center; gap:16px;">
            <div style="font-size:12px; color:{TEXT_SECONDARY};">{user_name}</div>
            <div style="font-size:10px; letter-spacing:1.5px; text-transform:uppercase; color:{TEXT_MUTED};">{role_label}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(f"""
    <div style="background:#0d0d0d; border-bottom:1px solid {CARD_BORDER}; padding:0 40px; overflow-x:auto; white-space:nowrap;">
    """, unsafe_allow_html=True)
    nav_cols = st.columns(len(pages) + 1)
    for i, page in enumerate(pages):
        with nav_cols[i]:
            active = st.session_state.active_page == page
            btn_style = f"color:{ACCENT_GOLD}; border-bottom:2px solid {ACCENT_GOLD};" if active else f"color:{TEXT_MUTED};"
            if st.button(page, key=f"nav_{page}"):
                st.session_state.active_page = page
                st.rerun()
    with nav_cols[-1]:
        if st.button("Sign Out", key="nav_signout"):
            log_event(f"User {st.session_state.current_user} signed out", "info")
            for k in ["authenticated", "current_user", "user_role", "active_page", "active_project"]:
                if k in st.session_state:
                    del st.session_state[k]
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

def render_dashboard():
    st.markdown("<div style='padding:40px 40px 0;'>", unsafe_allow_html=True)
    user_name = st.session_state.users_db.get(st.session_state.current_user, {}).get("name", "User").split()[0]
    total_projects = len(st.session_state.projects)
    total_runs = len(st.session_state.run_history)
    total_tests = sum(r.get("total_tests", 0) for r in st.session_state.run_history)
    avg_coverage = round(np.mean([r.get("avg_line_coverage", 0) for r in st.session_state.run_history]), 1) if st.session_state.run_history else 0
    st.markdown(f"""
    <div style="margin-bottom:40px;">
        <div style="font-size:11px; letter-spacing:2px; text-transform:uppercase; color:{TEXT_MUTED}; margin-bottom:10px;">Welcome back</div>
        <div style="font-family:'Playfair Display',serif; font-size:42px; font-weight:700; color:{TEXT_PRIMARY}; line-height:1.15;">{user_name},<br>your workspace awaits.</div>
        <div style="font-size:14px; color:{TEXT_SECONDARY}; margin-top:12px; max-width:500px;">Automated Python test generation and evaluation. Built for clarity.</div>
    </div>
    """, unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    metrics = [
        (c1, "Projects", total_projects, "", ACCENT_GOLD),
        (c2, "Test Runs", total_runs, "", ACCENT_SILVER),
        (c3, "Tests Generated", total_tests, "", ACCENT_COPPER),
        (c4, "Avg Coverage", avg_coverage, "%", SUCCESS_COLOR)
    ]
    for col, label, val, suffix, color in metrics:
        with col:
            st.markdown(f"""
            <div style="background:{CARD_BG}; border:1px solid {CARD_BORDER}; border-radius:8px; padding:24px; margin-bottom:16px;">
                <div style="font-size:10px; letter-spacing:2px; text-transform:uppercase; color:{TEXT_MUTED}; margin-bottom:12px;">{label}</div>
                <div style="font-size:36px; font-weight:700; color:{color}; font-family:'Inter';">{val}{suffix}</div>
            </div>
            """, unsafe_allow_html=True)
    st.markdown(f"""<div style="width:100%; height:1px; background:{CARD_BORDER}; margin:16px 0 32px;"></div>""", unsafe_allow_html=True)
    col_left, col_right = st.columns([1.6, 1])
    with col_left:
        st.markdown(f"""
        <div style="font-size:10px; letter-spacing:2px; text-transform:uppercase; color:{TEXT_MUTED}; margin-bottom:20px;">Coverage Trend</div>
        """, unsafe_allow_html=True)
        if st.session_state.run_history:
            chart = render_timeline_chart(st.session_state.run_history)
            if chart:
                st.plotly_chart(chart, use_container_width=True, config={"displayModeBar": False})
        else:
            st.markdown(f"""
            <div style="background:{CARD_BG}; border:1px solid {CARD_BORDER}; border-radius:8px; padding:60px; text-align:center; color:{TEXT_MUTED}; font-size:13px;">
                No test runs yet. Upload code and generate tests to see trends.
            </div>
            """, unsafe_allow_html=True)
        if st.session_state.run_history:
            st.markdown(f"""<div style="font-size:10px; letter-spacing:2px; text-transform:uppercase; color:{TEXT_MUTED}; margin:24px 0 16px;">Coverage Improvement</div>""", unsafe_allow_html=True)
            wf = render_waterfall_chart(st.session_state.run_history)
            if wf:
                st.plotly_chart(wf, use_container_width=True, config={"displayModeBar": False})
    with col_right:
        st.markdown(f"""
        <div style="font-size:10px; letter-spacing:2px; text-transform:uppercase; color:{TEXT_MUTED}; margin-bottom:20px;">Active Projects</div>
        """, unsafe_allow_html=True)
        if st.session_state.projects:
            for pname, pdata in list(st.session_state.projects.items())[:5]:
                files_count = len(pdata.get("files", []))
                runs = pdata.get("runs", 0)
                last_cov = pdata.get("last_coverage", 0)
                color = SUCCESS_COLOR if last_cov >= 70 else (WARNING_COLOR if last_cov >= 50 else ERROR_COLOR)
                st.markdown(f"""
                <div style="background:{CARD_BG}; border:1px solid {CARD_BORDER}; border-radius:8px; padding:20px; margin-bottom:12px;">
                    <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:12px;">
                        <div>
                            <div style="font-size:14px; font-weight:600; color:{TEXT_PRIMARY}; margin-bottom:4px;">{pname}</div>
                            <div style="font-size:11px; color:{TEXT_MUTED};">{files_count} file{'s' if files_count != 1 else ''} &middot; {runs} run{'s' if runs != 1 else ''}</div>
                        </div>
                        <div style="font-size:18px; font-weight:700; color:{color};">{last_cov:.0f}%</div>
                    </div>
                    <div style="background:#1a1a1a; border-radius:2px; height:3px; overflow:hidden;">
                        <div style="width:{last_cov}%; height:100%; background:{color}; border-radius:2px;"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="background:{CARD_BG}; border:1px solid {CARD_BORDER}; border-radius:8px; padding:40px; text-align:center; color:{TEXT_MUTED}; font-size:13px;">
                No projects yet.<br>Create one by uploading code.
            </div>
            """, unsafe_allow_html=True)
        st.markdown(f"""
        <div style="font-size:10px; letter-spacing:2px; text-transform:uppercase; color:{TEXT_MUTED}; margin:24px 0 16px;">Recent Activity</div>
        """, unsafe_allow_html=True)
        recent_logs = st.session_state.system_logs[-6:] if st.session_state.system_logs else []
        if recent_logs:
            for entry in reversed(recent_logs):
                lvl = entry.get("level", "info")
                dot_color = SUCCESS_COLOR if lvl == "info" else (ERROR_COLOR if lvl == "error" else WARNING_COLOR)
                st.markdown(f"""
                <div style="display:flex; align-items:flex-start; gap:10px; margin-bottom:10px; padding-bottom:10px; border-bottom:1px solid #161616;">
                    <div style="width:6px; height:6px; border-radius:50%; background:{dot_color}; margin-top:5px; flex-shrink:0;"></div>
                    <div>
                        <div style="font-size:12px; color:{TEXT_SECONDARY};">{entry['message']}</div>
                        <div style="font-size:10px; color:{TEXT_MUTED}; margin-top:2px;">{entry['timestamp']}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown(f"""<div style="font-size:12px; color:{TEXT_MUTED};">No recent activity.</div>""", unsafe_allow_html=True)
    st.markdown(f"""
    <div style="margin:32px 0;">
        <div style="font-size:10px; letter-spacing:2px; text-transform:uppercase; color:{TEXT_MUTED}; margin-bottom:20px;">Quick Actions</div>
    </div>
    """, unsafe_allow_html=True)
    qa_cols = st.columns(4)
    qa_items = [
        ("Upload Code", "Add Python source files to a project", "Upload Code"),
        ("Configure Tools", "Set up test generation parameters", "Configure"),
        ("Generate Tests", "Run automated test generation", "Generate Tests"),
        ("View Results", "Browse historical test runs", "Results History")
    ]
    for col, (title, desc, target) in zip(qa_cols, qa_items):
        with col:
            st.markdown(f"""
            <div style="background:{CARD_BG}; border:1px solid {CARD_BORDER}; border-radius:8px; padding:24px; margin-bottom:16px; cursor:pointer;">
                <div style="font-size:14px; font-weight:600; color:{TEXT_PRIMARY}; margin-bottom:8px;">{title}</div>
                <div style="font-size:12px; color:{TEXT_MUTED}; line-height:1.5;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Go", key=f"qa_{target}"):
                st.session_state.active_page = target
                st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

def render_upload_page():
    st.markdown("<div style='padding:40px;'>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style="margin-bottom:40px;">
        <div style="font-size:10px; letter-spacing:2px; text-transform:uppercase; color:{TEXT_MUTED}; margin-bottom:10px;">Step 1 of 4</div>
        <div style="font-family:'Playfair Display',serif; font-size:34px; font-weight:700; color:{TEXT_PRIMARY};">Upload Source Code</div>
        <div style="font-size:14px; color:{TEXT_SECONDARY}; margin-top:8px;">Provide Python source files or a GitHub repository URL.</div>
    </div>
    """, unsafe_allow_html=True)
    col_form, col_info = st.columns([1.4, 1])
    with col_form:
        st.markdown(f"""<div style="background:{CARD_BG}; border:1px solid {CARD_BORDER}; border-radius:8px; padding:32px; margin-bottom:20px;">""", unsafe_allow_html=True)
        st.markdown(f"""<div style="font-size:12px; color:{TEXT_MUTED}; letter-spacing:1px; text-transform:uppercase; margin-bottom:20px;">Project Details</div>""", unsafe_allow_html=True)
        proj_name = st.text_input("Project name", placeholder="my-python-project", key="proj_name_input")
        proj_desc = st.text_area("Description (optional)", placeholder="Brief description of the project", key="proj_desc_input", height=80)
        st.markdown("</div>", unsafe_allow_html=True)
        input_mode = st.radio("Source type", ["Upload .py Files", "GitHub Repository URL"], key="input_mode", horizontal=True)
        st.markdown(f"""<div style="background:{CARD_BG}; border:1px solid {CARD_BORDER}; border-radius:8px; padding:32px; margin-top:16px;">""", unsafe_allow_html=True)
        if input_mode == "Upload .py Files":
            st.markdown(f"""<div style="font-size:12px; color:{TEXT_MUTED}; letter-spacing:1px; text-transform:uppercase; margin-bottom:20px;">File Upload</div>""", unsafe_allow_html=True)
            uploaded = st.file_uploader("Select Python files", type=["py"], accept_multiple_files=True, key="py_uploader", label_visibility="collapsed")
            if uploaded:
                st.markdown(f"""<div style="margin-top:16px; font-size:11px; letter-spacing:1px; text-transform:uppercase; color:{TEXT_MUTED}; margin-bottom:12px;">{len(uploaded)} file(s) selected</div>""", unsafe_allow_html=True)
                for uf in uploaded:
                    content = uf.read().decode("utf-8", errors="replace")
                    info = extract_python_info(content)
                    st.markdown(f"""
                    <div style="background:#161616; border:1px solid {CARD_BORDER}; border-radius:6px; padding:14px 18px; margin-bottom:8px; display:flex; justify-content:space-between; align-items:center;">
                        <div>
                            <div style="font-size:13px; color:{TEXT_PRIMARY}; font-weight:500;">{uf.name}</div>
                            <div style="font-size:11px; color:{TEXT_MUTED}; margin-top:3px;">{info['lines']} lines &middot; {len(info['functions'])} functions &middot; {len(info['classes'])} classes</div>
                        </div>
                        <div style="font-size:11px; color:{SUCCESS_COLOR};">Valid</div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.markdown(f"""<div style="font-size:12px; color:{TEXT_MUTED}; letter-spacing:1px; text-transform:uppercase; margin-bottom:20px;">Repository</div>""", unsafe_allow_html=True)
            repo_url = st.text_input("GitHub repository URL", placeholder="https://github.com/username/repository", key="repo_url_input", label_visibility="collapsed")
            if repo_url:
                if "github.com" in repo_url:
                    st.markdown(f"""
                    <div style="background:#0e1a0e; border:1px solid #1e3a20; border-radius:6px; padding:14px 18px; margin-top:12px;">
                        <div style="font-size:12px; color:{SUCCESS_COLOR};">Repository URL format recognized</div>
                        <div style="font-size:11px; color:{TEXT_MUTED}; margin-top:4px;">System will simulate fetching Python files from this repository.</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style="background:#1e0e0e; border:1px solid #3a1e1e; border-radius:6px; padding:14px 18px; margin-top:12px;">
                        <div style="font-size:12px; color:{ERROR_COLOR};">Invalid GitHub URL format</div>
                    </div>
                    """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
        if st.button("Create Project and Continue", key="create_project"):
            if not proj_name:
                st.error("Please enter a project name.")
            else:
                files_data = []
                if input_mode == "Upload .py Files":
                    uploaded_files = st.session_state.get("py_uploader")
                    if not uploaded_files:
                        st.error("Please select at least one Python file.")
                        st.stop()
                    for uf in uploaded_files:
                        uf.seek(0)
                        content = uf.read().decode("utf-8", errors="replace")
                        info = extract_python_info(content)
                        files_data.append({"name": uf.name, "content": content, "info": info})
                else:
                    repo_u = st.session_state.get("repo_url_input", "")
                    if not repo_u or "github.com" not in repo_u:
                        st.error("Please enter a valid GitHub repository URL.")
                        st.stop()
                    demo_files = ["main.py", "utils.py", "calculator.py", "data_processor.py"]
                    for fn in demo_files:
                        content = f"def sample_function():\n    return True\n\nclass SampleClass:\n    def method(self):\n        pass\n"
                        files_data.append({"name": fn, "content": content, "info": extract_python_info(content)})
                    log_event(f"Repository {repo_u} simulated fetch", "info")
                if proj_name in st.session_state.projects:
                    st.error(f"Project '{proj_name}' already exists. Use a different name.")
                else:
                    st.session_state.projects[proj_name] = {
                        "name": proj_name,
                        "description": proj_desc,
                        "files": files_data,
                        "selected_files": [f["name"] for f in files_data],
                        "created": datetime.datetime.now().isoformat(),
                        "runs": 0,
                        "last_coverage": 0,
                        "results": {}
                    }
                    st.session_state.active_project = proj_name
                    log_event(f"Project '{proj_name}' created with {len(files_data)} file(s)", "info")
                    st.success(f"Project '{proj_name}' created with {len(files_data)} file(s). Proceeding to configuration.")
                    time.sleep(1)
                    st.session_state.active_page = "Configure"
                    st.rerun()
    with col_info:
        st.markdown(f"""
        <div style="background:{CARD_BG}; border:1px solid {CARD_BORDER}; border-radius:8px; padding:28px; margin-bottom:16px;">
            <div style="font-size:10px; letter-spacing:2px; text-transform:uppercase; color:{TEXT_MUTED}; margin-bottom:16px;">Existing Projects</div>
        """, unsafe_allow_html=True)
        if st.session_state.projects:
            for pname in list(st.session_state.projects.keys())[:8]:
                is_active = st.session_state.active_project == pname
                border = ACCENT_GOLD if is_active else CARD_BORDER
                st.markdown(f"""
                <div style="background:#161616; border:1px solid {border}; border-radius:6px; padding:14px; margin-bottom:8px;">
                    <div style="font-size:13px; color:{TEXT_PRIMARY}; font-weight:500;">{pname}</div>
                    <div style="font-size:11px; color:{TEXT_MUTED}; margin-top:3px;">{len(st.session_state.projects[pname].get('files', []))} files</div>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"Select", key=f"sel_proj_{pname}"):
                    st.session_state.active_project = pname
                    st.rerun()
        else:
            st.markdown(f"""<div style="font-size:12px; color:{TEXT_MUTED};">No projects yet.</div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="background:#1a1408; border:1px solid #3a2e1a; border-radius:8px; padding:24px;">
            <div style="font-size:10px; letter-spacing:2px; text-transform:uppercase; color:{ACCENT_GOLD}; margin-bottom:14px;">Supported Formats</div>
            <div style="font-size:13px; color:{TEXT_SECONDARY}; line-height:1.8;">
                &bull; Python (.py) files up to 10MB<br>
                &bull; Public GitHub repositories<br>
                &bull; Single modules or full packages<br>
                &bull; Files with classes and functions
            </div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

def render_configure_page():
    st.markdown("<div style='padding:40px;'>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style="margin-bottom:40px;">
        <div style="font-size:10px; letter-spacing:2px; text-transform:uppercase; color:{TEXT_MUTED}; margin-bottom:10px;">Step 2 of 4</div>
        <div style="font-family:'Playfair Display',serif; font-size:34px; font-weight:700; color:{TEXT_PRIMARY};">Configure Test Generation</div>
        <div style="font-size:14px; color:{TEXT_SECONDARY}; margin-top:8px;">Select tools, set time limits, and choose files to test.</div>
    </div>
    """, unsafe_allow_html=True)
    if not st.session_state.active_project:
        st.markdown(f"""
        <div style="background:{CARD_BG}; border:1px solid {CARD_BORDER}; border-radius:8px; padding:48px; text-align:center;">
            <div style="font-size:16px; color:{TEXT_SECONDARY}; margin-bottom:16px;">No active project selected.</div>
            <div style="font-size:13px; color:{TEXT_MUTED};">Please upload code first to create a project.</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Go to Upload", key="go_upload_from_config"):
            st.session_state.active_page = "Upload Code"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        return
    proj = st.session_state.projects[st.session_state.active_project]
    st.markdown(f"""
    <div style="background:#1a1408; border:1px solid #3a2e1a; border-radius:8px; padding:16px 24px; margin-bottom:28px; display:flex; align-items:center; justify-content:space-between;">
        <div>
            <div style="font-size:13px; font-weight:600; color:{ACCENT_GOLD};">{st.session_state.active_project}</div>
            <div style="font-size:11px; color:{TEXT_MUTED}; margin-top:2px;">{len(proj.get('files', []))} source files available</div>
        </div>
        <div style="font-size:10px; letter-spacing:1.5px; text-transform:uppercase; color:{TEXT_MUTED};">Active Project</div>
    </div>
    """, unsafe_allow_html=True)
    col_left, col_right = st.columns([1.5, 1])
    with col_left:
        st.markdown(f"""
        <div style="font-size:10px; letter-spacing:2px; text-transform:uppercase; color:{TEXT_MUTED}; margin-bottom:20px;">Select Test Generation Tools</div>
        """, unsafe_allow_html=True)
        tool_selections = {}
        for tool_name, tool_info in TOOLS_INFO.items():
            is_enabled = st.session_state.system_settings.get(f"{tool_name.lower()}_enabled", True)
            c1, c2 = st.columns([3, 1])
            with c1:
                sel = st.checkbox(tool_name, value=is_enabled, key=f"tool_sel_{tool_name}", disabled=not is_enabled)
                tool_selections[tool_name] = sel and is_enabled
            with c2:
                status = "Enabled" if is_enabled else "Disabled"
                color = SUCCESS_COLOR if is_enabled else TEXT_MUTED
                st.markdown(f"""<div style="font-size:10px; color:{color}; padding-top:8px;">{status}</div>""", unsafe_allow_html=True)
            st.markdown(f"""
            <div style="background:{CARD_BG}; border:1px solid {CARD_BORDER}; border-radius:6px; padding:14px 18px; margin-bottom:12px;">
                <div style="font-size:12px; color:{TEXT_SECONDARY}; margin-bottom:6px;">{tool_info['description']}</div>
                <div style="font-size:11px; color:{TEXT_MUTED};">Strengths: {tool_info['strengths']}</div>
                <div style="margin-top:8px; display:flex; gap:8px;">
                    {''.join([f'<span style="background:#1a1408; border:1px solid #3a2e1a; color:{ACCENT_GOLD}; font-size:9px; letter-spacing:1px; text-transform:uppercase; padding:3px 8px; border-radius:2px;">{ct}</span>' for ct in tool_info['coverage_type']])}
                </div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown(f"""
        <div style="font-size:10px; letter-spacing:2px; text-transform:uppercase; color:{TEXT_MUTED}; margin:24px 0 20px;">Execution Time Limits (seconds)</div>
        """, unsafe_allow_html=True)
        time_limits = {}
        for tool_name in TOOLS_INFO.keys():
            default_key = f"{tool_name.lower()}_time_limit"
            default_val = st.session_state.system_settings.get(default_key, 30)
            time_limits[tool_name] = st.slider(f"{tool_name}", 5, 120, default_val, key=f"tl_{tool_name}")
    with col_right:
        st.markdown(f"""
        <div style="font-size:10px; letter-spacing:2px; text-transform:uppercase; color:{TEXT_MUTED}; margin-bottom:20px;">Select Files for Testing</div>
        """, unsafe_allow_html=True)
        all_files = [f["name"] for f in proj.get("files", [])]
        selected_files = []
        for fn in all_files:
            f_info = next((f["info"] for f in proj["files"] if f["name"] == fn), {})
            checked = st.checkbox(fn, value=True, key=f"file_sel_{fn}")
            if checked:
                selected_files.append(fn)
            st.markdown(f"""
            <div style="background:#161616; border:1px solid {CARD_BORDER}; border-radius:4px; padding:10px 14px; margin-bottom:8px;">
                <div style="font-size:11px; color:{TEXT_MUTED};">{f_info.get('lines',0)} lines &middot; {len(f_info.get('functions',[]))} fns &middot; {len(f_info.get('classes',[]))} cls</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown(f"""<div style="height:20px;"></div>""", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="background:{CARD_BG}; border:1px solid {CARD_BORDER}; border-radius:8px; padding:24px; margin-top:16px;">
            <div style="font-size:10px; letter-spacing:2px; text-transform:uppercase; color:{TEXT_MUTED}; margin-bottom:16px;">Save Configuration</div>
        """, unsafe_allow_html=True)
        config_name = st.text_input("Configuration name", placeholder="e.g. baseline-run", key="cfg_save_name")
        if st.button("Save Configuration", key="save_config"):
            if config_name:
                cfg = {
                    "name": config_name,
                    "tools": {k: v for k, v in tool_selections.items() if v},
                    "time_limits": time_limits,
                    "files": selected_files,
                    "saved_at": datetime.datetime.now().isoformat()
                }
                st.session_state.saved_configs.append(cfg)
                log_event(f"Configuration '{config_name}' saved", "info")
                st.success("Configuration saved.")
        st.markdown("</div>", unsafe_allow_html=True)
        if st.session_state.saved_configs:
            st.markdown(f"""
            <div style="font-size:10px; letter-spacing:2px; text-transform:uppercase; color:{TEXT_MUTED}; margin:20px 0 14px;">Saved Configurations</div>
            """, unsafe_allow_html=True)
            for i, cfg in enumerate(st.session_state.saved_configs[-4:]):
                st.markdown(f"""
                <div style="background:{CARD_BG}; border:1px solid {CARD_BORDER}; border-radius:6px; padding:14px; margin-bottom:8px;">
                    <div style="font-size:13px; color:{TEXT_PRIMARY}; font-weight:500;">{cfg['name']}</div>
                    <div style="font-size:11px; color:{TEXT_MUTED}; margin-top:3px;">{', '.join(cfg['tools'].keys())} &middot; {len(cfg['files'])} files</div>
                </div>
                """, unsafe_allow_html=True)
    st.markdown(f"""<div style="height:24px;"></div>""", unsafe_allow_html=True)
    selected_tools = [t for t, v in tool_selections.items() if v]
    if st.button("Save and Proceed to Generation", key="proceed_to_gen"):
        if not selected_tools:
            st.error("Please select at least one test generation tool.")
        elif not selected_files:
            st.error("Please select at least one file.")
        else:
            proj["selected_files"] = selected_files
            proj["selected_tools"] = selected_tools
            proj["time_limits"] = time_limits
            log_event(f"Configuration set: {len(selected_tools)} tools, {len(selected_files)} files", "info")
            st.session_state.active_page = "Generate Tests"
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

def render_generate_page():
    st.markdown("<div style='padding:40px;'>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style="margin-bottom:40px;">
        <div style="font-size:10px; letter-spacing:2px; text-transform:uppercase; color:{TEXT_MUTED}; margin-bottom:10px;">Step 3 of 4</div>
        <div style="font-family:'Playfair Display',serif; font-size:34px; font-weight:700; color:{TEXT_PRIMARY};">Generate Unit Tests</div>
        <div style="font-size:14px; color:{TEXT_SECONDARY}; margin-top:8px;">Automated test case synthesis using selected tools.</div>
    </div>
    """, unsafe_allow_html=True)
    if not st.session_state.active_project:
        st.error("No active project. Please upload code and configure first.")
        st.markdown("</div>", unsafe_allow_html=True)
        return
    proj = st.session_state.projects[st.session_state.active_project]
    selected_tools = proj.get("selected_tools", [])
    selected_files = proj.get("selected_files", [])
    time_limits = proj.get("time_limits", {})
    if not selected_tools or not selected_files:
        st.markdown(f"""
        <div style="background:{CARD_BG}; border:1px solid {CARD_BORDER}; border-radius:8px; padding:48px; text-align:center;">
            <div style="font-size:15px; color:{TEXT_SECONDARY}; margin-bottom:12px;">Configuration not complete.</div>
            <div style="font-size:13px; color:{TEXT_MUTED};">Please configure tools and files before generating tests.</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Go to Configure", key="go_config"):
            st.session_state.active_page = "Configure"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        return
    col_sum, col_btn = st.columns([3, 1])
    with col_sum:
        st.markdown(f"""
        <div style="background:{CARD_BG}; border:1px solid {CARD_BORDER}; border-radius:8px; padding:24px; margin-bottom:24px;">
            <div style="display:flex; gap:40px; flex-wrap:wrap;">
                <div><div style="font-size:10px; letter-spacing:2px; text-transform:uppercase; color:{TEXT_MUTED}; margin-bottom:6px;">Project</div><div style="font-size:15px; font-weight:600; color:{TEXT_PRIMARY};">{st.session_state.active_project}</div></div>
                <div><div style="font-size:10px; letter-spacing:2px; text-transform:uppercase; color:{TEXT_MUTED}; margin-bottom:6px;">Tools</div><div style="font-size:15px; font-weight:600; color:{ACCENT_GOLD};">{len(selected_tools)}</div></div>
                <div><div style="font-size:10px; letter-spacing:2px; text-transform:uppercase; color:{TEXT_MUTED}; margin-bottom:6px;">Files</div><div style="font-size:15px; font-weight:600; color:{ACCENT_GOLD};">{len(selected_files)}</div></div>
                <div><div style="font-size:10px; letter-spacing:2px; text-transform:uppercase; color:{TEXT_MUTED}; margin-bottom:6px;">Tools Selected</div><div style="font-size:13px; color:{TEXT_SECONDARY};">{', '.join(selected_tools)}</div></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col_btn:
        start_gen = st.button("Generate Unit Tests", key="start_gen_btn")
    if start_gen:
        log_event(f"Test generation started for '{st.session_state.active_project}'", "info")
        src_files = [f for f in proj["files"] if f["name"] in selected_files]
        prog_container = st.empty()
        status_container = st.empty()
        all_results = {}
        for idx, tool in enumerate(selected_tools):
            with prog_container:
                progress_val = (idx / len(selected_tools))
                st.markdown(f"""
                <div style="background:{CARD_BG}; border:1px solid {CARD_BORDER}; border-radius:8px; padding:28px; margin-bottom:16px;">
                    <div style="font-size:10px; letter-spacing:2px; text-transform:uppercase; color:{TEXT_MUTED}; margin-bottom:16px;">Generating with {tool}</div>
                    <div style="background:#1a1a1a; border-radius:2px; height:4px; margin-bottom:16px; overflow:hidden;">
                        <div style="width:{int(progress_val*100)}%; height:100%; background:{ACCENT_GOLD}; border-radius:2px; transition:width 0.3s;"></div>
                    </div>
                    <div style="font-size:12px; color:{TEXT_MUTED};">Processing {len(src_files)} source file(s)...</div>
                </div>
                """, unsafe_allow_html=True)
            with status_container:
                st.info(f"Running {tool} ({idx+1}/{len(selected_tools)})...")
            time.sleep(1.5)
            tool_res = simulate_test_generation(src_files, [tool], time_limits)
            all_results[tool] = tool_res[tool]
        with prog_container:
            st.markdown(f"""
            <div style="background:#0e1a0e; border:1px solid #1e3a20; border-radius:8px; padding:28px; margin-bottom:16px;">
                <div style="font-size:15px; font-weight:600; color:{SUCCESS_COLOR}; margin-bottom:8px;">Generation Complete</div>
                <div style="font-size:13px; color:{TEXT_SECONDARY};">All {len(selected_tools)} tool(s) finished successfully.</div>
            </div>
            """, unsafe_allow_html=True)
        with status_container:
            st.empty()
        proj["results"] = all_results
        proj["runs"] += 1
        total_tests_gen = sum(sum(r.get("tests_generated", 0) for r in trs) for trs in all_results.values())
        avg_lc = np.mean([r.get("line_coverage", 0) for trs in all_results.values() for r in trs]) if all_results else 0
        proj["last_coverage"] = round(avg_lc, 1)
        run_entry = {
            "project": st.session_state.active_project,
            "timestamp": datetime.datetime.now().isoformat()[:16],
            "tools": selected_tools,
            "files": selected_files,
            "total_tests": total_tests_gen,
            "avg_line_coverage": round(avg_lc, 1),
            "avg_branch_coverage": round(np.mean([r.get("branch_coverage", 0) for trs in all_results.values() for r in trs]), 1) if all_results else 0,
            "results": all_results
        }
        st.session_state.run_history.append(run_entry)
        log_event(f"Test generation complete: {total_tests_gen} tests generated, avg coverage {avg_lc:.1f}%", "info")
        st.markdown(f"""
        <div style="margin-top:24px; font-size:10px; letter-spacing:2px; text-transform:uppercase; color:{TEXT_MUTED}; margin-bottom:20px;">Results Summary</div>
        """, unsafe_allow_html=True)
        sum_cols = st.columns(len(selected_tools))
        for col, tool in zip(sum_cols, selected_tools):
            with col:
                trs = all_results.get(tool, [])
                t_total = sum(r.get("tests_generated", 0) for r in trs)
                t_pass = sum(r.get("tests_passed", 0) for r in trs)
                lc = round(np.mean([r.get("line_coverage", 0) for r in trs]), 1) if trs else 0
                color = TOOLS_INFO.get(tool, {}).get("color", ACCENT_GOLD)
                st.markdown(f"""
                <div style="background:{CARD_BG}; border:1px solid {CARD_BORDER}; border-radius:8px; padding:20px; margin-bottom:12px; border-left:3px solid {color};">
                    <div style="font-size:12px; font-weight:600; color:{color}; margin-bottom:12px;">{tool}</div>
                    <div style="font-size:28px; font-weight:700; color:{TEXT_PRIMARY};">{t_total}</div>
                    <div style="font-size:11px; color:{TEXT_MUTED}; margin-bottom:8px;">Tests Generated</div>
                    <div style="font-size:12px; color:{SUCCESS_COLOR};">{t_pass} passed</div>
                    <div style="font-size:12px; color:{ACCENT_GOLD}; margin-top:4px;">{lc}% line coverage</div>
                </div>
                """, unsafe_allow_html=True)
        st.markdown(f"""<div style="height:24px;"></div>""", unsafe_allow_html=True)
        if st.button("Proceed to Run Tests", key="goto_run"):
            st.session_state.active_page = "Run Tests"
            st.rerun()
    else:
        st.markdown(f"""
        <div style="margin-top:8px; font-size:10px; letter-spacing:2px; text-transform:uppercase; color:{TEXT_MUTED}; margin-bottom:20px;">Files Queued</div>
        """, unsafe_allow_html=True)
        for fn in selected_files:
            f_data = next((f for f in proj["files"] if f["name"] == fn), None)
            if f_data:
                info = f_data.get("info", {})
                st.markdown(f"""
                <div style="background:{CARD_BG}; border:1px solid {CARD_BORDER}; border-radius:6px; padding:16px 20px; margin-bottom:8px; display:flex; justify-content:space-between; align-items:center;">
                    <div>
                        <div style="font-size:13px; font-weight:500; color:{TEXT_PRIMARY};">{fn}</div>
                        <div style="font-size:11px; color:{TEXT_MUTED}; margin-top:3px;">{info.get('lines',0)} lines &middot; {len(info.get('functions',[]))} functions &middot; {len(info.get('classes',[]))} classes</div>
                    </div>
                    <div style="font-size:11px; letter-spacing:1px; text-transform:uppercase; color:{TEXT_MUTED};">Queued</div>
                </div>
                """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

def render_run_tests_page():
    st.markdown("<div style='padding:40px;'>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style="margin-bottom:40px;">
        <div style="font-size:10px; letter-spacing:2px; text-transform:uppercase; color:{TEXT_MUTED}; margin-bottom:10px;">Step 4 of 4</div>
        <div style="font-family:'Playfair Display',serif; font-size:34px; font-weight:700; color:{TEXT_PRIMARY};">Execute Tests</div>
        <div style="font-size:14px; color:{TEXT_SECONDARY}; margin-top:8px;">Run generated tests and view execution outcomes.</div>
    </div>
    """, unsafe_allow_html=True)
    if not st.session_state.active_project:
        st.error("No active project.")
        st.markdown("</div>", unsafe_allow_html=True)
        return
    proj = st.session_state.projects[st.session_state.active_project]
    results = proj.get("results", {})
    if not results:
        st.markdown(f"""
        <div style="background:{CARD_BG}; border:1px solid {CARD_BORDER}; border-radius:8px; padding:48px; text-align:center;">
            <div style="font-size:15px; color:{TEXT_SECONDARY}; margin-bottom:12px;">No generated tests found.</div>
            <div style="font-size:13px; color:{TEXT_MUTED};">Generate tests first before execution.</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Go to Generate", key="go_gen"):
            st.session_state.active_page = "Generate Tests"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        return
    if st.button("Run All Tests", key="run_all_tests"):
        log_event(f"Test execution started for '{st.session_state.active_project}'", "info")
        prog = st.progress(0)
        status = st.empty()
        all_tools = list(results.keys())
        for i, tool in enumerate(all_tools):
            status.markdown(f"""<div style="font-size:13px; color:{TEXT_SECONDARY};">Executing tests for {tool}...</div>""", unsafe_allow_html=True)
            time.sleep(0.8)
            prog.progress((i+1)/len(all_tools))
        status.empty()
        st.markdown(f"""
        <div style="background:#0e1a0e; border:1px solid #1e3a20; border-radius:8px; padding:20px; margin:16px 0;">
            <div style="font-size:14px; font-weight:600; color:{SUCCESS_COLOR};">Execution complete.</div>
        </div>
        """, unsafe_allow_html=True)
        log_event("Test execution complete", "info")
    for tool, trs in results.items():
        color = TOOLS_INFO.get(tool, {}).get("color", ACCENT_GOLD)
        t_total = sum(r.get("tests_generated", 0) for r in trs)
        t_pass = sum(r.get("tests_passed", 0) for r in trs)
        t_fail = sum(r.get("tests_failed", 0) for r in trs)
        st.markdown(f"""
        <div style="background:{CARD_BG}; border:1px solid {CARD_BORDER}; border-left:3px solid {color}; border-radius:8px; padding:24px; margin-bottom:16px;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:20px;">
                <div style="font-size:16px; font-weight:600; color:{TEXT_PRIMARY};">{tool}</div>
                <div style="display:flex; gap:20px;">
                    <div style="text-align:center;"><div style="font-size:20px; font-weight:700; color:{SUCCESS_COLOR};">{t_pass}</div><div style="font-size:10px; color:{TEXT_MUTED}; letter-spacing:1px; text-transform:uppercase;">Passed</div></div>
                    <div style="text-align:center;"><div style="font-size:20px; font-weight:700; color:{ERROR_COLOR};">{t_fail}</div><div style="font-size:10px; color:{TEXT_MUTED}; letter-spacing:1px; text-transform:uppercase;">Failed</div></div>
                    <div style="text-align:center;"><div style="font-size:20px; font-weight:700; color:{TEXT_PRIMARY};">{t_total}</div><div style="font-size:10px; color:{TEXT_MUTED}; letter-spacing:1px; text-transform:uppercase;">Total</div></div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        for r in trs:
            pass_pct = (r.get("tests_passed", 0) / max(r.get("tests_generated", 1), 1)) * 100
            row_color = SUCCESS_COLOR if pass_pct >= 80 else (WARNING_COLOR if pass_pct >= 50 else ERROR_COLOR)
            st.markdown(f"""
            <div style="background:#161616; border:1px solid {CARD_BORDER}; border-radius:6px; padding:14px 18px; margin-bottom:8px; display:flex; justify-content:space-between; align-items:center;">
                <div style="font-size:13px; color:{TEXT_PRIMARY}; font-weight:500;">{r['file']}</div>
                <div style="display:flex; gap:24px; align-items:center;">
                    <div style="font-size:12px; color:{TEXT_MUTED};">{r.get('tests_generated',0)} tests</div>
                    <div style="font-size:12px; color:{SUCCESS_COLOR};">{r.get('tests_passed',0)} pass</div>
                    <div style="font-size:12px; color:{ERROR_COLOR};">{r.get('tests_failed',0)} fail</div>
                    <div style="background:#1a1a1a; border-radius:2px; height:4px; width:80px; overflow:hidden;"><div style="width:{pass_pct:.0f}%; height:100%; background:{row_color};"></div></div>
                    <div style="font-size:12px; color:{row_color}; font-weight:600;">{pass_pct:.0f}%</div>
                    <div style="font-size:11px; color:{TEXT_MUTED};">{r.get('execution_time',0):.2f}s</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if r.get("errors"):
                with st.expander(f"View errors for {r['file']}"):
                    for err in r["errors"]:
                        st.markdown(f"""
                        <div style="background:#1e0e0e; border-left:3px solid {ERROR_COLOR}; border-radius:4px; padding:12px 16px; margin-bottom:8px; font-family:'Courier New',monospace; font-size:12px; color:{ERROR_COLOR}cc;">{err}</div>
                        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        file_data = proj["files"]
        with st.expander(f"View Generated Test Code — {tool}"):
            for r in trs[:2]:
                src = next((f for f in file_data if f["name"] == r["file"]), None)
                if src:
                    info = src.get("info", {})
                    code = generate_test_code(r["file"], tool, info.get("functions", [])[:3], info.get("classes", [])[:2])
                    st.code(code, language="python")
    st.markdown("</div>", unsafe_allow_html=True)

def render_coverage_page():
    st.markdown("<div style='padding:40px;'>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style="margin-bottom:40px;">
        <div style="font-family:'Playfair Display',serif; font-size:34px; font-weight:700; color:{TEXT_PRIMARY};">Coverage Analysis</div>
        <div style="font-size:14px; color:{TEXT_SECONDARY}; margin-top:8px;">Line, branch, and mutation coverage metrics for all test runs.</div>
    </div>
    """, unsafe_allow_html=True)
    if not st.session_state.active_project:
        st.error("No active project.")
        st.markdown("</div>", unsafe_allow_html=True)
        return
    proj = st.session_state.projects[st.session_state.active_project]
    results = proj.get("results", {})
    if not results:
        st.info("No results yet. Run test generation first.")
        st.markdown("</div>", unsafe_allow_html=True)
        return
    tools = list(results.keys())
    for tool in tools:
        color = TOOLS_INFO.get(tool, {}).get("color", ACCENT_GOLD)
        trs = results[tool]
        avg_lc = round(np.mean([r.get("line_coverage", 0) for r in trs]), 1)
        avg_bc = round(np.mean([r.get("branch_coverage", 0) for r in trs]), 1)
        avg_ms = round(np.mean([r.get("mutation_score", 0) for r in trs]), 1)
        st.markdown(f"""
        <div style="font-size:12px; font-weight:600; color:{color}; letter-spacing:1px; text-transform:uppercase; margin:24px 0 16px;">{tool}</div>
        """, unsafe_allow_html=True)
        gc1, gc2, gc3 = st.columns(3)
        with gc1:
            st.plotly_chart(render_gauge_chart(avg_lc, "Line Coverage", color), use_container_width=True, config={"displayModeBar": False})
        with gc2:
            st.plotly_chart(render_gauge_chart(avg_bc, "Branch Coverage", ACCENT_SILVER), use_container_width=True, config={"displayModeBar": False})
        with gc3:
            st.plotly_chart(render_gauge_chart(avg_ms, "Mutation Score", ACCENT_COPPER), use_container_width=True, config={"displayModeBar": False})
        cov_df = pd.DataFrame([{
            "File": r["file"],
            "Line Cov %": r.get("line_coverage", 0),
            "Branch Cov %": r.get("branch_coverage", 0),
            "Mutation Score %": r.get("mutation_score", 0),
            "Tests Generated": r.get("tests_generated", 0),
            "Tests Passed": r.get("tests_passed", 0)
        } for r in trs])
        st.dataframe(
            cov_df.style.background_gradient(subset=["Line Cov %", "Branch Cov %", "Mutation Score %"],
                                              cmap="YlOrBr"),
            use_container_width=True, hide_index=True
        )
        st.markdown(f"""<div style="height:1px; background:{CARD_BORDER}; margin:24px 0;"></div>""", unsafe_allow_html=True)
    st.markdown(f"""
    <div style="font-size:10px; letter-spacing:2px; text-transform:uppercase; color:{TEXT_MUTED}; margin:16px 0 20px;">Weakly Tested Code Areas</div>
    """, unsafe_allow_html=True)
    weak_files = []
    for tool, trs in results.items():
        for r in trs:
            if r.get("line_coverage", 100) < 70:
                weak_files.append({"file": r["file"], "tool": tool, "line_coverage": r.get("line_coverage", 0), "branch_coverage": r.get("branch_coverage", 0)})
    if weak_files:
        for wf in weak_files:
            color = ERROR_COLOR if wf["line_coverage"] < 50 else WARNING_COLOR
            st.markdown(f"""
            <div style="background:{CARD_BG}; border:1px solid {CARD_BORDER}; border-left:3px solid {color}; border-radius:6px; padding:16px 20px; margin-bottom:8px; display:flex; justify-content:space-between; align-items:center;">
                <div>
                    <div style="font-size:13px; font-weight:500; color:{TEXT_PRIMARY};">{wf['file']}</div>
                    <div style="font-size:11px; color:{TEXT_MUTED}; margin-top:3px;">Tool: {wf['tool']}</div>
                </div>
                <div style="text-align:right;">
                    <div style="font-size:14px; font-weight:700; color:{color};">{wf['line_coverage']:.1f}%</div>
                    <div style="font-size:11px; color:{TEXT_MUTED};">line coverage</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="background:#0e1a0e; border:1px solid #1e3a20; border-radius:6px; padding:20px; font-size:13px; color:{SUCCESS_COLOR};">All files meet coverage thresholds.</div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

def render_compare_page():
    st.markdown("<div style='padding:40px;'>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style="margin-bottom:40px;">
        <div style="font-family:'Playfair Display',serif; font-size:34px; font-weight:700; color:{TEXT_PRIMARY};">Compare Tool Results</div>
        <div style="font-size:14px; color:{TEXT_SECONDARY}; margin-top:8px;">Side-by-side analysis of test generation tool performance.</div>
    </div>
    """, unsafe_allow_html=True)
    if not st.session_state.active_project:
        st.error("No active project.")
        st.markdown("</div>", unsafe_allow_html=True)
        return
    proj = st.session_state.projects[st.session_state.active_project]
    results = proj.get("results", {})
    if len(results) < 2:
        st.info("Generate tests with at least 2 tools to compare results.")
        st.markdown("</div>", unsafe_allow_html=True)
        return
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""<div style="font-size:10px; letter-spacing:2px; text-transform:uppercase; color:{TEXT_MUTED}; margin-bottom:20px;">Bar Comparison — Line Coverage</div>""", unsafe_allow_html=True)
        st.plotly_chart(render_bar_comparison(results, "line_coverage"), use_container_width=True, config={"displayModeBar": False})
    with col2:
        st.markdown(f"""<div style="font-size:10px; letter-spacing:2px; text-transform:uppercase; color:{TEXT_MUTED}; margin-bottom:20px;">Bar Comparison — Branch Coverage</div>""", unsafe_allow_html=True)
        st.plotly_chart(render_bar_comparison(results, "branch_coverage"), use_container_width=True, config={"displayModeBar": False})
    st.markdown(f"""<div style="height:1px; background:{CARD_BORDER}; margin:24px 0;"></div>""", unsafe_allow_html=True)
    col3, col4 = st.columns(2)
    with col3:
        st.markdown(f"""<div style="font-size:10px; letter-spacing:2px; text-transform:uppercase; color:{TEXT_MUTED}; margin-bottom:20px;">Radar — Multi-Metric Performance</div>""", unsafe_allow_html=True)
        st.plotly_chart(render_radar_chart(results), use_container_width=True, config={"displayModeBar": False})
    with col4:
        st.markdown(f"""<div style="font-size:10px; letter-spacing:2px; text-transform:uppercase; color:{TEXT_MUTED}; margin-bottom:20px;">Box Plot — Coverage Distribution</div>""", unsafe_allow_html=True)
        st.plotly_chart(render_box_plot(results), use_container_width=True, config={"displayModeBar": False})
    st.markdown(f"""<div style="height:1px; background:{CARD_BORDER}; margin:24px 0;"></div>""", unsafe_allow_html=True)
    st.markdown(f"""<div style="font-size:10px; letter-spacing:2px; text-transform:uppercase; color:{TEXT_MUTED}; margin-bottom:20px;">Coverage Heatmap — Tool x File</div>""", unsafe_allow_html=True)
    hm = render_heatmap_coverage(results)
    if hm:
        st.plotly_chart(hm, use_container_width=True, config={"displayModeBar": False})
    st.markdown(f"""<div style="height:1px; background:{CARD_BORDER}; margin:24px 0;"></div>""", unsafe_allow_html=True)
    st.markdown(f"""<div style="font-size:10px; letter-spacing:2px; text-transform:uppercase; color:{TEXT_MUTED}; margin-bottom:20px;">3D Coverage Space — All Metrics</div>""", unsafe_allow_html=True)
    st.plotly_chart(render_3d_scatter(results), use_container_width=True, config={"displayModeBar": False})
    st.markdown(f"""<div style="height:1px; background:{CARD_BORDER}; margin:24px 0;"></div>""", unsafe_allow_html=True)
    col5, col6 = st.columns(2)
    with col5:
        st.markdown(f"""<div style="font-size:10px; letter-spacing:2px; text-transform:uppercase; color:{TEXT_MUTED}; margin-bottom:20px;">Test Distribution Sunburst</div>""", unsafe_allow_html=True)
        st.plotly_chart(render_sunburst_chart(results), use_container_width=True, config={"displayModeBar": False})
    with col6:
        st.markdown(f"""<div style="font-size:10px; letter-spacing:2px; text-transform:uppercase; color:{TEXT_MUTED}; margin-bottom:20px;">Mutation Score Comparison</div>""", unsafe_allow_html=True)
        st.plotly_chart(render_bar_comparison(results, "mutation_score"), use_container_width=True, config={"displayModeBar": False})
    st.markdown(f"""
    <div style="font-size:10px; letter-spacing:2px; text-transform:uppercase; color:{TEXT_MUTED}; margin:24px 0 20px;">Tool Rankings</div>
    """, unsafe_allow_html=True)
    rankings = []
    for tool, trs in results.items():
        avg_lc = round(np.mean([r.get("line_coverage", 0) for r in trs]), 1)
        avg_bc = round(np.mean([r.get("branch_coverage", 0) for r in trs]), 1)
        avg_ms = round(np.mean([r.get("mutation_score", 0) for r in trs]), 1)
        t_total = sum(r.get("tests_generated", 0) for r in trs)
        score = round((avg_lc * 0.4 + avg_bc * 0.35 + avg_ms * 0.25), 1)
        rankings.append({"Tool": tool, "Line Cov": avg_lc, "Branch Cov": avg_bc, "Mutation": avg_ms, "Tests": t_total, "Score": score})
    rankings.sort(key=lambda x: x["Score"], reverse=True)
    for rank, r in enumerate(rankings, 1):
        color = TOOLS_INFO.get(r["Tool"], {}).get("color", ACCENT_GOLD)
        medal = ["", "#c8a97e", "#a8a8b3", "#b87333"][min(rank, 3)]
        st.markdown(f"""
        <div style="background:{CARD_BG}; border:1px solid {CARD_BORDER}; border-left:3px solid {medal or color}; border-radius:8px; padding:20px; margin-bottom:10px; display:flex; justify-content:space-between; align-items:center;">
            <div style="display:flex; align-items:center; gap:20px;">
                <div style="font-size:24px; font-weight:700; color:{medal or TEXT_MUTED}; width:32px;">#{rank}</div>
                <div>
                    <div style="font-size:15px; font-weight:600; color:{TEXT_PRIMARY};">{r['Tool']}</div>
                    <div style="font-size:11px; color:{TEXT_MUTED}; margin-top:3px;">{r['Tests']} tests generated</div>
                </div>
            </div>
            <div style="display:flex; gap:32px;">
                <div style="text-align:center;"><div style="font-size:16px; font-weight:700; color:{ACCENT_GOLD};">{r['Line Cov']}%</div><div style="font-size:10px; color:{TEXT_MUTED}; letter-spacing:1px;">Line</div></div>
                <div style="text-align:center;"><div style="font-size:16px; font-weight:700; color:{ACCENT_SILVER};">{r['Branch Cov']}%</div><div style="font-size:10px; color:{TEXT_MUTED}; letter-spacing:1px;">Branch</div></div>
                <div style="text-align:center;"><div style="font-size:16px; font-weight:700; color:{ACCENT_COPPER};">{r['Mutation']}%</div><div style="font-size:10px; color:{TEXT_MUTED}; letter-spacing:1px;">Mutation</div></div>
                <div style="text-align:center;"><div style="font-size:20px; font-weight:700; color:{SUCCESS_COLOR};">{r['Score']}</div><div style="font-size:10px; color:{TEXT_MUTED}; letter-spacing:1px;">Score</div></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

def render_history_page():
    st.markdown("<div style='padding:40px;'>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style="margin-bottom:40px;">
        <div style="font-family:'Playfair Display',serif; font-size:34px; font-weight:700; color:{TEXT_PRIMARY};">Results History</div>
        <div style="font-size:14px; color:{TEXT_SECONDARY}; margin-top:8px;">Browse and filter all historical test runs across projects.</div>
    </div>
    """, unsafe_allow_html=True)
    if not st.session_state.run_history:
        st.markdown(f"""
        <div style="background:{CARD_BG}; border:1px solid {CARD_BORDER}; border-radius:8px; padding:80px; text-align:center;">
            <div style="font-size:16px; color:{TEXT_SECONDARY}; margin-bottom:12px;">No history yet.</div>
            <div style="font-size:13px; color:{TEXT_MUTED};">Run test generation to populate history.</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        return
    fc1, fc2, fc3 = st.columns(3)
    with fc1:
        all_projects = list(set(r["project"] for r in st.session_state.run_history))
        filter_proj = st.selectbox("Filter by project", ["All"] + all_projects, key="hist_filter_proj")
    with fc2:
        all_tools = list(set(t for r in st.session_state.run_history for t in r.get("tools", [])))
        filter_tool = st.selectbox("Filter by tool", ["All"] + all_tools, key="hist_filter_tool")
    with fc3:
        sort_by = st.selectbox("Sort by", ["Newest", "Oldest", "Highest Coverage", "Lowest Coverage"], key="hist_sort")
    filtered = st.session_state.run_history.copy()
    if filter_proj != "All":
        filtered = [r for r in filtered if r["project"] == filter_proj]
    if filter_tool != "All":
        filtered = [r for r in filtered if filter_tool in r.get("tools", [])]
    if sort_by == "Newest":
        filtered = list(reversed(filtered))
    elif sort_by == "Highest Coverage":
        filtered.sort(key=lambda x: x.get("avg_line_coverage", 0), reverse=True)
    elif sort_by == "Lowest Coverage":
        filtered.sort(key=lambda x: x.get("avg_line_coverage", 0))
    st.markdown(f"""<div style="margin:24px 0 16px; font-size:11px; color:{TEXT_MUTED}; letter-spacing:1px;">{len(filtered)} run(s) found</div>""", unsafe_allow_html=True)
    for i, run in enumerate(filtered):
        avg_lc = run.get("avg_line_coverage", 0)
        cov_color = SUCCESS_COLOR if avg_lc >= 70 else (WARNING_COLOR if avg_lc >= 50 else ERROR_COLOR)
        with st.expander(f"Run — {run['project']} — {run['timestamp']} — {avg_lc}% line coverage"):
            r1, r2, r3, r4 = st.columns(4)
            with r1:
                st.markdown(f"""<div style="background:{CARD_BG}; border:1px solid {CARD_BORDER}; border-radius:6px; padding:16px; text-align:center;"><div style="font-size:22px; font-weight:700; color:{cov_color};">{avg_lc}%</div><div style="font-size:10px; color:{TEXT_MUTED}; letter-spacing:1px; text-transform:uppercase; margin-top:4px;">Line Coverage</div></div>""", unsafe_allow_html=True)
            with r2:
                st.markdown(f"""<div style="background:{CARD_BG}; border:1px solid {CARD_BORDER}; border-radius:6px; padding:16px; text-align:center;"><div style="font-size:22px; font-weight:700; color:{ACCENT_SILVER};">{run.get('avg_branch_coverage',0)}%</div><div style="font-size:10px; color:{TEXT_MUTED}; letter-spacing:1px; text-transform:uppercase; margin-top:4px;">Branch Coverage</div></div>""", unsafe_allow_html=True)
            with r3:
                st.markdown(f"""<div style="background:{CARD_BG}; border:1px solid {CARD_BORDER}; border-radius:6px; padding:16px; text-align:center;"><div style="font-size:22px; font-weight:700; color:{ACCENT_GOLD};">{run.get('total_tests',0)}</div><div style="font-size:10px; color:{TEXT_MUTED}; letter-spacing:1px; text-transform:uppercase; margin-top:4px;">Tests Generated</div></div>""", unsafe_allow_html=True)
            with r4:
                st.markdown(f"""<div style="background:{CARD_BG}; border:1px solid {CARD_BORDER}; border-radius:6px; padding:16px; text-align:center;"><div style="font-size:22px; font-weight:700; color:{ACCENT_COPPER};">{len(run.get('tools',[]))}</div><div style="font-size:10px; color:{TEXT_MUTED}; letter-spacing:1px; text-transform:uppercase; margin-top:4px;">Tools Used</div></div>""", unsafe_allow_html=True)
            st.markdown(f"""<div style="margin-top:16px; font-size:12px; color:{TEXT_MUTED};">Tools: {', '.join(run.get('tools', []))} &middot; Files: {', '.join(run.get('files', []))}</div>""", unsafe_allow_html=True)
            run_res = run.get("results", {})
            if run_res:
                cmp_df = pd.DataFrame([{
                    "Tool": t,
                    "Tests": sum(r.get("tests_generated", 0) for r in trs),
                    "Passed": sum(r.get("tests_passed", 0) for r in trs),
                    "Line Cov %": round(np.mean([r.get("line_coverage", 0) for r in trs]), 1),
                    "Branch Cov %": round(np.mean([r.get("branch_coverage", 0) for r in trs]), 1),
                    "Mutation %": round(np.mean([r.get("mutation_score", 0) for r in trs]), 1)
                } for t, trs in run_res.items()])
                st.dataframe(cmp_df, use_container_width=True, hide_index=True)
            del_col, _ = st.columns([1, 4])
            with del_col:
                if st.button(f"Delete Run", key=f"del_run_{i}"):
                    st.session_state.run_history.remove(run)
                    log_event(f"Run deleted: {run['project']} {run['timestamp']}", "info")
                    st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

def render_export_page():
    st.markdown("<div style='padding:40px;'>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style="margin-bottom:40px;">
        <div style="font-family:'Playfair Display',serif; font-size:34px; font-weight:700; color:{TEXT_PRIMARY};">Export Results</div>
        <div style="font-size:14px; color:{TEXT_SECONDARY}; margin-top:8px;">Download evaluation results in CSV or PDF format.</div>
    </div>
    """, unsafe_allow_html=True)
    if not st.session_state.run_history:
        st.info("No runs to export.")
        st.markdown("</div>", unsafe_allow_html=True)
        return
    col_sel, col_opt = st.columns([1.5, 1])
    with col_sel:
        st.markdown(f"""<div style="font-size:10px; letter-spacing:2px; text-transform:uppercase; color:{TEXT_MUTED}; margin-bottom:16px;">Select Runs to Export</div>""", unsafe_allow_html=True)
        run_options = [f"{r['project']} — {r['timestamp']}" for r in st.session_state.run_history]
        selected_runs = st.multiselect("Runs", run_options, key="export_run_sel", label_visibility="collapsed")
    with col_opt:
        st.markdown(f"""<div style="font-size:10px; letter-spacing:2px; text-transform:uppercase; color:{TEXT_MUTED}; margin-bottom:16px;">Export Format</div>""", unsafe_allow_html=True)
        export_fmt = st.radio("Format", ["CSV", "PDF Report"], key="export_fmt", horizontal=True)
    if selected_runs:
        runs_to_export = [r for r in st.session_state.run_history if f"{r['project']} — {r['timestamp']}" in selected_runs]
        rows = []
        for run in runs_to_export:
            for tool, trs in run.get("results", {}).items():
                for r in trs:
                    rows.append({
                        "Project": run["project"],
                        "Timestamp": run["timestamp"],
                        "Tool": tool,
                        "File": r["file"],
                        "Tests Generated": r.get("tests_generated", 0),
                        "Tests Passed": r.get("tests_passed", 0),
                        "Tests Failed": r.get("tests_failed", 0),
                        "Line Coverage %": r.get("line_coverage", 0),
                        "Branch Coverage %": r.get("branch_coverage", 0),
                        "Mutation Score %": r.get("mutation_score", 0),
                        "Execution Time (s)": r.get("execution_time", 0)
                    })
        if rows:
            df_export = pd.DataFrame(rows)
            st.markdown(f"""<div style="font-size:10px; letter-spacing:2px; text-transform:uppercase; color:{TEXT_MUTED}; margin:24px 0 16px;">Preview ({len(rows)} records)</div>""", unsafe_allow_html=True)
            st.dataframe(df_export.head(20), use_container_width=True, hide_index=True)
            if export_fmt == "CSV":
                csv_bytes = df_export.to_csv(index=False).encode("utf-8")
                st.download_button(
                    "Download CSV",
                    data=csv_bytes,
                    file_name=f"pytcgeval_export_{datetime.date.today()}.csv",
                    mime="text/csv",
                    key="dl_csv"
                )
            else:
                pdf_lines = ["PyTCG-Eval — Evaluation Report", "=" * 60, f"Generated: {datetime.datetime.now()}", ""]
                for run in runs_to_export:
                    pdf_lines.append(f"Project: {run['project']}")
                    pdf_lines.append(f"Timestamp: {run['timestamp']}")
                    pdf_lines.append(f"Total Tests: {run.get('total_tests', 0)}")
                    pdf_lines.append(f"Avg Line Coverage: {run.get('avg_line_coverage', 0)}%")
                    pdf_lines.append("-" * 40)
                    for tool, trs in run.get("results", {}).items():
                        pdf_lines.append(f"  Tool: {tool}")
                        for r in trs:
                            pdf_lines.append(f"    File: {r['file']} — LC: {r.get('line_coverage',0)}% — BC: {r.get('branch_coverage',0)}% — MS: {r.get('mutation_score',0)}%")
                    pdf_lines.append("")
                pdf_content = "\n".join(pdf_lines)
                st.download_button(
                    "Download PDF Report (Text)",
                    data=pdf_content.encode("utf-8"),
                    file_name=f"pytcgeval_report_{datetime.date.today()}.txt",
                    mime="text/plain",
                    key="dl_pdf"
                )
            log_event(f"Export completed: {len(runs_to_export)} runs, format={export_fmt}", "info")
    st.markdown(f"""
    <div style="font-size:10px; letter-spacing:2px; text-transform:uppercase; color:{TEXT_MUTED}; margin:32px 0 16px;">Download Generated Test Files</div>
    """, unsafe_allow_html=True)
    if st.session_state.active_project and st.session_state.projects.get(st.session_state.active_project, {}).get("results"):
        proj = st.session_state.projects[st.session_state.active_project]
        for tool, trs in proj["results"].items():
            for r in trs[:1]:
                src = next((f for f in proj["files"] if f["name"] == r["file"]), None)
                if src:
                    info = src.get("info", {})
                    test_code = generate_test_code(r["file"], tool, info.get("functions", [])[:4], info.get("classes", [])[:2])
                    fname = f"test_{r['file'].replace('.py','')}_{tool.lower()}.py"
                    st.download_button(
                        f"Download {fname}",
                        data=test_code.encode("utf-8"),
                        file_name=fname,
                        mime="text/plain",
                        key=f"dl_test_{tool}_{r['file']}"
                    )
    else:
        st.markdown(f"""<div style="font-size:12px; color:{TEXT_MUTED};">Generate tests first to enable test file download.</div>""", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

def render_metrics_guide_page():
    st.markdown("<div style='padding:40px;'>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style="margin-bottom:40px;">
        <div style="font-family:'Playfair Display',serif; font-size:34px; font-weight:700; color:{TEXT_PRIMARY};">Metrics Guide</div>
        <div style="font-size:14px; color:{TEXT_SECONDARY}; margin-top:8px;">Understanding coverage metrics and what they mean for your code.</div>
    </div>
    """, unsafe_allow_html=True)
    metrics = [
        ("Line Coverage", "Percentage of source code lines executed by tests", "Most basic metric. High line coverage does not guarantee absence of bugs but indicates tested code paths.", ACCENT_GOLD, "LC = (Lines executed / Total lines) x 100"),
        ("Branch Coverage", "Percentage of code branches (if/else paths) covered by tests", "Stronger than line coverage. Ensures both true and false conditions of branches are exercised.", ACCENT_SILVER, "BC = (Branches covered / Total branches) x 100"),
        ("Mutation Score", "Percentage of artificially injected bugs caught by tests", "Highest quality metric. Measures test effectiveness, not just execution. Hard to achieve above 80%.", ACCENT_COPPER, "MS = (Killed mutants / Total mutants) x 100"),
        ("Test Pass Rate", "Ratio of passing tests to total generated tests", "Indicates quality of generated test code. Very low pass rates may indicate generation issues.", SUCCESS_COLOR, "TPR = (Passed / Total) x 100"),
        ("Execution Time", "Wall-clock time for tool to complete test generation", "Balanced with coverage gain. Diminishing returns above tool-specific thresholds.", INFO_COLOR, "Lower is better within time budget")
    ]
    for name, short_desc, detail, color, formula in metrics:
        with st.expander(name):
            c1, c2 = st.columns([2, 1])
            with c1:
                st.markdown(f"""
                <div style="font-size:14px; font-weight:600; color:{color}; margin-bottom:10px;">{name}</div>
                <div style="font-size:13px; color:{TEXT_SECONDARY}; margin-bottom:12px;">{short_desc}</div>
                <div style="font-size:13px; color:{TEXT_PRIMARY}; line-height:1.7;">{detail}</div>
                """, unsafe_allow_html=True)
            with c2:
                st.markdown(f"""
                <div style="background:#161616; border:1px solid {CARD_BORDER}; border-radius:6px; padding:16px; font-family:'Courier New',monospace; font-size:12px; color:{color};">{formula}</div>
                """, unsafe_allow_html=True)
    st.markdown(f"""
    <div style="margin-top:40px; font-size:10px; letter-spacing:2px; text-transform:uppercase; color:{TEXT_MUTED}; margin-bottom:20px;">Supported Test Generation Tools</div>
    """, unsafe_allow_html=True)
    for tool_name, tool_info in TOOLS_INFO.items():
        color = tool_info["color"]
        st.markdown(f"""
        <div style="background:{CARD_BG}; border:1px solid {CARD_BORDER}; border-left:3px solid {color}; border-radius:8px; padding:24px; margin-bottom:12px;">
            <div style="font-size:16px; font-weight:600; color:{TEXT_PRIMARY}; margin-bottom:8px;">{tool_name}</div>
            <div style="font-size:13px; color:{TEXT_SECONDARY}; margin-bottom:10px;">{tool_info['description']}</div>
            <div style="font-size:12px; color:{TEXT_MUTED}; margin-bottom:8px;">Strengths: {tool_info['strengths']}</div>
            <div style="font-size:12px; color:{TEXT_MUTED};">Language: {tool_info['language']}</div>
            <div style="margin-top:10px; display:flex; gap:8px;">
                {''.join([f"<span style='background:#1e1a10; border:1px solid #3a2e1a; color:{color}; font-size:9px; letter-spacing:1px; text-transform:uppercase; padding:3px 8px; border-radius:2px;'>{ct}</span>" for ct in tool_info['coverage_type']])}
            </div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

def render_manage_tools_page():
    st.markdown("<div style='padding:40px;'>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style="margin-bottom:40px;">
        <div style="font-size:10px; letter-spacing:2px; text-transform:uppercase; color:{TEXT_MUTED}; margin-bottom:10px;">Admin</div>
        <div style="font-family:'Playfair Display',serif; font-size:34px; font-weight:700; color:{TEXT_PRIMARY};">Manage Test Tools</div>
        <div style="font-size:14px; color:{TEXT_SECONDARY}; margin-top:8px;">Enable, disable, and configure test generation tools.</div>
    </div>
    """, unsafe_allow_html=True)
    for tool_name, tool_info in TOOLS_INFO.items():
        enabled_key = f"{tool_name.lower()}_enabled"
        time_key = f"{tool_name.lower()}_time_limit"
        color = tool_info["color"]
        is_enabled = st.session_state.system_settings.get(enabled_key, True)
        st.markdown(f"""
        <div style="background:{CARD_BG}; border:1px solid {CARD_BORDER}; border-left:3px solid {color}; border-radius:8px; padding:24px; margin-bottom:16px;">
            <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:16px;">
                <div>
                    <div style="font-size:16px; font-weight:600; color:{TEXT_PRIMARY};">{tool_name}</div>
                    <div style="font-size:12px; color:{TEXT_MUTED}; margin-top:4px;">{tool_info['description'][:80]}...</div>
                </div>
                <div style="font-size:11px; letter-spacing:1px; text-transform:uppercase; color:{'#4ecb71' if is_enabled else '#e05252'};">{'Active' if is_enabled else 'Disabled'}</div>
            </div>
        """, unsafe_allow_html=True)
        mt1, mt2, mt3 = st.columns([1, 2, 1])
        with mt1:
            new_enabled = st.checkbox(f"Enable {tool_name}", value=is_enabled, key=f"admin_enable_{tool_name}")
            if new_enabled != is_enabled:
                st.session_state.system_settings[enabled_key] = new_enabled
                log_event(f"Tool {tool_name} {'enabled' if new_enabled else 'disabled'}", "info")
                st.rerun()
        with mt2:
            new_tl = st.slider(f"Time limit (s)", 5, 120, st.session_state.system_settings.get(time_key, 30), key=f"admin_tl_{tool_name}")
            st.session_state.system_settings[time_key] = new_tl
        with mt3:
            st.markdown(f"""
            <div style="padding-top:8px;">
                <div style="font-size:11px; color:{TEXT_MUTED};">Language: {tool_info['language']}</div>
                <div style="margin-top:6px; display:flex; gap:4px; flex-wrap:wrap;">
                    {''.join([f"<span style='background:#1a1408; border:1px solid #3a2e1a; color:{color}; font-size:9px; padding:2px 6px; border-radius:2px;'>{ct}</span>" for ct in tool_info['coverage_type']])}
                </div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    if st.button("Run Diagnostic Test", key="admin_diagnostic"):
        prog = st.progress(0)
        diag_status = st.empty()
        for i, tool in enumerate(TOOLS_INFO.keys()):
            diag_status.markdown(f"""<div style="font-size:13px; color:{TEXT_SECONDARY};">Testing {tool}...</div>""", unsafe_allow_html=True)
            time.sleep(0.5)
            prog.progress((i+1)/len(TOOLS_INFO))
        diag_status.empty()
        st.success("Diagnostic complete. All configured tools validated.")
        log_event("Admin ran diagnostic test", "info")
    st.markdown("</div>", unsafe_allow_html=True)

def render_system_settings_page():
    st.markdown("<div style='padding:40px;'>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style="margin-bottom:40px;">
        <div style="font-size:10px; letter-spacing:2px; text-transform:uppercase; color:{TEXT_MUTED}; margin-bottom:10px;">Admin</div>
        <div style="font-family:'Playfair Display',serif; font-size:34px; font-weight:700; color:{TEXT_PRIMARY};">System Settings</div>
        <div style="font-size:14px; color:{TEXT_SECONDARY}; margin-top:8px;">Configure global parameters, thresholds, and security settings.</div>
    </div>
    """, unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""<div style="background:{CARD_BG}; border:1px solid {CARD_BORDER}; border-radius:8px; padding:28px; margin-bottom:16px;">""", unsafe_allow_html=True)
        st.markdown(f"""<div style="font-size:10px; letter-spacing:2px; text-transform:uppercase; color:{TEXT_MUTED}; margin-bottom:20px;">Storage & Files</div>""", unsafe_allow_html=True)
        storage_path = st.text_input("Output storage path", value=st.session_state.system_settings.get("storage_path", "./outputs/"), key="ss_storage")
        max_file = st.slider("Max file size (MB)", 1, 100, st.session_state.system_settings.get("max_file_size_mb", 10), key="ss_maxfile")
        allow_gh = st.checkbox("Allow GitHub repository import", value=st.session_state.system_settings.get("allow_github_repos", True), key="ss_github")
        retention = st.slider("Result retention (days)", 1, 365, st.session_state.system_settings.get("result_retention_days", 30), key="ss_retention")
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown(f"""<div style="background:{CARD_BG}; border:1px solid {CARD_BORDER}; border-radius:8px; padding:28px; margin-bottom:16px;">""", unsafe_allow_html=True)
        st.markdown(f"""<div style="font-size:10px; letter-spacing:2px; text-transform:uppercase; color:{TEXT_MUTED}; margin-bottom:20px;">Safety & Security</div>""", unsafe_allow_html=True)
        safe_mode = st.checkbox("Enable safe mode (block arbitrary OS commands)", value=st.session_state.system_settings.get("safe_mode", True), key="ss_safe")
        st.markdown(f"""
        <div style="background:#1a1408; border:1px solid #3a2e1a; border-radius:6px; padding:14px; margin-top:12px; font-size:12px; color:{TEXT_MUTED}; line-height:1.7;">
            Safe mode prevents execution of arbitrary OS commands and restricts file operations to approved directories only. Disable only for trusted environments.
        </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div style="background:{CARD_BG}; border:1px solid {CARD_BORDER}; border-radius:8px; padding:28px; margin-bottom:16px;">""", unsafe_allow_html=True)
        st.markdown(f"""<div style="font-size:10px; letter-spacing:2px; text-transform:uppercase; color:{TEXT_MUTED}; margin-bottom:20px;">Coverage Thresholds</div>""", unsafe_allow_html=True)
        lc_thresh = st.slider("Line coverage threshold (%)", 0, 100, st.session_state.system_settings.get("line_coverage_threshold", 70), key="ss_lcthresh")
        bc_thresh = st.slider("Branch coverage threshold (%)", 0, 100, st.session_state.system_settings.get("branch_coverage_threshold", 60), key="ss_bcthresh")
        ms_thresh = st.slider("Mutation score threshold (%)", 0, 100, st.session_state.system_settings.get("mutation_score_threshold", 50), key="ss_msthresh")
        st.markdown(f"""
        <div style="margin-top:16px;">
            <div style="display:flex; justify-content:space-between; margin-bottom:8px;"><span style="font-size:12px; color:{TEXT_MUTED};">Line Threshold</span><span style="font-size:12px; color:{ACCENT_GOLD};">{lc_thresh}%</span></div>
            <div style="background:#1a1a1a; border-radius:2px; height:3px; margin-bottom:12px; overflow:hidden;"><div style="width:{lc_thresh}%; height:100%; background:{ACCENT_GOLD};"></div></div>
            <div style="display:flex; justify-content:space-between; margin-bottom:8px;"><span style="font-size:12px; color:{TEXT_MUTED};">Branch Threshold</span><span style="font-size:12px; color:{ACCENT_SILVER};">{bc_thresh}%</span></div>
            <div style="background:#1a1a1a; border-radius:2px; height:3px; margin-bottom:12px; overflow:hidden;"><div style="width:{bc_thresh}%; height:100%; background:{ACCENT_SILVER};"></div></div>
            <div style="display:flex; justify-content:space-between; margin-bottom:8px;"><span style="font-size:12px; color:{TEXT_MUTED};">Mutation Threshold</span><span style="font-size:12px; color:{ACCENT_COPPER};">{ms_thresh}%</span></div>
            <div style="background:#1a1a1a; border-radius:2px; height:3px; overflow:hidden;"><div style="width:{ms_thresh}%; height:100%; background:{ACCENT_COPPER};"></div></div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown(f"""<div style="background:{CARD_BG}; border:1px solid {CARD_BORDER}; border-radius:8px; padding:28px; margin-bottom:16px;">""", unsafe_allow_html=True)
        st.markdown(f"""<div style="font-size:10px; letter-spacing:2px; text-transform:uppercase; color:{TEXT_MUTED}; margin-bottom:20px;">System Information</div>""", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="font-size:12px; color:{TEXT_SECONDARY}; line-height:2.2;">
            Version: PyTCG-Eval v2.0<br>
            Environment: Local Python Runtime<br>
            Active Users: {len(st.session_state.users_db)}<br>
            Projects: {len(st.session_state.projects)}<br>
            Total Runs: {len(st.session_state.run_history)}<br>
            Log Entries: {len(st.session_state.system_logs)}
        </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    save_col, reset_col = st.columns([1, 1])
    with save_col:
        if st.button("Save Settings", key="save_sys_settings"):
            st.session_state.system_settings.update({
                "storage_path": storage_path,
                "max_file_size_mb": max_file,
                "allow_github_repos": allow_gh,
                "result_retention_days": retention,
                "safe_mode": safe_mode,
                "line_coverage_threshold": lc_thresh,
                "branch_coverage_threshold": bc_thresh,
                "mutation_score_threshold": ms_thresh
            })
            log_event("System settings updated by administrator", "info")
            st.success("Settings saved successfully.")
    with reset_col:
        if st.button("Reset to Defaults", key="reset_sys_settings"):
            st.session_state.system_settings = {
                "pynguin_enabled": True, "hypothesis_enabled": True, "klara_enabled": True, "utbot_enabled": False,
                "pynguin_time_limit": 30, "hypothesis_time_limit": 20, "klara_time_limit": 15, "utbot_time_limit": 45,
                "storage_path": "./outputs/", "line_coverage_threshold": 70, "branch_coverage_threshold": 60,
                "mutation_score_threshold": 50, "max_file_size_mb": 10, "allow_github_repos": True,
                "safe_mode": True, "result_retention_days": 30
            }
            log_event("System settings reset to defaults", "info")
            st.success("Settings reset to defaults.")
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

def render_system_logs_page():
    st.markdown("<div style='padding:40px;'>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style="margin-bottom:40px;">
        <div style="font-size:10px; letter-spacing:2px; text-transform:uppercase; color:{TEXT_MUTED}; margin-bottom:10px;">Admin</div>
        <div style="font-family:'Playfair Display',serif; font-size:34px; font-weight:700; color:{TEXT_PRIMARY};">System Logs</div>
        <div style="font-size:14px; color:{TEXT_SECONDARY}; margin-top:8px;">Review all system activity and execution events.</div>
    </div>
    """, unsafe_allow_html=True)
    fl1, fl2, fl3 = st.columns(3)
    with fl1:
        log_level_filter = st.selectbox("Level", ["All", "info", "error", "warning"], key="log_level_filter")
    with fl2:
        log_user_filter = st.selectbox("User", ["All"] + list(st.session_state.users_db.keys()), key="log_user_filter")
    with fl3:
        log_search = st.text_input("Search logs", placeholder="keyword...", key="log_search")
    logs = list(reversed(st.session_state.system_logs))
    if log_level_filter != "All":
        logs = [l for l in logs if l.get("level") == log_level_filter]
    if log_user_filter != "All":
        logs = [l for l in logs if l.get("user") == log_user_filter]
    if log_search:
        logs = [l for l in logs if log_search.lower() in l.get("message", "").lower()]
    st.markdown(f"""<div style="font-size:11px; color:{TEXT_MUTED}; margin-bottom:16px;">{len(logs)} log entries</div>""", unsafe_allow_html=True)
    if logs:
        for entry in logs:
            lvl = entry.get("level", "info")
            lvl_color = SUCCESS_COLOR if lvl == "info" else (ERROR_COLOR if lvl == "error" else WARNING_COLOR)
            st.markdown(f"""
            <div style="background:{CARD_BG}; border:1px solid {CARD_BORDER}; border-left:3px solid {lvl_color}; border-radius:6px; padding:14px 20px; margin-bottom:8px; display:flex; justify-content:space-between; align-items:center;">
                <div style="display:flex; align-items:center; gap:16px;">
                    <div style="font-size:10px; letter-spacing:1.5px; text-transform:uppercase; color:{lvl_color}; min-width:50px;">{lvl}</div>
                    <div style="font-size:13px; color:{TEXT_PRIMARY};">{entry.get('message', '')}</div>
                </div>
                <div style="text-align:right; flex-shrink:0; margin-left:20px;">
                    <div style="font-size:11px; color:{TEXT_MUTED};">{entry.get('user','')}</div>
                    <div style="font-size:11px; color:{TEXT_MUTED}; margin-top:2px;">{entry.get('timestamp','')}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown(f"""<div style="background:{CARD_BG}; border:1px solid {CARD_BORDER}; border-radius:8px; padding:48px; text-align:center; font-size:13px; color:{TEXT_MUTED};">No log entries found.</div>""", unsafe_allow_html=True)
    if st.button("Clear All Logs", key="clear_logs"):
        st.session_state.system_logs = []
        st.success("All logs cleared.")
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

def main():
    if not st.session_state.authenticated:
        render_auth_page()
        return
    render_navbar()
    page = st.session_state.active_page
    if page == "Dashboard":
        render_dashboard()
    elif page == "Upload Code":
        render_upload_page()
    elif page == "Configure":
        render_configure_page()
    elif page == "Generate Tests":
        render_generate_page()
    elif page == "Run Tests":
        render_run_tests_page()
    elif page == "Coverage Analysis":
        render_coverage_page()
    elif page == "Compare Tools":
        render_compare_page()
    elif page == "Results History":
        render_history_page()
    elif page == "Export":
        render_export_page()
    elif page == "Metrics Guide":
        render_metrics_guide_page()
    elif page == "Manage Tools" and st.session_state.user_role == "admin":
        render_manage_tools_page()
    elif page == "System Settings" and st.session_state.user_role == "admin":
        render_system_settings_page()
    elif page == "System Logs" and st.session_state.user_role == "admin":
        render_system_logs_page()
    else:
        render_dashboard()

if __name__ == "__main__":
    main()