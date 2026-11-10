# Assignment Track 3: Data Science Foundations & Numerical Computing with NumPy

This directory contains coursework submissions, laboratory notebooks, and applied assignments for **Assignment 3: Numerical Computing & NumPy Foundations**.

All sessions follow an **`.ipynb`-first** interactive format with pre-rendered results, paired with standalone `.py` scripts and zero-dependency terminal execution runners.

---

## 🗂️ Sessions Index

| Session | Topic | Key Deliverables | Status |
| :--- | :--- | :--- | :--- |
| **Session 1** | [NumPy Foundations (Part 1: Arrays & Creation)](./s01_kirana_numpy/README.md) | [`kirana_numpy.ipynb`](./s01_kirana_numpy/kirana_numpy.ipynb) <br> [`kirana_numpy.py`](./s01_kirana_numpy/kirana_numpy.py) | ✅ Completed (Executed) |

---

## 🛠️ Module Structure

```text
assignment-3/
├── README.md                          # This directory index and track documentation
├── kirana_numpy.ipynb                 # Quick-access copy of Session 1 notebook
├── kirana_numpy.py                    # Quick-access copy of Session 1 Python runner
│
└── s01_kirana_numpy/                  # Session 1: NumPy Foundations (Part 1: Arrays & Creation)
    ├── README.md                      # Comprehensive session documentation & task analysis
    ├── kirana_numpy.ipynb             # Executed interactive Jupyter Notebook (All 4 tasks solved)
    └── kirana_numpy.py                # Standalone zero-dependency verification script
```

---

## 💡 Key Conceptual Highlights

- **Contiguous Memory Buffers:** NumPy arrays allocate flat, unbroken blocks in memory (`C_CONTIGUOUS`), enabling direct hardware cache prefetching.
- **Pointer Overhead Elimination:** Python lists store pointers to `PyObject` wrappers (~28 bytes per integer). NumPy stores raw bytes (8 bytes for `int64`), reducing memory consumption by over **75%**.
- **Vectorized SIMD Execution:** NumPy operations bypass Python's bytecode evaluation loop and execute pre-compiled C loops with SIMD vectorization, achieving speedups of **20x to 100x**.
- **Array Attributes & Diagnostics:** Complete visibility into dimensionality, data types, strides, and memory footprint through the custom `array_report()` tool.
