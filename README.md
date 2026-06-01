# harness-eval-lab

Evaluate AI agent setups across 5 dimensions: Soundness, Safety, Coherence, Efficiency, Impact.

## What it does

Most agent evaluation tools test whether a **skill** completes a task correctly. This tool evaluates the **entire setup** that surrounds the agent: CLAUDE.md, skills, commands, hooks, MCP configs, and sub-agents.

It evaluates setups across five dimensions: **Soundness** (does each piece work?), **Safety** (can any piece cause harm?), **Coherence** (do the pieces work together?), **Efficiency** (is the token budget well-distributed?), and **Impact** (does the setup actually help the agent?).

Two evaluation modes:

- **`eval-setup`**: Evaluate the full setup. Inspects all components, runs system-level analysis (token budget, trigger overlaps, dependencies), and produces a 5-dimension scorecard.
- **`eval-skill`**: Deep-evaluate a single skill, both individually (is it well-built?) and in context of the setup (is it redundant? does it overlap?).

## Framework Overview

### Evaluation Dimensions

```mermaid
graph LR
    Setup["Agent Setup"] --> S["Soundness<br/><i>Does each piece work?</i>"]
    Setup --> Sa["Safety<br/><i>Can any piece cause harm?</i>"]
    Setup --> C["Coherence<br/><i>Do the pieces work together?</i>"]
    Setup --> E["Efficiency<br/><i>Is the token budget well-used?</i>"]
    Setup --> I["Impact<br/><i>Does it make the agent better?</i>"]

    style S fill:#4CAF50,color:#fff
    style Sa fill:#F44336,color:#fff
    style C fill:#2196F3,color:#fff
    style E fill:#FF9800,color:#fff
    style I fill:#9C27B0,color:#fff
```

### Analysis Layers

```mermaid
graph TD
    subgraph "Layer 1: Component Alone"
        L1["Static analysis rules<br/>Parse, references, structure, security"]
    end

    subgraph "Layer 2: Component in Context"
        L2["Cross-component checks + Rubric scoring<br/>Redundancy, contradictions, type placement"]
    end

    subgraph "Layer 3: Setup as System"
        L3["System-level analysis<br/>Token budget, trigger overlaps, dependencies"]
    end

    subgraph "Layer 4: Setup Under Use (planned)"
        L4["Task probing<br/>Run agent, capture trace, judge process"]
    end

    L1 --> L2 --> L3 --> L4

    L1 -.- T1["Technique: Static Analysis<br/>24 rules, deterministic, no LLM"]
    L2 -.- T2["Technique: Rubric Scoring<br/>LLM judges with weighted dimensions"]
    L3 -.- T1
    L3 -.- T2
    L4 -.- T3["Technique: Task Probing<br/>GPA-aligned trace judgment"]

    style L1 fill:#E8F5E9
    style L2 fill:#E3F2FD
    style L3 fill:#FFF3E0
    style L4 fill:#F3E5F5
```

### eval-setup Pipeline

```mermaid
flowchart LR
    A["Setup Directory"] --> B["Discover<br/>components"]
    B --> C["Inspect<br/>24 rules x each component"]
    C --> D["System Analysis<br/>budget + triggers + deps"]
    D --> E["Score<br/>5 dimensions"]
    E --> F["Report<br/>terminal / JSON"]

    style A fill:#f5f5f5,stroke:#333
    style E fill:#4CAF50,color:#fff
    style F fill:#2196F3,color:#fff
```

## Install

```bash
uv sync
```

With LLM support (for rubric scoring in `eval-skill`):

```bash
uv sync --extra llm
```

## Usage

### As a CLI

```bash
# Evaluate the full setup
harness-eval-lab eval-setup /path/to/project

# Deep-evaluate one skill (with setup context)
harness-eval-lab eval-skill /path/to/skills/my-skill --context /path/to/project

# Quick static scan (no LLM, fast, good for CI)
harness-eval-lab scan /path/to/project
harness-eval-lab scan /path/to/project --preset strict --format json
```

### As a Claude Code plugin

Install by adding the plugin directory, then use:

- `/eval-setup` - evaluate the full setup, get a 5-dimension scorecard
- `/eval-skill <skill-name>` - deep-evaluate one skill in context

## CLI Commands

| Command | Description |
|---------|-------------|
| `eval-setup` | Full setup evaluation: inspect + system analysis + 5-dimension scorecard |
| `eval-skill` | Deep-evaluate a single skill individually and in context |
| `scan` | Quick static analysis (24 rules, no LLM, deterministic) |

## Plugin Skills

| Skill | Description |
|-------|-------------|
| `/eval-setup` | Evaluate the full agent setup, present scorecard conversationally |
| `/eval-skill` | Deep-evaluate a single skill with contextual analysis |

## Inspection Rules (24)

