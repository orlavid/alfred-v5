# Developer Bootstrap

Use `scripts/alfred-dev.sh` from the repository root to validate the local Alfred UI/tooling setup without remembering separate Python and npm commands.

## What It Does

- Verifies `.venv` exists
- Uses `.venv/bin/python` for Python build steps
- Verifies `node_modules` exists and runs `npm install` if needed
- Builds the Dashboard API
- Runs `npm run build`
- Prints the local dev server command

## Usage

From the repository root:

```bash
scripts/alfred-dev.sh
```

This performs the bootstrap checks and prints:

```bash
npm run dev -- --host 127.0.0.1
```

## Serve Mode

To start the Vite dev server automatically after bootstrap:

```bash
scripts/alfred-dev.sh --serve
```

## PASS / FAIL Output

The script reports each step explicitly:

- `PASS`: the step completed successfully
- `FAIL`: the step failed and execution stopped
