"""
Core ranking functionality with feedback-based learning.
"""

import os
import pickle
import numpy as np
from typing import List, Tuple, Optional
from numpy.typing import NDArray


class FeedbackRanker:
    """
    A ranking system that learns from user feedback to improve document retrieval.

    This class implements a feedback-based ranking algorithm that uses a learned
    weight matrix to measure similarity between query and document vectors.

    Attributes:
        user_id (str): User identifier for model persistence
        password (str): Password for authentication
        session_id (str): Session identifier to support multiple models per user
        model_location (str): Directory path where models are stored
        dimension (Optional[int]): Vector dimension size
        W (Optional[NDArray]): Weight matrix for similarity computation
    """

    def __init__(
        self,
        user_id: str,
        password: str,
        session_id: str,
        model_location: str = "models/",
        dimension: Optional[int] = None,
    ):
        """
        Initialize the FeedbackRanker.

        Args:
            user_id: User identifier
            password: Authentication password
            session_id: Session identifier
            model_location: Directory to store model files (default: "models/")
            dimension: Vector dimension (optional, inferred from first use)
        """
        self.user_id = user_id
        self.password = password
        self.session_id = session_id
        self.model_location = model_location
        self.dimension = dimension
        self.W = None

        # Create model directory if it doesn't exist
        os.makedirs(self.model_location, exist_ok=True)

    def _login(self) -> bool:
        """
        Authenticate user credentials.

        Returns:
            bool: True if authentication successful
        """
        # TODO: Implement proper authentication
        return True

    def _get_model_path(self) -> str:
        """Get the file path for the current model."""
        return os.path.join(self.model_location, f"{self.user_id}_{self.session_id}")

    def load_model(self, dimension: int) -> NDArray:
        """
        Load the weight matrix from disk or initialize a new one.

        Args:
            dimension: Vector dimension size

        Returns:
            Weight matrix W

        Raises:
            Exception: If authentication fails
        """
        if not self._login():
            raise Exception("Login failed: Unauthorized (check credentials)")

        self.dimension = dimension
        filename = self._get_model_path()

        if not os.path.exists(filename):
            # Initialize with identity matrix
            self.W = np.zeros((dimension, dimension)) + np.eye(dimension, dimension)
        else:
            with open(filename, "rb") as file:
                self.W = pickle.load(file)

        return self.W

    def save_model(self) -> None:
        """
        Save the current weight matrix to disk.

        Raises:
            Exception: If authentication fails or model not initialized
        """
        if not self._login():
            raise Exception("Login failed: Unauthorized (check credentials)")

        if self.W is None:
            raise Exception("No model to save. Run rank() or feedback() first.")

        filename = self._get_model_path()
        with open(filename, "wb") as file:
            pickle.dump(self.W, file)

    def rank(self, target_vector_array: NDArray, query_vector: NDArray) -> NDArray:
        """
        Rank target vectors based on similarity to query vector.

        Args:
            target_vector_array: Array of document vectors to rank (shape: [n_docs, dim])
            query_vector: Query vector (shape: [dim])

        Returns:
            Array of indices representing the ranking order

        Raises:
            Exception: If vector dimensions don't match
        """
        if len(query_vector) != len(target_vector_array[0]):
            raise Exception("Error: Vector sizes do not match.")

        # Load model if not already loaded
        if self.W is None:
            self.load_model(len(query_vector))

        # Calculate energy for each target vector
        energies = [
            -0.5 * np.dot(query_vector, np.dot(self.W, target_vector_array[i]))
            for i in range(len(target_vector_array))
        ]

        # Sort by energy (lower energy = higher rank)
        ranks = np.argsort(energies)
        return ranks

    def feedback(
        self,
        target_vector_array: NDArray,
        query_vector_array: NDArray,
        feedback_array: NDArray,
        rank_array: Optional[NDArray] = None,
        learning_rate: float = 1.0,
    ) -> None:
        """
        Update the model based on user feedback.

        Args:
            target_vector_array: Array of document vectors (shape: [n_docs, dim])
            query_vector_array: Array of query vectors (shape: [n_docs, dim])
            feedback_array: Feedback labels (0: not similar, 1: similar)
            rank_array: Optional ranking array for performance measurement
            learning_rate: Learning rate for weight updates (default: 1.0)

        Raises:
            Exception: If vector dimensions don't match
        """
        # Handle empty arrays
        if len(target_vector_array) == 0 or len(query_vector_array) == 0:
            return

        if len(query_vector_array[0]) != len(target_vector_array[0]):
            raise Exception("Error: Vector sizes do not match.")

        # Load model if not already loaded
        if self.W is None:
            self.load_model(len(query_vector_array[0]))

        # Update weight matrix using outer product of vectors
        update = learning_rate * sum(
            feedback_array[i] * np.outer(target_vector_array[i], query_vector_array[i])
            for i in range(len(feedback_array))
        )

        self.W = self.W + update
        self.save_model()


# Functional API for backward compatibility
def rank(
    user_id: str,
    password: str,
    session_id: str,
    target_vector_array: NDArray,
    query_vector: NDArray,
    model_location: str = "models/",
) -> NDArray:
    """
    Rank target vectors based on similarity to query vector.

    Args:
        user_id: User identifier
        password: Authentication password
        session_id: Session identifier
        target_vector_array: Array of document vectors to rank
        query_vector: Query vector
        model_location: Directory for model storage

    Returns:
        Array of indices representing the ranking order
    """
    ranker = FeedbackRanker(user_id, password, session_id, model_location)
    return ranker.rank(target_vector_array, query_vector)


def feedback(
    user_id: str,
    password: str,
    session_id: str,
    target_vector_array: NDArray,
    query_vector_array: NDArray,
    feedback_array: NDArray,
    rank_array: Optional[NDArray] = None,
    model_location: str = "models/",
) -> None:
    """
    Update the model based on user feedback.

    Args:
        user_id: User identifier
        password: Authentication password
        session_id: Session identifier
        target_vector_array: Array of document vectors
        query_vector_array: Array of query vectors
        feedback_array: Feedback labels (0: not similar, 1: similar)
        rank_array: Optional ranking array for performance measurement
        model_location: Directory for model storage
    """
    ranker = FeedbackRanker(user_id, password, session_id, model_location)
    ranker.feedback(target_vector_array, query_vector_array, feedback_array, rank_array)
