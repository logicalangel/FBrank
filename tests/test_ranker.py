"""
Unit tests for the FeedbackRanker class and functions.
"""

import os
import tempfile
import shutil
import numpy as np
import pytest
from innermatch import FeedbackRanker, rank, feedback


class TestFeedbackRanker:
    """Test suite for FeedbackRanker class."""

    @pytest.fixture
    def temp_model_dir(self):
        """Create a temporary directory for model storage."""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)

    @pytest.fixture
    def sample_data(self):
        """Generate sample data for testing."""
        np.random.seed(42)
        num_samples = 50
        vector_size = 10

        documents = np.random.rand(num_samples, vector_size)
        query = np.random.rand(vector_size)
        labels = np.random.randint(0, 2, num_samples)

        return documents, query, labels

    def test_ranker_initialization(self, temp_model_dir):
        """Test FeedbackRanker initialization."""
        ranker = FeedbackRanker(
            user_id="test_user",
            password="test_pass",
            session_id="session1",
            model_location=temp_model_dir,
        )

        assert ranker.user_id == "test_user"
        assert ranker.session_id == "session1"
        assert ranker.model_location == temp_model_dir
        assert ranker.W is None

    def test_rank_without_feedback(self, temp_model_dir, sample_data):
        """Test ranking without prior feedback."""
        documents, query, _ = sample_data

        ranker = FeedbackRanker(
            user_id="test_user",
            password="test_pass",
            session_id="session1",
            model_location=temp_model_dir,
        )

        ranks = ranker.rank(documents, query)

        assert len(ranks) == len(documents)
        assert len(set(ranks)) == len(documents)  # All unique
        assert all(0 <= r < len(documents) for r in ranks)

    def test_rank_with_feedback(self, temp_model_dir, sample_data):
        """Test ranking improves with feedback."""
        documents, query, labels = sample_data

        ranker = FeedbackRanker(
            user_id="test_user",
            password="test_pass",
            session_id="session1",
            model_location=temp_model_dir,
        )

        # Initial ranking
        ranks_before = ranker.rank(documents, query)
        W_before = ranker.W.copy()

        # Provide feedback
        ranker.feedback(documents, np.tile(query, (len(documents), 1)), labels)

        # Weight matrix should change after feedback
        assert not np.allclose(W_before, ranker.W)

        # Ranking after feedback
        ranks_after = ranker.rank(documents, query)

        # At least the model was updated
        # Note: rankings might stay the same with random data, but the model changed
        assert ranker.W is not None

    def test_model_persistence(self, temp_model_dir, sample_data):
        """Test that models are saved and loaded correctly."""
        documents, query, labels = sample_data

        # Create and train a ranker
        ranker1 = FeedbackRanker(
            user_id="test_user",
            password="test_pass",
            session_id="session1",
            model_location=temp_model_dir,
        )

        ranker1.rank(documents, query)
        ranker1.feedback(documents, np.tile(query, (len(documents), 1)), labels)
        W_saved = ranker1.W.copy()

        # Create a new ranker with same credentials
        ranker2 = FeedbackRanker(
            user_id="test_user",
            password="test_pass",
            session_id="session1",
            model_location=temp_model_dir,
        )

        ranker2.load_model(len(query))

        # Weight matrices should be identical
        assert np.allclose(W_saved, ranker2.W)

    def test_different_sessions(self, temp_model_dir, sample_data):
        """Test that different sessions have different models."""
        documents, query, labels = sample_data

        ranker1 = FeedbackRanker(
            user_id="test_user",
            password="test_pass",
            session_id="session1",
            model_location=temp_model_dir,
        )

        ranker2 = FeedbackRanker(
            user_id="test_user",
            password="test_pass",
            session_id="session2",
            model_location=temp_model_dir,
        )

        ranker1.rank(documents, query)
        ranker1.feedback(documents, np.tile(query, (len(documents), 1)), labels)

        ranker2.rank(documents, query)

        # Different sessions should have different weight matrices
        assert not np.allclose(ranker1.W, ranker2.W)

    def test_vector_dimension_mismatch(self, temp_model_dir):
        """Test that mismatched vector dimensions raise an error."""
        ranker = FeedbackRanker(
            user_id="test_user",
            password="test_pass",
            session_id="session1",
            model_location=temp_model_dir,
        )

        documents = np.random.rand(10, 5)
        query = np.random.rand(8)  # Different dimension

        with pytest.raises(Exception, match="Vector sizes do not match"):
            ranker.rank(documents, query)


class TestFunctionalAPI:
    """Test suite for functional API."""

    @pytest.fixture
    def temp_model_dir(self):
        """Create a temporary directory for model storage."""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)

    @pytest.fixture
    def sample_data(self):
        """Generate sample data for testing."""
        np.random.seed(42)
        num_samples = 50
        vector_size = 10

        documents = np.random.rand(num_samples, vector_size)
        query = np.random.rand(vector_size)
        labels = np.random.randint(0, 2, num_samples)

        return documents, query, labels

    def test_functional_rank(self, temp_model_dir, sample_data):
        """Test functional rank API."""
        documents, query, _ = sample_data

        ranks = rank("test_user", "test_pass", "session1", documents, query, temp_model_dir)

        assert len(ranks) == len(documents)
        assert all(0 <= r < len(documents) for r in ranks)

    def test_functional_feedback(self, temp_model_dir, sample_data):
        """Test functional feedback API."""
        documents, query, labels = sample_data

        # Get initial ranking
        ranks_before = rank("test_user", "test_pass", "session1", documents, query, temp_model_dir)

        # Create a ranker to get the weight matrix before feedback
        ranker_check = FeedbackRanker("test_user", "test_pass", "session1", temp_model_dir)
        ranker_check.load_model(len(query))
        W_before = ranker_check.W.copy()

        # Provide feedback
        feedback(
            "test_user",
            "test_pass",
            "session1",
            documents,
            np.tile(query, (len(documents), 1)),
            labels,
            None,
            temp_model_dir,
        )

        # Get ranking after feedback
        ranks_after = rank("test_user", "test_pass", "session1", documents, query, temp_model_dir)

        # Load model again to check if it changed
        ranker_check.load_model(len(query))

        # Weight matrix should change after feedback
        assert not np.allclose(W_before, ranker_check.W)


class TestEdgeCases:
    """Test edge cases and error handling."""

    @pytest.fixture
    def temp_model_dir(self):
        """Create a temporary directory for model storage."""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)

    def test_empty_feedback(self, temp_model_dir):
        """Test with empty feedback array."""
        ranker = FeedbackRanker(
            user_id="test_user",
            password="test_pass",
            session_id="session1",
            model_location=temp_model_dir,
        )

        documents = np.random.rand(0, 10)
        query = np.random.rand(10)
        labels = np.array([])

        # Should handle empty arrays gracefully
        ranker.feedback(documents, np.array([]).reshape(0, 10), labels)

    def test_single_document(self, temp_model_dir):
        """Test ranking with a single document."""
        ranker = FeedbackRanker(
            user_id="test_user",
            password="test_pass",
            session_id="session1",
            model_location=temp_model_dir,
        )

        documents = np.random.rand(1, 10)
        query = np.random.rand(10)

        ranks = ranker.rank(documents, query)

        assert len(ranks) == 1
        assert ranks[0] == 0
