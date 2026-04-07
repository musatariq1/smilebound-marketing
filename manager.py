import re
import json
from pathlib import Path
from datetime import datetime
import anthropic

from agents import AGENT_CONFIGS

client = anthropic.Anthropic()
MODEL = "claude-haiku-4-5"
REPORTS_DIR = Path("reports")
MEMORY_DIR = Path("memory")
REPORTS_DIR.mkdir(exist_ok=True)
MEMORY_DIR.mkdir(exist_ok=True)


# ── Memory helpers ────────────────────────────────────────────────────────────

def _load_memory() -> str:
    """Load SmileBound context + agent memory into a single string."""
    parts = []
    for fname in ["smilebound_context.md", "agent_memory.md"]:
        path = MEMORY_DIR / fname
        if path.exists():
            parts.append(path.read_text())
    return "\n\n---\n\n".join(parts)


def _save_memory_entry(task: str, summary: str):
    """Append a task summary to the agent memory log."""
    path = MEMORY_DIR / "agent_memory.md"
    existing = path.read_text() if path.exists() else ""
    date_str = datetime.now().strftime("%d %b %Y, %H:%M")
    entry = (
        f"\n### {date_str}\n"
        f"**Task:** {task[:120]}{'...' if len(task) > 120 else ''}\n"
        f"**Summary:** {summary[:300]}{'...' if len(summary) > 300 else ''}\n"
    )
    # Insert after "## Tasks Completed" header
    if "## Tasks Completed" in existing:
        updated = existing.replace(
            "## Tasks Completed\n*(Updated automatically after each run)*",
            f"## Tasks Completed\n*(Updated automatically after each run)*\n{entry}"
        )
    else:
        updated = existing + entry
    path.write_text(updated)


def _build_system_prompt(agent_system: str) -> str:
    """Inject SmileBound memory into an agent's system prompt."""
    memory = _load_memory()
    return (
        f"=== SMILEBOUND BUSINESS CONTEXT & MEMORY ===\n"
        f"{memory}\n"
        f"=== END CONTEXT ===\n\n"
        f"Always use the above context to make every output specific to SmileBound. "
        f"Never give generic advice — everything must be tailored to Musa's business.\n\n"
        f"--- YOUR SPECIALIST ROLE ---\n"
        f"{agent_system}"
    )


# ── Core agent functions ──────────────────────────────────────────────────────

def _determine_agents(task: str) -> list[str]:
    """Ask Claude which agents are relevant for this task."""
    try:
        response = client.messages.create(
            model=MODEL,
            max_tokens=100,
            system="""You are a CMO assigning a task to marketing specialists.
Available specialists: content, seo, social, email, analytics
Reply with ONLY a JSON array of relevant specialists. Example: ["content", "seo"]
Be selective — only include those truly needed for the task.""",
            messages=[{"role": "user", "content": task}],
        )
        text = response.content[0].text.strip()
        match = re.search(r"\[.*?\]", text, re.DOTALL)
        if match:
            agents = json.loads(match.group())
            valid = [a for a in agents if a in AGENT_CONFIGS]
            if valid:
                return valid
    except Exception:
        pass
    return list(AGENT_CONFIGS.keys())


def stream_single_agent(agent_key: str, task: str):
    """Stream a single agent's response with SmileBound memory injected."""
    config = AGENT_CONFIGS[agent_key]
    full_text = ""
    system = _build_system_prompt(config["system"])

    with client.messages.stream(
        model=MODEL,
        max_tokens=4000,
        system=system,
        messages=[{"role": "user", "content": task}],
    ) as stream:
        for chunk in stream.text_stream:
            full_text += chunk
            yield chunk

    # Save report
    path = REPORTS_DIR / config["report_file"]
    path.write_text(
        f"# {config['name']} Report — SmileBound\n"
        f"*Generated {datetime.now().strftime('%d %b %Y, %H:%M')}*\n\n"
        f"{full_text}"
    )


def _stream_summary(task: str, combined_reports: str):
    """Stream the CMO's synthesis. Saves to disk and updates memory."""
    full_text = ""
    memory = _load_memory()

    with client.messages.stream(
        model=MODEL,
        max_tokens=2000,
        system=(
            f"=== SMILEBOUND CONTEXT ===\n{memory}\n=== END ===\n\n"
            "You are the CMO of SmileBound. Synthesise the team's reports into a "
            "concise executive summary specific to SmileBound's goals and stage."
        ),
        messages=[{
            "role": "user",
            "content": (
                f"Task: {task}\n\nTeam reports:\n{combined_reports}\n\n"
                "Write an executive summary covering:\n"
                "1. What each specialist produced for SmileBound\n"
                "2. Top 3 priority actions for Musa\n"
                "3. Cross-channel synergies\n"
                "4. Specific next steps"
            ),
        }],
    ) as stream:
        for chunk in stream.text_stream:
            full_text += chunk
            yield chunk

    # Save report + update memory
    path = REPORTS_DIR / "manager_summary.md"
    path.write_text(
        f"# CMO Summary — SmileBound\n"
        f"*Task: {task}*\n"
        f"*{datetime.now().strftime('%d %b %Y, %H:%M')}*\n\n"
        f"{full_text}"
    )
    _save_memory_entry(task, full_text)


def stream_weekly_summary():
    """Read all saved reports and stream a weekly summary."""
    report_sections = []
    for config in AGENT_CONFIGS.values():
        path = REPORTS_DIR / config["report_file"]
        if path.exists():
            report_sections.append(
                f"### {config['emoji']} {config['name']}\n{path.read_text()}"
            )

    if not report_sections:
        yield "No reports found yet. Run some tasks first to generate agent reports."
        return

    date_str = datetime.now().strftime("%Y-%m-%d")
    memory = _load_memory()
    full_text = ""

    with client.messages.stream(
        model=MODEL,
        max_tokens=3000,
        system=(
            f"=== SMILEBOUND CONTEXT ===\n{memory}\n=== END ===\n\n"
            "You are the CMO of SmileBound writing a weekly marketing summary for Musa."
        ),
        messages=[{
            "role": "user",
            "content": (
                f"SmileBound team reports — week ending {date_str}:\n\n"
                + "\n\n".join(report_sections)
                + "\n\nWrite a structured weekly summary:\n"
                "## Executive Summary\n"
                "## Channel Performance\n"
                "## Top Wins This Week\n"
                "## Priorities for Next Week\n"
                "## Action Items for Musa"
            ),
        }],
    ) as stream:
        for chunk in stream.text_stream:
            full_text += chunk
            yield chunk

    path = REPORTS_DIR / f"weekly_summary_{date_str}.md"
    path.write_text(f"# SmileBound Weekly Summary\n*{date_str}*\n\n{full_text}")
    _save_memory_entry(f"Weekly summary {date_str}", full_text)
