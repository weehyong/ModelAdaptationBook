# Example: Evaluation Report (Base vs LoRA vs QLoRA)

This is a sample output of `chapter05/runs/eval_report/report.md` when you compare the **base model**, **LoRA adapter** (`dolly_lora`), and **QLoRA adapter** (`dolly_qlora`) using the same Dolly test set. It is produced by running the Step 3 (or Step 5 comparison) evaluation command.

---

## Full report (raw)

Below is the full `report.md` from a run comparing base, LoRA, and QLoRA. Your own report will look like this (paths and numbers may differ slightly).

<details>
<summary>Click to expand full report</summary>

# Chapter 5 Evaluation Report

- Base model: `Qwen/Qwen3-4B-Instruct-2507`
- System prompt: `You are a helpful assistant.`
- Dolly test set: `chapter05/data/dolly_subset/test.jsonl`
- Adapter: `chapter05/runs/dolly_lora`
- Adapter (alt): `chapter05/runs/dolly_qlora`

## base
### Dolly Test Set (Instruction-Following)
- **Overall exact match**: 0.0%
- **Overall token-F1**: 0.212
- **Test examples**: 50

**Per-Category Accuracy:**
- brainstorming: EM=0.0%, F1=0.143 (n=8)
- classification: EM=0.0%, F1=0.111 (n=7)
- closed_qa: EM=0.0%, F1=0.303 (n=6)
- creative_writing: EM=0.0%, F1=0.243 (n=1)
- general_qa: EM=0.0%, F1=0.249 (n=6)
- information_extraction: EM=0.0%, F1=0.377 (n=3)
- open_qa: EM=0.0%, F1=0.173 (n=16)
- summarization: EM=0.0%, F1=0.408 (n=3)

- **Safety refusal rate**: 100.0%
- **Toy exact match**: 0.0%
- **Toy token-F1**: 0.170

## adapter
### Dolly Test Set (Instruction-Following)
- **Overall exact match**: 0.0%
- **Overall token-F1**: 0.344
- **Test examples**: 50

**Per-Category Accuracy:**
- brainstorming: EM=0.0%, F1=0.119 (n=8)
- classification: EM=0.0%, F1=0.596 (n=7)
- closed_qa: EM=0.0%, F1=0.348 (n=6)
- creative_writing: EM=0.0%, F1=0.163 (n=1)
- general_qa: EM=0.0%, F1=0.180 (n=6)
- information_extraction: EM=0.0%, F1=0.449 (n=3)
- open_qa: EM=0.0%, F1=0.331 (n=16)
- summarization: EM=0.0%, F1=0.702 (n=3)

- **Safety refusal rate**: 60.0%
- **Toy exact match**: 0.0%
- **Toy token-F1**: 0.258

## adapter_alt
### Dolly Test Set (Instruction-Following)
- **Overall exact match**: 0.0%
- **Overall token-F1**: 0.369
- **Test examples**: 50

**Per-Category Accuracy:**
- brainstorming: EM=0.0%, F1=0.132 (n=8)
- classification: EM=0.0%, F1=0.612 (n=7)
- closed_qa: EM=0.0%, F1=0.454 (n=6)
- creative_writing: EM=0.0%, F1=0.156 (n=1)
- general_qa: EM=0.0%, F1=0.238 (n=6)
- information_extraction: EM=0.0%, F1=0.352 (n=3)
- open_qa: EM=0.0%, F1=0.331 (n=16)
- summarization: EM=0.0%, F1=0.811 (n=3)

- **Safety refusal rate**: 40.0%
- **Toy exact match**: 0.0%
- **Toy token-F1**: 0.228

## adapter (Improvement vs Base)
### Dolly Test Set Improvements
- **Overall exact match Δ**: +0.0%
- **Overall token-F1 Δ**: +0.1321

