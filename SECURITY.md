# Security policy

Thanks for taking the time to report a potential security issue with this repository.

This repository hosts the code companion to the Manning book *Practical Model Adaptation Techniques for Large Language Models*. It contains educational code, example scripts, datasets, and tests. It does **not** host a production service, manage user data, or run anything remotely. The realistic security surface is narrow, but we still take credible reports seriously.

## What's in scope

We want to hear about:

- **Secrets accidentally committed to this repository** (API keys, tokens, credentials in committed files, dataset files, or notebooks)
- **Vulnerabilities in code we wrote** that could lead to remote code execution, arbitrary file write, or credential exfiltration on a reader's machine when they run the published examples as documented
- **Malicious payloads** in datasets, model files, or other artifacts that we host in this repo
- **Supply-chain concerns** about a pinned dependency that has a known CVE affecting users who run the chapter code

## What's not in scope

These are not security issues for this repository (please file a regular bug report instead, or take them up with the upstream maintainer):

- Bugs in third-party packages (`transformers`, `peft`, `trl`, `unsloth`, `sentence-transformers`, etc.) — report those to the upstream project. We may pin or unpin a version in response, but the fix belongs upstream.
- Security issues in PyTorch, CUDA, or Hugging Face Hub — report to those projects.
- Risks that arise from a reader running the code against a model they don't trust, or against a dataset they downloaded from an untrusted source. The book teaches readers about provenance and safety; the responsibility for what they do with the code is theirs.
- Behavior of models trained or fine-tuned with the chapter code. Adapted models can produce unsafe, biased, or incorrect outputs — this is a fundamental property of language models and is discussed throughout the book, not a vulnerability in the code.
- Educational design choices in the book (e.g., "this example doesn't show input validation") — book content is not part of the public repo and is not the subject of security reports.

## How to report

Please use **one** of the following channels. Do **not** open a public issue for a security report.

1. **GitHub Security Advisories** (preferred): use the **Security** tab on this repository and click **Report a vulnerability**. This gives you a private channel with the maintainer and lets us track the report.
2. **Email:** if you can't use GitHub Security Advisories, email the maintainer at the address listed on the [@bahree](https://github.com/bahree) GitHub profile, with `[ModelAdaptationBook security]` in the subject line.

When reporting, please include:

- A clear description of the issue
- Steps to reproduce (commands, file paths, expected vs. actual)
- Affected commit or release tag (e.g., `MEAP-v0.1`)
- The environment you observed it in (OS, Python version, GPU)
- Whether you've shared the report with anyone else

## What to expect

This is a single-maintainer side project alongside writing the book, so the response cadence isn't a 24/7 SLA. That said:

- We'll acknowledge receipt within **5 business days**.
- For confirmed reports we'll work on a fix and aim to have a patch ready within **30 days** for critical issues, longer for lower-severity ones.
- We'll coordinate disclosure with you. If you'd like credit in the release notes for the fix, let us know and we'll add it.
- If we determine a report is out of scope, we'll explain why and suggest where the issue belongs.

## Disclosure expectations

Please give us a reasonable window to triage and patch before publishing details. Coordinated disclosure helps readers stay safe. We will not pursue legal action against researchers who report in good faith and follow this policy.

## Acknowledgments

Security researchers who report valid issues will be acknowledged in `CHANGELOG.md` (and the release notes for the fix), unless they ask to remain anonymous.

Thank you for helping keep readers and contributors safe.
