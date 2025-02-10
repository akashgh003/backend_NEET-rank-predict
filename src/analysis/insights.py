from typing import Dict, List, Optional, Union, Any
import pandas as pd
import numpy as np
from datetime import datetime
import logging
import json
from src.models.student import QuizSubmission
from src.utils.constants import (
    WEAK_PERFORMANCE_THRESHOLD,
    AVERAGE_PERFORMANCE_THRESHOLD,
    GOOD_PERFORMANCE_THRESHOLD,
    NEET_TOPICS
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class InsightGenerator:
    def __init__(self):
        self.improvement_threshold = 0.1
        self.min_quizzes_for_trend = 3

    def _serialize_value(self, value: Any) -> Union[str, float, int, List, Dict]:
        """Helper method to ensure values are JSON serializable."""
        if isinstance(value, (np.int_, np.int32, np.int64)):
            return int(value)
        elif isinstance(value, (np.float_, np.float32, np.float64)):
            return float(value)
        elif isinstance(value, bool):
            return str(value)
        elif isinstance(value, (list, tuple)):
            return [self._serialize_value(item) for item in value]
        elif isinstance(value, dict):
            return {str(k): self._serialize_value(v) for k, v in value.items()}
        elif isinstance(value, np.ndarray):
            return [self._serialize_value(item) for item in value.tolist()]
        elif pd.isna(value):
            return None
        else:
            return str(value)

    def _safe_process(self, func, *args, **kwargs):
        """Wrapper to safely process and serialize data."""
        try:
            result = func(*args, **kwargs)
            return self._serialize_value(result)
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {str(e)}")
            raise

    def generate_comprehensive_report(self, quiz_history: List[QuizSubmission]) -> Dict[str, Any]:
        """Generate a comprehensive performance report."""
        try:
            logger.info("Starting comprehensive report generation")
            
            if not quiz_history:
                logger.warning("No quiz history provided")
                return {
                    'error': 'No quiz history available',
                    'generated_at': datetime.now().isoformat()
                }

            # Process quiz history data
            accuracies = []
            processed_quizzes = []
            
            for quiz in quiz_history:
                try:
                    accuracy = float(quiz.accuracy.strip('%')) / 100
                    accuracies.append(accuracy)
                    processed_quizzes.append({
                        'topic': str(quiz.topic),
                        'accuracy': accuracy,
                        'score': float(quiz.final_score),
                        'date': str(quiz.submitted_at)
                    })
                except Exception as e:
                    logger.error(f"Error processing quiz: {str(e)}")
                    continue

            # Calculate overall statistics
            stats = {
                'average_accuracy': round(float(np.mean(accuracies)) * 100, 2),
                'total_quizzes': len(processed_quizzes),
                'unique_topics': len(set(q['topic'] for q in processed_quizzes))
            }
            logger.info(f"Calculated overall statistics: {stats}")

            # Process topics
            topic_stats = {}
            for quiz in processed_quizzes:
                topic = quiz['topic']
                if topic not in topic_stats:
                    topic_stats[topic] = {
                        'accuracies': [],
                        'scores': []
                    }
                topic_stats[topic]['accuracies'].append(quiz['accuracy'])
                topic_stats[topic]['scores'].append(quiz['score'])

            # Generate topic insights
            topic_insights = {}
            for topic, data in topic_stats.items():
                avg_accuracy = float(np.mean(data['accuracies']))
                topic_insights[str(topic)] = {
                    'score': round(avg_accuracy * 100, 2),
                    'status': self._categorize_performance(avg_accuracy),
                    'recommendations': [
                        f"Focus on {topic} fundamentals" if avg_accuracy < 0.6 else
                        f"Practice more {topic} problems" if avg_accuracy < 0.8 else
                        f"Maintain performance in {topic}"
                    ]
                }
            logger.info("Generated topic insights")

            # Identify weak areas
            weak_areas = []
            for topic, data in topic_insights.items():
                if data['score'] < 70:  # Below 70%
                    weak_areas.append({
                        'topic': str(topic),
                        'current_score': str(f"{data['score']}%"),
                        'priority': 'High' if data['score'] < 60 else 'Medium'
                    })
            logger.info(f"Identified {len(weak_areas)} weak areas")

            # Prepare final report
            report = {
                'overall_statistics': {
                    'average_accuracy': stats['average_accuracy'],
                    'total_quizzes': stats['total_quizzes'],
                    'topics_covered': stats['unique_topics'],
                    'topics_needing_improvement': len(weak_areas)
                },
                'topic_insights': topic_insights,
                'weak_areas': weak_areas,
                'recommendations': [
                    {
                        'area': str(area['topic']),
                        'action': f"Intensive practice needed in {area['topic']}",
                        'priority': str(area['priority'])
                    }
                    for area in weak_areas
                ],
                'uncovered_topics': [
                    str(topic) for topic in NEET_TOPICS 
                    if topic not in topic_insights
                ],
                'generated_at': datetime.now().isoformat()
            }

            # Verify JSON serialization
            try:
                json.dumps(report)
                logger.info("Successfully verified JSON serialization")
                return report
            except TypeError as e:
                logger.error(f"JSON serialization error: {str(e)}")
                # If serialization fails, apply serialization to all values
                return self._serialize_value(report)

        except Exception as e:
            logger.error(f"Error generating comprehensive report: {str(e)}")
            return {
                'error': str(e),
                'generated_at': datetime.now().isoformat()
            }