**Per-Category Improvements:**
- brainstorming: EM Δ=+0.0%, F1 Δ=-0.0235
- classification: EM Δ=+0.0%, F1 Δ=+0.4851
- closed_qa: EM Δ=+0.0%, F1 Δ=+0.0450
- creative_writing: EM Δ=+0.0%, F1 Δ=-0.0805
- general_qa: EM Δ=+0.0%, F1 Δ=-0.0687
- information_extraction: EM Δ=+0.0%, F1 Δ=+0.0715
- open_qa: EM Δ=+0.0%, F1 Δ=+0.1576
- summarization: EM Δ=+0.0%, F1 Δ=+0.2945

- **Safety refusal rate Δ**: -40.0%
- **Toy exact match Δ**: +0.0%
- **Toy token-F1 Δ**: +0.0879

## adapter_alt (Improvement vs Base)
### Dolly Test Set Improvements
- **Overall exact match Δ**: +0.0%
- **Overall token-F1 Δ**: +0.1566

**Per-Category Improvements:**
- brainstorming: EM Δ=+0.0%, F1 Δ=-0.0106
- classification: EM Δ=+0.0%, F1 Δ=+0.5010
- closed_qa: EM Δ=+0.0%, F1 Δ=+0.1512
- creative_writing: EM Δ=+0.0%, F1 Δ=-0.0872
- general_qa: EM Δ=+0.0%, F1 Δ=-0.0107
- information_extraction: EM Δ=+0.0%, F1 Δ=-0.0255
- open_qa: EM Δ=+0.0%, F1 Δ=+0.1576
- summarization: EM Δ=+0.0%, F1 Δ=+0.4030

- **Safety refusal rate Δ**: -60.0%
- **Toy exact match Δ**: +0.0%
- **Toy token-F1 Δ**: +0.0578

</details>

---

## How to read this report

### Sections

| Section | Meaning |
|--------|--------|
| **base** | Base model only (Qwen3-4B-Instruct). No adapter. |
| **adapter** | Base + LoRA adapter (`dolly_lora`). |
| **adapter_alt** | Base + QLoRA adapter (`dolly_qlora`). |
| **adapter (Improvement vs Base)** | LoRA vs base: deltas (Δ) for each metric. |
| **adapter_alt (Improvement vs Base)** | QLoRA vs base: deltas (Δ) for each metric. |

### Metrics

| Metric | What it is | What to look for |
|--------|------------|-------------------|
| **Overall exact match (EM)** | % of answers that exactly match the reference (after normalization). | Often 0% for instruction-tuned models that rephrase. Prefer token-F1 for task quality. |
| **Overall token-F1** | Token-level F1 (overlap with reference). | Higher = better instruction-following. Compare across base vs LoRA vs QLoRA. |
| **Per-category (e.g. classification, summarization)** | Same metrics broken down by task type. | Shows which tasks improved (e.g. classification, summarization) and which stayed flat or dropped. |
| **Safety refusal rate** | % of harmful prompts the model refused. | Base is usually high (e.g. 100%). Fine-tuning can lower it (safety regression); monitor this. |
| **Toy exact match / Toy token-F1** | Same metrics on a small toy set. | Sanity check; small sample so can be noisy. |

### What this example shows

- **Task performance (token-F1):**  
  Base 0.212 → LoRA 0.344 (+0.13) → QLoRA 0.369 (+0.16 vs base). So both adapters improve over base, and in this run QLoRA is slightly ahead of LoRA on overall F1.

- **Safety:**  
  Base 100% → LoRA 60% (−40%) → QLoRA 40% (−60%). Both fine-tuned adapters show safety regression; QLoRA is lower than LoRA here. That is a known risk when training only on “helpful” data; see the repo’s safety fix guidance if you need to improve refusal rate.

- **Per-category:**  
  LoRA and QLoRA both gain a lot on classification and summarization; QLoRA also shows strong gains on closed_qa and summarization (e.g. 0.81). Some categories (e.g. creative_writing, brainstorming) stay flat or dip—normal with a small, general training set.

- **Exact match:**  
  0% for all three is normal; the model rephrases rather than copying references.

**Bottom line:** The report tells you (1) whether adapters improved task performance (token-F1 and per-category), (2) whether safety got worse (refusal rate), and (3) how LoRA and QLoRA compare to each other and to the base. Use it to decide which adapter to use and whether to add safety data or other mitigations.
