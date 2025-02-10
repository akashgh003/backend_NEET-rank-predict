import json
import os
from typing import Dict, List, Optional

class QuizClient:
    def __init__(self, data_dir: str = "src/data/mock"):
        """Initialize the quiz client with the data directory path."""
        self.data_dir = data_dir

    async def get_historical_quiz_data(self, user_id: str) -> List[Dict]:
        """Fetch historical quiz data for a user."""
        file_path = os.path.join(self.data_dir, "api_endpoint.json")
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            return [quiz for quiz in data if quiz['user_id'] == user_id]
        except FileNotFoundError:
            return []

    async def get_current_quiz_submission(self, user_id: str) -> Optional[Dict]:
        """Fetch the most recent quiz submission for a user."""
        file_path = os.path.join(self.data_dir, "quiz_submission.json")
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            return data if data['user_id'] == user_id else None
        except FileNotFoundError:
            return None

    async def get_quiz_details(self, quiz_id: int) -> Optional[Dict]:
        """Fetch quiz details including questions and options."""
        file_path = os.path.join(self.data_dir, "quiz_endpoint.json")
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            return data['quiz'] if data['quiz']['id'] == quiz_id else None
        except FileNotFoundError:
            return None

    def parse_response_map(self, response_map: Dict) -> List[Dict]:
        """Parse the response map into a list of question-answer pairs."""
        return [
            {
                'question_id': int(q_id), 
                'selected_option_id': opt_id
            } 
            for q_id, opt_id in response_map.items()
        ]

__all__ = ['QuizClient']