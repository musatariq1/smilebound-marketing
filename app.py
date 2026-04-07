import streamlit as st
import os
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="Marketing Ops",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Dark Ops CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

* { box-sizing: border-box; }
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
#MainMenu, footer, header { visibility: hidden; }

.stApp {
    background: #080a0e;
    background-image:
        radial-gradient(ellipse at 10% 10%, rgba(0,212,255,0.04) 0%, transparent 50%),
        radial-gradient(ellipse at 90% 80%, rgba(224,64,251,0.04) 0%, transparent 50%);
    color: #e2e8f0;
}

/* ── Header ── */
.ops-header {
    display: flex; align-items: center; justify-content: space-between;
    padding: 18px 28px; margin-bottom: 24px;
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 16px;
}
.ops-logo { display: flex; align-items: center; gap: 12px; }
.ops-logo-icon { font-size: 1.5rem; }
.ops-logo-text { font-size: 1.1rem; font-weight: 700; letter-spacing: 0.12em;
    color: #fff; text-transform: uppercase; }
.ops-logo-sub { font-size: 0.7rem; color: #475569; letter-spacing: 0.2em;
    text-transform: uppercase; margin-top: 1px; }
.status-badge {
    display: flex; align-items: center; gap: 8px;
    background: rgba(0,255,136,0.08); border: 1px solid rgba(0,255,136,0.2);
    border-radius: 50px; padding: 6px 14px;
    font-size: 0.75rem; font-weight: 600; color: #00ff88;
    letter-spacing: 0.1em; text-transform: uppercase;
}
.status-dot { width: 7px; height: 7px; border-radius: 50%;
    background: #00ff88; animation: blink 2s infinite; }
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.3} }

/* ── Metric cards ── */
.metric-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; margin-bottom: 24px; }
.metric-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px; padding: 20px 22px;
    position: relative; overflow: hidden;
}
.metric-card::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: var(--accent, #00d4ff);
}
.metric-label { font-size: 0.7rem; color: #475569; letter-spacing: 0.15em;
    text-transform: uppercase; margin-bottom: 8px; }