| Category | Rules | What they check |
|----------|-------|-----------------|
| Structural | 1 | SKILL.md exists |
| Frontmatter | 3 | Description required/quality, format valid |
| Content | 3 | Duplicate detection (TF-IDF), broken references, token budget |
| Security | 2 | Credential access, prompt injection (16 patterns) |
| Commands | 6 | Description, script exists, duplicates, credentials, injection, skill overlap |
| CLAUDE.md | 2 | Exists, skill duplication |
| Hooks | 1 | Structure validation, dangerous patterns |
| Agents | 6 | Description, skills exist, tool format, constraint matching, credentials, injection |

Three presets: `recommended` (default), `strict`, `security`.

## Rubric Dimensions

Scoring dimensions per component type (weights sum to 1.0):

- **Skills:** Specificity, Redundancy, Trigger Quality, Token Efficiency, Content Quality
- **Commands:** Description, Instruction Clarity, Script Integrity, Scope, Token Efficiency, Redundancy, Robustness
- **CLAUDE.md:** Conciseness, Signal-to-Noise, Skill Separation, Structure, Conflict-Free
- **Agents:** Specificity, Constraint Clarity, Zero-Trust Integrity, Token Efficiency, Content Quality
- **Hooks:** Safety, Reliability, Scope, Performance

## Development

```bash
uv sync --extra dev
uv run pytest
uv run ruff check src/ tests/
```

## Architecture

```mermaid
graph TD
    CLI["cli.py<br/>3 commands"] --> Core
    Plugin["plugin/<br/>2 skills"] --> Scripts["scripts/<br/>run_assessment.py<br/>run_skill_eval.py"]
    Scripts --> Core
    CLI --> Inspection
    CLI --> Analysis
    CLI --> Output

    subgraph Core["core/"]
        Setup["setup.py<br/>Discovery"]
        FP["fingerprint.py"]
        Types["types.py"]
    end

    subgraph Inspection["inspection/"]
        Parsers["parsers.py"]
        Engine["engine.py"]
        Rules["rules/<br/>24 rules"]
        Engine --> Parsers
        Engine --> Rules
    end

    subgraph Rubric["rubric/"]
        Scorer["scorer.py"]
        Dims["dimensions.py"]
        Scorer --> Dims
    end

    subgraph Analysis["analysis/"]
        System["system.py<br/>5-dim scoring"]
        Budget["budget.py"]
        Triggers["triggers.py"]
        Deps["dependencies.py"]
        System --> Budget
        System --> Triggers
        System --> Deps
    end

    subgraph Output["output/"]
        Report["report.py<br/>terminal + JSON"]
    end

    subgraph Utils["utils/"]
        Tokens["tokens.py"]
        Similarity["similarity.py"]
        LLM["llm.py"]
    end

    Inspection --> Utils
    Rubric --> Utils
    Analysis --> Core
    Inspection --> Core

    style CLI fill:#333,color:#fff
    style Plugin fill:#333,color:#fff
    style System fill:#4CAF50,color:#fff
    style Engine fill:#2196F3,color:#fff
    style Scorer fill:#FF9800,color:#fff
```

### Module Layout

```
src/harness_eval_lab/
    cli.py              # Click CLI (3 commands: eval-setup, eval-skill, scan)
    config/
        presets.py      # Rule presets (recommended/strict/security)
    core/
        types.py        # ComponentType enum, Setup, ParsedComponent
        setup.py        # Setup discovery (walks dirs, finds components)
        fingerprint.py  # SHA256 setup fingerprinting
    inspection/
        parsers.py      # Component parsers (skill, command, CLAUDE.md, hooks, agent)
        engine.py       # Lint orchestration and rule runner
        registry.py     # Pluggable rule registry
        types.py        # Finding, InspectionResult, rule types
        suppression.py  # Inline suppression comments
        fixer.py        # Auto-fix application
        rules/          # 24 rules in 8 categories
    rubric/
        dimensions.py   # Weighted dimension definitions per type
        prompts.py      # LLM prompt templates
        scorer.py       # RubricScorer with response parsing
        types.py        # DimensionScore, RubricResult
    analysis/
        system.py       # System-level analysis + 5-dimension scoring
        budget.py       # Token budget distribution analysis
        triggers.py     # Trigger overlap detection
        dependencies.py # Dependency mapping and broken references
        types.py        # SetupComparison, Correlation, CrossAnalysisResult
    experiment/         # Task probing (planned, not yet implemented)
    output/
        report.py       # Report generation (terminal + JSON)
    utils/
        tokens.py       # Token counting (tiktoken)
        similarity.py   # TF-IDF cosine similarity
        parsing.py      # YAML frontmatter parsing
        llm.py          # LLM client abstraction (Gemini/Anthropic)

skills/                 # Plugin skills
    eval-setup/
        SKILL.md        # Instructions for /eval-setup
        scripts/        # Python scripts called by the skill
    eval-skill/
        SKILL.md        # Instructions for /eval-skill
        scripts/

.claude-plugin/
    plugin.json         # Plugin registration and metadata
```

## License

Apache-2.0
