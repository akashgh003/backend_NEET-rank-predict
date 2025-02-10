from typing import List, Dict, Any
import pandas as pd
from datetime import datetime

class ChartGenerator:
    def __init__(self):
        self.colors = {
            'primary': '#2563eb',
            'secondary': '#16a34a',
            'error': '#ef4444',
            'neutral': '#64748b'
        }

    def generate_performance_trend(self, quiz_history: List[Dict]) -> Dict[str, Any]:
        """Generate performance trend data."""
        trend_data = []
        
        for quiz in quiz_history:
            trend_data.append({
                'date': quiz['submitted_at'],
                'accuracy': round(float(quiz['accuracy'].strip('%')), 2),
                'score': round(float(quiz['final_score']), 2)
            })
        
        # Sort by date
        trend_data.sort(key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d'))
        
        return {
            'data': trend_data,
            'axes': {
                'x': {'label': 'Quiz Date', 'dataKey': 'date'},
                'y': {'label': 'Score/Accuracy (%)', 'domain': [0, 100]}
            },
            'series': [
                {'name': 'Accuracy', 'dataKey': 'accuracy', 'color': self.colors['primary']},
                {'name': 'Score', 'dataKey': 'score', 'color': self.colors['secondary']}
            ]
        }

    def generate_topic_performance(self, topic_data: Dict[str, float]) -> Dict[str, Any]:
        """Generate topic-wise performance data."""
        chart_data = [
            {
                'topic': topic,
                'accuracy': round(acc * 100, 2),
                'status': 'Good' if acc >= 0.7 else 'Needs Improvement'
            }
            for topic, acc in topic_data.items()
        ]
        
        # Sort by accuracy descending
        chart_data.sort(key=lambda x: x['accuracy'], reverse=True)
        
        return {
            'data': chart_data,
            'axes': {
                'x': {'label': 'Subjects', 'dataKey': 'topic'},
                'y': {'label': 'Accuracy (%)', 'domain': [0, 100]}
            },
            'series': [
                {'name': 'Current Performance', 'dataKey': 'accuracy', 'color': self.colors['primary']}
            ]
        }

    def generate_weak_areas_chart(self, weak_areas_data: Dict[str, float]) -> Dict[str, Any]:
        """Generate weak areas data."""
        chart_data = [
            {
                'topic': topic,
                'accuracy': round(acc * 100, 2),
                'gap': round((70 - acc * 100), 2),  # Gap to reach 70%
                'status': 'Critical' if acc < 0.6 else 'Needs Work'
            }
            for topic, acc in weak_areas_data.items()
        ]
        
        # Sort by accuracy ascending
        chart_data.sort(key=lambda x: x['accuracy'])
        
        return {
            'data': chart_data,
            'axes': {
                'x': {'label': 'Current Score (%)', 'domain': [0, 100]},
                'y': {'label': 'Subjects', 'dataKey': 'topic'}
            },
            'series': [
                {'name': 'Current Score', 'dataKey': 'accuracy', 'color': self.colors['error']}
            ]
        }

    def generate_improvement_chart(self, improvement_data: Dict[str, List[float]]) -> Dict[str, Any]:
        """Generate improvement trends data."""
        chart_data = []
        quiz_numbers = range(1, len(next(iter(improvement_data.values()))) + 1)
        
        for quiz_num in quiz_numbers:
            data_point = {'quiz': f'Quiz {quiz_num}'}
            for topic, scores in improvement_data.items():
                data_point[topic] = round(scores[quiz_num - 1] * 100, 2)
            chart_data.append(data_point)
        
        return {
            'data': chart_data,
            'axes': {
                'x': {'label': 'Quiz Number', 'dataKey': 'quiz'},
                'y': {'label': 'Score (%)', 'domain': [0, 100]}
            },
            'series': [
                {'name': topic, 'dataKey': topic, 'color': f'hsl({i * 45}, 70%, 50%)'}
                for i, topic in enumerate(improvement_data.keys())
            ]
        }

    def generate_difficulty_distribution(self, quiz_data: List[Dict]) -> Dict[str, Any]:
        """Generate difficulty distribution data."""
        stats = {
            'Easy': {'total': 0, 'correct': 0},
            'Medium': {'total': 0, 'correct': 0},
            'Hard': {'total': 0, 'correct': 0}
        }
        
        for quiz in quiz_data:
            for question in quiz['questions']:
                level = question['difficulty']
                stats[level]['total'] += 1
                if question['is_correct']:
                    stats[level]['correct'] += 1
        
        chart_data = [
            {
                'level': level,
                'total': data['total'],
                'correct': data['correct'],
                'accuracy': round((data['correct'] / data['total'] * 100), 2) if data['total'] > 0 else 0
            }
            for level, data in stats.items()
        ]
        
        return {
            'data': chart_data,
            'axes': {
                'x': {'label': 'Difficulty Level', 'dataKey': 'level'},
                'y': {'label': 'Number of Questions'}
            },
            'series': [
                {'name': 'Total Questions', 'dataKey': 'total', 'color': self.colors['neutral']},
                {'name': 'Correct Answers', 'dataKey': 'correct', 'color': self.colors['primary']}
            ]
        }