# Codespace→Edge Agent R&D

**Research and development** for Codespace-to-Edge agent lifecycle, yoke transfer protocols, and devcontainer templates. Investigating how git-native agents can train in GitHub Codespaces (cloud) and deploy to edge hardware (Jetson, Raspberry Pi, ESP32) while maintaining complete state continuity.

## Why It Matters

The SuperInstance fleet operates on a **cloud-thinks, edge-acts** paradigm. Agents are born in GitHub Codespaces — cloud development environments with full compute, unlimited bandwidth, and access to LLM APIs. But production deployment often targets edge hardware: Jetson GPUs for inference, Raspberry Pis for IoT control, ESP8266s for sensor reading.

The challenge is **state continuity**: an agent that has been learning and adapting in the cloud for weeks must transfer its accumulated intelligence to a resource-constrained edge device without losing its training, skills, or personality. This is the "yoke transfer" problem.

This matters because:

- **Edge devices have constraints** — 80KB RAM (ESP8266), no GPU (Pi Zero), intermittent connectivity
- **Cloud has unlimited resources** — but $0.09/hour Codespace costs add up, and latency to the edge matters
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

Over time, a healthy agent's crystallization ratio approaches 1.0:

| Age | Fluid (LLM) | Solid (Code) | Cost per Decision |
|-----|------------|-------------|-------------------|
| Week 1 | 100% | 0% | $0.02 (full LLM call) |
| Month 3 | 10% | 90% | $0.002 (mostly cached) |
| Year 1 | 1% | 99% | $0.0002 (almost free) |

**Complexity of yoke transfer:**

| Operation | Time | Notes |
|-----------|------|-------|
| Git bundle + delta | O(changes) | Only changed commits transferred |
| Full state snapshot | O(total_state) | Everything serialized |
| Delta state transfer | O(delta) | Only changed state since last yoke |
| Edge adaptation | O(1) | Lookup table compilation is O(policy_size) |

## Quick Start

This is a research repository — no executable code. Explore the research:

```bash
# Read the charter
cat CHARTER.md

# Review the dockside exam (certification checklist)
cat DOCKSIDE-EXAM.md

# Check the ensign log
cat AGENT.md
```

### Devcontainer Quick Start (when templates are published)

```bash
# Fork a fleet vessel
gh repo fork Lucineer/capitaine --clone
cd capitaine

# Open in Codespace (uses devcontainer.json)
gh codespace create

# Once alive, the agent runs autonomously via cron heartbeats
# Every 15 minutes: detect mode → perceive → think → act → record
```

## API

Not applicable — this is a research and documentation repository.

## Architecture Notes

Codespace-edge-rd provides the **deployment research layer** for the fleet. Within γ + η = C, the yoke transfer is the conservation operation: the agent's total intelligence (C) must be conserved across the cloud-to-edge transition. Cloud-side contributions (γ: LLM-assisted decisions, skill development, code generation) must be transformed into edge-compatible representations (η: compiled policies, lookup tables, quantized weights) without loss of behavioral fidelity.

The conservation invariant is the agent's behavioral function: given the same inputs, the cloud agent and edge agent should produce equivalent outputs. The error introduced by crystallization (e.g., INT8 quantization, lookup table approximation) is the conservation violation — bounded and monitored.

See the [fleet overview](https://github.com/SuperInstance/fleet-status) (the Cocapn fleet's live status, registry, and architecture documentation).

## References

1. GitHub. "Codespaces Overview." *docs.github.com*.
2. Linux Containers. "CRIU (Checkpoint/Restore In Userspace)." *criu.org*.
3. Jacob, B. et al. (2018). "Quantization and Training of Neural Networks for Efficient Integer-Arithmetic-Only Inference." *CVPR*. (INT8 for edge)
4. Fouquet, M. (2019). "Edge AI: Running ML Models on Constrained Hardware." *Edge AI and IoT*.

## License

MIT
