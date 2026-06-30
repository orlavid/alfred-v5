# Obsidian Knowledge Platform

Generated: 2026-06-30T21:41:58.616545


## Purpose

Defines the live Obsidian vault as Alfred's authoritative source of truth.

## Responsibilities

- Store source notes, captures, daily logs, people, companies, projects and governance artefacts.
- Remain human-readable and recoverable without Alfred.
- Provide the evidence base for enrichment, routing and semantic retrieval.

## Inputs

- User notes
- Captures
- Daily logs
- Batch enrichments

## Outputs

- Markdown evidence
- Source paths
- Knowledge graph substrate

## Dependencies

- Obsidian Sync
- Markdown files
- Vault filesystem

## Failure Modes

- Vault stale or not synced.
- Wrong vault path indexed.
- Derived artefacts mistaken for source truth.

## Recovery Procedure

- Verify `/docker/obsidian-vault` exists.
- Check markdown count and recent files.
- Confirm sync markers or recent expected notes.
- Rebuild LlamaIndex from the live vault only.

## Source Evidence

### obsidian/vault_summary.txt

Size: 12391 bytes

```text
===== size =====
55M	/docker/obsidian-vault
===== md count =====
4538
===== top folders =====
/docker/obsidian-vault
/docker/obsidian-vault/00 Inbox
/docker/obsidian-vault/00 Inbox/AI Imports
/docker/obsidian-vault/00 Inbox/Captures
/docker/obsidian-vault/00 Inbox/Historical Backfill
/docker/obsidian-vault/01 Daily Logs
/docker/obsidian-vault/02 People
/docker/obsidian-vault/02 People/01. HR
/docker/obsidian-vault/03 Projects
/docker/obsidian-vault/03 Projects/0. Finance
/docker/obsidian-vault/04 Companies
/docker/obsidian-vault/04 Companies/IG
/docker/obsidian-vault/04 Decisions
/docker/obsidian-vault/05 Knowledge
/docker/obsidian-vault/05 Knowledge/01. Compliance
/docker/obsidian-vault/05 Knowledge/AI
/docker/obsidian-vault/05 Open Loops
/docker/obsidian-vault/06 Systems
/docker/obsidian-vault/06 Systems/Entity Registry
/docker/obsidian-vault/06 Systems/Second Brain Scripts
/docker/obsidian-vault/07 AI Memory
/docker/obsidian-vault/07 AI Memory/Agent Council
/docker/obsidian-vault/07 AI Memory/Agent State
/docker/obsidian-vault/07 AI Memory/Agents
/docker/obsidian-vault/07 AI Memory/Alfred v2
/docker/obsidian-vault/07 AI Memory/Delegations
/docker/obsidian-vault/07 AI Memory/Enriched Captures
/docker/obsidian-vault/07 AI Memory/Entities
/docker/obsidian-vault/07 AI Memory/Entity Intelligence
/docker/obsidian-vault/07 AI Memory/Entity Registry
/docker/obsidian-vault/07 AI Memory/Historical Ingestion
/docker/obsidian-vault/07 AI Memory/Reporting Evidence
/docker/obsidian-vault/07 AI Memory/Strategic Graph
/docker/obsidian-vault/07 AI Memory/Strategic Synthesis
/docker/obsidian-vault/07 Executive Briefings
/docker/obsidian-vault/08 Open Loops
/docker/obsidian-vault/08 Open Loops/Escalation
/docker/obsidian-vault/08 Strategic Analysis
/docker/obsidian-vault/08 Strategic Analysis/Image Artifacts
/docker/obsidian-vault/09 Governance
/docker/obsidian-vault/09 Governance/AI Agent Reviews
/docker/obsidian-vault/09 Governance/Agent Deployments
/docker/obsidian-vault/09 Governance/Agent Governance
/docker/obsidian-vault/09 Governance/Agent Opinions
/docker/obsidian-vault/09 Governance/Architecture
/docker/obsidian-vault/09 Governance/Board Packs
/docker/obsidian-vault/09 Governance/Board Secretary
/docker/obsidian-vault/09 Governance/Board Sessions
/docker/obsidian-vault/09 Governance/Capture Lifecycle
/docker/obsidian-vault/09 Governance/Capture Review
/docker/obsidian-vault/09 Governance/Change Management
/docker/obsidian-vault/09 Governance/Daily Governance
/docker/obsidian-vault/09 Governance/Decision Intelligence
/docker/obsidian-vault/09 Governance/Delegation Queue
/docker/obsidian-vault/09 Governance/Escalations
/docker/obsidian-vault/09 Governance/Executive Graph
/docker/obsidian-vault/09 Governance/Executive Metrics
/docker/obsidian-vault/09 Governance/Executive Signals
/docker/obsidian-vault/09 Governance/Governance Intelligence
/docker/obsidian-vault/09 Governance/Healthchecks
/docker/obsidian-vault/09 Governance/Human Action Queue
/docker/obsidian-vault/09 Governance/Objective Intelligence
/docker/obsidian-vault/09 Governance/Objectives
/docker/obsidian-vault/09 Governance/Open Loops
/docker/obsidian-vault/09 Governance/Organisation
/docker/obsidian-vault/09 Governance/Prompt Governance
/docker/obsidian-vault/09 Governance/Recovery
/docker/obsidian-vault/09 Governance/Reflection Intelligence
/docker/obsidian-vault/09 Governance/Reports
/docker/obsidian-vault/09 Governance/Retention Policies
/docker/obsidian-vault/09 Governance/Reviews
/docker/obsidian-vault/09 Governance/Runtime Registry
/docker/obsidian-vault/09 Governance/Service Ownership
/docker/obsidian-vault/09 Governance/State Registry
/docker/obsidian-vault/09 Governance/Tasks
/docker/obsidian-vault/09 Governance/Watchlists
/docker/obsidian-vault/09 Governance/Weekly Councils
/docker/obsidian-vault/10 Domains
/docker/obsidian-vault/10 Domains/Personal
/docker/obsidian-vault/10 Domains/Work
/docker/obsidian-vault/10 Intelligence
/docker/obsidian-vault/10 Intelligence/Agent Collaboration
/docker/obsidian-vault/10 Intelligence/Autonomous Signals
/docker/obsidian-vault/10 Intelligence/Entity Graphs
/docker/obsidian-vault/10 Intelligence/Executive Intelligence
/docker/obsidian-vault/10 Intelligence/Executive Visuals
/docker/obsidian-vault/10 Intelligence/Reasoning Reviews
/docker/obsidian-vault/10 Intelligence/Relationship Memory
/docker/obsidian-vault/10 Intelligence/Retrieval Quality
/docker/obsidian-vault/11 Strategic Intelligence
/docker/obsidian-vault/11 Strategic Intelligence/Contradictions
/docker/obsidian-vault/11 Strategic Intelligence/Decision Register
/docker/obsidian-vault/11 Strategic Intelligence/Executive Narrative
/docker/obsidian-vault/11 Strategic Intelligence/Strategic Drift
/docker/obsidian-vault/11 Strategic Intelligence/Theme Detection
/docker/obsidian-vault/98 Archive
/docker/obsidian-vault/98 Archive/Captures
/docker/obsidian-vault/98 Archive/Historical Backfill
/docker/obsidian-vault/98 Archive/Logs
/docker/obsidian-vault/AI
/docker/obsidian-vault/Alfred
/docker/obsidian-vault/Alfred/Reviews
/docker/obsidian-vault/Attachments
/docker/obsidian-vault/Finance
/docker/obsidian-vault/LLM Wiki
/docker/obsidian-vault/LLM Wiki/People
/docker/obsidian-vault/LLM Wiki/Suppliers
/docker/obsidian-vault/Minutes
/docker/obsidian-vault/People
/docker/obsidian-vault/Phillip @FML
/docker/obsidian-vault/Phillip @FML/IG
/docker/obsidian-vault/Phillip @FML/New Section 2
/docker/obsidian-vault/Phillip @FML/Risk Compliance
/docker/obsidian-vault/Phillip @FML/Strategy or Project
/docker/obsidian-vault/Phillip @FML/Talend and Mentor
/docker/obsidian-vault/Suppliers
/docker/obsidian-vault/Tools
/docker/obsidian-vault/Work import
/docker/obsidian-vault/Work import/Apple Notes
===== recent md =====
Test.md
Telegram.md
Note.md
Inbox.md
Are.md
2026-06-28 16:52 /docker/obsidian-vault/00 Inbox/Test Sync.md.md
2026-06-28 07:10 /docker/obsidian-vault/07 Executive Briefings/2026-06-28 Executive Brief.md
2026-06-28 02:00 /docker/obsidian-vault/09 Governance/Reflection Intelligence/Latest Reflection Intelligence.md
2026-06-28 02:00 /docker/obsidian-vault/09 Governance/Objective Intelligence/Latest Objective Intelligence Report.md
2026-06-28 02:00 /docker/obsidian-vault/09 Governance/Objective Intelligence/2026-06-28 Objective Intelligence Report.md
2026-06-28 02:00 /docker/obsidian-vault/09 Governance/Governance Intelligence/Latest Governance Intelligence.md
2026-06-28 02:00 /docker/obsidian-vault/09 Governance/Executive Metrics/Latest Executive Metrics.md
2026-06-28 02:00 /docker/obsidian-vault/09 Governance/Daily Governance/Latest Daily Governance Index.md
2026-06-28 02:00 /docker/obsidian-vault/09 Governance/Board Secretary/Latest Board Secretary Agenda.md
2026-06-28 02:00 /docker/obsidian-vault/09 Governance/Board Packs/Latest Board Pack.md
2026-06-28 02:00 /docker/obsidian-vault/09 Governance/Board Packs/BOARD-PACK-2026-06-28-020010-WEEKLY.md
2026-06-28 02:00 /docker/obsidian-vault/09 Governance/AI Agent Reviews/Latest AI Agent Reviews.md
2026-06-28 02:00 /docker/obsidian-vault/09 Governance/AI Agent Reviews/Executive Committee.md
2026-06-28 02:00 /docker/obsidian-vault/09 Governance/AI Agent Reviews/Executive AI Briefing.md
2026-06-28 02:00 /docker/obsidian-vault/09 Governance/AI Agent Reviews/AI Agent Debate.md
2026-06-28 00:16 /docker/obsidian-vault/__.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/vCISO.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/Workday.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/Vyanta.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/Vodafone.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/Version 1.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/VCOL Website.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/Upguard.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/Trintech - ADRA.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/Testrail.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/TRAX.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/Sync.com.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/Synapx.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/SwissRe - CatNet.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/Softcat website.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/SoftCat.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/SoftCat portal.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/Sharepoint - Lime Risk.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/Serium.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/SQL Spreads.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/SES.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/SAP Ariba.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/Reg Network.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/QA.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/QA service.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/Power BI.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/PolicyFly.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/Pluralsite.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/PlacingHub.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/Pine Walk.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/PaloAlto.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/PWD Google.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/PO Consilio.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/One Communications.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/Obsidian.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/Nettitude - Security as a service.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/Netitude.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/NAVEX.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/Mudlur.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/Moodys.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/Monday.Com.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/Model Builder.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/Managed Print.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/LloydsListIntelligence.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/Lloyds list.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/LWR.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/Kocho group limited.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/Jira -Atlassian.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/Insurance Insider.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/Idera.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/IBA.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/Hoyle.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/Hillbrooke.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/Hamilton hotel.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/HP.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/Gamma.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/Four Seasons.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/Forcepoint.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/Flight Radar.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/Finscan.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/EE Proposal.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/Dreamix.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/Docusign.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/Docosoft.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/Digital Realty Trust.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/Digicel.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/DEX.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/Cyber Chain Alliance.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/Crowdstrike.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/Consilio.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/Co-Pilot.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/CloudBridge.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/Cloud Ally.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/Cardio.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/Blacksun.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/BitDefender.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/BeyondFS.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/Backupify.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/BDO.md
2026-06-28 00:16 /docker/obsidian-vault/Suppliers/BA OnBusiness.md

```

