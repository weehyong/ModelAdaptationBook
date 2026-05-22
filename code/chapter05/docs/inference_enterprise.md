# Chapter 5 enterprise inference patterns (adapters)

This chapter focuses on training adapters. In enterprise settings, the adapter is typically treated as a first-class artifact that can be versioned, tested, promoted, and rolled back independently from the base model.

## Option A — Load base + adapter at inference (modular)

- **Pros**: small artifacts, fast iteration, supports Multi-LoRA (switching adapters)
- **Cons**: requires loading adapter at startup; slightly more moving parts

Typical pattern:

1. Pin base model **name + revision** (and tokenizer revision)
2. Load base model
3. Load adapter weights on top
4. Serve requests

## Option B — Merge adapter into base (single checkpoint)

- **Pros**: simplest runtime (one checkpoint)
- **Cons**: loses modularity; artifact becomes large; harder to A/B multiple adapters

Use this when you only need a single tuned model and want the simplest deployment.

## Option C — Serve multiple adapters (routing)

- **Pros**: one base model + multiple behaviors (support/compliance/risk) without duplicating weights
- **Cons**: requires a serving layer that supports LoRA adapters and routing

Common approaches:

- Run separate endpoints per adapter (simplest routing)
- Use a single server that can load multiple adapters and switch per request

## What to version/pin

At minimum, keep these together:

- Base model id and revision (commit hash or tag)
- Tokenizer revision
- System prompt / chat template behavior
- Adapter files + adapter manifest (hyperparameters, target modules)
- Dataset manifest(s) for the training subset(s)
- Eval report (base vs adapter; safety regression sanity suite)

