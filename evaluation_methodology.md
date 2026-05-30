# How Vision-Language Models (VLMs) Are Evaluated

## Overview

A Vision-Language Model (VLM) is an AI model that takes both an image and a text input (such as a question) and produces a text output (such as an answer). Evaluating a VLM means measuring how well its answers match the correct answers across a set of test examples.

The general evaluation process is:

1. Prepare a **test dataset** — images paired with questions and known correct answers
2. **Run the model** on each image and question
3. **Compare** the model's output to the correct answer
4. **Compute metrics** that measure how accurate or relevant the model's answers are

---

## Nature of the Data

### Input
A VLM receives two inputs at the same time:
- **Image:** A satellite photo, aerial image, or any visual input
- **Text:** A question or instruction (e.g., "Is this area flooded?")

### Output
The model produces a **natural language response** (e.g., "Yes, the area shows significant flooding.")

### Ground Truth
The test dataset contains **reference answers** written by humans, which the model's output is compared against. These can be:
- **Closed-form answers:** short, fixed responses like "yes", "no", "major damage", or "3 buildings"
- **Open-form answers:** longer text descriptions or full reports

---

## Task Types and Evaluation Metrics

### 1. Visual Question Answering (VQA)

The model is shown an image and asked a question. It must answer correctly.

**Example:**
- Image: satellite photo after a flood
- Question: "Is there flooding visible in this image?"
- Ground truth: "yes"
- Model output: "Yes, flooding is visible."

**Metrics:**
- **Accuracy:** percentage of questions answered correctly overall
- **Exact Match (EM):** the model output must match the reference answer exactly
- **Factual correctness / semantic correctness:** checks whether the answer is correct in meaning, even if the wording is different.

---

### 2. Damage Assessment

The model must classify the level of damage shown in an image.

**Typical categories:** no damage / minor damage / major damage / destroyed

**Metrics:**
- **Accuracy:** percentage of correctly classified samples
- **F1 Score:** balances precision (how many predicted positives are truly correct) and recall (how many actual positives were found). Useful when some damage categories are rare.

---

### 3. Object Counting

The model must count specific objects visible in an image (e.g., number of collapsed buildings).

**Metrics:**
- **Mean Absolute Error (MAE):** the average difference between the predicted count and the actual count
- **Root Mean Squared Error (RMSE):** similar to MAE but penalizes large errors more heavily

---

### 4. Referring Segmentation

The model must identify and segment a specific object based on a text description (e.g., "Segment the damaged building in the lower-left corner").

**Metrics:**
- **IoU (Intersection over Union):** measures how much the predicted region overlaps with the correct region

```
IoU = Area of Overlap / Area of Union
```

A score of 1.0 means a perfect match. A score of 0 means no overlap at all.

- **cIoU:** cumulative IoU across all test examples
- **mIoU:** mean IoU — the average overlap score across all examples

---

### 5. Report Generation

The model generates a multi-sentence assessment report describing the damage in an image.

**Metrics:**
- **BLEU:** measures how much the generated text overlaps with the reference text at the word level
- **ROUGE:** measures how much of the reference text appears in the generated output

These metrics are useful for measuring text overlap, but they may not fully capture whether the generated answer is visually and factually correct.

---

## Key Evaluation Concepts

### Benchmark vs. Dataset
- A **dataset** is a collection of labeled data (images + annotations)
- A **benchmark** is a standardized evaluation protocol that uses a dataset to compare models fairly — same test split, same metrics, same conditions for everyone

### Zero-shot vs. Fine-tuned Evaluation
- **Zero-shot:** the model is tested on a task without any task-specific training — measures general capability
- **Fine-tuned:** the model has been additionally trained on task-specific data before evaluation — measures specialized capability

### Why Evaluation Matters
Without systematic evaluation, we cannot know which AI model actually performs better on a given task. Evaluation makes it possible to compare models objectively, identify failure patterns, and decide which model is suitable for real-world use cases such as disaster response.

---

## Summary Table

| Task | Input | Expected Output | Key Metric |
|---|---|---|---|
| VQA | Image + question | Short answer | Accuracy, Exact Match |
| Damage assessment | Image | Damage category | F1, Accuracy |
| Object counting | Image + query | Integer count | MAE, RMSE |
| Referring segmentation | Image + text reference | Pixel-level mask | cIoU, mIoU |
| Report generation | Image pair | Multi-sentence text | BLEU, ROUGE |
