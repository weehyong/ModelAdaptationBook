<!--
Thanks for opening a pull request!

This repo is the code companion to the book *Practical Model Adaptation Techniques for Large Language Models* (Manning). Code fixes, test improvements, and README clarifications are welcome. The book's prose is not part of this repo and cannot be changed via PR -- for book content corrections, please use the Errata issue template instead.

Before submitting, please:
- Review CONTRIBUTING.md
- Run `pytest -q` and `ruff check .` from the `code/` directory
-->

## What does this PR do

<!-- One or two sentences. What changes, and why? -->

## Related issue

<!-- e.g., Closes #42, or N/A if there isn't one. -->

## Which chapter or area does this touch

<!-- e.g., chapter05 training script, common/jsonl utility, chapter04 tests, root README -->

## How to test

<!-- Concrete commands a reviewer can run to verify your change. Run from the code/ directory. -->

```bash
# example
cd code
pytest chapter05/tests -q
```

## Checklist

- [ ] Tests added or updated for the change (if it's a bug fix or behavior change)
- [ ] `pytest -q` passes from `code/`
- [ ] `ruff check .` passes from `code/`
- [ ] README or chapter README updated if user-facing instructions changed
- [ ] No secrets, API keys, or personal data in the diff
- [ ] No large binary artifacts (model checkpoints, training runs) in the diff
- [ ] The change does not alter file paths the book references in listings

## Additional context

<!-- Anything a reviewer should know. Tradeoffs, alternatives considered, follow-up work. -->
