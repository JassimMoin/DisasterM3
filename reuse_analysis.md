# Reuse Analysis: EarthVQA

> This analysis is based on direct inspection of the EarthVQA repository source code,
> specifically `data/earthvqa.py` and `utils/metric.py`.
> GitHub: https://github.com/Junjue-Wang/EarthVQA

---

## Overview

EarthVQA is a remote sensing Visual Question Answering dataset focused on urban land-use
analysis from satellite imagery. Unlike DisasterM3, which handles all dataset loading
inside its main execution script, EarthVQA separates dataset loading, model logic, and
evaluation metrics into dedicated modules. This makes it a useful reference for the
modular framework being designed.

---

## Identified Reusable Design Pattern: Question-Type-Aware Evaluator with `summary()`

### What the pattern is

In `utils/metric.py`, EarthVQA defines two metric classes:

**`VQA_OA_Metric`** — measures accuracy per question type:

```python
class VQA_OA_Metric(object):
    def __init__(self, ques_classes: list, logger=None):
        self.ques_classes = ques_classes
        self.cls_true_num = [0 for _ in range(len(self.ques_classes))]
        self.cls_total_num = [0 for _ in range(len(self.ques_classes))]

    def __call__(self, pred, gt, questype):
        matched = (pred == gt).astype(np.uint8)
        for ques_t, m_i in zip(questype, matched):
            cls_idx = self.ques_classes.index(ques_t)
            self.cls_total_num[cls_idx] += 1
            self.cls_true_num[cls_idx] += int(m_i)

    def summary(self):
        # prints per-class accuracy + overall accuracy (OA)
```

**`Count_RMSE_Metric`** — measures RMSE for counting questions:

```python
class Count_RMSE_Metric(object):
    def __call__(self, pred, gt, questype):
        # accumulates predictions per question type

    def summary(self):
        # prints per-class RMSE + overall RMSE
```

### Why this pattern is reusable

Both classes share the same structure:
- `__call__()` accumulates predictions during evaluation
- `summary()` computes and prints the final metrics

This is a clean, consistent evaluator interface. The `summary()` method means any
evaluator can be called the same way at the end of a run — regardless of whether it
measures accuracy, RMSE, F1, or IoU.

Crucially, both classes group results **by question type** (e.g., Basic Judging,
Reasoning-based Counting, Object Situation Analysis). This means a single evaluator
can report fine-grained performance across different task subtypes — not just one
overall number.

This pattern is not clearly separated in the current DisasterM3 execution script, which mainly saves raw predictions to a `.jsonl` file rather than providing a dedicated evaluation module.

---

## How It Fits Into the Proposed Framework

The proposed framework includes an `evaluation/` module:

```
evaluation/
├── base.py             ← abstract BaseEvaluator
├── vqa.py              ← VQA accuracy evaluator
└── damage_assessment.py ← damage classification evaluator
```

EarthVQA's evaluator pattern maps directly onto `evaluation/base.py`. The abstract
base class can be designed around the same two-method interface:

```python
# evaluation/base.py
from abc import ABC, abstractmethod

class BaseEvaluator(ABC):

    @abstractmethod
    def update(self, predictions, ground_truth, metadata):
        """Accumulate predictions during evaluation."""
        raise NotImplementedError

    @abstractmethod
    def summary(self) -> dict:
        """Compute and return final metrics."""
        raise NotImplementedError
```

A VQA evaluator implementing this interface would mirror EarthVQA's `VQA_OA_Metric`:

```python
# evaluation/vqa.py
from evaluation.base import BaseEvaluator

class VQAEvaluator(BaseEvaluator):

    def update(self, predictions, ground_truth, metadata):
        # accumulate correct/total per task type
        pass

    def summary(self) -> dict:
        # return accuracy per task type + overall accuracy
        pass
```

The experiment runner calls `evaluator.summary()` at the end of every run —
regardless of which evaluator is used. This keeps the runner completely decoupled
from metric computation logic, exactly as EarthVQA demonstrates.

---

## Secondary Observation: `__getitem__` and `__len__` Dataset Interface

In `data/earthvqa.py`, `EarthVQADataset` inherits from PyTorch's `Dataset` and
implements both `__getitem__` and `__len__`. This is more complete than DisasterM3's
approach and confirms that our `BaseDataset` should also require these two methods
alongside `load()` — allowing datasets to be iterated over naturally in a loop or
DataLoader.

---

## Conclusion

EarthVQA's question-type-aware evaluator with a consistent `summary()` interface is
the most directly reusable pattern for the proposed framework. It provides a clean
blueprint for `evaluation/base.py` and demonstrates how task-specific metrics can be
computed in a modular, pluggable way — which is exactly the design goal of the
evaluation layer being built.
