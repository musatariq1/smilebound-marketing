#!/usr/bin/env python3
"""
AI Marketing Team — 5 specialist agents + manager/CMO

Usage:
  python main.py --task "Launch campaign for our new product"
  python main.py --summary
  python main.py --agent content --task "Write a blog post about AI in marketing"
  python main.py --agent seo --task "Audit keywords for our SaaS homepage"
  python main.py --agent social --task "Create a week of LinkedIn posts"
  python main.py --agent email --task "Build a 5-email welcome sequence"
  python main.py --agent analytics --task "Define KPIs for our Q3 campaign"
"""

import argparse
import sys
import os
from pathlib import Path
from dotenv import load_dotenv
import anyio

load_dotenv()

if not os.getenv("ANTHROPIC_API_KEY"):
    print("ERROR: ANTHROPIC_API_KEY not set.")
    print("Copy .env.example to .env and add your key, or set the env var directly.")
    sys.exit(1)

# Ensure reports directory exists
Path("reports").mkdir(exist_ok=True)


def print_header():
    print("\n" + "=" * 60)
    print("  AI MARKETING TEAM")
    print("  5 Specialist Agents + CMO Manager")
    print("=" * 60 + "\n")


def print_agents():
    agents = [
        ("content-strategist",   "Blog posts, copy, content calendars"),
        ("seo-specialist",        "Keywords, on-page SEO, audits"),
        ("social-media-manager",  "Platform content, scheduling, engagement"),
        ("email-marketer",        "Campaigns, sequences, newsletters"),
        ("analytics-analyst",     "KPIs, performance reports, insights"),
    ]
    print("Available agents:")
    for name, desc in agents:
        print(f"  • {name:<25} {desc}")
    print()


async def main():
    parser = argparse.ArgumentParser(
        description="AI Marketing Team — delegate tasks to specialist agents",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--task", "-t",
        help="Marketing task to delegate (manager decides which agents to use)",
    )
    parser.add_argument(
        "--summary", "-s",
        action="store_true",
        help="Generate a weekly summary from all agent reports",
    )
    parser.add_argument(
        "--agent", "-a",
        choices=["content", "seo", "social", "email", "analytics"],
        help="Run a specific agent directly",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show session details",
    )
    parser.add_argument(
        "--list", "-l",
        action="store_true",
        help="List available agents",
    )

    args = parser.parse_args()

    print_header()

    if args.list:
        print_agents()
        return

    # Lazy import after env check
    from manager import run_manager, run_weekly_summary, run_agent_task

    # --- Weekly summary mode ---
    if args.summary:
        print("Generating weekly marketing summary...\n")
        print("The manager will read all agent reports and synthesise them.\n")
        result = await run_weekly_summary(verbose=args.verbose)
        print("\n" + "─" * 60)
        print(result)
        print("─" * 60)
        print("\nSummary saved to reports/weekly_summary_<date>.md")
        return

    # --- Single agent mode ---
    if args.agent:
        if not args.task:
            print(f"ERROR: --task is required when using --agent")
            print(f"Example: python main.py --agent {args.agent} --task 'your task here'")
            sys.exit(1)

        agent_labels = {
            "content":   "Content Strategist",
            "seo":       "SEO Specialist",
            "social":    "Social Media Manager",
            "email":     "Email Marketer",
            "analytics": "Analytics Analyst",
        }
        label = agent_labels[args.agent]
        print(f"Running {label}...")
        print(f"Task: {args.task}\n")

        result = await run_agent_task(args.agent, args.task, verbose=args.verbose)
        print("\n" + "─" * 60)
        print(result)
        print("─" * 60)
        return

    # --- Manager / full team mode ---
    if args.task:
        print("Delegating to marketing team...\n")
        print(f"Task: {args.task}\n")
        print("The CMO manager will analyse your task, delegate to relevant")
        print("specialist agents, and synthesise a final report.\n")

        result = await run_manager(args.task, verbose=args.verbose)
        print("\n" + "─" * 60)
        print(result)
        print("─" * 60)
        print("\nIndividual agent reports saved to reports/")
        return

    # --- No args: show help ---
    parser.print_help()
    print()
    print_agents()


if __name__ == "__main__":
    anyio.run(main)
