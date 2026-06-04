# Future Integration: codespace-edge-rd

## Current State
Research and development for the Codespace→Edge agent pattern: git-agents live in GitHub Codespaces (cloud IDE with full compute), and the same agent clones to edge hardware in exactly the state left in the cloud. Cloud thinks, edge acts. Research questions cover Codespace-as-habitat, yoke-out protocol, bidirectional sync, and agent lifecycle.

## Integration Opportunities

### With room-as-codespace
This IS the room-as-codespace architecture's research document. Every research question has been answered by the architecture: Codespaces run agents (yes, via OpenClaw), yoke-out uses git branches, bidirectional sync works via commit-push, and the agent lifecycle (spawn → equip → tick → suspend → resume → hibernate → terminate) maps to room lifecycle. codespace-edge-rd becomes the specification document.

### With construct-core
The yoke-out protocol (serialization of state beyond git repos: environment variables, running processes, memory state, skill registry) maps to construct-core's capability export. When a construct migrates from Codespace to Jetson, it serializes its loaded skills, active queries, and accumulated state into a yoke bundle. The receiving hardware reconstructs the construct from the yoke.

### With JetsonClaw1-vessel
The edge deployment target. JetsonClaw1 is the first edge vessel — running agents on Jetson Orin Nano. codespace-edge-rd's bandwidth constraints and delta transfer protocols are tested against JetsonClaw1's WiFi connection. Field-to-war-room sync: Jetson learns on edge, pushes yoke state back to Codespace.

## Dormant Ideas Now Unlockable
The research questions are now answerable. Construct-core provides the state serialization format. ternary-protocol provides the communication layer. Room-as-codespace provides the deployment pattern. The R&D is done; it's time to implement.

## Potential in Mature Systems
Every room can be yoked out to edge hardware. The room runs in the cloud when it needs LLM access, yokes out to Jetson when it needs GPU, and yokes out to ESP32 when it needs bare-metal latency. The same room, three deployments, one agent identity.

## Cross-Pollination Ideas
- **git-agent-codespace**: The template for Codespace rooms
- **lever-runner**: Trust compiler's teach-once-run-forever model for yoke-out state
- **pincherOS**: Shell-portable agent state machine for migration between hardware tiers

## Dependencies for Next Steps
- Implement yoke format based on construct-core's SkillSpec serialization
- Delta transfer protocol using git-bundle
- Bidirectional sync with conflict resolution
