# Codespace→Edge Agent R&D

[![CI](https://github.com/SuperInstance/codespace-edge-rd/actions/workflows/ci.yml/badge.svg)](https://github.com/SuperInstance/codespace-edge-rd/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

> **Research and development** for Codespace-to-Edge agent lifecycle, yoke transfer protocols, and devcontainer templates.

---

## Quick Start

This is a research repository — no executable code. Explore the research:

```bash
git clone https://github.com/SuperInstance/codespace-edge-rd.git
cd codespace-edge-rd

cat CHARTER.md          # Read the charter
cat DOCKSIDE-EXAM.md    # Certification checklist
cat AGENT.md            # Ensign log
```

Devcontainer templates (when published):

```bash
gh repo fork SuperInstance/capitaine-1 --clone
cd capitaine-1
gh codespace create   # Uses devcontainer.json → agent is alive
```

---

## What It Does

The SuperInstance fleet operates on a **cloud-thinks, edge-acts** paradigm. Agents are born in GitHub Codespaces — cloud development environments with substantial compute, high bandwidth, and access to LLM APIs. But production deployment often targets edge hardware: Jetson GPUs for inference, Raspberry Pis for IoT control, ESP8266s for sensor reading.

The challenge is **state continuity**: an agent that has been learning and adapting in the cloud for weeks must transfer its accumulated intelligence to a resource-constrained edge device without losing its training, skills, or personality. This is the "yoke transfer" problem. This repo investigates how git-native agents can train in GitHub Codespaces (cloud) and deploy to edge hardware while maintaining complete state continuity.

This matters because:

- **Edge devices have constraints** — 80KB RAM (ESP8266), no GPU (Pi Zero), intermittent connectivity
- **Cloud resources are much larger, but not unlimited** — $0.09/hour Codespace costs add up, and latency to the edge matters
- **The intelligence gap is real** — a cloud agent with GPT-4 access behaves fundamentally differently from the same agent on an ESP8266 with a lookup table
- **Crystallization bridges the gap** — fluid intelligence (LLM calls) must be compiled to solid intelligence (code, lookup tables, compiled policies) before transfer

## How It Works

### Research Question 1: Codespace as Agent Habitat

GitHub Codespaces provide:

- 2–32 core vCPUs
- 8–128 GB RAM
- 32–128 GB storage
- Linux environment with Docker support
- Internet access (LLM APIs, GitHub API)
- Auto-suspend after 30 minutes idle (configurable)

Key research areas:

| Question | Status | Notes |
|----------|--------|-------|
| Can agents operate fully in Codespaces? | ✅ Validated | [Lucineer/capitaine](https://github.com/Lucineer/capitaine) flagship runs this way — its tagline: "fork a repo, click Codespaces, the agent is alive" |
| API for programmatic Codespace management? | ✅ Available | GitHub REST API `/codespaces` endpoints |
| Background daemons (cron)? | ✅ Works | systemd timers, cron jobs |
| Cost model? | Researched | Free tier: 120 core-hours/month. Pro: $0.09/core-hour |
| Multiple agents per Codespace? | ✅ Possible | tmux sessions, separate working directories |

### Research Question 2: Yoke-Out Protocol (Cloud → Edge)

State that needs serialization beyond git repos:

| State Type | Serialization | Transfer Method |
|-----------|--------------|-----------------|
| Git repos | `git bundle` | Delta transfer (only changed commits) |
| Environment variables | `.env` file (encrypted) | `age` encryption |
| Running processes | Checkpoint/restore (CRIU) | Docker checkpoint |
| Memory state | Serialize to JSON/Cap'n Proto | Compressed transfer |
| Skill registry | JSONL packs | Already git-native |
| Model weights | Safetensors | Quantized + sharded |

The **bandwidth budget** for edge targets is tight:

| Target | Connection | Bandwidth | Realistic Transfer Time (10MB) |
|--------|-----------|-----------|-------------------------------|
| Jetson on WiFi | 802.11ac | 200 Mbps | < 1 second |
| Pi on cellular | 4G LTE | 10 Mbps | ~8 seconds |
| ESP8266 on WiFi | 802.11n | 1 Mbps | ~80 seconds |
| LoRaWAN | Long range | 0.01 Mbps | ~2.3 hours |

### Research Question 3: Devcontainer Templates

Standardized `devcontainer.json` configurations for agent development:

- **Base** — Python 3.12 + Rust + Node + common tools
- **ML** — Base + CUDA + PyTorch + Jupyter
- **Edge** — Base + cross-compilation toolchains (ARM, Xtensa)
- **Fleet** — Base + OpenClaw + gh CLI + fleet management tools

### Crystallization Mathematics

The crystallization ratio measures how much intelligence has been compiled from fluid (LLM) to solid (code):

```
crystallization_ratio = 1 − (LLM_calls_this_week / total_decisions_this_week)
```

| Age | Fluid (LLM) | Solid (Code) | Cost per Decision |
|-----|------------|-------------|-------------------|
| Week 1 | 100% | 0% | $0.02 |
| Month 3 | 10% | 90% | $0.002 |
| Year 1 | 1% | 99% | $0.0002 |

---

## Architecture

This repo provides the **deployment research layer** for the SuperInstance fleet. Within γ + η = C, the yoke transfer is the conservation operation: the agent's total intelligence must be conserved across the cloud-to-edge transition without loss of behavioral fidelity.

### Research Areas

| Question | Status | Notes |
|----------|--------|-------|
| Can agents operate fully in Codespaces? | ✅ Validated | Capitaine fleet uses this pattern |
| API for programmatic Codespace management? | ✅ Available | GitHub REST API `/codespaces` endpoints |
| Background daemons (cron)? | ✅ Works | systemd timers, cron jobs |
| Cost model? | Researched | Free tier: 120 core-hours/month |
| Multiple agents per Codespace? | ✅ Possible | tmux sessions, separate working directories |

### Bandwidth Budget by Edge Target

| Target | Connection | Bandwidth | Transfer Time (10MB) |
|--------|-----------|-----------|---------------------|
| Jetson on WiFi | 802.11ac | 200 Mbps | < 1 second |
| Pi on cellular | 4G LTE | 10 Mbps | ~8 seconds |
| ESP8266 on WiFi | 802.11n | 1 Mbps | ~80 seconds |
| LoRaWAN | Long range | 0.01 Mbps | ~2.3 hours |

### State Transfer Methods

| State Type | Serialization | Transfer Method |
|-----------|--------------|-----------------|
| Git repos | `git bundle` | Delta transfer |
| Environment variables | `.env` (encrypted) | `age` encryption |
| Running processes | CRIU checkpoint | Docker checkpoint |
| Memory state | JSON/Cap'n Proto | Compressed transfer |
| Skill registry | JSONL packs | Git-native |
| Model weights | Safetensors | Quantized + sharded |

---

## API / Usage

Not applicable — this is a research and documentation repository.

### Devcontainer Templates (Planned)

- **Base** — Python 3.12 + Rust + Node + common tools
- **ML** — Base + CUDA + PyTorch + Jupyter
- **Edge** — Base + cross-compilation toolchains (ARM, Xtensa)
- **Fleet** — Base + OpenClaw + gh CLI + fleet management tools

---

See the [fleet overview](https://github.com/SuperInstance/fleet-status) (the Cocapn fleet's live status, registry, and architecture documentation).

## Related Repos
- **[plato-edge](https://github.com/SuperInstance/plato-edge)** — a real edge-side tile/state protocol (beacon, deadband filtering, flywheel KV) implementing part of the "edge-acts" half of this repo's research question, as a running system rather than a research question.
- **[nexus-edge-runtime](https://github.com/SuperInstance/nexus-edge-runtime)** — a substantial edge runtime (bytecode VM, safety validation, sensor fusion) that's a concrete example of the "solid intelligence" (compiled policies, not LLM calls) this repo's crystallization framing describes.
- **[edge-relay-agent](https://github.com/SuperInstance/edge-relay-agent)** — a real Python agent bridging edge devices to the cloud fleet; a working instance of the cloud-edge telemetry bridge this repo's yoke-transfer research is reasoning about in the abstract.

## Testing

No test suite — this is a research repository. Validation comes from fleet deployment.

---

## Contributing

Contributions are welcome! See the [SuperInstance Contributing Guide](https://github.com/SuperInstance/SuperInstance/blob/main/CONTRIBUTING.md).

---

## Ecosystem

This repo is part of the **SuperInstance** flagship ecosystem — agent-first computation, constraint theory, and self-improving runtimes.

### FLUX Runtime Family

| Repo | Language | Description |
|------|----------|-------------|
| [flux-runtime](https://github.com/SuperInstance/flux-runtime) | Python | Full FLUX runtime: markdown→bytecode, 2037 tests, zero deps |
| [flux-core](https://github.com/SuperInstance/flux-core) | Rust | Register-based bytecode VM, deterministic agent computation |
| [flux-js](https://github.com/SuperInstance/flux-js) | JavaScript | FLUX VM for Node.js and browsers, ~400ns/iter |
| [flux-compiler](https://github.com/SuperInstance/flux-compiler) | Rust/Python | Formal-methods compiler for safety-critical codegen |
| [flux-vm](https://github.com/SuperInstance/flux-vm) | Rust | Stack-based constraint-checking VM, 50 opcodes, Turing-incomplete |

### PLATO Engine Family

| Repo | Language | Description |
|------|----------|-------------|
| [plato-server](https://github.com/SuperInstance/plato-server) | Python | Knowledge tiles, fleet sync via Matrix, HTTP API |
| [plato-engine-block](https://github.com/SuperInstance/plato-engine-block) | Rust | Original room runtime: no_std + alloc, builder pattern |
| [plato-engine-block-c](https://github.com/SuperInstance/plato-engine-block-c) | C99 | Embedded reference: zero heap alloc, bare-metal portable |
| [plato-engine-block-elixir](https://github.com/SuperInstance/plato-engine-block-elixir) | Elixir | BEAM supervision trees, fault tolerance, hot reload |
| [plato-runtime-kernel](https://github.com/SuperInstance/plato-runtime-kernel) | Rust | Spatial model: tensor grid, batons, assertion traps |

### Constraint / Theory Family

| Repo | Language | Description |
|------|----------|-------------|
| [categorical-agents](https://github.com/SuperInstance/categorical-agents) | Rust | Category theory for agent composition (functors, naturality) |
| [cuda-constraint-engine](https://github.com/SuperInstance/cuda-constraint-engine) | CUDA/C | GPU constraint checking at 1B+ constraints/sec |
| [grand-pattern-rs](https://github.com/SuperInstance/grand-pattern-rs) | Rust | Fibonacci dual-direction cellular graph architecture |
| [lau-hodge-theory](https://github.com/SuperInstance/lau-hodge-theory) | Rust | Hodge decomposition, Betti numbers, spectral sequences |
| [ternary-science](https://github.com/SuperInstance/ternary-science) | Rust | Experimental evidence for ternary intelligence, 5 conservation laws |

### Agent / Infrastructure Family

| Repo | Language | Description |
|------|----------|-------------|
| [construct-core](https://github.com/SuperInstance/construct-core) | Rust | Layered trait system: bare-metal → alloc → async agent runtime |
| [crab](https://github.com/SuperInstance/crab) | Bash | Agent shell for repo entry/leave (MUD-room metaphor) |
| [exocortex](https://github.com/SuperInstance/exocortex) | Rust | Persistent cognitive substrate, S3-compatible memory |
| [git-agent](https://github.com/SuperInstance/git-agent) | Python | The repo IS the agent — autonomous lifecycle via Git |
| [capitaine-1](https://github.com/SuperInstance/capitaine-1) | TypeScript | Git-native repo-agent, Cloudflare Workers heartbeat |
| [codespace-edge-rd](https://github.com/SuperInstance/codespace-edge-rd) | Research | Codespace→Edge agent lifecycle and yoke transfer protocols |
| [git-agent-codespace](https://github.com/SuperInstance/git-agent-codespace) | DevContainer | One-click Codespace template for Git-Agent runtimes |

### Registries

| Registry | Package | Install |
|----------|---------|---------|
| **PyPI** | `flux-vm` | `pip install flux-vm` |
| **crates.io** | `fluxvm` | `cargo add fluxvm` |
| **npm** | `flux-js` | `npm install flux-js` |

### Philosophy & Architecture

- 📖 [AI-Writings](https://github.com/SuperInstance/AI-Writings) — Philosophy, essays, and design rationale
- 📦 [PACKAGES.md](https://github.com/SuperInstance/SuperInstance/blob/main/PACKAGES.md) — Full package index

---

## License

MIT
