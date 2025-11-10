<div align="center">

# InnerMatch

**A feedback-based ranking algorithm for adaptive information retrieval**

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-Custom-orange)](LICENSE.txt)
[![GitHub Stars](https://img.shields.io/github/stars/iBM88/FBrank?style=social)](https://github.com/iBM88/FBrank)

[Features](#features) •
[Installation](#installation) •
[Quick Start](#quick-start) •
[Documentation](#api-reference) •
[Examples](#examples) •
[Contributing](#contributing)

</div>

---

## Overview

InnerMatch is a machine learning library that implements a feedback-based ranking algorithm for information retrieval systems. Unlike traditional ranking methods, InnerMatch learns from user feedback to continuously improve document ranking quality over time.

### Key Features

- 🎯 **Adaptive Learning** - Improves ranking based on user feedback
- 🔄 **Multi-Session Support** - Manage multiple models per user
- 💾 **Persistent Models** - Automatically save and load trained models
- 🐍 **Type-Safe** - Complete type hints for better development experience
- 📦 **Dual API** - Both object-oriented and functional interfaces
- ⚡ **Lightweight** - Minimal dependencies (only NumPy required)

### Performance

Tested on the [Wikipedia 2023-11 Retrieval Dataset](https://huggingface.co/datasets/ellamind/wikipedia-2023-11-retrieval-multilingual-qrels):

| Metric | Baseline | With InnerMatch | Improvement |
|--------|----------|-----------------|-------------|
| MRR    | 0.3      | 0.4             | **+33%**    |

---

## Installation

### Install from PyPI

```bash
pip install innermatch
```

### Install from Source

```bash
git clone https://github.com/iBM88/FBrank.git
cd FBrank
pip install -e .
```

### Requirements

- Python 3.8+
- NumPy >= 1.20.0

## Quick Start

### Object-Oriented API (Recommended)

```python
import numpy as np
from innermatch import FeedbackRanker

# Create a ranker instance
ranker = FeedbackRanker(
    user_id="user123",
    password="password",
    session_id="session1"
)

# Prepare your data
documents = np.random.rand(100, 10)  # 100 documents, 10-dimensional vectors
query = np.random.rand(10)           # Query vector
labels = np.random.randint(0, 2, 100) # Feedback: 0=irrelevant, 1=relevant

# Get initial ranking
ranks = ranker.rank(documents, query)

# Provide feedback to improve the model
ranker.feedback(
    documents,
    np.tile(query, (len(documents), 1)),
    labels
)

# Get improved ranking
improved_ranks = ranker.rank(documents, query)
```

### Functional API

```python
import numpy as np
from innermatch import rank, feedback

documents = np.random.rand(100, 10)
query = np.random.rand(10)
labels = np.random.randint(0, 2, 100)

# Rank documents
ranks = rank("user123", "password", "session1", documents, query)

# Provide feedback
feedback("user123", "password", "session1", 
         documents, np.tile(query, (len(documents), 1)), labels)

# Re-rank with improved model
improved_ranks = rank("user123", "password", "session1", documents, query)
```

---

## Examples

Check out the [`examples/`](examples/) directory for complete working examples:

- [`basic_usage.py`](examples/basic_usage.py) - Object-oriented API walkthrough
- [`functional_api.py`](examples/functional_api.py) - Functional API demonstration

### Running Examples

```bash
python examples/basic_usage.py
```

---

#### Constructor

```python
FeedbackRanker(user_id, password, session_id, model_location="models/", dimension=None)
```

**Parameters:**

- `user_id` (str): User identifier
- `password` (str): Authentication password  
- `session_id` (str): Session identifier for model management
- `model_location` (str, optional): Directory for model storage (default: "models/")
- `dimension` (int, optional): Vector dimension

#### Methods

**`rank(target_vector_array, query_vector)`**

Rank documents by similarity to query.

- **Returns**: Array of indices representing ranking order

**`feedback(target_vector_array, query_vector_array, feedback_array, rank_array=None, learning_rate=1.0)`**

Update model with user feedback.

- **Parameters**:
  - `feedback_array`: Labels (0=irrelevant, 1=relevant)
  - `learning_rate`: Learning rate for updates (default: 1.0)

**`load_model(dimension)`** / **`save_model()`**

Load or save the weight matrix.

---

## License

This project is **free for personal and academic use**.

**Commercial use requires a paid license**. Contact [synaptosearch@gmail.com](mailto:synaptosearch@gmail.com) for details.

See [LICENSE.txt](LICENSE.txt) for more information.

---

## Citation

If you use InnerMatch in your research, please cite:

```bibtex
@software{innermatch2024,
  author = {Mehrparvar, Behrang},
  title = {InnerMatch: Feedback-based Ranking Algorithm},
  year = {2024},
  publisher = {Synaptosearch},
  url = {https://github.com/iBM88/FBrank}
}
```

---

## Contact & Support

**Author**: Behrang Mehrparvar - Synaptosearch  
**Email**: <synaptosearch@gmail.com>  
**Issues**: [GitHub Issues](https://github.com/iBM88/FBrank/issues)

---

<div align="center">

**⭐ Star us on GitHub if InnerMatch helps your project! ⭐**

Made with ❤️ by [Synaptosearch](mailto:synaptosearch@gmail.com)

</div>
