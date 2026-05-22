#!/usr/bin/env bash
# Run the chapter 4 GPU-required validations.
#
# This script must be executed on a machine with at least one CUDA GPU
# (~12 GB VRAM is enough; the book's reference setup is two A30s).
# It runs the `hf` backends end-to-end and saves the outputs into
# chapter04/runs/ so the resulting JSON can be committed and browsed
# without re-running the model.
#
# Usage (from code/, with the venv activated):
#     ./chapter04/scripts/run_on_gpu.sh
#
# The full run takes a few minutes on a single A30: model download is
# the long pole the first time; subsequent runs hit the local HF cache.

set -euo pipefail

if [[ "${VIRTUAL_ENV:-}" == "" ]]; then
    echo "ERROR: activate the project venv first (source .venv/bin/activate)" >&2
    exit 1
fi

if ! python -c "import torch; assert torch.cuda.is_available()" 2>/dev/null; then
    echo "ERROR: this script requires CUDA. Run on the A30 machine." >&2
    exit 1
fi

mkdir -p chapter04/runs

echo "===> few_shot_demo (Qwen3-4B, 8 shots)"
python -m chapter04.few_shot_demo \
    --shots 8 --backend hf \
    --output chapter04/runs/few_shot_hf.json \
    --details chapter04/runs/few_shot_hf_details.jsonl

echo "===> prompt_validator (Qwen3-4B, 8 shots, 3 runs at temperature 0.7)"
python -m chapter04.prompt_validator \
    --shots 8 --runs 3 --backend hf \
    --output chapter04/runs/validator_hf.json

echo
echo "Done. Inspect:"
echo "  chapter04/runs/few_shot_hf.json"
echo "  chapter04/runs/few_shot_hf_details.jsonl"
echo "  chapter04/runs/validator_hf.json"
