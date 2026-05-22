# Chapter 2: How to do model adaptation

This folder backs Chapter 2's hands-on quickstart and the optional Dragon-LLM open-finance recipe. The chapter itself is a landscape chapter: it walks the adaptation continuum, the buy-versus-build decision, base model selection, and security considerations. The two pieces of code in this folder play two different roles:

1. **`quickstart.py`** is what chapter 2's section 2.8 walks through: a small five-step LoRA fine-tune on Qwen3-4B-Instruct-2507 using a 40-example subset of Dolly 15K. It runs in under 10 minutes on a 12 GB GPU and lands on the same base model the rest of the book uses, so the adapter it produces is a valid starting point for chapter 5.
2. **`run_chapter5_adapter.py`** is an optional script for curious readers. It loads the chapter 5 LoRA adapter onto the base model and runs the same three demo prompts the quickstart prints, side by side with the base model output. The script resolves the adapter in three tiers: local `chapter05/runs/dolly_lora/` first, then Hugging Face Hub (`bahree/qwen3-4b-dolly-lora-ch5` by default), then optionally the local Ch2 quickstart adapter (only when `--use-quickstart` is passed). Most readers will get the Hub path automatically; readers who have run Ch5 locally get their own copy; readers who only have the quickstart see a clearly-labelled fallback. The script errors with the three resolution paths printed if none is available.
3. **`ch02_openfinance_finetuning.py`** is a bonus reference implementation by Weehyong Tok of the Dragon LLM open-finance recipe (arXiv:2511.08621). It uses Unsloth on `unsloth/Qwen3-0.6B` for a heavier production-style run on a different model family. The chapter prose does not walk this end to end; it is here as supplementary material for readers who want to see a complete Dragon-LLM-style pipeline. **`ch02-openfinance-finetuning.py`** is the original hyphenated copy, kept for compatibility with the Hugging Face short link in the chapter text.

## Assumptions

This README assumes you have completed the one-time setup from [`code/README.md`](../README.md) (Python 3.10+, virtual environment, PyTorch with CUDA). If not, start there first.

**The quickstart needs only the base install.** The Dragon-LLM bonus script needs the Chapter 2 extras:

```bash
# For quickstart.py: nothing beyond the base install
pip install -e ".[dev]"

# For the Dragon-LLM bonus (Unsloth + bitsandbytes):
pip install -e ".[chapter02]"
```

Unsloth's CUDA kernels do not run on macOS or CPU-only environments. The quickstart in section 2.8 does not use Unsloth, so it runs anywhere PyTorch+CUDA works.

## Hardware requirements

| Use case | GPU | VRAM | Time on A30 |
|---|---|---|---|
| `quickstart.py` (Chapter 2 §2.8) | NVIDIA, CUDA | 12 GB+ | ~8 minutes end to end |
| `ch02_openfinance_finetuning.py` (bonus) | NVIDIA, CUDA | 24 GB+ for Qwen3-0.6B | 15-25 min |
| CPU only | n/a | n/a | Not recommended (hours) |

The book's spine model (used in chapters 4 through 9) is `Qwen/Qwen3-4B-Instruct-2507`. The quickstart uses this model. The bonus Dragon-LLM script uses a different model (`unsloth/Qwen3-0.6B`) because that is what Weehyong's reference implementation was written against; the recipe generalizes to other base models.

## Running the quickstart (Chapter 2 §2.8)

From the `code/` directory with your venv activated:

```bash
cd /path/to/repo/code
source .venv/bin/activate

# One-time install (covers the quickstart)
pip install -e ".[dev]"

# Run the five-step LoRA fine-tune
python -m chapter02.quickstart
```

What you should see:

```
Step 1: prepare dataset
  train=40 valid=5 demo=3
Step 2: load base model and configure LoRA
Step 3: train for 20 steps
  train wall time: ~56s on A30
Step 4: compare outputs on held-out prompts
  ...
Step 5: save adapter to chapter02/runs/ch2_quickstart
Done.
```

Outputs land in `chapter02/runs/ch2_quickstart/`:

- `adapter_model.safetensors` (~130 MB) and `adapter_config.json`: the trained LoRA adapter
- Tokenizer files: ensure the adapter is loadable without a second download
- `manifest.json`: seed, base model, hyperparameters, and the three sample generations

Chapter 5's training scripts can resume from this checkpoint directory, so the quickstart adapter is a valid starting point for the deeper chapter 5 work.

## Running the optional Ch5-adapter preview

