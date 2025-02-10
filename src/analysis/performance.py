from typing import Dict, List
import pandas as pd
import numpy as np
from src.models.student import QuizSubmission, StudentPerformance

class PerformanceAnalyzer:
    def __init__(self):
        """Initialize the performance analyzer."""
        pass

    def analyze_topic_performance(self, quiz_history: List[QuizSubmission]) -> Dict[str, float]:
        """Analyze performance by topic."""
        topic_scores = {}
        topic_counts = {}
        
        for quiz in quiz_history:
            if quiz.topic not in topic_scores:
                topic_scores[quiz.topic] = 0
                topic_counts[quiz.topic] = 0
            
            topic_scores[quiz.topic] += float(quiz.accuracy.strip('%')) / 100
            topic_counts[quiz.topic] += 1
        
        return {topic: score/count for topic, (score, count) in 
                zip(topic_scores.keys(), zip(topic_scores.values(), topic_counts.values()))}

    def identify_weak_areas(self, topic_performance: Dict[str, float]) -> List[str]:
        """Identify topics where performance is below threshold."""
        WEAKNESS_THRESHOLD = 0.6  # 60% accuracy
        return [topic for topic, score in topic_performance.items() 
                if score < WEAKNESS_THRESHOLD]

    def calculate_improvement_trends(self, quiz_history: List[QuizSubmission]) -> Dict[str, List[float]]:
        """Calculate improvement trends by topic."""
        topic_trends = {}
        
        # Sort quizzes by date
        sorted_quizzes = sorted(quiz_history, key=lambda x: x.submitted_at)
        
        for quiz in sorted_quizzes:
            if quiz.topic not in topic_trends:
                topic_trends[quiz.topic] = []
            topic_trends[quiz.topic].append(float(quiz.accuracy.strip('%')) / 100)
        
        return topic_trends

    def analyze_student_performance(self, quiz_history: List[QuizSubmission]) -> StudentPerformance:
        """Analyze overall student performance."""
        if not quiz_history:
            raise ValueError("Quiz history is empty")
            
        topic_performance = self.analyze_topic_performance(quiz_history)
        weak_areas = self.identify_weak_areas(topic_performance)
        improvement_trends = self.calculate_improvement_trends(quiz_history)
        
        return StudentPerformance(
            user_id=quiz_history[0].user_id,
            quiz_history=quiz_history,
            topic_wise_accuracy=topic_performance,
            weak_areas=weak_areas,
            improvement_trends=improvement_trends
        )