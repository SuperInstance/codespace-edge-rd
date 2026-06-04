# Room Implementation: Codespace Edge

How `codespace-edge-rd` uses the ternary-room trait for edge compute rooms.

## Room Configuration

```rust
use ternary_room::{Room, RoomBuilder, Door, DoorAccess};
use ternary_cell::CellGrid;

let engine_room = RoomBuilder::new("engine-monitor")
    .env("tier", "edge")
    .env("backend", "jetson")
    .env("inference", "local")       // No cloud LLM — local inference
    .env("latency_ms", "50")         // Real-time constraint
    .initial_agent(monitor_agent_id)
    .build();
```

## Edge Room Characteristics

| Property | Value | Why |
|---|---|---|
| Tier | `edge` | Runs on edge hardware (Jetson, RPi) |
| Backend | `jetson` | GPU-accelerated local inference |
| Doors | `Locked` or `OneWay` | No bi-directional room transfer — edge rooms are isolated |
| Ensigns | Pre-loaded | Can't load specialists on demand — compiled in |
| Cell grid | Small | Limited memory — 10-100 cells max |
| Tick rate | High | Real-time requirements → fast ticks |

## The Edge Room Lifecycle

1. **Boot**: Room created from compiled configuration (no dynamic loading)
2. **Load Ensigns**: Specialists compiled into the binary — `SensorEnsign`, `KalmanEnsign`, `AlertEnsign`
3. **Tick Loop**: `CellGrid::tick_all()` runs at fixed frequency (e.g., 20Hz)
4. **Signal**: `TernaryMessenger::Suppress` from any cell triggers immediate alert
5. **Report**: Room state snapshots sent upstream via `OneWay` door to Codespace room
6. **Sleep**: Room suspends when host powers down; state persisted to flash

## Door Configuration for Edge

```rust
// Edge room can push data upstream but can't receive tasks
let upstream = Door::new("engine-monitor", "fleet-coordinator")
    .access(DoorAccess::OneWay("engine-monitor", "fleet-coordinator"));
// Only signals flow out, never commands flow in
```

## Cell Grid for Sensor Fusion

```
┌─────────────────────────────────┐
│  CellGrid (engine-monitor)      │
│  ┌───────┐  ┌───────┐          │
│  │Cell 0 │  │Cell 1 │          │
│  │Temp   │  │Vibr.  │          │
│  │Sensor │  │Sensor │          │
│  └───┬───┘  └───┬───┘          │
│      │Signal    │Signal         │
│      ▼          ▼               │
│  ┌──────────────────┐          │
│  │   Cell 2         │          │
│  │   Fusion         │──Suppress──► Alert Ensign
│  │   (Kalman)       │          │
│  └──────────────────┘          │
└─────────────────────────────────┘
```

Each sensor is a `TernaryCell`. The fusion cell combines signals. If surprise exceeds threshold, the alert ensign fires.

---

*Room implementation for codespace-edge-rd, 2026-06-04*