```bash
# Default: tries local Ch5 path, then Hugging Face Hub
python -m chapter02.run_chapter5_adapter

# Override the Hub repo if the canonical adapter has moved
python -m chapter02.run_chapter5_adapter --hub-repo your-org/your-adapter

# Fall back to the local quickstart adapter as a last resort
python -m chapter02.run_chapter5_adapter --use-quickstart
```

## Publishing the Ch5 adapter to Hugging Face Hub

Whoever maintains the book pushes the canonical Ch5 adapter to the Hub once after each chapter 5 retrain, using the chapter 5 publish script:

```bash
huggingface-cli login   # one time, with a token that has write scope on the target repo

python chapter05/scripts/publish_adapter.py \
  --adapter chapter05/runs/dolly_lora \
  --repo_id bahree/qwen3-4b-dolly-lora-ch5 \
  --base Qwen/Qwen3-4B-Instruct-2507 \
  --notes "Chapter 5 LoRA adapter on Qwen3-4B + Dolly subset (400 train / 50 valid / 50 test, seed 42)"
```

After the push, `chapter02/run_chapter5_adapter.py` resolves to the Hub automatically.

## Running the Dragon-LLM bonus

```bash
pip install -e ".[chapter02]"
python -m chapter02.ch02_openfinance_finetuning
```

This is the underscored, `def main()`-wrapped version of Weehyong's original. The hyphenated original (`ch02-openfinance-finetuning.py`) is also in the folder and runs the same code.

Expected runtime: 15 to 25 minutes per run on DGX Spark or A100, longer on a 24 GB consumer card. The script downloads four Hugging Face datasets on first run (Financial PhraseBank, Sujet Finance, FiQA, Alpaca) and combines them at the Dragon LLM 54/20/16/8/2 ratio. Outputs land in `chapter02/runs/finance_lora/`.

## What gets downloaded on first run

| Asset | Source | Used by |
|---|---|---|
| Qwen3-4B-Instruct-2507 | `Qwen/Qwen3-4B-Instruct-2507` | quickstart.py |
| Databricks Dolly 15K | `databricks/databricks-dolly-15k` | quickstart.py |
| Qwen3-0.6B (Unsloth mirror) | `unsloth/Qwen3-0.6B` | Dragon-LLM bonus |
| Financial PhraseBank | `takala/financial_phrasebank` | Dragon-LLM bonus |
| Sujet Finance Instruct 177k | `sujet-ai/Sujet-Finance-Instruct-177k` | Dragon-LLM bonus |
| FiQA 2018 | `pauri32/fiqa-2018` | Dragon-LLM bonus |
| Alpaca Cleaned | `yahma/alpaca-cleaned` | Dragon-LLM bonus |

The quickstart's downloads are small (Qwen3-4B is ~8 GB; the Dolly subset filtered down is a handful of MB). The Dragon-LLM bonus downloads several GB of dataset files on first run.

## Troubleshooting

**`No module named 'unsloth'`** when running the bonus script: run `pip install -e ".[chapter02]"` from the `code/` directory. The quickstart does not need Unsloth.

**CUDA out of memory** in the quickstart: this should not happen on a 12 GB GPU. If it does, set `per_device_train_batch_size=1` (the default) and confirm `gradient_checkpointing_enable()` was called. As a fallback, reduce `max_length` from 512 to 256 in `quickstart.py`.

**Slow dataset download** on first run: set `HF_TOKEN` in your environment to use authenticated downloads.

**`fatal error: Python.h: No such file or directory` during training**: Triton's runtime compiler shells out to `gcc` and needs the Python development headers on the include path. Install the matching `python3.X-dev` package (`sudo apt install python3.12-dev` on Ubuntu) and export `CPATH=/usr/include/python3.12` before running the script.

**`NameError: VARIANT_KWARG_KEYS is not defined`** (Unsloth bonus only): Unsloth's compile-cache generator has not yet caught up with PEFT 0.18+. The book pins `peft<0.18` in `pyproject.toml`; if your environment has a newer PEFT, run `pip install "peft<0.18"` and delete `code/unsloth_compiled_cache/` before retrying.

**`Can't pickle <class 'builtins.safe_open'>` during dataset map** (Unsloth bonus only): triggered by `safetensors>=0.6`. The book pins `safetensors<0.6`; reinstall with `pip install "safetensors<0.6"` if a newer version has crept in.

---

**Repository:** <https://github.com/bahree/ModelAdaptationBook>