.metric-value { font-size: 2rem; font-weight: 800; color: var(--accent, #fff);
    line-height: 1; font-variant-numeric: tabular-nums; }
.metric-sub { font-size: 0.72rem; color: #374151; margin-top: 6px; }

/* ── Pipeline ── */
.pipeline {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 14px; padding: 18px 24px; margin-bottom: 24px;
    display: flex; align-items: center; gap: 0;
}
.pipeline-label { font-size: 0.68rem; color: #475569; letter-spacing: 0.15em;
    text-transform: uppercase; margin-bottom: 14px; }
.pipe-steps { display: flex; align-items: center; width: 100%; }
.pipe-step {
    display: flex; flex-direction: column; align-items: center; flex: 1; gap: 6px;
}
.pipe-dot {
    width: 32px; height: 32px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.85rem; font-weight: 700;
    border: 2px solid rgba(255,255,255,0.1);
    background: rgba(255,255,255,0.03); color: #475569;
    transition: all 0.3s;
}
.pipe-dot.active { border-color: var(--c); background: rgba(var(--cr),0.15); color: var(--c); }
.pipe-dot.done { border-color: #00ff88; background: rgba(0,255,136,0.15); color: #00ff88; }
.pipe-name { font-size: 0.68rem; color: #475569; text-transform: uppercase;
    letter-spacing: 0.08em; text-align: center; }
.pipe-name.active { color: #e2e8f0; }
.pipe-line { flex: 1; height: 1px; background: rgba(255,255,255,0.07); margin: 0 8px; margin-bottom: 20px; }
.pipe-line.done { background: #00ff88; opacity: 0.4; }

/* ── Section titles ── */
.section-title {
    font-size: 0.68rem; color: #475569; letter-spacing: 0.2em;
    text-transform: uppercase; margin-bottom: 14px; margin-top: 4px;
    display: flex; align-items: center; gap: 8px;
}
.section-title::after { content: ''; flex: 1; height: 1px; background: rgba(255,255,255,0.05); }

/* ── Agent cards ── */
.agent-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 12px; margin-bottom: 24px; }
.agent-card {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px; padding: 18px 16px;
    position: relative; overflow: hidden;
    transition: border-color 0.3s, background 0.3s;
    cursor: default;
}
.agent-card.working {
    border-color: var(--accent);
    background: rgba(var(--rgb), 0.06);
    box-shadow: 0 0 20px rgba(var(--rgb), 0.1);
}
.agent-card.done {
    border-color: rgba(0,255,136,0.3);
    background: rgba(0,255,136,0.04);
}
.agent-card-top { display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px; }
.agent-icon-wrap {
    width: 36px; height: 36px; border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.1rem;
    background: rgba(var(--rgb), 0.1);
    border: 1px solid rgba(var(--rgb), 0.2);
}
.agent-status-pill {
    font-size: 0.62rem; font-weight: 600; letter-spacing: 0.1em;
    text-transform: uppercase; padding: 3px 8px; border-radius: 50px;
}
.pill-idle { background: rgba(255,255,255,0.05); color: #475569; border: 1px solid rgba(255,255,255,0.07); }
.pill-working { background: rgba(245,158,11,0.15); color: #f59e0b; border: 1px solid rgba(245,158,11,0.3);
    animation: pulse-pill 1.5s infinite; }
.pill-done { background: rgba(0,255,136,0.1); color: #00ff88; border: 1px solid rgba(0,255,136,0.25); }
@keyframes pulse-pill { 0%,100%{opacity:1} 50%{opacity:0.6} }
.agent-name-text { font-size: 0.82rem; font-weight: 700; color: #e2e8f0; margin-bottom: 4px;
    text-transform: uppercase; letter-spacing: 0.05em; }
.agent-spec { font-size: 0.7rem; color: #475569; line-height: 1.4; }
.agent-glow {
    position: absolute; top: -30px; right: -30px; width: 80px; height: 80px;
    border-radius: 50%; background: radial-gradient(circle, rgba(var(--rgb),0.15) 0%, transparent 70%);
    pointer-events: none;
}

/* ── Task input ── */
.task-panel {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px; padding: 24px; margin-bottom: 20px;
}
.stTextArea textarea {
    background: rgba(0,0,0,0.3) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important; color: #e2e8f0 !important;
    font-size: 0.9rem !important; font-family: 'Inter', sans-serif !important;
    resize: none !important;
}
.stTextArea textarea:focus {
    border-color: rgba(0,212,255,0.4) !important;
    box-shadow: 0 0 0 3px rgba(0,212,255,0.08) !important;
    outline: none !important;
}
.stTextArea textarea::placeholder { color: #374151 !important; }

/* ── Buttons ── */
.stButton > button {
    border-radius: 10px !important; padding: 12px 24px !important;
    font-weight: 700 !important; font-size: 0.85rem !important;
    letter-spacing: 0.08em !important; text-transform: uppercase !important;
    border: 1px solid rgba(0,212,255,0.3) !important;
    background: rgba(0,212,255,0.08) !important; color: #00d4ff !important;
    transition: all 0.2s !important; font-family: 'Inter', sans-serif !important;
}
.stButton > button:hover {
    background: rgba(0,212,255,0.15) !important;
    border-color: rgba(0,212,255,0.6) !important;
    box-shadow: 0 0 20px rgba(0,212,255,0.2) !important;
    transform: translateY(-1px) !important;
}

/* ── Radio ── */
.stRadio label { color: #94a3b8 !important; font-size: 0.85rem !important; }
.stRadio [data-testid="stMarkdownContainer"] p { color: #475569 !important; font-size: 0.8rem !important; }

/* ── Output ── */
.output-panel {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(0,212,255,0.15);
    border-radius: 16px; padding: 28px 32px; margin-bottom: 20px;
}
.output-header { display: flex; align-items: center; gap: 10px; margin-bottom: 18px; }
.output-dot { width: 8px; height: 8px; border-radius: 50%; background: #00d4ff; }
.output-title { font-size: 0.72rem; color: #00d4ff; letter-spacing: 0.15em; text-transform: uppercase; font-weight: 600; }

/* ── Terminal ── */
.terminal-wrap {
    background: #050608;
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px; overflow: hidden; margin-bottom: 20px;
}
.terminal-titlebar {
    background: rgba(255,255,255,0.03); padding: 10px 16px;
    display: flex; align-items: center; gap: 8px;
    border-bottom: 1px solid rgba(255,255,255,0.05);
}
.t-dot { width: 10px; height: 10px; border-radius: 50%; }
.terminal-body {
    padding: 16px 20px; font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem; color: #4ade80; line-height: 1.7;
    max-height: 200px; overflow-y: auto;
    background: #050608;
}
.t-line-time { color: #1e3a2f; margin-right: 8px; }
.t-line-sys { color: #374151; }
.t-line-active { color: #4ade80; }
.t-line-warn { color: #f59e0b; }
.t-line-done { color: #00d4ff; }

/* ── Misc ── */
.stDownloadButton > button {
    border-radius: 8px !important; font-size: 0.78rem !important;
    background: rgba(0,255,136,0.05) !important;
    border: 1px solid rgba(0,255,136,0.2) !important;
    color: #00ff88 !important; padding: 8px 16px !important;
}
hr { border-color: rgba(255,255,255,0.05) !important; }
.streamlit-expanderHeader { background: rgba(255,255,255,0.03) !important;
    border-radius: 8px !important; color: #94a3b8 !important; }
</style>
""", unsafe_allow_html=True)

# ── API key guard ─────────────────────────────────────────────────────────────
if not os.getenv("ANTHROPIC_API_KEY") or os.getenv("ANTHROPIC_API_KEY") == "your_api_key_here":
    st.markdown("""<div style="text-align:center;padding:80px 20px;">
        <div style="font-size:2.5rem;margin-bottom:12px;">🔐</div>
        <h3 style="color:#f87171;">API Key Required</h3>
        <p style="color:#475569;">Open <code>.env</code> and set your ANTHROPIC_API_KEY</p>
    </div>""", unsafe_allow_html=True)
    st.stop()

# ── Imports ───────────────────────────────────────────────────────────────────
from agents import AGENT_CONFIGS

AGENT_RGB = {
    "content":   "0,212,255",
    "seo":       "0,255,136",
    "social":    "224,64,251",
    "email":     "251,191,36",
    "analytics": "255,107,107",
}
AGENT_HEX = {
    "content":   "#00d4ff",
    "seo":       "#00ff88",
    "social":    "#e040fb",
    "email":     "#fbbf24",
    "analytics": "#ff6b6b",
}
AGENT_SPECS = {
    "content":   "Blog · Copy · Calendars",
    "seo":       "Keywords · Audits · Rankings",
    "social":    "Posts · Strategy · Growth",
    "email":     "Campaigns · Sequences · Lists",
    "analytics": "KPIs · Reports · Insights",
}

# ── Session state ─────────────────────────────────────────────────────────────
for key, default in {
    "total_tasks": 0,
    "total_reports": 0,
    "agent_status": {k: "idle" for k in AGENT_CONFIGS},
    "terminal_logs": [
        ("sys", "MARKETING OPS v2.0 — BOOT SEQUENCE"),
        ("sys", "Loading agent modules..."),
        ("done", "Content Strategist .......... ONLINE"),
        ("done", "SEO Specialist .............. ONLINE"),
        ("done", "Social Media Manager ........ ONLINE"),
        ("done", "Email Marketer .............. ONLINE"),
        ("done", "Analytics Analyst ........... ONLINE"),
        ("active", "All systems operational. Awaiting task."),
    ],
    "pipeline_stage": 0,
    "last_result": None,
    "last_label": "",
    "weekly_summary": None,
}.items():
    if key not in st.session_state:
        st.session_state[key] = default


def log(msg: str, kind: str = "active"):
    ts = datetime.now().strftime("%H:%M:%S")
    st.session_state.terminal_logs.append((kind, f"{ts}  {msg}"))
    if len(st.session_state.terminal_logs) > 40:
        st.session_state.terminal_logs = st.session_state.terminal_logs[-40:]


# ── Render helpers ────────────────────────────────────────────────────────────
def render_header():
    st.markdown("""
    <div class="ops-header">
        <div class="ops-logo">
            <span class="ops-logo-icon">⚡</span>
            <div>
                <div class="ops-logo-text">Marketing Ops</div>
                <div class="ops-logo-sub">AI Agent Command Centre</div>
            </div>
        </div>
        <div class="status-badge">
            <div class="status-dot"></div>
            All Systems Online
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_metrics():
    reports_count = len(list(Path("reports").glob("*.md"))) if Path("reports").exists() else 0
    st.markdown(f"""
    <div class="metric-grid">
        <div class="metric-card" style="--accent:#00d4ff">
            <div class="metric-label">Tasks Deployed</div>
            <div class="metric-value">{st.session_state.total_tasks:02d}</div>
            <div class="metric-sub">Total runs this session</div>
        </div>
        <div class="metric-card" style="--accent:#00ff88">
            <div class="metric-label">Reports Generated</div>
            <div class="metric-value">{reports_count:02d}</div>
            <div class="metric-sub">Saved to reports/</div>
        </div>
        <div class="metric-card" style="--accent:#e040fb">
            <div class="metric-label">Active Agents</div>
            <div class="metric-value">5</div>
            <div class="metric-sub">Specialists online</div>
        </div>
        <div class="metric-card" style="--accent:#fbbf24">
            <div class="metric-label">Pipeline Stage</div>
            <div class="metric-value">{st.session_state.pipeline_stage}/4</div>
            <div class="metric-sub">Current task progress</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_pipeline():
    s = st.session_state.pipeline_stage
    steps = [
        ("01", "Input",    "#00d4ff", "0,212,255"),
        ("02", "Routing",  "#e040fb", "224,64,251"),
        ("03", "Execute",  "#fbbf24", "251,191,36"),
        ("04", "Complete", "#00ff88", "0,255,136"),
    ]
    html = '<div class="section-title">Pipeline</div><div class="pipeline"><div class="pipe-steps">'
    for i, (num, name, color, rgb) in enumerate(steps):
        if i > 0:
            done_class = "done" if s > i else ""
            html += f'<div class="pipe-line {done_class}"></div>'
        if s > i:
            dot_class = "done"
            style = ""
        elif s == i:
            dot_class = "active"
            style = f"--c:{color};--cr:{rgb};"
        else:
            dot_class = ""
            style = ""
        name_class = "active" if s >= i else ""
        html += (f'<div class="pipe-step">'
                 f'<div class="pipe-dot {dot_class}" style="{style}">{num}</div>'
                 f'<div class="pipe-name {name_class}">{name}</div>'
                 f'</div>')
    html += "</div></div>"
    st.markdown(html, unsafe_allow_html=True)


def render_agent_grid():
    st.markdown('<div class="section-title">Agent Grid</div>', unsafe_allow_html=True)
    statuses = st.session_state.agent_status
    cols = st.columns(5)
    for i, (key, cfg) in enumerate(AGENT_CONFIGS.items()):
        status = statuses.get(key, "idle")
        color = AGENT_HEX[key]
        rgb = AGENT_RGB[key]
        pill = (f"<span class='agent-status-pill pill-{status}'>"
                + ("● ACTIVE" if status == "working" else "✓ DONE" if status == "done" else "IDLE")
                + "</span>")
        with cols[i]:
            st.markdown(f"""
            <div class="agent-card {status}" style="--accent:{color};--rgb:{rgb};">
                <div class="agent-glow"></div>
                <div class="agent-card-top">
                    <div class="agent-icon-wrap" style="--rgb:{rgb};">{cfg['emoji']}</div>
                    {pill}
                </div>
                <div class="agent-name-text" style="color:{color};">{cfg['name']}</div>
                <div class="agent-spec">{AGENT_SPECS[key]}</div>
            </div>
            """, unsafe_allow_html=True)


def render_terminal():
    lines_html = ""
    for kind, msg in st.session_state.terminal_logs[-18:]:
        cls = f"t-line-{kind}"
        ts_part = msg[:8] if len(msg) > 8 and msg[2] == ":" else ""
        rest = msg[8:] if ts_part else msg
        if ts_part:
            lines_html += f'<div><span class="t-line-time">{ts_part}</span><span class="{cls}">{rest}</span></div>'
        else:
            lines_html += f'<div class="{cls}">{msg}</div>'

    st.markdown(f"""
    <div class="terminal-wrap">
        <div class="terminal-titlebar">
            <div class="t-dot" style="background:#ff5f56;"></div>
            <div class="t-dot" style="background:#ffbd2e;"></div>
            <div class="t-dot" style="background:#27c93f;"></div>
            <span style="font-family:'JetBrains Mono';font-size:0.7rem;color:#374151;margin-left:8px;">
                SYSTEM TERMINAL — LIVE FEED
            </span>
        </div>
        <div class="terminal-body">{lines_html}</div>
    </div>
    """, unsafe_allow_html=True)


# ── Layout ────────────────────────────────────────────────────────────────────
render_header()
render_metrics()
render_pipeline()
render_agent_grid()

st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="section-title">Deploy Task</div>', unsafe_allow_html=True)

# ── Task input ────────────────────────────────────────────────────────────────
AGENT_OPTIONS = {
    "⚡ Full Team — CMO decides": "team",
    "✍️ Content":                "content",
    "🔍 SEO":                    "seo",
    "📱 Social Media":           "social",
    "📧 Email":                  "email",
    "📊 Analytics":              "analytics",
}

col_input, col_ctrl = st.columns([3, 1])

with col_ctrl:
    st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
    selected_label = st.radio(
        "Target Agent",
        list(AGENT_OPTIONS.keys()),
        label_visibility="collapsed",
    )
    agent_key = AGENT_OPTIONS[selected_label]
    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
    run_btn = st.button("⚡  DEPLOY", use_container_width=True)
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    summary_btn = st.button("📋  WEEKLY REPORT", use_container_width=True)

with col_input:
    task = st.text_area(
        "Task",
        height=148,
        label_visibility="collapsed",
        placeholder="Describe your marketing objective...\n\ne.g. Build a full launch campaign for our new SaaS product targeting startup founders. Include content, SEO keywords, social posts and email sequence.",
    )

# ── Execution ────────────────────────────────────────────────────────────────
output_placeholder = st.empty()
terminal_placeholder = st.empty()

if run_btn:
    if not task.strip():
        st.warning("Enter a task first.")
    else:
        from manager import stream_single_agent, _determine_agents, _stream_summary

        st.session_state.total_tasks += 1
        st.session_state.pipeline_stage = 1
        log(f"Task received: {task[:60]}{'...' if len(task)>60 else ''}", "active")

        if agent_key == "team":
            # Determine agents
            st.session_state.pipeline_stage = 2
            log("CMO routing task to relevant specialists...", "warn")
            with st.spinner("Routing to specialists..."):
                agents_to_run = _determine_agents(task)
            log(f"Assigned: {', '.join(agents_to_run)}", "done")

            # Run each agent
            st.session_state.pipeline_stage = 3
            all_reports = {}

            for ak in agents_to_run:
                cfg = AGENT_CONFIGS[ak]
                st.session_state.agent_status[ak] = "working"
                log(f"Agent [{cfg['name']}] executing...", "warn")

                agent_task = (
                    f"Overall marketing objective:\n\n{task}\n\n"
                    f"Handle the {cfg['name']} aspects specifically. Be detailed and actionable."
                )

                with output_placeholder.container():
                    st.markdown(
                        f"<div class='output-panel'>"
                        f"<div class='output-header'>"
                        f"<div class='output-dot' style='background:{AGENT_HEX[ak]}'></div>"
                        f"<div class='output-title' style='color:{AGENT_HEX[ak]};'>{cfg['emoji']} {cfg['name']}</div>"
                        f"</div></div>",
                        unsafe_allow_html=True,
                    )
                    text = st.write_stream(stream_single_agent(ak, agent_task))
                    all_reports[ak] = text

                st.session_state.agent_status[ak] = "done"
                st.session_state.total_reports += 1
                log(f"Agent [{cfg['name']}] complete. Report saved.", "done")

            # Summary
            log("CMO synthesising final summary...", "warn")
            combined = "\n\n".join(
                f"### {AGENT_CONFIGS[k]['emoji']} {AGENT_CONFIGS[k]['name']}\n{v}"
                for k, v in all_reports.items()
            )
            with output_placeholder.container():
                st.markdown(
                    "<div class='output-panel'>"
                    "<div class='output-header'>"
                    "<div class='output-dot'></div>"
                    "<div class='output-title'>⚡ CMO EXECUTIVE SUMMARY</div>"
                    "</div></div>",
                    unsafe_allow_html=True,
                )
                summary_text = st.write_stream(_stream_summary(task, combined))
                st.session_state.last_result = summary_text
                st.session_state.last_label = "CMO Summary"

        else:
            cfg = AGENT_CONFIGS[agent_key]
            st.session_state.agent_status[agent_key] = "working"
            st.session_state.pipeline_stage = 3
            log(f"Agent [{cfg['name']}] executing...", "warn")

            with output_placeholder.container():
                st.markdown(
                    f"<div class='output-panel'>"
                    f"<div class='output-header'>"
                    f"<div class='output-dot' style='background:{AGENT_HEX[agent_key]}'></div>"
                    f"<div class='output-title' style='color:{AGENT_HEX[agent_key]};'>{cfg['emoji']} {cfg['name']}</div>"
                    f"</div></div>",
                    unsafe_allow_html=True,
                )
                text = st.write_stream(stream_single_agent(agent_key, task))
                st.session_state.last_result = text
                st.session_state.last_label = cfg["name"]

            st.session_state.agent_status[agent_key] = "done"
            st.session_state.total_reports += 1
            log(f"Agent [{cfg['name']}] complete. Report saved.", "done")

        st.session_state.pipeline_stage = 4
        log("Task complete. All outputs written to reports/", "done")
        st.rerun()

if summary_btn:
    from manager import stream_weekly_summary
    st.session_state.pipeline_stage = 3
    log("Generating weekly executive summary...", "warn")
    with output_placeholder.container():
        st.markdown(
            "<div class='output-panel'>"
            "<div class='output-header'>"
            "<div class='output-dot' style='background:#818cf8'></div>"
            "<div class='output-title' style='color:#818cf8;'>📋 WEEKLY SUMMARY</div>"
            "</div></div>",
            unsafe_allow_html=True,
        )
        text = st.write_stream(stream_weekly_summary())
        st.session_state.weekly_summary = text
    st.session_state.pipeline_stage = 4
    log("Weekly summary complete.", "done")
    st.rerun()

# ── Show last result ──────────────────────────────────────────────────────────
if st.session_state.last_result and not run_btn and not summary_btn:
    with output_placeholder.container():
        st.markdown(
            f"<div class='output-panel'>"
            f"<div class='output-header'>"
            f"<div class='output-dot'></div>"
            f"<div class='output-title'>LAST OUTPUT — {st.session_state.last_label.upper()}</div>"
            f"</div></div>",
            unsafe_allow_html=True,
        )
        st.markdown(st.session_state.last_result)
        st.download_button(
            "⬇  Export Report",
            data=st.session_state.last_result,
            file_name=f"report_{datetime.now().strftime('%Y%m%d_%H%M')}.md",
            mime="text/markdown",
        )

# ── Reports viewer ────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="section-title">Saved Reports</div>', unsafe_allow_html=True)

reports_dir = Path("reports")
report_files = sorted(reports_dir.glob("*.md"), key=lambda p: p.stat().st_mtime, reverse=True) if reports_dir.exists() else []

if report_files:
    cols = st.columns(min(len(report_files), 4))
    for i, path in enumerate(report_files[:8]):
        with cols[i % 4]:
            with st.expander(f"📄 {path.stem.replace('_', ' ').title()}"):
                st.markdown(path.read_text())
                st.download_button(
                    "⬇ Download",
                    data=path.read_text(),
                    file_name=path.name,
                    mime="text/markdown",
                    key=f"dl_{path.name}",
                )
else:
    st.markdown(
        "<p style='color:#374151;font-size:0.85rem;text-align:center;padding:20px;'>"
        "No reports yet — deploy a task to generate them.</p>",
        unsafe_allow_html=True,
    )

# ── Terminal ──────────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
render_terminal()
