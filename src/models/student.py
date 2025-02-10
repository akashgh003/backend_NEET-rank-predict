from dataclasses import dataclass
from typing import Dict, List, Optional
from datetime import datetime

@dataclass
class QuizResponse:
    question_id: int
    selected_option_id: int
    is_correct: bool
    topic: str
    difficulty_level: str

@dataclass
class QuizSubmission:
    id: int
    quiz_id: int
    user_id: str
    submitted_at: datetime
    score: float
    accuracy: str
    speed: str
    final_score: str
    correct_answers: int
    incorrect_answers: int
    total_questions: int
    response_map: Dict[str, int]
    topic: str

@dataclass
class StudentPerformance:
    user_id: str
    quiz_history: List[QuizSubmission]
    topic_wise_accuracy: Dict[str, float]
    weak_areas: List[str]
    improvement_trends: Dict[str, List[float]]
    predicted_rank: Optional[int] = None
    recommended_colleges: Optional[List[str]] = None