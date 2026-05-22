# Chapter 5 notices (datasets and attribution)

## Primary Dataset

- **Databricks Dolly 15K**: `databricks/databricks-dolly-15k` (license: CC-BY-SA-3.0)
  - Dataset: `https://huggingface.co/datasets/databricks/databricks-dolly-15k`
  - Created by Databricks employees in March-April 2023
  - 15,000 instruction-response pairs across 7 task categories
  - Used for fine-tuning demonstrations in this chapter
  - Commercially viable (CC-BY-SA-3.0 license)

## Why Dolly 15K?

This dataset is used because:
1. **Narrative continuity**: Chapter 4 uses Dolly for few-shot prompting; Chapter 5 uses it for LoRA fine-tuning, showing progression on the same dataset.
2. **Real-world dataset**: Not a toy example—widely used in production fine-tuning.
3. **Measurable tasks**: 7 distinct categories enable clear before/after evaluation.
4. **Appropriate size**: 400-500 examples is ideal for LoRA demonstration.
