from typing import List, Dict
from datetime import datetime, timedelta
import numpy as np
from .constants import (
    WEAK_PERFORMANCE_THRESHOLD,
    GOOD_PERFORMANCE_THRESHOLD,
    SIGNIFICANT_IMPROVEMENT,
    RECENT_ACTIVITY_DAYS
)

def calculate_accuracy(correct: int, total: int) -> float:
    """Calculate accuracy percentage."""
    return (correct / total * 100) if total > 0 else 0

def calculate_improvement(old_score: float, new_score: float) -> float:
    """Calculate improvement percentage."""
    return ((new_score - old_score) / old_score * 100) if old_score > 0 else 0

def get_recent_activities(activities: List[Dict], days: int = RECENT_ACTIVITY_DAYS) -> List[Dict]:
    """Filter activities within recent days."""
    cutoff_date = datetime.now() - timedelta(days=days)
    return [
        activity for activity in activities 
        if datetime.fromisoformat(activity['submitted_at']) > cutoff_date
    ]

def categorize_performance(accuracy: float) -> str:
    """Categorize performance based on accuracy."""
    if accuracy >= GOOD_PERFORMANCE_THRESHOLD:
        return "Good"
    elif accuracy <= WEAK_PERFORMANCE_THRESHOLD:
        return "Needs Improvement"
    return "Average"

def calculate_consistency_score(accuracies: List[float]) -> float:
    """Calculate consistency score based on standard deviation of accuracies."""
    if not accuracies:
        return 0
    std_dev = np.std(accuracies)
    max_std = 100  # Maximum possible standard deviation
    consistency = 1 - (std_dev / max_std)
    return max(0, min(1, consistency))  # Normalize between 0 and 1

def format_time_taken(seconds: int) -> str:
    """Format seconds into readable time string."""
    minutes, seconds = divmod(seconds, 60)
    return f"{minutes:02d}:{seconds:02d}"

def detect_significant_improvement(scores: List[float]) -> bool:
    """Detect if there's significant improvement in scores."""
    if len(scores) < 2:
        return False
    return (scores[-1] - scores[0]) / scores[0] >= SIGNIFICANT_IMPROVEMENT