# DisasterM3 Repository Analysis

> This analysis is based on direct inspection of the DisasterM3 repository source code,
> including `models/__init__.py`, `pyscripts/run_vllm.py`, and the README.

---

## 1. Current Repository Structure

```
DisasterM3/
├── models/
│   └── __init__.py       # All model classes: QwenVL, InternVL, Llava + factory function
├── pyscripts/
│   ├── __init__.py       # Empty package marker
│   └── run_vllm.py       # Main script: data loading + inference + result saving
├── README.md
└── __init__.py           # Root package marker
```

The repository contains only **4 Python files** in total. The entire pipeline is concentrated
in two files: `models/__init__.py` and `pyscripts/run_vllm.py`.

---

## 2. Code Organization Analysis

### What `models/__init__.py` contains

This file contains all model-related code. It defines:

- An abstract base class `ModelConfig` (using Python's `ABC`) with one abstract method:
  `get_prompt_from_question()`. This is a good design pattern — it forces every model
  to implement prompt formatting in a standardized way.

- Three concrete model implementations: `QwenVL`, `InternVL`, and `Llava`.
  Each handles prompt construction differently depending on the model's format requirements.

- A factory function `build_model_config()` that selects the right model class based on
  string matching in the model ID:

```python
if "llava" in model_id.lower():
    model_config = Llava(model_id=model_id, **kwargs)
elif "qwen" in model_id.lower() and "vl" in model_id.lower():
    model_config = QwenVL(model_id=model_id, **kwargs)
elif "intern" in model_id.lower() and "vl" in model_id.lower():
    model_config = InternVL(model_id=model_id, **kwargs)
else:
    raise NotImplementedError(model_id)
```

- A large collection of image and video preprocessing utility functions
  (`build_transform`, `dynamic_preprocess`, `load_video`, etc.) placed directly in the
  same file as the model classes rather than in a separate `utils/` module.

### What `pyscripts/run_vllm.py` contains

This single script handles the entire evaluation pipeline end-to-end:

- **Prompt templates:** A `prompt_libs` dictionary hardcodes all task-specific prompt
  strings (bearing_body, landuse, caption, recovery, etc.) directly in the script.

- **Data loading:** Reads data from a hardcoded path:
  `{PROJECT_ROOT}/data/{subset}.json`
  Field names such as `"pre_image_path"` and `"post_image_path"` are assumed throughout.

- **Message construction:** A `get_messages_from_data()` function uses a long `if/elif`
  chain to handle each DisasterM3 subset differently.

- **Inference:** Runs the vLLM inference engine directly inside the script.

- **Result saving:** Writes predictions to a `.jsonl` file at
  `results/{subset}/{model_id}/finished.jsonl`.

Notably, **no evaluation metrics are computed anywhere in the codebase**. The script
produces predictions but does not calculate accuracy, F1, IoU, or any other metric.

---

## 3. Is the Framework Tied to a Specific Dataset?

**Yes — it is tightly coupled to DisasterM3 throughout `run_vllm.py`.**

Evidence of this coupling found directly in the code:

| Location | Coupling |
|---|---|
| `prompt_libs` dict | All prompts are DisasterM3-specific task names |
| `get_messages_from_data()` | `if subset in ["bearing_body", "building_damage_counting", ...]` — these are DisasterM3 subset names |
| Data loading path | `join(PROJECT_ROOT, "data", f"{args.subset}.json")` — assumes DisasterM3 file layout |
| Field names | `data_dict["pre_image_path"]`, `data_dict["post_image_path"]` — DisasterM3-specific fields |
| Image paths | `join(PROJECT_ROOT, "data", "images", ...)` — hardcoded directory structure |

### What would it take to add EarthVQA or MONITRS?

To run a different dataset through this codebase, a developer would need to:

1. Add new entries to the `prompt_libs` dictionary for the new dataset's task prompts
2. Add new `elif` branches inside `get_messages_from_data()` for the new subset names
3. Ensure the new dataset's JSON file matches the field names expected by the script
   (`pre_image_path`, `post_image_path`, `prompts`, `options_str`)
4. Place the dataset files in the hardcoded `data/` directory structure
5. Manually verify that none of these changes break the existing DisasterM3 workflow

There is no plugin interface, abstract dataset class, or configuration file that would
allow adding a new dataset without modifying core script logic.

---

## 4. Identified Limitations

| Limitation | Evidence in Code |
|---|---|
| Single-script architecture | All pipeline logic lives in `run_vllm.py` |
| Dataset coupling | Hardcoded paths, field names, and subset names throughout |
| No evaluation layer | Script saves predictions but computes no metrics |
| No configuration system | Dataset and model selected via CLI flags, not YAML |
| No experiment tracking | No MLflow, W&B, or equivalent integration |
| vLLM-only backend | `from vllm import LLM` — no abstraction over inference engines |
| Incomplete model abstraction | `ModelConfig` only standardizes prompt formatting, not inference |
| Adding a model requires editing core code | `build_model_config()` must be modified for every new model |
| Utility functions mixed with model classes | Image preprocessing code sits inside `models/__init__.py` |

---

## 5. What Is Worth Reusing

Despite the limitations, two patterns in the existing code are worth preserving:

**`ModelConfig` abstract base class:** The use of Python's `ABC` to define a common
interface for all model runners is the right approach. It should be extended to also
include an abstract `run(image, prompt) -> str` method so that inference itself is
also standardized — not just prompt formatting.

**`build_model_config()` factory function:** The factory pattern for model selection is
reusable. In the proposed framework it would be driven by a YAML config value rather
than string matching, but the concept of a single entry point that returns the right
model object is sound.

---

## 6. Proposed Modular Redesign

Based on the analysis above, the following architecture resolves all identified limitations.

### Core principle
```
Dataset → Model Runner → Evaluator → Experiment Tracker
```
Each stage is a separate, replaceable component connected by a clean interface.
Swapping any component requires only a configuration file change — no code modification.

### Target structure

```
framework/
├── configs/
│   ├── disasterm3_qwen.yaml        # One YAML file per experiment
│   └── earthvqa_internvl.yaml
├── datasets/
│   ├── base.py                     # Abstract BaseDataset class
│   ├── disasterm3.py               # DisasterM3 adapter
│   ├── monitrs.py                  # MONITRS adapter
│   └── earthvqa.py                 # EarthVQA adapter
├── models/
│   ├── base.py                     # Abstract BaseModelRunner with run() method
│   ├── qwen_runner.py              # Qwen2.5-VL adapter
│   └── internvl_runner.py          # InternVL3 adapter
├── evaluation/
│   ├── base.py                     # Abstract BaseEvaluator class
│   ├── vqa.py                      # Accuracy, exact match metrics
│   └── damage_assessment.py        # F1, classification metrics
├── experiments/
│   ├── runner.py                   # Orchestrates the full pipeline
│   └── tracker.py                  # MLflow / W&B logging
├── utils/
│   └── image_utils.py              # Image preprocessing (moved out of models)
└── main.py                         # Entry point: reads YAML config, runs experiment
```

### How this resolves the identified problems

| Original Problem | Solution |
|---|---|
| Dataset coupling | `BaseDataset` interface — each dataset has its own adapter class |
| No evaluation layer | `BaseEvaluator` classes compute metrics separately from inference |
| No config system | YAML files control dataset, model, task, and tracker selection |
| No experiment tracking | `tracker.py` logs all results automatically to MLflow or W&B |
| vLLM-only backend | `BaseModelRunner.run()` abstracts over any inference backend |
| Adding model edits core code | New model = new adapter file only, no existing code touched |
| Utils mixed with models | `utils/image_utils.py` separates preprocessing from model logic |

### What is reused from DisasterM3

- The `ModelConfig` ABC concept is preserved and extended into `BaseModelRunner`
- The factory pattern from `build_model_config()` is kept, now config-driven
- The batch processing approach from `create_batch_inputs()` is preserved in `runner.py`
- The `.jsonl` results format is retained as a prediction artifact saved by `tracker.py`

---

## 7. Conclusion

The current DisasterM3 repository provides useful benchmark code for running VLM inference on DisasterM3 tasks. It already contains a partial model abstraction through `ModelConfig` and model-specific classes for QwenVL, InternVL, and LLaVA. However, the framework is still tightly coupled to the DisasterM3 dataset structure because dataset loading, prompt construction, task handling, inference, and result saving are mostly handled inside one script.

To support broader evaluation across datasets such as EarthVQA or MONITRS, the codebase should be redesigned into a modular framework with separate dataset adapters, model runners, evaluators, YAML configuration files, and experiment tracking.