### trees/vault.json

Size: 872489 bytes

```text
[
  {
    "path": "/docker/obsidian-vault/LLM Wiki",
    "type": "dir",
    "size": 4096,
    "mtime": "2026-06-28T00:02:12.985041"
  },
  {
    "path": "/docker/obsidian-vault/05 Knowledge",
    "type": "dir",
    "size": 4096,
    "mtime": "2026-06-28T00:04:23.359791"
  },
  {
    "path": "/docker/obsidian-vault/04 Decisions",
    "type": "dir",
    "size": 4096,
    "mtime": "2026-06-28T00:08:33.919265"
  },
  {
    "path": "/docker/obsidian-vault/Work import",
    "type": "dir",
    "size": 4096,
    "mtime": "2026-06-28T00:03:08.912931"
  },
  {
    "path": "/docker/obsidian-vault/Finance",
    "type": "dir",
    "size": 4096,
    "mtime": "2026-06-28T16:53:38.301398"
  },
  {
    "path": "/docker/obsidian-vault/08 Open Loops",
    "type": "dir",
    "size": 4096,
    "mtime": "2026-06-28T00:06:14.524592"
  },
  {
    "path": "/docker/obsidian-vault/SSH Key.md",
    "type": "file",
    "size": 731,
    "mtime": "2026-06-10T22:17:13.989000"
  },
  {
    "path": "/docker/obsidian-vault/People",
    "type": "dir",
    "size": 4096,
    "mtime": "2026-06-28T16:53:55.837341"
  },
  {
    "path": "/docker/obsidian-vault/__.md",
    "type": "file",
    "size": 23,
    "mtime": "2026-06-28T00:16:35.243999"
  },
  {
    "path": "/docker/obsidian-vault/Pinewalk migration.md",
    "type": "file",
    "size": 719,
    "mtime": "2026-06-28T00:16:35.226999"
  },
  {
    "path": "/docker/obsidian-vault/05 Open Loops",
    "type": "dir",
    "size": 4096,
    "mtime": "2026-06-28T00:02:49.076969"
  },
  {
    "path": "/docker/obsidian-vault/07 AI Memory",
    "type": "dir",
    "size": 4096,
    "mtime": "2026-06-28T00:08:35.068260"
  },
  {
    "path": "/docker/obsidian-vault/Procurement Policy.md",
    "type": "file",
    "size": 2669,
    "mtime": "2026-06-28T00:16:35.226999"
  },
  {
    "path": "/docker/obsidian-vault/Alfred",
    "type": "dir",
    "size": 4096,
    "mtime": "2026-06-28T00:04:40.519759"
  },
  {
    "path": "/docker/obsidian-vault/02 People",
    "type": "dir",
    "size": 4096,
    "mtime": "2026-06-28T00:08:32.006274"
  },
  {
    "path": "/docker/obsidian-vault/Nettitude.md",
    "type": "file",
    "size": 0,
    "mtime": "2026-06-28T00:16:35.216000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments",
    "type": "dir",
    "size": 12288,
    "mtime": "2026-06-28T00:05:54.607627"
  },
  {
    "path": "/docker/obsidian-vault/06 Systems",
    "type": "dir",
    "size": 4096,
    "mtime": "2026-06-28T00:06:31.900562"
  },
  {
    "path": "/docker/obsidian-vault/AI",
    "type": "dir",
    "size": 4096,
    "mtime": "2026-06-28T16:53:59.893327"
  },
  {
    "path": "/docker/obsidian-vault/Tools",
    "type": "dir",
    "size": 4096,
    "mtime": "2026-06-28T00:03:56.778840"
  },
  {
    "path": "/docker/obsidian-vault/Phase 2 - Vendor Management.md",
    "type": "file",
    "size": 9029,
    "mtime": "2026-06-28T00:16:35.220000"
  },
  {
    "path": "/docker/obsidian-vault/03 Projects",
    "type": "dir",
    "size": 4096,
    "mtime": "2026-06-28T00:05:48.244638"
  },
  {
    "path": "/docker/obsidian-vault/2026-05-07.md",
    "type": "file",
    "size": 404,
    "mtime": "2026-06-28T00:16:35.158999"
  },
  {
    "path": "/docker/obsidian-vault/KYC Company Due Diligence Report.md",
    "type": "file",
    "size": 10541,
    "mtime": "2026-06-28T00:16:35.163000"
  },
  {
    "path": "/docker/obsidian-vault/Minutes",
    "type": "dir",
    "size": 4096,
    "mtime": "2026-06-28T00:04:48.970744"
  },
  {
    "path": "/docker/obsidian-vault/Untitled.base",
    "type": "file",
    "size": 39,
    "mtime": "2026-05-26T15:55:44.489000"
  },
  {
    "path": "/docker/obsidian-vault/Suppliers",
    "type": "dir",
    "size": 12288,
    "mtime": "2026-06-28T16:53:59.233330"
  },
  {
    "path": "/docker/obsidian-vault/Phillip @FML",
    "type": "dir",
    "size": 4096,
    "mtime": "2026-06-28T16:53:58.012334"
  },
  {
    "path": "/docker/obsidian-vault/2026-05-14.md",
    "type": "file",
    "size": 0,
    "mtime": "2026-06-28T00:16:35.158999"
  },
  {
    "path": "/docker/obsidian-vault/01 Daily Logs",
    "type": "dir",
    "size": 4096,
    "mtime": "2026-06-28T00:05:01.138722"
  },
  {
    "path": "/docker/obsidian-vault/2026-06-12.md",
    "type": "file",
    "size": 0,
    "mtime": "2026-06-12T23:05:40.555999"
  },
  {
    "path": "/docker/obsidian-vault/08 Strategic Analysis",
    "type": "dir",
    "size": 4096,
    "mtime": "2026-06-28T00:07:16.378486"
  },
  {
    "path": "/docker/obsidian-vault/Untitled 1.canvas",
    "type": "file",
    "size": 28,
    "mtime": "2026-06-24T09:07:37.880000"
  },
  {
    "path": "/docker/obsidian-vault/09 Governance",
    "type": "dir",
    "size": 4096,
    "mtime": "2026-06-28T00:07:32.667459"
  },
  {
    "path": "/docker/obsidian-vault/10 Intelligence",
    "type": "dir",
    "size": 4096,
    "mtime": "2026-06-28T00:07:07.714501"
  },
  {
    "path": "/docker/obsidian-vault/98 Archive",
    "type": "dir",
    "size": 4096,
    "mtime": "2026-06-28T00:07:32.295459"
  },
  {
    "path": "/docker/obsidian-vault/Untitled.canvas",
    "type": "file",
    "size": 2,
    "mtime": "2026-06-12T23:05:46.112999"
  },
  {
    "path": "/docker/obsidian-vault/2026-05-11.md",
    "type": "file",
    "size": 0,
    "mtime": "2026-06-28T00:16:35.158999"
  },
  {
    "path": "/docker/obsidian-vault/Pernix meeting.md",
    "type": "file",
    "size": 1988,
    "mtime": "2026-06-28T00:16:35.219000"
  },
  {
    "path": "/docker/obsidian-vault/00 Inbox",
    "type": "dir",
    "size": 4096,
    "mtime": "2026-06-28T16:53:27.159435"
  },
  {
    "path": "/docker/obsidian-vault/Claude.md.md",
    "type": "file",
    "size": 3237,
    "mtime": "2026-05-08T20:36:27.176000"
  },
  {
    "path": "/docker/obsidian-vault/04 Companies",
    "type": "dir",
    "size": 12288,
    "mtime": "2026-06-28T00:08:15.453353"
  },
  {
    "path": "/docker/obsidian-vault/11 Strategic Intelligence",
    "type": "dir",
    "size": 4096,
    "mtime": "2026-06-28T00:07:31.324461"
  },
  {
    "path": "/docker/obsidian-vault/07 Executive Briefings",
    "type": "dir",
    "size": 20480,
    "mtime": "2026-06-28T07:10:47.293694"
  },
  {
    "path": "/docker/obsidian-vault/10 Domains",
    "type": "dir",
    "size": 4096,
    "mtime": "2026-06-28T00:05:07.876710"
  },
  {
    "path": "/docker/obsidian-vault/Jira.md",
    "type": "file",
    "size": 0,
    "mtime": "2026-06-28T00:16:35.163000"
  },
  {
    "path": "/docker/obsidian-vault/2026-05-26.md",
    "type": "file",
    "size": 0,
    "mtime": "2026-05-26T10:24:25.966000"
  },
  {
    "path": "/docker/obsidian-vault/Hermes Windows install.md",
    "type": "file",
    "size": 13854,
    "mtime": "2026-06-10T15:27:11.821000"
  },
  {
    "path": "/docker/obsidian-vault/LLM Wiki/People",
    "type": "dir",
    "size": 4096,
    "mtime": "2026-06-28T00:08:31.937275"
  },
  {
    "path": "/docker/obsidian-vault/LLM Wiki/Suppliers",
    "type": "dir",
    "size": 4096,
    "mtime": "2026-06-28T00:08:31.874275"
  },
  {
    "path": "/docker/obsidian-vault/LLM Wiki/index.md",
    "type": "file",
    "size": 2530,
    "mtime": "2026-05-09T05:24:36.519000"
  },
  {
    "path": "/docker/obsidian-vault/05 Knowledge/EOF.md",
    "type": "file",
    "size": 70,
    "mtime": "2026-05-22T21:08:00.420000"
  },
  {
    "path": "/docker/obsidian-vault/05 Knowledge/JSON.md",
    "type": "file",
    "size": 71,
    "mtime": "2026-05-22T21:08:00.420000"
  },
  {
    "path": "/docker/obsidian-vault/05 Knowledge/Add.md",
    "type": "file",
    "size": 70,
    "mtime": "2026-05-22T21:08:00.418999"
  },
  {
    "path": "/docker/obsidian-vault/05 Knowledge/Source\nTelegram.md",
    "type": "file",
    "size": 82,
    "mtime": "2026-05-21T21:23:14.490000"
  },
  {
    "path": "/docker/obsidian-vault/05 Knowledge/GitHub.md",
    "type": "file",
    "size": 73,
    "mtime": "2026-05-22T21:08:00.421000"
  },
  {
    "path": "/docker/obsidian-vault/05 Knowledge/HOME.md",
    "type": "file",
    "size": 71,
    "mtime": "2026-05-22T21:08:00.420000"
  },
  {
    "path": "/docker/obsidian-vault/05 Knowledge/Decisions.md",
    "type": "file",
    "size": 76,
    "mtime": "2026-05-21T09:01:17.443000"
  },
  {
    "path": "/docker/obsidian-vault/05 Knowledge/Needs.md",
    "type": "file",
    "size": 72,
    "mtime": "2026-05-20T22:50:13.153000"
  },
  {
    "path": "/docker/obsidian-vault/05 Knowledge/InsTech 2026.md",
    "type": "file",
    "size": 8552,
    "mtime": "2026-06-11T16:47:10.045000"
  },
  {
    "path": "/docker/obsidian-vault/05 Knowledge/Iseconds.md",
    "type": "file",
    "size": 75,
    "mtime": "2026-05-22T21:08:00.420000"
  },
  {
    "path": "/docker/obsidian-vault/05 Knowledge/Capture.md",
    "type": "file",
    "size": 74,
    "mtime": "2026-05-20T22:50:13.151999"
  },
  {
    "path": "/docker/obsidian-vault/05 Knowledge/Run.md",
    "type": "file",
    "size": 70,
    "mtime": "2026-05-22T21:08:00.421000"
  },
  {
    "path": "/docker/obsidian-vault/05 Knowledge/Configure.md",
    "type": "file",
    "size": 76,
    "mtime": "2026-05-22T21:08:00.418999"
  },
  {
    "path": "/docker/obsidian-vault/05 Knowledge/Seed.md",
    "type": "file",
    "size": 71,
    "mtime": "2026-05-22T21:08:00.421000"
  },
  {
    "path": "/docker/obsidian-vault/05 Knowledge/Content - Decision.md",
    "type": "file",
    "size": 83,
    "mtime": "2026-05-21T09:01:17.443000"
  },
  {
    "path": "/docker/obsidian-vault/05 Knowledge/Content - What.md",
    "type": "file",
    "size": 79,
    "mtime": "2026-05-21T09:01:17.443000"
  },
  {
    "path": "/docker/obsidian-vault/05 Knowledge/Set.md",
    "type": "file",
    "size": 70,
    "mtime": "2026-05-22T21:08:00.421000"
  },
  {
    "path": "/docker/obsidian-vault/05 Knowledge/PATH.md",
    "type": "file",
    "size": 71,
    "mtime": "2026-05-22T21:08:00.420000"
  },
  {
    "path": "/docker/obsidian-vault/05 Knowledge/Ive.md",
    "type": "file",
    "size": 70,
    "mtime": "2026-05-22T21:08:00.421000"
  },
  {
    "path": "/docker/obsidian-vault/05 Knowledge/Source - Telegram.md",
    "type": "file",
    "size": 82,
    "mtime": "2026-05-20T22:50:13.153000"
  },
  {
    "path": "/docker/obsidian-vault/05 Knowledge/Content - Procurement.md",
    "type": "file",
    "size": 86,
    "mtime": "2026-05-20T22:50:13.151999"
  },
  {
    "path": "/docker/obsidian-vault/05 Knowledge/System.md",
    "type": "file",
    "size": 73,
    "mtime": "2026-05-22T21:08:00.421000"
  },
  {
    "path": "/docker/obsidian-vault/05 Knowledge/AI",
    "type": "dir",
    "size": 4096,
    "mtime": "2026-06-28T00:06:33.487560"
  },
  {
    "path": "/docker/obsidian-vault/05 Knowledge/EUR.md",
    "type": "file",
    "size": 70,
    "mtime": "2026-05-22T21:08:00.420000"
  },
  {
    "path": "/docker/obsidian-vault/05 Knowledge/Content\nNote.md",
    "type": "file",
    "size": 79,
    "mtime": "2026-05-22T21:08:00.421000"
  },
  {
    "path": "/docker/obsidian-vault/05 Knowledge/Content - You.md",
    "type": "file",
    "size": 78,
    "mtime": "2026-05-21T10:01:24.845999"
  },
  {
    "path": "/docker/obsidian-vault/05 Knowledge/Example.md",
    "type": "file",
    "size": 74,
    "mtime": "2026-05-22T21:08:00.420000"
  },
  {
    "path": "/docker/obsidian-vault/05 Knowledge/Procurement.md",
    "type": "file",
    "size": 88,
    "mtime": "2026-05-20T22:44:59.865999"
  },
  {
    "path": "/docker/obsidian-vault/05 Knowledge/Next.md",
    "type": "file",
    "size": 71,
    "mtime": "2026-05-22T21:08:00.420000"
  },
  {
    "path": "/docker/obsidian-vault/05 Knowledge/DORA.md",
    "type": "file",
    "size": 81,
    "mtime": "2026-05-20T22:48:38.637000"
  },
  {
    "path": "/docker/obsidian-vault/05 Knowledge/Content\nTest.md",
    "type": "file",
    "size": 79,
    "mtime": "2026-05-21T21:23:14.490000"
  },
  {
    "path": "/docker/obsidian-vault/05 Knowledge/API.md",
    "type": "file",
    "size": 70,
    "mtime": "2026-05-22T21:08:00.418999"
  },
  {
    "path": "/docker/obsidian-vault/05 Knowledge/USER.md",
    "type": "file",
    "size": 71,
    "mtime": "2026-05-22T21:08:00.421000"
  },
  {
    "path": "/docker/obsidian-vault/05 Knowledge/Status - Inbox.md",
    "type": "file",
    "size": 79,
    "mtime": "2026-05-20T22:50:13.153000"
  },
  {
    "path": "/docker/obsidian-vault/05 Knowledge/NousResearch.md",
    "type": "file",
    "size": 79,
    "mtime": "2026-05-22T21:08:00.420000"
  },
  {
    "path": "/docker/obsidian-vault/05 Knowledge/Create.md",
    "type": "file",
    "size": 73,
    "mtime": "2026-05-22T21:08:00.418999"
  },
  {
    "path": "/docker/obsidian-vault/05 Knowledge/Entities.md",
    "type": "file",
    "size": 75,
    "mtime": "2026-05-20T22:50:13.151999"
  },
  {
    "path": "/docker/obsidian-vault/05 Knowledge/Status\nInbox.md",
    "type": "file",
    "size": 79,
    "mtime": "2026-05-21T21:23:14.490000"
  },
  {
    "path": "/docker/obsidian-vault/05 Knowledge/01. Compliance",
    "type": "dir",
    "size": 4096,
    "mtime": "2026-06-28T00:08:31.807275"
  },
  {
    "path": "/docker/obsidian-vault/05 Knowledge/Untitled.canvas",
    "type": "file",
    "size": 2,
    "mtime": "2026-05-24T17:13:29.400000"
  },
  {
    "path": "/docker/obsidian-vault/05 Knowledge/Content\nAre.md",
    "type": "file",
    "size": 78,
    "mtime": "2026-05-21T23:21:34.651999"
  },
  {
    "path": "/docker/obsidian-vault/05 Knowledge/Keep.md",
    "type": "file",
    "size": 71,
    "mtime": "2026-05-22T21:08:00.420000"
  },
  {
    "path": "/docker/obsidian-vault/05 Knowledge/Should.md",
    "type": "file",
    "size": 73,
    "mtime": "2026-05-22T21:08:00.421000"
  },
  {
    "path": "/docker/obsidian-vault/04 Decisions/Monthly Pursource Governance.md",
    "type": "file",
    "size": 13746,
    "mtime": "2026-05-24T15:13:13.342000"
  },
  {
    "path": "/docker/obsidian-vault/04 Decisions/Decision - Hermes Host Networking.md",
    "type": "file",
    "size": 1502,
    "mtime": "2026-05-24T17:13:46.496999"
  },
  {
    "path": "/docker/obsidian-vault/04 Decisions/Capture - 20260520-221048 Decision.md",
    "type": "file",
    "size": 462,
    "mtime": "2026-05-20T23:12:31.476999"
  },
  {
    "path": "/docker/obsidian-vault/04 Decisions/Mancom - ExCo.md",
    "type": "file",
    "size": 637,
    "mtime": "2026-05-24T15:12:28.029000"
  },
  {
    "path": "/docker/obsidian-vault/04 Decisions/Decision Template.md",
    "type": "file",
    "size": 377,
    "mtime": "2026-05-20T20:59:31.753999"
  },
  {
    "path": "/docker/obsidian-vault/Work import/Apple Notes",
    "type": "dir",
    "size": 4096,
    "mtime": "2026-06-28T00:05:32.376666"
  },
  {
    "path": "/docker/obsidian-vault/Finance/Finance review.md",
    "type": "file",
    "size": 30333,
    "mtime": "2026-05-12T14:18:43"
  },
  {
    "path": "/docker/obsidian-vault/Finance/Finance discussion.md",
    "type": "file",
    "size": 13076,
    "mtime": "2026-05-12T14:21:20"
  },
  {
    "path": "/docker/obsidian-vault/Finance/VAT.md",
    "type": "file",
    "size": 2868,
    "mtime": "2026-05-08T22:34:15"
  },
  {
    "path": "/docker/obsidian-vault/Finance/Finance 2024 review.md",
    "type": "file",
    "size": 443,
    "mtime": "2026-06-28T00:16:35.161999"
  },
  {
    "path": "/docker/obsidian-vault/Finance/Finance lookup.md",
    "type": "file",
    "size": 2940,
    "mtime": "2026-05-12T14:20:56"
  },
  {
    "path": "/docker/obsidian-vault/Finance/CAPEX.md",
    "type": "file",
    "size": 1320,
    "mtime": "2026-06-28T00:16:35.161999"
  },
  {
    "path": "/docker/obsidian-vault/Finance/PO.md",
    "type": "file",
    "size": 2866,
    "mtime": "2026-05-14T13:59:46"
  },
  {
    "path": "/docker/obsidian-vault/Finance/Expense management.md",
    "type": "file",
    "size": 2049,
    "mtime": "2026-05-08T22:34:15"
  },
  {
    "path": "/docker/obsidian-vault/Finance/Finance.md",
    "type": "file",
    "size": 342,
    "mtime": "2026-06-28T00:16:35.163000"
  },
  {
    "path": "/docker/obsidian-vault/08 Open Loops/Open Loop Review.md",
    "type": "file",
    "size": 2922,
    "mtime": "2026-05-24T20:01:51"
  },
  {
    "path": "/docker/obsidian-vault/08 Open Loops/Open Loop Register.md",
    "type": "file",
    "size": 2615,
    "mtime": "2026-05-24T20:23:56"
  },
  {
    "path": "/docker/obsidian-vault/08 Open Loops/2026-05-20 Open Loops.md",
    "type": "file",
    "size": 3367,
    "mtime": "2026-05-20T23:08:32.818000"
  },
  {
    "path": "/docker/obsidian-vault/08 Open Loops/Escalation",
    "type": "dir",
    "size": 4096,
    "mtime": "2026-06-28T02:00:10.293432"
  },
  {
    "path": "/docker/obsidian-vault/08 Open Loops/Hermes Open Loops.md",
    "type": "file",
    "size": 4873,
    "mtime": "2026-06-11T22:49:26.635999"
  },
  {
    "path": "/docker/obsidian-vault/08 Open Loops/Loop Candidates.md",
    "type": "file",
    "size": 5230,
    "mtime": "2026-05-24T20:14:22"
  },
  {
    "path": "/docker/obsidian-vault/People/Neil Lindo.md",
    "type": "file",
    "size": 1292,
    "mtime": "2026-05-08T22:34:11"
  },
  {
    "path": "/docker/obsidian-vault/People/Cindy Eves.md",
    "type": "file",
    "size": 3370,
    "mtime": "2026-05-12T14:24:10"
  },
  {
    "path": "/docker/obsidian-vault/People/James Plunkett.md",
    "type": "file",
    "size": 529,
    "mtime": "2026-06-28T00:16:35.217999"
  },
  {
    "path": "/docker/obsidian-vault/People/Olivia Brindle.md",
    "type": "file",
    "size": 2716,
    "mtime": "2026-05-08T22:34:11"
  },
  {
    "path": "/docker/obsidian-vault/People/Graham Dawe.md",
    "type": "file",
    "size": 35681,
    "mtime": "2026-06-28T00:16:35.217999"
  },
  {
    "path": "/docker/obsidian-vault/People/Lee Harper.md",
    "type": "file",
    "size": 923,
    "mtime": "2026-05-08T22:34:11"
  },
  {
    "path": "/docker/obsidian-vault/People/Eleen - Ali - AP.md",
    "type": "file",
    "size": 468,
    "mtime": "2026-06-28T00:16:35.217000"
  },
  {
    "path": "/docker/obsidian-vault/People/Suzanne Wells.md",
    "type": "file",
    "size": 5543,
    "mtime": "2026-05-19T10:06:05"
  },
  {
    "path": "/docker/obsidian-vault/People/Nigel Lee.md",
    "type": "file",
    "size": 1576,
    "mtime": "2026-05-12T14:26:45"
  },
  {
    "path": "/docker/obsidian-vault/People/Edison Lusha.md",
    "type": "file",
    "size": 2329,
    "mtime": "2026-05-08T22:34:11"
  },
  {
    "path": "/docker/obsidian-vault/People/Ricard Torres Marti.md",
    "type": "file",
    "size": 3021,
    "mtime": "2026-05-12T14:26:45"
  },
  {
    "path": "/docker/obsidian-vault/People/Rinku.md",
    "type": "file",
    "size": 7331,
    "mtime": "2026-05-12T14:26:45"
  },
  {
    "path": "/docker/obsidian-vault/People/Micheal Monks.md",
    "type": "file",
    "size": 687,
    "mtime": "2026-05-08T22:45:24"
  },
  {
    "path": "/docker/obsidian-vault/People/Debbie Lean.md",
    "type": "file",
    "size": 188,
    "mtime": "2026-05-08T22:34:11"
  },
  {
    "path": "/docker/obsidian-vault/People/Phil Murfet.md",
    "type": "file",
    "size": 4456,
    "mtime": "2026-06-28T00:16:35.219000"
  },
  {
    "path": "/docker/obsidian-vault/People/Julie Broom.md",
    "type": "file",
    "size": 3499,
    "mtime": "2026-05-08T22:34:11"
  },
  {
    "path": "/docker/obsidian-vault/People/Rhys Puddy - Finance-Expense-Purchase.md",
    "type": "file",
    "size": 3971,
    "mtime": "2026-05-12T14:21:23"
  },
  {
    "path": "/docker/obsidian-vault/People/Ash Bailey.md",
    "type": "file",
    "size": 287,
    "mtime": "2026-05-12T14:18:15"
  },
  {
    "path": "/docker/obsidian-vault/People/Alex Lott.md",
    "type": "file",
    "size": 11361,
    "mtime": "2026-05-12T14:26:45"
  },
  {
    "path": "/docker/obsidian-vault/People/Gary Whiston.md",
    "type": "file",
    "size": 5303,
    "mtime": "2026-05-12T14:24:10"
  },
  {
    "path": "/docker/obsidian-vault/People/Chris Sweetser.md",
    "type": "file",
    "size": 2070,
    "mtime": "2026-05-08T22:34:11"
  },
  {
    "path": "/docker/obsidian-vault/People/Dinesh.md",
    "type": "file",
    "size": 249,
    "mtime": "2026-06-28T00:16:35.217000"
  },
  {
    "path": "/docker/obsidian-vault/People/Phillip Doheny.md",
    "type": "file",
    "size": 933,
    "mtime": "2026-06-28T00:16:35.219000"
  },
  {
    "path": "/docker/obsidian-vault/People/Yvonne Lancaster - Risk.md",
    "type": "file",
    "size": 1440,
    "mtime": "2026-05-08T22:45:24"
  },
  {
    "path": "/docker/obsidian-vault/People/David Reid.md",
    "type": "file",
    "size": 1292,
    "mtime": "2026-05-12T14:20:57"
  },
  {
    "path": "/docker/obsidian-vault/People/Emily Puddifer.md",
    "type": "file",
    "size": 50,
    "mtime": "2026-06-28T00:16:35.217000"
  },
  {
    "path": "/docker/obsidian-vault/People/Denise Bareford.md",
    "type": "file",
    "size": 5400,
    "mtime": "2026-05-12T14:21:22"
  },
  {
    "path": "/docker/obsidian-vault/People/Gary McInally.md",
    "type": "file",
    "size": 1320,
    "mtime": "2026-05-08T22:34:11"
  },
  {
    "path": "/docker/obsidian-vault/People/John Paul O'Hare.md",
    "type": "file",
    "size": 2092,
    "mtime": "2026-05-12T14:26:45"
  },
  {
    "path": "/docker/obsidian-vault/People/Gyorgy Penczu.md",
    "type": "file",
    "size": 4240,
    "mtime": "2026-05-18T13:59:00"
  },
  {
    "path": "/docker/obsidian-vault/People/Francesca Harrison.md",
    "type": "file",
    "size": 1184,
    "mtime": "2026-05-08T22:45:24"
  },
  {
    "path": "/docker/obsidian-vault/People/Stephen.md",
    "type": "file",
    "size": 1974,
    "mtime": "2026-05-08T22:34:12"
  },
  {
    "path": "/docker/obsidian-vault/People/Chika.md",
    "type": "file",
    "size": 1205,
    "mtime": "2026-05-22T18:09:02"
  },
  {
    "path": "/docker/obsidian-vault/People/Ali Ajaz.md",
    "type": "file",
    "size": 415,
    "mtime": "2026-06-28T00:16:35.217000"
  },
  {
    "path": "/docker/obsidian-vault/People/Mat Nieznanski.md",
    "type": "file",
    "size": 158,
    "mtime": "2026-06-28T00:16:35.219000"
  },
  {
    "path": "/docker/obsidian-vault/People/Mark Rowe - Compliance.md",
    "type": "file",
    "size": 5606,
    "mtime": "2026-05-12T14:21:23"
  },
  {
    "path": "/docker/obsidian-vault/People/Joe Bosberry.md",
    "type": "file",
    "size": 19751,
    "mtime": "2026-06-28T00:16:35.217999"
  },
  {
    "path": "/docker/obsidian-vault/People/Michael Hay.md",
    "type": "file",
    "size": 1239,
    "mtime": "2026-05-08T22:34:11"
  },
  {
    "path": "/docker/obsidian-vault/People/Marc Avery.md",
    "type": "file",
    "size": 836,
    "mtime": "2026-05-08T22:34:11"
  },
  {
    "path": "/docker/obsidian-vault/People/Matt Rudge.md",
    "type": "file",
    "size": 4304,
    "mtime": "2026-05-12T14:26:47"
  },
  {
    "path": "/docker/obsidian-vault/People/Will Thrower.md",
    "type": "file",
    "size": 2025,
    "mtime": "2026-05-08T22:34:12"
  },
  {
    "path": "/docker/obsidian-vault/People/Donal Glackin.md",
    "type": "file",
    "size": 1179,
    "mtime": "2026-05-12T14:18:43"
  },
  {
    "path": "/docker/obsidian-vault/People/Jake Groves - Infrastructure.md",
    "type": "file",
    "size": 531,
    "mtime": "2026-05-12T14:20:57"
  },
  {
    "path": "/docker/obsidian-vault/People/Megan.md",
    "type": "file",
    "size": 5920,
    "mtime": "2026-05-18T11:34:07"
  },
  {
    "path": "/docker/obsidian-vault/People/Mark Dean.md",
    "type": "file",
    "size": 10761,
    "mtime": "2026-05-12T14:24:10"
  },
  {
    "path": "/docker/obsidian-vault/People/Anna.md",
    "type": "file",
    "size": 2653,
    "mtime": "2026-05-08T22:45:24"
  },
  {
    "path": "/docker/obsidian-vault/People/Marcus Denison.md",
    "type": "file",
    "size": 85,
    "mtime": "2026-06-28T00:16:35.217999"
  },
  {
    "path": "/docker/obsidian-vault/People/Dee Pang.md",
    "type": "file",
    "size": 710,
    "mtime": "2026-05-08T22:34:11"
  },
  {
    "path": "/docker/obsidian-vault/People/Andy Wetmiller - CTO.md",
    "type": "file",
    "size": 1942,
    "mtime": "2026-05-08T22:45:24"
  },
  {
    "path": "/docker/obsidian-vault/People/Bernie 11.md",
    "type": "file",
    "size": 1077,
    "mtime": "2026-05-08T22:45:24"
  },
  {
    "path": "/docker/obsidian-vault/People/Neil Flanagan.md",
    "type": "file",
    "size": 2914,
    "mtime": "2026-05-12T14:20:57"
  },
  {
    "path": "/docker/obsidian-vault/People/Julia Weeks - Legal.md",
    "type": "file",
    "size": 4289,
    "mtime": "2026-05-12T14:26:45"
  },
  {
    "path": "/docker/obsidian-vault/People/Dan Clow.md",
    "type": "file",
    "size": 7135,
    "mtime": "2026-05-20T10:36:18"
  },
  {
    "path": "/docker/obsidian-vault/People/Tom Lawson.md",
    "type": "file",
    "size": 1518,
    "mtime": "2026-05-15T09:20:41"
  },
  {
    "path": "/docker/obsidian-vault/People/Annu Dhillon - Service Desk.md",
    "type": "file",
    "size": 1271,
    "mtime": "2026-05-12T14:18:15"
  },
  {
    "path": "/docker/obsidian-vault/People/Niall Purcell.md",
    "type": "file",
    "size": 656,
    "mtime": "2026-05-08T22:34:11"
  },
  {
    "path": "/docker/obsidian-vault/People/John Hurworth.md",
    "type": "file",
    "size": 10352,
    "mtime": "2026-05-15T09:20:41"
  },
  {
    "path": "/docker/obsidian-vault/05 Open Loops/Open Loops.md",
    "type": "file",
    "size": 221,
    "mtime": "2026-05-20T23:17:21.569999"
  },
  {
    "path": "/docker/obsidian-vault/07 AI Memory/2026-05-25 Hermes Conversations.md",
    "type": "file",
    "size": 126,
    "mtime": "2026-05-25T18:44:55.351000"
  },
  {
    "path": "/docker/obsidian-vault/07 AI Memory/Agent Council",
    "type": "dir",
    "size": 4096,
    "mtime": "2026-06-28T00:06:04.832609"
  },
  {
    "path": "/docker/obsidian-vault/07 AI Memory/Agent State",
    "type": "dir",
    "size": 4096,
    "mtime": "2026-06-28T00:06:55.745521"
  },
  {
    "path": "/docker/obsidian-vault/07 AI Memory/Reporting Evidence",
    "type": "dir",
    "size": 4096,
    "mtime": "2026-06-28T00:07:17.688484"
  },
  {
    "path": "/docker/obsidian-vault/07 AI Memory/Strategic Graph",
    "type": "dir",
    "size": 4096,
    "mtime": "2026-06-28T00:06:36.057555"
  },
  {
    "path": "/docker/obsidian-vault/07 AI Memory/Agents",
    "type": "dir",
    "size": 4096,
    "mtime": "2026-06-28T00:08:17.648343"
  },
  {
    "path": "/docker/obsidian-vault/07 AI Memory/Entities",
    "type": "dir",
    "size": 57344,
    "mtime": "2026-06-28T16:53:25.847439"
  },
  {
    "path": "/docker/obsidian-vault/07 AI Memory/Alfred v2",
    "type": "dir",
    "size": 4096,
    "mtime": "2026-06-28T02:00:03.909450"
  },
  {
    "path": "/docker/obsidian-vault/07 AI Memory/Entity Intelligence",
    "type": "dir",
    "size": 4096,
    "mtime": "2026-06-28T00:07:25.527471"
  },
  {
    "path": "/docker/obsidian-vault/07 AI Memory/Historical Ingestion",
    "type": "dir",
    "size": 4096,
    "mtime": "2026-06-28T00:08:01.316410"
  },
  {
    "path": "/docker/obsidian-vault/07 AI Memory/Entity Registry",
    "type": "dir",
    "size": 4096,
    "mtime": "2026-06-28T00:06:46.617537"
  },
  {
    "path": "/docker/obsidian-vault/07 AI Memory/Strategic Synthesis",
    "type": "dir",
    "size": 4096,
    "mtime": "2026-06-28T00:07:25.388471"
  },
  {
    "path": "/docker/obsidian-vault/07 AI Memory/Operating Manual.md",
    "type": "file",
    "size": 1836,
    "mtime": "2026-05-20T21:02:46.763000"
  },
  {
    "path": "/docker/obsidian-vault/07 AI Memory/Enriched Captures",
    "type": "dir",
    "size": 36864,
    "mtime": "2026-06-28T00:08:31.382277"
  },
  {
    "path": "/docker/obsidian-vault/07 AI Memory/Delegations",
    "type": "dir",
    "size": 4096,
    "mtime": "2026-06-28T00:06:00.542617"
  },
  {
    "path": "/docker/obsidian-vault/Alfred/Reviews",
    "type": "dir",
    "size": 4096,
    "mtime": "2026-06-28T00:04:40.520759"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Neil Lindo.md",
    "type": "file",
    "size": 1294,
    "mtime": "2026-05-24T15:13:13.546000"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Cindy Eves.md",
    "type": "file",
    "size": 12698,
    "mtime": "2026-06-10T08:55:34.234999"
  },
  {
    "path": "/docker/obsidian-vault/02 People/James Plunkett.md",
    "type": "file",
    "size": 529,
    "mtime": "2026-05-08T22:34:11.831000"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Olivia Brindle.md",
    "type": "file",
    "size": 2739,
    "mtime": "2026-05-24T15:13:13.548000"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Graham Dawe.md",
    "type": "file",
    "size": 44778,
    "mtime": "2026-06-26T14:11:32.362999"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Lee Harper.md",
    "type": "file",
    "size": 962,
    "mtime": "2026-05-24T15:13:13.540999"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Eleen - Ali - AP.md",
    "type": "file",
    "size": 468,
    "mtime": "2026-05-08T22:45:24.220000"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Suzanne Wells.md",
    "type": "file",
    "size": 5757,
    "mtime": "2026-05-24T15:13:13.552000"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Nigel Lee.md",
    "type": "file",
    "size": 1670,
    "mtime": "2026-05-24T15:13:13.548000"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Edison Lusha.md",
    "type": "file",
    "size": 2342,
    "mtime": "2026-05-24T15:13:13.533999"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Ricard Torres Marti.md",
    "type": "file",
    "size": 3024,
    "mtime": "2026-05-24T15:13:13.551000"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Oracle Procurement.md",
    "type": "file",
    "size": 82,
    "mtime": "2026-05-20T22:53:41.203000"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Rinku.md",
    "type": "file",
    "size": 7539,
    "mtime": "2026-05-24T17:14:20.177000"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Micheal Monks.md",
    "type": "file",
    "size": 700,
    "mtime": "2026-05-24T15:13:13.545000"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Install Hermes.md",
    "type": "file",
    "size": 78,
    "mtime": "2026-05-22T21:08:00.420000"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Debbie Lean.md",
    "type": "file",
    "size": 214,
    "mtime": "2026-05-24T15:13:13.529999"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Auto Links.md",
    "type": "file",
    "size": 74,
    "mtime": "2026-05-20T22:50:13.151999"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Phil Murfet.md",
    "type": "file",
    "size": 4456,
    "mtime": "2026-05-08T22:34:12.010999"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Julie Broom.md",
    "type": "file",
    "size": 3537,
    "mtime": "2026-05-24T17:14:20.176000"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Rhys Puddy - Finance-Expense-Purchase.md",
    "type": "file",
    "size": 4010,
    "mtime": "2026-05-24T15:13:13.549999"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Ash Bailey.md",
    "type": "file",
    "size": 292,
    "mtime": "2026-05-24T15:13:13.526000"
  },
  {
    "path": "/docker/obsidian-vault/02 People/01. HR",
    "type": "dir",
    "size": 4096,
    "mtime": "2026-06-28T00:04:29.919779"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Alex Lott.md",
    "type": "file",
    "size": 18776,
    "mtime": "2026-06-26T16:53:58.660000"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Gary Whiston.md",
    "type": "file",
    "size": 5411,
    "mtime": "2026-05-24T17:14:20.170000"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Chris Sweetser.md",
    "type": "file",
    "size": 2080,
    "mtime": "2026-05-24T15:12:28.030999"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Content - Maria Jose Lloret Crespo.md",
    "type": "file",
    "size": 96,
    "mtime": "2026-05-20T22:53:41.203000"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Dinesh.md",
    "type": "file",
    "size": 249,
    "mtime": "2026-05-08T22:34:11.721999"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Verify Hermes.md",
    "type": "file",
    "size": 77,
    "mtime": "2026-05-22T21:08:00.421000"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Phillip Doheny.md",
    "type": "file",
    "size": 933,
    "mtime": "2026-05-08T22:47:18.542000"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Processing Notes.md",
    "type": "file",
    "size": 80,
    "mtime": "2026-05-20T22:50:13.153000"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Start Hermes.md",
    "type": "file",
    "size": 76,
    "mtime": "2026-05-22T21:08:00.421000"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Ensure Hermes.md",
    "type": "file",
    "size": 77,
    "mtime": "2026-05-22T21:08:00.420000"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Yvonne Lancaster - Risk.md",
    "type": "file",
    "size": 1450,
    "mtime": "2026-05-24T15:12:28.042999"
  },
  {
    "path": "/docker/obsidian-vault/02 People/David Reid.md",
    "type": "file",
    "size": 1640,
    "mtime": "2026-06-08T16:17:09.069000"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Emily Puddifer.md",
    "type": "file",
    "size": 50,
    "mtime": "2026-05-08T22:34:11.730999"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Denise Bareford.md",
    "type": "file",
    "size": 5508,
    "mtime": "2026-05-24T17:14:20.168999"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Garry Sweeney.md",
    "type": "file",
    "size": 1960,
    "mtime": "2026-05-28T14:31:36.783999"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Gary McInally.md",
    "type": "file",
    "size": 1333,
    "mtime": "2026-05-24T15:13:13.535000"
  },
  {
    "path": "/docker/obsidian-vault/02 People/John Paul O'Hare.md",
    "type": "file",
    "size": 2108,
    "mtime": "2026-05-24T15:13:13.539000"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Gyorgy Penczu.md",
    "type": "file",
    "size": 9243,
    "mtime": "2026-06-22T13:47:14.868999"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Francesca Harrison.md",
    "type": "file",
    "size": 1197,
    "mtime": "2026-05-24T15:13:13.533999"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Stephen.md",
    "type": "file",
    "size": 1976,
    "mtime": "2026-05-24T15:13:13.552000"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Obsidian Sync.md",
    "type": "file",
    "size": 77,
    "mtime": "2026-05-21T21:23:14.490000"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Chika.md",
    "type": "file",
    "size": 3421,
    "mtime": "2026-06-23T16:50:34.321000"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Ali Ajaz.md",
    "type": "file",
    "size": 415,
    "mtime": "2026-05-08T22:34:11.660000"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Mat Nieznanski.md",
    "type": "file",
    "size": 1250,
    "mtime": "2026-06-23T16:20:19.763999"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Mark Rowe - Compliance.md",
    "type": "file",
    "size": 5622,
    "mtime": "2026-05-24T15:13:13.542999"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Joe Bosberry.md",
    "type": "file",
    "size": 27477,
    "mtime": "2026-06-26T14:08:25.401000"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Auto Tags.md",
    "type": "file",
    "size": 73,
    "mtime": "2026-05-20T22:50:13.151999"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Michael Hay.md",
    "type": "file",
    "size": 1252,
    "mtime": "2026-05-24T15:13:13.545000"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Marc Avery.md",
    "type": "file",
    "size": 849,
    "mtime": "2026-05-24T15:13:13.542000"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Create Hermes.md",
    "type": "file",
    "size": 77,
    "mtime": "2026-05-22T21:08:00.418999"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Matt Rudge.md",
    "type": "file",
    "size": 4345,
    "mtime": "2026-05-25T10:23:20.973000"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Will Thrower.md",
    "type": "file",
    "size": 2051,
    "mtime": "2026-05-24T15:13:13.553999"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Donal Glackin.md",
    "type": "file",
    "size": 2428,
    "mtime": "2026-06-15T15:55:12.687999"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Jake Groves - Infrastructure.md",
    "type": "file",
    "size": 547,
    "mtime": "2026-05-24T15:13:13.536999"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Megan.md",
    "type": "file",
    "size": 5914,
    "mtime": "2026-06-15T11:06:43.665999"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Mark Dean.md",
    "type": "file",
    "size": 10877,
    "mtime": "2026-05-24T17:14:20.177000"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Anna.md",
    "type": "file",
    "size": 2666,
    "mtime": "2026-05-24T15:13:13.523999"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Marcus Denison.md",
    "type": "file",
    "size": 85,
    "mtime": "2026-05-08T22:34:11.923000"
  },
  {
    "path": "/docker/obsidian-vault/02 People/MSCI World UCITS.md",
    "type": "file",
    "size": 80,
    "mtime": "2026-05-22T21:08:00.420000"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Microsoft Azure.md",
    "type": "file",
    "size": 79,
    "mtime": "2026-05-20T22:50:13.153000"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Dee Pang.md",
    "type": "file",
    "size": 712,
    "mtime": "2026-05-24T15:13:13.529999"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Andy Wetmiller - CTO.md",
    "type": "file",
    "size": 1967,
    "mtime": "2026-05-24T15:13:13.523999"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Bernie 11.md",
    "type": "file",
    "size": 1090,
    "mtime": "2026-05-24T15:13:13.526000"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Neil Flanagan.md",
    "type": "file",
    "size": 3013,
    "mtime": "2026-05-24T15:13:13.546000"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Jonathan Croud.md",
    "type": "file",
    "size": 2992,
    "mtime": "2026-06-25T10:24:04.759999"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Julia Weeks - Legal.md",
    "type": "file",
    "size": 7797,
    "mtime": "2026-06-25T14:31:51.114000"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Dan Clow.md",
    "type": "file",
    "size": 8528,
    "mtime": "2026-06-24T11:22:08.223000"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Related Memories.md",
    "type": "file",
    "size": 80,
    "mtime": "2026-05-20T22:50:13.153000"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Tom Lawson.md",
    "type": "file",
    "size": 1543,
    "mtime": "2026-05-24T15:13:13.552999"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Decision Template.md",
    "type": "file",
    "size": 81,
    "mtime": "2026-05-21T09:01:17.443000"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Pearly NG.md",
    "type": "file",
    "size": 184,
    "mtime": "2026-05-29T11:45:37.256000"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Annu Dhillon - Service Desk.md",
    "type": "file",
    "size": 1289,
    "mtime": "2026-05-24T15:13:13.525000"
  },
  {
    "path": "/docker/obsidian-vault/02 People/Niall Purcell.md",
    "type": "file",
    "size": 768,
    "mtime": "2026-06-22T12:31:43.466000"
  },
  {
    "path": "/docker/obsidian-vault/02 People/John Hurworth.md",
    "type": "file",
    "size": 10552,
    "mtime": "2026-05-24T15:13:13.539000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507100138-0.png",
    "type": "file",
    "size": 264899,
    "mtime": "2026-05-07T10:01:39.874000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507085306-1.png",
    "type": "file",
    "size": 318879,
    "mtime": "2026-05-07T08:53:08.302999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507085142-0.png",
    "type": "file",
    "size": 191375,
    "mtime": "2026-05-07T08:51:43.625000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507134509-10.png",
    "type": "file",
    "size": 181283,
    "mtime": "2026-05-07T13:45:10.269999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/f23fa4f1-6832-479a-822d-3f1b624f26bf (1).md",
    "type": "file",
    "size": 1555904,
    "mtime": "2026-06-04T15:37:02.006000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507084307-0.png",
    "type": "file",
    "size": 720,
    "mtime": "2026-05-07T08:43:08.836999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507134109-1.png",
    "type": "file",
    "size": 107232,
    "mtime": "2026-05-07T13:41:10.835999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507134515-14.png",
    "type": "file",
    "size": 93748,
    "mtime": "2026-05-07T13:45:16.670000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507100410-0.png",
    "type": "file",
    "size": 50311,
    "mtime": "2026-05-07T10:04:11.915999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507100350-0.jpeg",
    "type": "file",
    "size": 6178,
    "mtime": "2026-05-07T10:03:51.828999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507100252-0.png",
    "type": "file",
    "size": 97456,
    "mtime": "2026-05-07T10:02:57.381000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507100417-1.png",
    "type": "file",
    "size": 63081,
    "mtime": "2026-05-07T10:04:19.023999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Pasted image 20260511162016.png",
    "type": "file",
    "size": 24973,
    "mtime": "2026-05-11T16:20:16.602999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507100317-0.png",
    "type": "file",
    "size": 4962,
    "mtime": "2026-05-07T10:03:18.921999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507134500-3.png",
    "type": "file",
    "size": 182029,
    "mtime": "2026-05-07T13:45:01.180999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507100428-2.png",
    "type": "file",
    "size": 203431,
    "mtime": "2026-05-07T10:04:30.339999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507085244-0.png",
    "type": "file",
    "size": 286514,
    "mtime": "2026-05-07T08:52:45.342000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507085143-1.png",
    "type": "file",
    "size": 245913,
    "mtime": "2026-05-07T08:51:44.960000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507134108-0.png",
    "type": "file",
    "size": 123179,
    "mtime": "2026-05-07T13:41:09.753999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507100652-2.png",
    "type": "file",
    "size": 208072,
    "mtime": "2026-05-07T10:06:56.377000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507100122-2.png",
    "type": "file",
    "size": 7448,
    "mtime": "2026-05-07T10:01:23.963999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507085259-4.png",
    "type": "file",
    "size": 151293,
    "mtime": "2026-05-07T08:53:01.405999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507084538-4.png",
    "type": "file",
    "size": 291225,
    "mtime": "2026-05-07T08:45:42.654999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507100123-3.png",
    "type": "file",
    "size": 6323,
    "mtime": "2026-05-07T10:01:28.526999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507134514-12.png",
    "type": "file",
    "size": 46690,
    "mtime": "2026-05-07T13:45:14.947000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507084321-0.png",
    "type": "file",
    "size": 374,
    "mtime": "2026-05-07T08:43:26.648999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507085126-1.png",
    "type": "file",
    "size": 37288,
    "mtime": "2026-05-07T08:51:27.711999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507084959-1.png",
    "type": "file",
    "size": 17556,
    "mtime": "2026-05-07T08:50:00.089999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507100120-0.png",
    "type": "file",
    "size": 21897,
    "mtime": "2026-05-07T10:01:21.305000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507085245-1.png",
    "type": "file",
    "size": 192777,
    "mtime": "2026-05-07T08:52:46.720999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507084542-5.png",
    "type": "file",
    "size": 266519,
    "mtime": "2026-05-07T08:45:43.772000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507100323-5.png",
    "type": "file",
    "size": 13372,
    "mtime": "2026-05-07T10:03:27.420000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507134510-11.png",
    "type": "file",
    "size": 119282,
    "mtime": "2026-05-07T13:45:14.128999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507085237-0.png",
    "type": "file",
    "size": 123545,
    "mtime": "2026-05-07T08:52:39.105999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507084331-0.png",
    "type": "file",
    "size": 105720,
    "mtime": "2026-05-07T08:43:32.904000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507085301-5.png",
    "type": "file",
    "size": 174204,
    "mtime": "2026-05-07T08:53:02.450999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507100132-7.png",
    "type": "file",
    "size": 25676,
    "mtime": "2026-05-07T10:01:33.776999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507134114-5.png",
    "type": "file",
    "size": 288264,
    "mtime": "2026-05-07T13:41:15.545000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507084500-0.png",
    "type": "file",
    "size": 374,
    "mtime": "2026-05-07T08:45:05.575999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507100327-6.png",
    "type": "file",
    "size": 34487,
    "mtime": "2026-05-07T10:03:28.533999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507134131-1.png",
    "type": "file",
    "size": 3659,
    "mtime": "2026-05-07T13:41:32.269000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507084209-1.png",
    "type": "file",
    "size": 384,
    "mtime": "2026-05-07T08:42:10.368999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507085125-0.png",
    "type": "file",
    "size": 6147,
    "mtime": "2026-05-07T08:51:26.637000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507084535-2.png",
    "type": "file",
    "size": 303582,
    "mtime": "2026-05-07T08:45:37.125999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507095958-0.png",
    "type": "file",
    "size": 393310,
    "mtime": "2026-05-07T10:00:00.013000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507100808-0.png",
    "type": "file",
    "size": 195989,
    "mtime": "2026-05-07T10:08:12.486999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507085155-3.png",
    "type": "file",
    "size": 119221,
    "mtime": "2026-05-07T08:51:57.232000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507085004-0.png",
    "type": "file",
    "size": 35924,
    "mtime": "2026-05-07T08:50:09.710000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507085027-0.png",
    "type": "file",
    "size": 145623,
    "mtime": "2026-05-07T08:50:28.941999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507100041-2.png",
    "type": "file",
    "size": 127965,
    "mtime": "2026-05-07T10:00:45.555000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507134505-6.png",
    "type": "file",
    "size": 88493,
    "mtime": "2026-05-07T13:45:06.732000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507085034-0.png",
    "type": "file",
    "size": 56989,
    "mtime": "2026-05-07T08:50:36.059000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507085111-2.png",
    "type": "file",
    "size": 123744,
    "mtime": "2026-05-07T08:51:13.766000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507084559-0.png",
    "type": "file",
    "size": 68095,
    "mtime": "2026-05-07T08:46:00.779999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507084214-1.png",
    "type": "file",
    "size": 282148,
    "mtime": "2026-05-07T08:42:16.134000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507134111-3.png",
    "type": "file",
    "size": 235279,
    "mtime": "2026-05-07T13:41:13.375999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507100331-0.png",
    "type": "file",
    "size": 2326,
    "mtime": "2026-05-07T10:03:32.835000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507100318-1.png",
    "type": "file",
    "size": 4599,
    "mtime": "2026-05-07T10:03:19.917999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Pasted image 20260526113344.png",
    "type": "file",
    "size": 259849,
    "mtime": "2026-05-26T11:33:44.447000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507134507-8.png",
    "type": "file",
    "size": 15843,
    "mtime": "2026-05-07T13:45:08.601000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507100416-0.png",
    "type": "file",
    "size": 287026,
    "mtime": "2026-05-07T10:04:17.703999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507085135-5.png",
    "type": "file",
    "size": 16838,
    "mtime": "2026-05-07T08:51:36.450000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507084543-6.png",
    "type": "file",
    "size": 406385,
    "mtime": "2026-05-07T08:45:45.040999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507100319-2.png",
    "type": "file",
    "size": 14835,
    "mtime": "2026-05-07T10:03:21.115999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507100034-0.png",
    "type": "file",
    "size": 233573,
    "mtime": "2026-05-07T10:00:35.388999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507084453-0.png",
    "type": "file",
    "size": 1442,
    "mtime": "2026-05-07T08:44:54.016000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507100246-0.png",
    "type": "file",
    "size": 58481,
    "mtime": "2026-05-07T10:02:47.753000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507100038-0.png",
    "type": "file",
    "size": 343924,
    "mtime": "2026-05-07T10:00:39.667999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507085247-3.png",
    "type": "file",
    "size": 139907,
    "mtime": "2026-05-07T08:52:59.813999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507100228-0.png",
    "type": "file",
    "size": 80724,
    "mtime": "2026-05-07T10:02:29.431999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507100000-1.png",
    "type": "file",
    "size": 800385,
    "mtime": "2026-05-07T10:00:02.010999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Pasted image 20260518162228.png",
    "type": "file",
    "size": 196597,
    "mtime": "2026-05-18T16:22:28.582999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507134514-13.png",
    "type": "file",
    "size": 89440,
    "mtime": "2026-05-07T13:45:15.815000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507134508-9.png",
    "type": "file",
    "size": 94418,
    "mtime": "2026-05-07T13:45:09.382999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507100651-1.png",
    "type": "file",
    "size": 266772,
    "mtime": "2026-05-07T10:06:52.377000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507084511-0.png",
    "type": "file",
    "size": 158117,
    "mtime": "2026-05-07T08:45:13.151000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507100423-0.png",
    "type": "file",
    "size": 463869,
    "mtime": "2026-05-07T10:04:24.698999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507085128-3.png",
    "type": "file",
    "size": 8095,
    "mtime": "2026-05-07T08:51:33.516999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507085246-2.png",
    "type": "file",
    "size": 93976,
    "mtime": "2026-05-07T08:52:47.825999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507134506-7.png",
    "type": "file",
    "size": 84047,
    "mtime": "2026-05-07T13:45:07.585999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507085109-1.png",
    "type": "file",
    "size": 127915,
    "mtime": "2026-05-07T08:51:11.003000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507100322-4.png",
    "type": "file",
    "size": 12713,
    "mtime": "2026-05-07T10:03:23.315999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507084957-0.png",
    "type": "file",
    "size": 94370,
    "mtime": "2026-05-07T08:49:59.058000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507100446-0.png",
    "type": "file",
    "size": 46912,
    "mtime": "2026-05-07T10:04:47.678999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507100656-3.png",
    "type": "file",
    "size": 42648,
    "mtime": "2026-05-07T10:06:57.226999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507084257-0.png",
    "type": "file",
    "size": 892531,
    "mtime": "2026-05-07T08:42:58.871000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507100021-0.png",
    "type": "file",
    "size": 249489,
    "mtime": "2026-05-07T10:00:23.173000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507084856-0.png",
    "type": "file",
    "size": 149616,
    "mtime": "2026-05-07T08:48:57.970999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507100351-1.jpeg",
    "type": "file",
    "size": 6178,
    "mtime": "2026-05-07T10:03:53.542999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507100321-3.png",
    "type": "file",
    "size": 8569,
    "mtime": "2026-05-07T10:03:22.068000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507085144-2.png",
    "type": "file",
    "size": 102197,
    "mtime": "2026-05-07T08:51:55.924000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507100046-4.png",
    "type": "file",
    "size": 217130,
    "mtime": "2026-05-07T10:00:48.407000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507134531-0.png",
    "type": "file",
    "size": 19356,
    "mtime": "2026-05-07T13:45:32.164999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507084907-0.png",
    "type": "file",
    "size": 92724,
    "mtime": "2026-05-07T08:49:08.517999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507134118-0.png",
    "type": "file",
    "size": 169240,
    "mtime": "2026-05-07T13:41:19.516000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507085108-0.png",
    "type": "file",
    "size": 31574,
    "mtime": "2026-05-07T08:51:09.822999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/a.md",
    "type": "file",
    "size": 2226,
    "mtime": "2026-06-04T16:42:17.871999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507134110-2.png",
    "type": "file",
    "size": 231909,
    "mtime": "2026-05-07T13:41:11.892999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507085305-0.png",
    "type": "file",
    "size": 264899,
    "mtime": "2026-05-07T08:53:06.423000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507134516-15.png",
    "type": "file",
    "size": 210253,
    "mtime": "2026-05-07T13:45:17.648000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507084445-0.png",
    "type": "file",
    "size": 116209,
    "mtime": "2026-05-07T08:44:46.124000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507084315-0.png",
    "type": "file",
    "size": 93470,
    "mtime": "2026-05-07T08:43:16.470999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507085136-6.png",
    "type": "file",
    "size": 17623,
    "mtime": "2026-05-07T08:51:37.487999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507100333-2.png",
    "type": "file",
    "size": 1340,
    "mtime": "2026-05-07T10:03:34.898000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507084208-0.png",
    "type": "file",
    "size": 384,
    "mtime": "2026-05-07T08:42:09.424000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507134519-18.png",
    "type": "file",
    "size": 99767,
    "mtime": "2026-05-07T13:45:23.289999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507085133-4.png",
    "type": "file",
    "size": 14833,
    "mtime": "2026-05-07T08:51:35.122999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507134517-16.png",
    "type": "file",
    "size": 127275,
    "mtime": "2026-05-07T13:45:18.536999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507100139-1.png",
    "type": "file",
    "size": 318879,
    "mtime": "2026-05-07T10:01:44.082000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507084537-3.png",
    "type": "file",
    "size": 372877,
    "mtime": "2026-05-07T08:45:38.194999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507084513-1.png",
    "type": "file",
    "size": 539,
    "mtime": "2026-05-07T08:45:14.227999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507084441-0.png",
    "type": "file",
    "size": 1554,
    "mtime": "2026-05-07T08:44:42.311000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507100114-0.png",
    "type": "file",
    "size": 1554,
    "mtime": "2026-05-07T10:01:16.153000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507134518-17.png",
    "type": "file",
    "size": 121364,
    "mtime": "2026-05-07T13:45:19.398000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507085206-0.png",
    "type": "file",
    "size": 208631,
    "mtime": "2026-05-07T08:52:07.927999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Pasted image 20260618090354.png",
    "type": "file",
    "size": 0,
    "mtime": "2026-06-18T09:03:54.516999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507085137-7.png",
    "type": "file",
    "size": 35004,
    "mtime": "2026-05-07T08:51:38.808000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507134457-0.png",
    "type": "file",
    "size": 59231,
    "mtime": "2026-05-07T13:44:58.404999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507100159-0.png",
    "type": "file",
    "size": 62766,
    "mtime": "2026-05-07T10:02:00.375000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507100437-0.png",
    "type": "file",
    "size": 65059,
    "mtime": "2026-05-07T10:04:38.256999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507100129-5.png",
    "type": "file",
    "size": 66875,
    "mtime": "2026-05-07T10:01:31.315999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507134459-2.png",
    "type": "file",
    "size": 184543,
    "mtime": "2026-05-07T13:45:00.253999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507084442-1.png",
    "type": "file",
    "size": 45923,
    "mtime": "2026-05-07T08:44:43.082999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507100332-1.png",
    "type": "file",
    "size": 1221,
    "mtime": "2026-05-07T10:03:33.785000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507085127-2.png",
    "type": "file",
    "size": 9681,
    "mtime": "2026-05-07T08:51:28.752000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507100131-6.png",
    "type": "file",
    "size": 1554,
    "mtime": "2026-05-07T10:01:32.464999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507084532-0.png",
    "type": "file",
    "size": 244975,
    "mtime": "2026-05-07T08:45:34.723000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507134113-4.png",
    "type": "file",
    "size": 242000,
    "mtime": "2026-05-07T13:41:14.427999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507100128-4.png",
    "type": "file",
    "size": 5324,
    "mtime": "2026-05-07T10:01:29.864000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507084214-0.png",
    "type": "file",
    "size": 65535,
    "mtime": "2026-05-07T08:42:14.970999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507100002-2.png",
    "type": "file",
    "size": 531317,
    "mtime": "2026-05-07T10:00:03.470999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507100133-8.png",
    "type": "file",
    "size": 1554,
    "mtime": "2026-05-07T10:01:34.963000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507100121-1.png",
    "type": "file",
    "size": 19862,
    "mtime": "2026-05-07T10:01:22.769000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507100315-0.png",
    "type": "file",
    "size": 195989,
    "mtime": "2026-05-07T10:03:16.786999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507134505-5.png",
    "type": "file",
    "size": 102671,
    "mtime": "2026-05-07T13:45:05.937000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507100202-0.png",
    "type": "file",
    "size": 212748,
    "mtime": "2026-05-07T10:02:04.039000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507134134-0.png",
    "type": "file",
    "size": 1442,
    "mtime": "2026-05-07T13:41:35.655999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507100424-1.png",
    "type": "file",
    "size": 18973,
    "mtime": "2026-05-07T10:04:28.973000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507134458-1.png",
    "type": "file",
    "size": 180284,
    "mtime": "2026-05-07T13:44:59.236999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507084534-1.png",
    "type": "file",
    "size": 22316,
    "mtime": "2026-05-07T08:45:35.841000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507134501-4.png",
    "type": "file",
    "size": 92671,
    "mtime": "2026-05-07T13:45:05.009999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507100650-0.png",
    "type": "file",
    "size": 199251,
    "mtime": "2026-05-07T10:06:51.266999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507085337-1.png",
    "type": "file",
    "size": 13726,
    "mtime": "2026-05-07T08:53:42.200000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507134127-0.png",
    "type": "file",
    "size": 2765,
    "mtime": "2026-05-07T13:41:31.290999"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507085336-0.png",
    "type": "file",
    "size": 19343,
    "mtime": "2026-05-07T08:53:37.516000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507100039-1.png",
    "type": "file",
    "size": 48517,
    "mtime": "2026-05-07T10:00:41.187000"
  },
  {
    "path": "/docker/obsidian-vault/Attachments/Exported image 20260507100045-3.png",
    "type": "file",
    "size": 39017,
    "mtime": "2026-05-07T10:00:46.892999"
  },
  {
    "path": "/docker/obsidian-vault/06 Systems/Obsidian 1.md",
    "type": "file",
    "size": 0,
    "mtime": "2026-05-21T22:48:22.598999"
  },
  {
    "path": "/docker/obsidian-vault/06 Systems/Hermes.md",
    "type": "file",
    "size": 81,
    "mtime": "2026-05-20T22:44:59.865000"
  },
  {
    "path": "/docker/obsidian-vault/06 Systems/Hermes Architecture.md",
    "type": "file",
    "size": 1141,
    "mtime": "2026-05-20T21:03:48.055999"
  },
  {
    "path": "/docker/obsidian-vault/06 Systems/GitHub.md",
    "type": "file",
    "size": 4075,
    "mtime": "2026-05-10T22:08:35.444999"
  },
  {
    "path": "/docker/obsidian-vault/06 Systems/Demos.md",
    "type": "file",
    "size": 1576,
    "mtime": "2026-05-24T17:14:20.240000"
  },
  {
    "path": "/docker/obsidian-vault/06 Systems/Code blueprint.md",
    "type": "file",
    "size": 2868,
    "mtime": "2026-05-08T22:34:15.125000"
  },
  {
    "path": "/docker/obsidian-vault/06 Systems/Contract tooling.md",
    "type": "file",
    "size": 1244,
    "mtime": "2026-05-24T17:14:20.240000"
  },
  {
    "path": "/docker/obsidian-vault/06 Systems/DF Training.md",
    "type": "file",
    "size": 2712,
    "mtime": "2026-05-24T17:14:20.240999"
  },
  {
    "path": "/docker/obsidian-vault/06 Systems/Second Brain Scripts",
    "type": "dir",
    "size": 4096,
    "mtime": "2026-06-28T00:06:31.901562"
  },
  {
    "path": "/docker/obsidian-vault/06 Systems/Hermes Sync Test.md",
    "type": "file",
    "size": 69,
    "mtime": "2026-05-20T18:59:35"
  },
  {
    "path": "/docker/obsidian-vault/06 Systems/Hermes website instruction.md",
    "type": "file",
    "size": 12671,
    "mtime": "2026-05-11T19:44:31.701999"
  },
  {
    "path": "/docker/obsidian-vault/06 Systems/Claude command lines.jpeg",
    "type": "file",
    "size": 62652,
    "mtime": "2026-04-07T20:49:50.756000"
  },
  {
    "path": "/docker/obsidian-vault/06 Systems/Docker.md",
    "type": "file",
    "size": 81,
    "mtime": "2026-05-22T21:08:00.381000"
  },
  {
    "path": "/docker/obsidian-vault/06 Systems/Keys.md",
    "type": "file",
    "size": 975,
    "mtime": "2026-05-24T18:51:00.450000"
  },
  {
    "path": "/docker/obsidian-vault/06 Systems/Obsidian Sync Operating Model.md",
    "type": "file",
    "size": 858,
    "mtime": "2026-05-21T21:23:59.029000"
  },
  {
    "path": "/docker/obsidian-vault/06 Systems/obsidian and hermes.md",
    "type": "file",
    "size": 5579,
    "mtime": "2026-05-11T07:40:27.358000"
  },
  {
    "path": "/docker/obsidian-vault/06 Systems/WhatsApp.md",
    "type": "file",
    "size": 20495,
    "mtime": "2026-05-10T21:00:26.357000"
  },
  {
    "path": "/docker/obsidian-vault/06 Systems/Entity Registry",
    "type": "dir",
    "size": 4096,
    "mtime": "2026-06-28T00:05:07.578711"
  },
  {
    "path": "/docker/obsidian-vault/06 Systems/Microsoft.md",
    "type": "file",
    "size": 84,
    "mtime": "2026-05-20T22:48:38.637000"
  },
  {
    "path": "/docker/obsidian-vault/06 Systems/Azure.md",
    "type": "file",
    "size": 80,
    "mtime": "2026-05-20T22:48:38.637000"
  },
  {
    "path": "/docker/obsidian-vault/06 Systems/Obsidian.md",
    "type": "file",
    "size": 83,
    "mtime": "2026-05-21T21:23:14.464999"
  },
  {
    "path": "/docker/obsidian-vault/06 Systems/Perplexity.md",
    "type": "file",
    "size": 305,
    "mtime": "2026-05-10T23:12:48.720999"
  },
  {
    "path": "/docker/obsidian-vault/06 Systems/Telegram.md",
    "type": "file",
    "size": 83,
    "mtime": "2026-05-20T22:44:59.865999"
  },
  {
    "path": "/docker/obsidian-vault/06 Systems/Claude design.md",
    "type": "file",
    "size": 143,
    "mtime": "2026-05-08T22:34:15.114000"
  },
  {
    "path": "/docker/obsidian-vault/06 Systems/Perplexity company search.md",
    "type": "file",
    "size": 471,
    "mtime": "2026-05-11T11:03:59.671999"
  },
  {
    "path": "/docker/obsidian-vault/06 Systems/Hermes to do.md",
    "type": "file",
    "size": 722,
    "mtime": "2026-05-10T21:24:59.576999"
  },
  {
    "path": "/docker/obsidian-vault/06 Systems/VPS Sync test.md",
    "type": "file",
    "size": 148,
    "mtime": "2026-05-25T16:55:46.346999"
  },
  {
    "path": "/docker/obsidian-vault/06 Systems/Hermes VPS Skills.md",
    "type": "file",
    "size": 17821,
    "mtime": "2026-05-19T23:46:21.299000"
  },
  {
    "path": "/docker/obsidian-vault/06 Systems/Oracle.md",
    "type": "file",
    "size": 81,
    "mtime": "2026-05-20T22:53:41.171000"
  },
  {
    "path": "/docker/obsidian-vault/06 Systems/Hermes 1.md",
    "type": "file",
    "size": 23728,
    "mtime": "2026-05-10T22:06:55.168999"
  },
  {
    "path": "/docker/obsidian-vault/06 Systems/OpenRouter.md",
    "type": "f
```
