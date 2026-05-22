# Contributing

Thanks for your interest in improving this code repository.

This repo holds the runnable code that accompanies the book *Practical Model Adaptation Techniques for Large Language Models* (Manning). Code contributions are welcome. Book content (prose, figures, structure) is owned by Manning Publications and is not part of this repo — for book content please use [Manning's liveBook forum](https://livebook.manning.com/) instead of opening a pull request here.

## What we welcome

- Bug fixes in chapter code, common utilities, or tests
- Tests that cover an existing module more thoroughly
- README clarifications when a step is unclear or out of date
- Dataset or manifest corrections (typos, wrong counts, broken URLs)
- Cross-platform fixes (the code runs on Linux, Windows, and macOS for the non-GPU paths)
- Performance improvements that don't change the pedagogical structure

## What we don't accept

- Rewrites of the book's prose or examples (those live in the manuscript at Manning)
- Sweeping refactors that change the file/folder structure (the book references files by path, so structural changes break the book)
- Adding new chapters or replacing the running example (Qwen3-4B-Instruct-2507 + Dolly-15K is the book's single spine)
- Adding heavy dependencies that aren't required by the chapter content

If you're unsure whether a change fits, open an issue first to discuss before sending a pull request.

## Development setup

Follow the workspace setup in [`code/README.md`](code/README.md). The short version:

```bash
cd code
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
python -m pip install -U pip
pip install -e ".[dev]"
```

For chapters that need PyTorch, follow the CUDA install command in `code/README.md`. Optional chapter extras (`pip install -e ".[chapter02]"`, `pip install -e ".[chapter03]"`, etc.) install the heavier dependencies only when you need them.

## Running tests

From the `code/` directory:

```bash
pytest -q                                # all tests
pytest chapter04/tests -q                # one chapter's tests
pytest chapter05/tests/test_metrics.py   # one file
```

CI runs the same tests on Ubuntu and Windows with Python 3.11. Your change should keep CI green.

## Code style

Code is formatted and linted with [Ruff](https://docs.astral.sh/ruff/). From the `code/` directory:

```bash
ruff check .              # lint check
ruff check --fix .        # auto-fix what's safe
ruff format .             # format
```

Style notes specific to this repo:

- Line length: 100 characters
- Target Python version: 3.10+
- Prefer explicit imports over `from x import *`
- Type hints encouraged but not required for tutorial code
- Add a docstring at the top of any new script explaining what it does and how to run it

## Opening an issue

Before opening an issue, please check if one already exists. We use three templates:

- **Bug report:** runtime errors, wrong outputs, broken examples
- **Errata:** typos or factual errors in the book itself (include chapter, page or section, and MEAP version)
- **Question:** if it's about the book's content, please ask in [Manning's liveBook forum](https://livebook.manning.com/) instead. If it's about the code, the bug report template is the right place.

## Opening a pull request

1. Fork the repo and create a branch off `main`: `git checkout -b fix/short-description`
2. Make your change. Keep it focused — one fix per PR.
3. Add a test if you're fixing a bug.
4. Run `pytest -q` and `ruff check .` from `code/` and make sure both pass.
5. Open a pull request against `main`. The PR template will ask for a brief description and a test plan.
6. CI will run on your PR. The author will review when they can — please be patient; this is a side project alongside writing the book.

## Code of conduct

Be kind. Assume good faith. We're all here because we want to make the book better for readers who come after us.

## License

By contributing, you agree that your contributions will be licensed under the same MIT License that covers the rest of the code in this repository.
