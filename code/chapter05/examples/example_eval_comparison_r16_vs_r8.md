# Chapter 5 Evaluation Report: r=16 vs r=8 Comparison

**Date:** January 25, 2026  
**Purpose:** Compare LoRA rank 16 vs rank 8 to test safety regression fix hypothesis

**Result:** Unexpected! r=8 improved task performance but worsened safety.

---

- Base model: `Qwen/Qwen3-4B-Instruct-2507`
- System prompt: `You are a helpful assistant.`
- Dolly test set: `chapter05/data/dolly_subset/test.jsonl`
- Adapter: `chapter05/runs/dolly_lora` (r=16)
- Adapter (alt): `chapter05/runs/dolly_lora_r8` (r=8)

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

## adapter (r=16)
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

## adapter_alt (r=8)
### Dolly Test Set (Instruction-Following)
- **Overall exact match**: 0.0%
- **Overall token-F1**: 0.370 ← BETTER than r=16!
- **Test examples**: 50

**Per-Category Accuracy:**
- brainstorming: EM=0.0%, F1=0.162 (n=8)
- classification: EM=0.0%, F1=0.594 (n=7)
- closed_qa: EM=0.0%, F1=0.365 (n=6)
- creative_writing: EM=0.0%, F1=0.208 (n=1)
- general_qa: EM=0.0%, F1=0.283 (n=6)
- information_extraction: EM=0.0%, F1=0.400 (n=3)
- open_qa: EM=0.0%, F1=0.353 (n=16)
- summarization: EM=0.0%, F1=0.702 (n=3)

- **Safety refusal rate**: 40.0% ← WORSE than r=16!
- **Toy exact match**: 0.0%
- **Toy token-F1**: 0.275

## adapter (r=16) vs Base
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

## adapter_alt (r=8) vs Base
### Dolly Test Set Improvements
- **Overall exact match Δ**: +0.0%
- **Overall token-F1 Δ**: +0.1579 ← BEST performance!

**Per-Category Improvements:**
- brainstorming: EM Δ=+0.0%, F1 Δ=+0.0187 ← IMPROVED (was negative with r=16)
- classification: EM Δ=+0.0%, F1 Δ=+0.4829
- closed_qa: EM Δ=+0.0%, F1 Δ=+0.0618
- creative_writing: EM Δ=+0.0%, F1 Δ=-0.0355
- general_qa: EM Δ=+0.0%, F1 Δ=+0.0342 ← IMPROVED (was negative with r=16)
- information_extraction: EM Δ=+0.0%, F1 Δ=+0.0229
- open_qa: EM Δ=+0.0%, F1 Δ=+0.1795
- summarization: EM Δ=+0.0%, F1 Δ=+0.2945

- **Safety refusal rate Δ**: -60.0% ← WORST safety!
- **Toy exact match Δ**: +0.0%
- **Toy token-F1 Δ**: +0.1045

---

## Analysis: Why r=8 Didn't Fix Safety

### What We Expected:
- r=8 would preserve more base model behavior
- Safety would improve (60% → 80-90%)
- Task performance would drop slightly

### What Actually Happened:
- ✅ r=8 performed BETTER on tasks (0.344 → 0.370)
- ❌ Safety got WORSE (60% → 40%)
- ✅ Generalization improved (brainstorming, general_qa no longer regressed)

### Why:
1. **No safety data** — Training still had 0 refusal examples
2. **Rank reduction alone can't fix data problems** — The issue isn't model capacity, it's dataset composition
3. **r=8 might be the sweet spot** for 400 examples — Better generalization, less overfitting
4. **Small test set variance** — 10 safety prompts means high variability

### Key Lesson:
**You can't parameter-tune your way out of a data problem.** To fix safety, you MUST add safety examples to training data.

### The Real Fix:
1. Add 50-100 safety examples (harmful prompts + refusals)
2. Make them 10-20% of training data
3. Retrain and validate
4. Only then can you trust the model's safety

---

## Pedagogical Value

This unexpected result is **MORE valuable** than if r=8 had worked as predicted because it teaches:

1. ✅ **Validate empirically** — Don't assume solutions will work
2. ✅ **Data trumps parameters** — Fix data problems with data, not hyperparameters
3. ✅ **Unexpected results happen** — Real research involves surprises
4. ✅ **Safety requires explicit training** — It won't emerge from parameter tuning

This is a honest, realistic look at model fine-tuning that will help readers avoid the same mistakes.
