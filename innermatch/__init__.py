"""
InnerMatch - A feedback-based ranking algorithm
Author: Behrang Mehrparvar - Synaptosearch
Contact: synaptosearch@gmail.com
"""

from .ranker import FeedbackRanker, rank, feedback

__version__ = "0.1.0"
__all__ = ["FeedbackRanker", "rank", "feedback"]
