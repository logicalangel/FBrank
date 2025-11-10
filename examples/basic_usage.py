"""
Example usage of InnerMatch library
"""

import numpy as np
from innermatch import FeedbackRanker


def main():
    """Demonstrate basic usage of FeedbackRanker."""
    
    # Generate a dataset of 100 samples
    num_samples = 100
    vector_size = 10

    # Initialize empty lists for vectors and labels
    vectors1 = []
    labels = []

    for _ in range(num_samples):
        vector1 = np.random.rand(vector_size)
        label = np.random.randint(0, 2)  # Binary label (0 or 1)
        
        # Append to respective lists
        vectors1.append(vector1)
        labels.append(label)
    
    vector2 = np.random.rand(vector_size)

    # Convert lists to NumPy arrays
    vectors1_array = np.array(vectors1)
    vector2_array = np.array(vector2)
    labels_array = np.array(labels)

    # Create a FeedbackRanker instance
    ranker = FeedbackRanker(
        user_id="behrang",
        password="123456",
        session_id="1"
    )

    # Initial ranking
    print("Initial ranking:")
    ranks = ranker.rank(vectors1_array, vector2_array)
    print(ranks)

    # Provide feedback to improve the model
    print("\nProviding feedback...")
    ranker.feedback(
        vectors1_array,
        np.tile(vector2_array, (len(vectors1_array), 1)),
        labels_array,
        ranks
    )

    # Ranking after feedback
    print("\nRanking after feedback:")
    ranks = ranker.rank(vectors1_array, vector2_array)
    print(ranks)


if __name__ == "__main__":
    main()
