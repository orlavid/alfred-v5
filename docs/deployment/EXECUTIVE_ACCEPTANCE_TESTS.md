# Executive Acceptance Tests

## Purpose

This pack defines the minimum executive acceptance gate for Project Phoenix Gate 3. The goal is to prove Alfred is operational, evidence-backed, and reading real Obsidian knowledge without modifying Hermes, Cloudflare, Telegram, or the vault.

## Preconditions

- `deploy_stage1.sh` completed successfully.
- `deploy_stage2.sh` completed successfully.
- `deploy_validation.sh` is ready to run from the Alfred application root.
- `scripts/vps/certify_live_knowledge.sh` has been prepared to confirm non-placeholder knowledge counts.

## Required Questions

Run each question through `build_ask_alfred.py` during validation:

1. `What should I focus on today?`
2. `What are my top objectives?`
3. `Prepare me for the next executive meeting.`
4. `What changed yesterday?`
5. `Which projects are at risk?`
6. `What follow-ups need action?`

## Acceptance Criteria

- Alfred returns an executive answer for each question.
- Supporting evidence is present for each question.
- Confidence is shown for each response.
- Recommended next actions are present for each response.
- Responses are grounded in generated intelligence rather than placeholder text.
- Meeting preparation must reflect the generated meeting brief when live meeting evidence exists.
- Follow-up and open-loop answers must align with the latest generated intelligence outputs.

## Validation Sequence

1. Rebuild the executive pipeline.
2. Rebuild follow-up and open-loop intelligence.
3. Run live knowledge certification and review entity counts.
4. Build the daily brief.
5. Run the six Ask Alfred prompts.
6. Review `output/Ask_Alfred.md`, `output/Daily_Brief.md`, `output/Executive_Pipeline_Report.md`, and `output/Operational_Readiness_Report.md`.

## Failure Conditions

- Any core knowledge count is zero unexpectedly.
- ExecutiveState is not generated.
- Operational Readiness is not `GREEN`.
- Ask Alfred fails to answer one of the required questions.
- Responses clearly reflect placeholder or demo data.

## Artefacts To Preserve

- `output/Executive_Pipeline_Report.md`
- `output/ExecutiveState_Summary.md`
- `output/Daily_Brief.md`
- `output/Ask_Alfred.md`
- `output/Operational_Readiness_Report.md`
- deployment logs from `deploy_validation.sh` and `scripts/vps/certify_live_knowledge.sh`
