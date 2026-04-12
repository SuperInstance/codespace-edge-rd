# 🔬 Codespace→Edge Agent R&D

## The Concept
Git-agents live in GitHub Codespaces (cloud IDE with full compute). Same agent clones to edge hardware in the exact state left in the cloud. Cloud thinks, edge acts.

## Research Questions

### 1. Codespace as Agent Habitat
- [ ] Can an agent fully operate inside a Codespace without external tools?
- [ ] What's the API for programmatic Codespace creation/management?
- [ ] Can Codespaces run background daemons (cron, watchbots)?
- [ ] How long can a Codespace stay alive? Cost model?
- [ ] Can multiple agents share one Codespace?

### 2. Yoke-Out Protocol (Cloud → Edge)
- [ ] What state needs serialization beyond git repos?
- [ ] How to capture: environment variables, running processes, memory state, skill registry
- [ ] Protobuf vs JSON vs git-bundle for yoke format
- [ ] Delta transfer: only ship what changed since last yoke-out
- [ ] Bandwidth constraints for edge targets (Jetson on WiFi, Pi on cellular)

### 3. Codespace↔Edge Sync
- [ ] Can edge push yoke state BACK to Codespace? (field → war room)
- [ ] Bidirectional sync: agent learns on edge, updates cloud yoke
- [ ] Conflict resolution when cloud and edge diverge
- [ ] Git-based sync (commit yoke state as a branch) vs API sync

### 4. Agent Lifecycle
```
SPAWN (Codespace created from template)
  → BOOTCAMP (agent reads charter, learns domain)
  → WORK (agent codes, researches, collaborates)
  → YOKE-OUT (freeze state, transfer to edge)
  → DEPLOY (agent runs on Jetson/Pi/VPS)
  → YOKE-IN (edge agent syncs learnings back to cloud)
  → EVOLVE (updated yoke spawns improved Codespace)
```

### 5. Codespace Templates per Claw Type
- [ ] CUDAClaw template: CUDA toolkit, FLUX runtime, sensor libs
- [ ] ZeroClaw template: minimal Python/Go, FLUX runtime, bottle system
- [ ] HybridClaw template: both + hardware detection scripts
- [ ] Per-role templates: Architect, Foreman, Auditor, Quartermaster

## Current Fleet State
- 2 Codespaces exist on SuperInstance account (shutdown, 2-core/8GB)
- Both can be reactivated or new ones created from `.devcontainer` configs
- Fleet-mechanic already has a `.devcontainer/devcontainer.json`

## API Notes
```bash
# List codespaces
GET /user/codespaces

# Create from repo
POST /user/codespaces
{ "repository": "SuperInstance/hybridclaw", "ref": "main" }

# Start/stop
POST /user/codespaces/{name}/start
POST /user/codespaces/{name}/stop

# Machine types
GET /user/codespaces/machines  # available SKUs
```

## Dependencies
- GitHub Codespaces API (available, tested)
- .devcontainer configs (partially done for fleet-mechanic)
- Yoke serialization format (needs design — see claw-arch research)
- Edge hardware (JetsonClaw1 has Jetson, Oracle1 has VPS)
