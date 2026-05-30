# Execution Notes — DisasterM3 Minimal Execution Attempt

## Environment

| Item | Details |
|---|---|
| Operating System | Windows 11 |
| Python Version | 3.12.4 |
| Virtual Environment | `.venv` (created via `python -m venv .venv`) |
| GPU | Not available (CPU-only machine) |
| Date | May 2026 |

---

## Step 1 — Repository Setup

Forked the official DisasterM3 repository and cloned it locally:

```bash
git clone https://github.com/YOUR_USERNAME/DisasterM3.git
cd DisasterM3
```

A virtual environment was created and activated before installing any packages:

```bash
python -m venv .venv
.venv\Scripts\activate
```

The prompt confirmed activation by showing `(.venv)` at the start of the terminal line.

---

## Step 2 — Dependency Installation

### Packages that installed successfully

```bash
pip install pillow tqdm transformers torch torchvision numpy qwen-vl-utils decord
```

The following packages were confirmed working:

```
(.venv) C:\Users\jassi\Desktop\DisasterM3> python -c "import torch; print('torch:', torch.__version__)"
torch: 2.12.0+cpu

(.venv) C:\Users\jassi\Desktop\DisasterM3> python -c "import transformers; print('transformers OK')"
transformers OK

(.venv) C:\Users\jassi\Desktop\DisasterM3> python -c "import PIL; print('Pillow OK')"
Pillow OK

(.venv) C:\Users\jassi\Desktop\DisasterM3> python -c "import qwen_vl_utils; print('qwen_vl_utils OK')"
qwen_vl_utils OK
```

Note: torch installed as **CPU-only** (`2.12.0+cpu`). No CUDA version was available
because the machine does not have an NVIDIA GPU.

### vLLM — installation failed

```bash
pip install vllm
```

vLLM could not be installed. Verification confirmed it is not present:

```
(.venv) C:\Users\jassi\Desktop\DisasterM3> pip show vllm
WARNING: Package(s) not found: vllm
```

**Reason:** vLLM only supports Linux operating systems with NVIDIA CUDA-capable GPUs.
It cannot be installed or run on Windows or on CPU-only machines.

---

## Step 3 — Execution Attempt

The main benchmarking script was invoked with the `--help` flag to test basic execution:

```bash
python pyscripts/run_vllm.py --help
```

**Output:**

```
Traceback (most recent call last):
  File "C:\Users\jassi\Desktop\DisasterM3\pyscripts\run_vllm.py", line 12, in <module>
    from vllm import EngineArgs, LLM, SamplingParams
ModuleNotFoundError: No module named 'vllm'
```

The script fails at import time before any execution logic runs.
This confirms that the entire `run_vllm.py` pipeline is blocked by the vLLM dependency.

---

## Step 4 — Encountered Issues

### Issue 1 — vLLM is not installable on Windows

**Description:** vLLM requires Linux and an NVIDIA GPU with CUDA support.
It cannot be installed on Windows at all, regardless of Python version.

**Impact:** The main benchmarking script `pyscripts/run_vllm.py` cannot be executed
on any Windows or CPU-only machine.

**Classification:** Hard blocker — not a configuration issue.

---

### Issue 2 — PyTorch installed without CUDA support

**Description:** `pip install torch` on a CPU-only Windows machine installs
the CPU-only build (`torch 2.12.0+cpu`). Even if vLLM were available,
GPU-accelerated inference would not be possible without a CUDA-compatible GPU.

**Impact:** Even partial model loading would run extremely slowly or not at all.

---

### Issue 3 — Dataset not available

**Description:** The DisasterM3 dataset must be requested via an official form:
https://forms.gle/APQpmyuThh28HsJdA

The script expects dataset files at `{PROJECT_ROOT}/data/{subset}.json` and
images at `{PROJECT_ROOT}/data/images/`. These files are not included in the
repository and were not available at time of testing.

**Impact:** Even if vLLM were installed, the script would fail at data loading.

---

### Issue 4 — README missing setup requirements

**Description:** The README provides only two example run commands. It does not mention:
- Minimum OS requirements (Linux only)
- GPU requirements (NVIDIA CUDA required)
- Python version compatibility
- How to structure the dataset directory after download

This makes it difficult for new users to understand the requirements before attempting setup.

---

## Step 5 — README Update

Based on the above findings, the following section should be added to the README:

```markdown
## Requirements

- **Operating System:** Linux (Ubuntu 20.04+ recommended)
- **GPU:** NVIDIA GPU with CUDA support (required for vLLM)
- **Python:** 3.9 or higher
- **Dataset:** Must be requested separately via https://forms.gle/APQpmyuThh28HsJdA

## Setup

### 1. Create a virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/macOS

### 2. Install dependencies
pip install vllm transformers torch torchvision pillow tqdm numpy qwen-vl-utils

### 3. Download and place the dataset
Place the downloaded dataset under:
  data/
  ├── bearing_body.json
  ├── caption.json
  └── images/
```

---

## Summary

| Step | Status | Notes |
|---|---|---|
| Repository clone | Done | Forked and cloned successfully |
| Virtual environment | Done | Created and activated |
| Core dependencies | Partial | transformers, torch (CPU), Pillow, qwen_vl_utils installed |
| vLLM installation | Failed | Linux + NVIDIA GPU required — not available on Windows |
| Script execution | Failed | `ModuleNotFoundError: No module named 'vllm'` |
| Dataset download | Not completed | Requires form submission and approval |

---

## Reproducibility Assessment

The DisasterM3 benchmarking pipeline has significant reproducibility barriers
for users without access to:

1. A Linux operating system
2. An NVIDIA CUDA-compatible GPU
3. Approved access to the dataset

These are understandable constraints for a GPU-intensive research benchmark,
but they should be explicitly stated in the README to prevent confusion.
The modular framework proposed in `analysis.md` and implemented in `datasets/`
is designed to allow incremental testing without requiring the full environment.
