---
layout: default
title: Installation
nav_order: 2
---

# Installation

## Requirements

- Python 3.8 or higher
- NumPy ≥ 1.21
- SciPy ≥ 1.7
- Matplotlib ≥ 3.4

## From Source (recommended)

```bash
git clone https://github.com/QL-UoHull/Ellipsoid-Fitting-via-Least-Squares-with-Ellipsoid-Specific-Constraints-Li-Griffiths-2004-.git
cd Ellipsoid-Fitting-via-Least-Squares-with-Ellipsoid-Specific-Constraints-Li-Griffiths-2004-
pip install -e .
```

## Dependencies Only

```bash
pip install numpy scipy matplotlib
```

Then add the `src/` directory to your Python path:

```python
import sys
sys.path.insert(0, 'path/to/repo/src')
```

## Google Colab

Open the demo notebook directly in Colab – no local installation needed:

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/QL-UoHull/Ellipsoid-Fitting-via-Least-Squares-with-Ellipsoid-Specific-Constraints-Li-Griffiths-2004-/blob/main/notebooks/ellipsoid_fitting_demo.ipynb)
