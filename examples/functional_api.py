"""
Example using the functional API (backward compatible with old code)
"""

import numpy as np
from innermatch import rank, feedback


def main():
    """Demonstrate functional API usage."""
    
    # Generate a dataset
    num_samples = 100
    vector_size = 10

    vectors1 = []
    labels = []

    for _ in range(num_samples):
        vector1 = np.random.rand(vector_size)
        label = np.random.randint(0, 2)
        vectors1.append(vector1)
        labels.append(label)
    
    vector2 = np.random.rand(vector_size)

    vectors1_array = np.array(vectors1)
    vector2_array = np.array(vector2)
    labels_array = np.array(labels)

    # Using functional API
    print("Initial ranking (functional API):")
    ranks = rank("behrang", "123456", "1", vectors1_array, vector2_array)
    print(ranks)

    print("\nProviding feedback...")
    feedback(
        "behrang", "123456", "1",
        vectors1_array,
        np.tile(vector2_array, (len(vectors1_array), 1)),
        labels_array,
        ranks
    )

    print("\nRanking after feedback:")
    ranks = rank("behrang", "123456", "1", vectors1_array, vector2_array)
    print(ranks)


if __name__ == "__main__":
    main()
