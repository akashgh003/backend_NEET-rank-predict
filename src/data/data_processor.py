from typing import Dict, List
import pandas as pd
from datetime import datetime
from src.models.student import QuizSubmission

class DataProcessor:
    def __init__(self):
        self.required_fields = [
            'id', 'quiz_id', 'user_id', 'submitted_at', 
            'score', 'accuracy', 'final_score'
        ]

    def preprocess_quiz_submission(self, raw_data: Dict) -> QuizSubmission:
        """Process raw quiz submission data into QuizSubmission object."""
        # Validate required fields
        for field in self.required_fields:
            if field not in raw_data:
                raise ValueError(f"Missing required field: {field}")
        
        # Convert string datetime to datetime object
        submitted_at = datetime.fromisoformat(raw_data['submitted_at'].replace('Z', '+00:00'))
        
        # Extract topic from quiz data
        topic = raw_data.get('quiz', {}).get('topic', 'Unknown')
        
        return QuizSubmission(
            id=raw_data['id'],
            quiz_id=raw_data['quiz_id'],
            user_id=raw_data['user_id'],
            submitted_at=submitted_at,
            score=float(raw_data['score']),
            accuracy=raw_data['accuracy'],
            speed=raw_data.get('speed', '0'),
            final_score=raw_data['final_score'],
            correct_answers=raw_data.get('correct_answers', 0),
            incorrect_answers=raw_data.get('incorrect_answers', 0),
            total_questions=raw_data.get('total_questions', 0),
            response_map=raw_data.get('response_map', {}),
            topic=topic
        )

    def process_historical_data(self, raw_data: List[Dict]) -> List[QuizSubmission]:
        """Process a list of historical quiz submissions."""
        processed_data = []
        for submission in raw_data:
            try:
                processed = self.preprocess_quiz_submission(submission)
                processed_data.append(processed)
            except ValueError as e:
                print(f"Skipping invalid submission: {e}")
                continue
        return processed_data

    def extract_topic_performance(self, quiz_submissions: List[QuizSubmission]) -> pd.DataFrame:
        """Extract topic-wise performance metrics."""
        data = []
        for submission in quiz_submissions:
            data.append({
                'topic': submission.topic,
                'accuracy': float(submission.accuracy.strip('%')),
                'score': float(submission.final_score),
                'date': submission.submitted_at
            })
        return pd.DataFrame(data)