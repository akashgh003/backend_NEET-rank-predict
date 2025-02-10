from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from typing import List, Dict

from data.quiz_client import QuizClient
from analysis.performance import PerformanceAnalyzer
from models.predictor import RankPredictor
from models.student import StudentPerformance

app = FastAPI(title="NEET Rank Predictor API")

# Initialize components
quiz_client = QuizClient()
analyzer = PerformanceAnalyzer()
predictor = RankPredictor()

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

@app.get("/analysis/{user_id}")
async def analyze_performance(user_id: str):
    """Analyze student performance and predict rank."""
    try:
        # Fetch quiz data
        quiz_history = await quiz_client.get_historical_quiz_data(user_id)
        current_quiz = await quiz_client.get_current_quiz_submission(user_id)
        
        if current_quiz:
            quiz_history.append(current_quiz)
            
        if not quiz_history:
            raise HTTPException(status_code=404, detail="No quiz data found")
            
        # Analyze performance
        performance = analyzer.analyze_student_performance(quiz_history)
        
        # Predict rank
        predicted_rank = predictor.predict_rank(performance)
        performance.predicted_rank = predicted_rank
        
        # Predict colleges
        recommended_colleges = predictor.predict_colleges(predicted_rank)
        performance.recommended_colleges = recommended_colleges
        
        return JSONResponse(content={
            "user_id": user_id,
            "topic_wise_accuracy": performance.topic_wise_accuracy,
            "weak_areas": performance.weak_areas,
            "improvement_trends": performance.improvement_trends,
            "predicted_rank": performance.predicted_rank,
            "recommended_colleges": performance.recommended_colleges
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/visualization/{user_id}")
async def get_performance_visualization(user_id: str):
    """Generate performance visualizations."""
    # This would be implemented using a visualization library
    pass