# project-absorber

A Claude Code skill that automatically absorbs the best features from competing open-source projects into your own — turning it into a "fusion monster" that combines the strengths of its entire category.

## What it does

Given any project, `project-absorber` will:

1. **Scan your project** — understand what it does, its tech stack, and current gaps
2. **Discover competitors** — search GitHub for similar open-source projects (Stars-ranked)
3. **Deep-analyze each competitor** — shallow-clone the repo and examine 8 dimensions: UX, config/extensibility, error handling, testing, docs, performance, community, and security
4. **PM-style planning** — deduplicate findings across all competitors, globally re-rank by impact, and generate a prioritized absorption plan
5. **Execute with confirmation** — implement each improvement one by one, with your approval before each step

It keeps going until your project has absorbed everything worth taking — then moves to the next competitor.

## Demo

Real run on [quant-os](https://github.com/weiquyun123/quant-os) — an AI-native quantitative research workflow skill for Claude ​Code.

**Phase 1 — Self-scan:**
```
✅ Self-portrait complete
Type: AI agent tool (Claude ​Code skill)
Stack: Markdown + YAML (prompt engineering)
Core features: 5-route workflow (framing / report translation / A-share guard / execution / review)
Known gaps: no session state · no task tracking · no onboarding · no cross-worker handoff spec
```

**Phase 2 — Competitor discovery (11 candidates → 4 selected):**
```
🔍 Found 4 relevant competitors:
1. Microsoft RD-Agent   (⭐ 12.4k) — most mature LLM quant research orchestrator, has persistence
2. TradingAgents        (⭐ 48.5k) — multi-agent workflow with session state + guided onboarding
3. FinRobot             (⭐  6.6k) — Smart Scheduler routing + Synthesis quality gate
4. QuantaAlpha          (⭐   623) — natural language → factor → validation loop

Confirmed? (or add/remove entries)
```

**Phase 3 — Deep analysis (3 competitors, 8 dimensions each):**
```
📊 RD-Agent findings:
  P0: KnowledgeBase persistence → inspires state.json session protocol
  P0: Trace research log       → inspires RESEARCH_BACKLOG.md (3-state tracking)
  P1: Failure record structure → inspires structured failure log in execution contract
  Not absorbing: dill/Docker (wrong layer for a Markdown skill)

📊 TradingAgents findings:
  P0: AgentState named fields  → inspires Delivery Contracts table
  P0: 8-step guided onboarding → inspires first-run detection + 4-question wizard
  P1: Conditional back-routing → inspires route backflow declarations
  ...
```

**Phase 4 — PM absorption plan (13 items, deduplicated):**
```
📋 Absorption plan generated

Analyzed 3 competitors · 13 absorbable items found:
  P0 (do first): 4 items
  P1 (next sprint): 5 items
  P2 (optional): 3 items
  Not absorbing: 5 items (with reasons)

P0 preview:
  PA-001  Session State persistence (state.json)       | from: RD-Agent + TradingAgents | effort: low
  PA-002  Research task backlog (3-state tracking)     | from: RD-Agent                 | effort: low
  PA-003  Guided onboarding wizard                     | from: TradingAgents             | effort: low
  PA-004  Delivery Contracts table (typed handoffs)    | from: TradingAgents             | effort: low

Start executing?
```

**Phase 5 — Execute PA-001 (session state, ~30 lines added to SKILL.md):**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Implementing PA-001: Session State Protocol
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Source: RD-Agent KnowledgeBase + TradingAgents AgentState
Impact: controller reads .quant-os/state.json on startup → resumes last session
Files: quant-os/SKILL.md (append ~30 lines)

Continue? ✓

✅ PA-001 done. Progress: 1/13 items complete (P0 remaining: 3)
Next: PA-002 Research Backlog | effort: low
Continue?
```

Full demo artifacts: [`quant-os/absorber-workspace/`](https://github.com/weiquyun123/quant-os/tree/main/absorber-workspace)

## Requirements

- [Claude Code](https://claude.ai/code) (CLI or IDE extension)
- Git (for shallow-cloning competitors)
- Python 3.8+ (for `repo_scanner.py`)

## Installation

**Option 1: Install as a `.skill` file**

Download `project-absorber.skill` from [Releases](../../releases) and install it in Claude Code.

**Option 2: Clone manually**

```bash
git clone https://github.com/YOUR_USERNAME/project-absorber \
  ~/.claude/skills/project-absorber
```

## Usage

Navigate to your project directory and tell Claude Code:

```
开始吸收          # Start from Phase 1
继续吸收          # Resume from where you left off
大吞噬器          # Same as above
帮我吸收竞品      # Trigger with Chinese
absorb competitors  # English trigger also works
run project absorber
```

You can also be more specific:

```
分析这几个竞品：[GitHub URL1] [URL2]   # Provide specific competitors
从 PA-003 开始执行                      # Start from a specific plan item
只做 P0 的项目                          # Only execute high-priority items
```

## How it works

```
project-absorber/
├── SKILL.md                  # Main entry — 5-phase workflow
├── phases/
│   ├── p1_self_scan.md       # Project self-profiling
│   ├── p2_discover.md        # Competitor discovery strategy
│   ├── p3_analyze.md         # 8-dimension analysis framework
│   ├── p4_pm_plan.md         # PM deduplication + global prioritization
│   └── p5_execute.md         # Execution loop with confirmation gates
├── templates/
│   └── absorption_plan.md    # Plan document template
└── scripts/
    └── repo_scanner.py       # Fast repo structure scanner
```

All intermediate artifacts are saved to `absorber-workspace/` inside your project:

```
absorber-workspace/
├── self_profile.md           # Your project's self-portrait
├── competitor_list.md        # Confirmed competitor queue
├── [competitor-name]/
│   └── analysis.md           # Per-competitor findings
└── ABSORPTION_PLAN.md        # Master plan (live progress tracking)
```

Cloned competitor repos go to `/tmp/absorber/` and are never committed to your project.

## The 8 Analysis Dimensions

For each competitor, the skill evaluates:

| # | Dimension | What it looks for |
|---|-----------|-------------------|
| 1 | UX & Interface | CLI help quality, API consistency, onboarding |
| 2 | Config & Extensibility | Config format, plugin/hook systems |
| 3 | Error Handling & Observability | Error message quality, logging, metrics |
| 4 | Testing Architecture | Coverage strategy, test tooling, data management |
| 5 | Documentation & DX | README structure, API docs, CONTRIBUTING |
| 6 | Performance & Engineering | Caching, concurrency, dependency hygiene |
| 7 | Community & Ecosystem | Issue templates, badges, integrations |
| 8 | Security | Input validation, secrets handling, auth |

## Absorption Principles

- **Borrow ideas, don't copy code** — reimplement patterns in your project's style
- **Only adopt what's actually better** — if it's not a clear win, it goes in the "not absorbing" list with reasons
- **Feature-level AND pattern-level** — both "add a plugin system" and "their error messages give fix suggestions" count
- **Honest PM** — if something is too risky or incompatible, it's labeled as such, not forced in

## Safety

- Code changes only happen after your explicit confirmation per item
- High-difficulty items always require confirmation, even in "auto" mode
- If implementation hits a blocker, it stops and explains — never pushes through
- Competitor code is analyzed in `/tmp/`, never mixed into your project

## License

MIT
