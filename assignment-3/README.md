# Assignment Track 3: Data Science Foundations & Numerical Computing with NumPy

This directory contains coursework submissions, laboratory notebooks, and applied assignments for **Assignment 3: Numerical Computing & NumPy Foundations**.

All sessions follow an **`.ipynb`-first** interactive format with pre-rendered results, paired with standalone `.py` scripts and zero-dependency terminal execution runners.

---

## 🗂️ Sessions Index

| Session | Topic | Key Deliverables | Status |
| :--- | :--- | :--- | :--- |
| **Session 1** | [NumPy Foundations (Part 1: Arrays & Creation)](./s01_kirana_numpy/README.md) | [`kirana_numpy.ipynb`](./s01_kirana_numpy/kirana_numpy.ipynb) <br> [`kirana_numpy.py`](./s01_kirana_numpy/kirana_numpy.py) | ✅ Completed (Executed) |
| **Session 2** | [NumPy Intermediate (Part 2: Indexing, Slicing, Broadcasting)](./s02_kirana_indexing/README.md) | [`kirana_indexing.ipynb`](./s02_kirana_indexing/kirana_indexing.ipynb) <br> [`kirana_indexing.py`](./s02_kirana_indexing/kirana_indexing.py) | ✅ Completed (Executed) |

---

## 🛠️ Module Structure

```text
assignment-3/
├── README.md                          # This directory index and track documentation
├── kirana_numpy.ipynb                 # Quick-access copy of Session 1 notebook
├── kirana_numpy.py                    # Quick-access copy of Session 1 Python runner
├── kirana_indexing.ipynb              # Quick-access copy of Session 2 notebook
├── kirana_indexing.py                 # Quick-access copy of Session 2 Python runner
│
├── s01_kirana_numpy/                  # Session 1: NumPy Foundations (Part 1: Arrays & Creation)
│   ├── README.md                      # Comprehensive session documentation & task analysis
│   ├── kirana_numpy.ipynb             # Executed interactive Jupyter Notebook (All 4 tasks solved)
│   └── kirana_numpy.py                # Standalone zero-dependency verification script
│
└── s02_kirana_indexing/               # Session 2: NumPy Intermediate (Part 2: Indexing, Slicing, Broadcasting)
    ├── README.md                      # Comprehensive session documentation & broadcasting guide
    ├── kirana_indexing.ipynb          # Executed interactive Jupyter Notebook (All 4 tasks solved)
    └── kirana_indexing.py             # Standalone zero-dependency verification script
```

---

## 💡 Key Conceptual Highlights

- **Contiguous Memory Buffers:** NumPy arrays allocate flat, unbroken blocks in memory (`C_CONTIGUOUS`), enabling direct hardware cache prefetching.
- **Pointer Overhead Elimination:** Python lists store pointers to `PyObject` wrappers (~28 bytes per integer). NumPy stores raw bytes (8 bytes for `int64`), reducing memory consumption by over **75%**.
- **Vectorized SIMD Execution:** NumPy operations bypass Python's bytecode evaluation loop and execute pre-compiled C loops with SIMD vectorization, achieving speedups of **20x to 100x**.
- **Slicing & Memory Views:** Slices share underlying memory buffers; modifications affect the parent array unless `.copy()` is explicitly invoked.
- **Multi-Dimensional Indexing:** Flexible slicing syntax (`[start:end:step]`), boolean masking (`units_sold > 40`), and fancy indexing (`[[0, 3, 5]]`) without loops.
- **Broadcasting Principles:** Automatic dimension expansion across scalar and array operands when dimensions are equal or one is 1.
- **Feature Scaling:** Efficient row-wise Min-Max normalization preserving dimensions with `keepdims=True`.
