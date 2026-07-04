# UI Product Backlog

## Goal

Turn Alfred Executive UI into a practical executive operating surface while keeping the frontend read-only and the backend canonical.

## Principles

- Obsidian remains the source of truth.
- The dashboard is the interaction layer.
- Important dashboard-entered content must be exportable and queued for write-back to Obsidian.
- Local Mac mode comes first; hosted/VPS/API sync comes later.
- Deep Research is a future tier, not part of this v1 implementation.

## Backlog

### P0

- Collapsible sidebar
- Daily Brief moved near top of navigation
- Persistent floating Ask Alfred bar at the bottom of every page
- Dedicated Follow-ups page
- Dedicated Open Loops page
- Dedicated Actions page
- Work Instructions / Help page
- Admin / Security page

### P1

- Dashboard action ledger model
- Obsidian write-back queue model for important dashboard-entered content
- Cross-platform access model: local Mac now, hosted/VPS/API sync later
- Objective active set and objective detail page
- Board bios, portraits, org chart, board meeting invocation
- Basic enrichment vs Deep Research model

### P2

- Bulk update model
- Project roadmap generation and approval workflow

## Product Notes

### Dashboard action ledger model

Interim safe model:

Dashboard input  
↓  
Alfred interaction ledger  
↓  
Obsidian write-back queue  
↓  
Markdown evidence note  
↓  
ExecutiveState recomputed

### Write-back model

- Do not write back directly from the browser in this phase.
- Capture interaction intent locally first.
- Queue important items for future Obsidian markdown write-back.

### Cross-platform model

- Current mode: local Mac-only usage.
- Future mode: hosted sync/API so Mac, VPS, Telegram, and browser share the same state.

### Admin / Security

- Carry forward the old email authentication concept as a requirement.
- Production deployment requires authentication and administration controls.
- Admin should eventually manage:
  - users
  - allowed emails
  - authentication mode
  - API keys/secrets status, not values
  - access logs
  - sync/write-back settings
  - Obsidian vault path
  - token/deep research limits
