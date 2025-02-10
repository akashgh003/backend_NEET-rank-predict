from typing import List, Optional, Tuple
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from src.models.student import StudentPerformance, QuizSubmission

class RankPredictor:
    def __init__(self):
        """Initialize the rank predictor with a machine learning model."""
        self.model = RandomForestRegressor(
            n_estimators=100,
            random_state=42
        )
        self.is_trained = False

    def _extract_features(self, performance: StudentPerformance) -> np.ndarray:
        """Extract features from student performance data."""
        features = []
        
        # Average accuracy across all topics
        avg_accuracy = np.mean(list(performance.topic_wise_accuracy.values()))
        features.append(avg_accuracy)
        
        # Number of weak areas
        features.append(len(performance.weak_areas))
        
        # Average improvement trend
        avg_improvement = np.mean([
            trend[-1] - trend[0] 
            for trend in performance.improvement_trends.values()
            if len(trend) > 1
        ])
        features.append(avg_improvement)
        
        # Latest quiz score
        latest_quiz = max(performance.quiz_history, key=lambda x: x.submitted_at)
        features.append(float(latest_quiz.final_score))
        
        return np.array(features).reshape(1, -1)

    def train(self, 
             training_data: List[Tuple[StudentPerformance, int]]) -> None:
        """Train the model using historical data."""
        X = np.vstack([
            self._extract_features(perf) 
            for perf, _ in training_data
        ])
        y = np.array([rank for _, rank in training_data])
        
        self.model.fit(X, y)
        self.is_trained = True

    def predict_rank(self, performance: StudentPerformance) -> int:
        """Predict NEET rank based on student performance."""
        if not self.is_trained:
            # Return a dummy prediction for testing
            return 5000
            
        features = self._extract_features(performance)
        predicted_rank = self.model.predict(features)[0]
        
        return int(predicted_rank)

    def predict_colleges(self, predicted_rank: int) -> List[str]:
        """Predict potential colleges based on predicted rank."""
        # This would require a database of colleges and their previous year cutoffs
        # For now, return a placeholder
        return [
            "All India Institute of Medical Sciences",
            "Christian Medical College",
            "Armed Forces Medical College"
        ]