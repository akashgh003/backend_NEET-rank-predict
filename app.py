import os
import sys
from pathlib import Path
import logging
from typing import Dict, List, Any, Optional, Union
import uvicorn
from fastapi import FastAPI, HTTPException, Path as PathParam
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from pydantic import BaseModel, Field
from datetime import datetime

# Add project root to Python path
PROJECT_ROOT = Path(__file__).parent
sys.path.append(str(PROJECT_ROOT))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import project modules
from src.data.quiz_client import QuizClient
from src.data.data_processor import DataProcessor
from src.analysis.performance import PerformanceAnalyzer
from src.analysis.insights import InsightGenerator
from src.models.predictor import RankPredictor
from src.visualization.charts import ChartGenerator

# Define response models
class DifficultyAnalysis(BaseModel):
    easy: float = Field(..., ge=0, le=100, description="Accuracy percentage for easy questions")
    medium: float = Field(..., ge=0, le=100, description="Accuracy percentage for medium questions")
    hard: float = Field(..., ge=0, le=100, description="Accuracy percentage for hard questions")

class DataPoint(BaseModel):
    date: str
    value: float
    label: str

class PerformanceData(BaseModel):
    labels: List[str]
    datasets: List[Dict[str, Union[str, List[float]]]]
    title: str

class QuizAnalysisResponse(BaseModel):
    user_id: str
    topic_wise_accuracy: Dict[str, float]
    difficulty_analysis: Dict[str, DifficultyAnalysis]
    weak_areas: List[str]
    improvement_trends: Dict[str, List[float]]

class TopicInsight(BaseModel):
    score: float = Field(..., ge=0, le=100)
    status: str
    recommendations: List[str]

class InsightResponse(BaseModel):
    overall_statistics: Dict[str, Union[float, str]]
    topic_insights: Dict[str, Dict[str, Union[float, str, List[str]]]]
    weak_areas: List[Dict[str, str]]
    recommendations: List[Dict[str, str]]
    uncovered_topics: List[str]

class CollegePrediction(BaseModel):
    name: str
    probability: float = Field(..., ge=0, le=1)
    cutoff_range: str

class RankPredictionResponse(BaseModel):
    user_id: str
    predicted_rank: int = Field(..., ge=1)
    rank_range: str
    confidence_score: float = Field(..., ge=0, le=1)
    recommended_colleges: List[CollegePrediction]

class ChartAxis(BaseModel):
    label: str = Field(..., description="Axis label")
    dataKey: Optional[str] = Field(None, description="Data key for the axis")
    domain: Optional[List[float]] = Field(None, description="Value range [min, max]")
    
class ChartSeries(BaseModel):
    name: str = Field(..., description="Series name")
    dataKey: str = Field(..., description="Data key for the series")
    color: str = Field(..., description="Color for the series")

class ChartTooltip(BaseModel):
    enabled: bool = True
    fields: List[str]

class Chart(BaseModel):
    type: str = Field(..., description="Type of chart (line, bar, etc.)")
    title: str = Field(..., description="Chart title")
    data: List[Dict[str, Any]] = Field(..., description="Chart data points")
    axes: Dict[str, ChartAxis] = Field(..., description="Axis configurations")
    series: List[ChartSeries] = Field(..., description="Series configurations")

class VisualizationResponse(BaseModel):
    overall_performance: Dict[str, Any] = Field(..., description="Overall performance trend")
    topic_wise_scores: Dict[str, Any] = Field(..., description="Scores by subject")
    weak_areas: Dict[str, Any] = Field(..., description="Areas needing improvement")
    difficulty_analysis: Dict[str, Any] = Field(..., description="Performance by difficulty")
    improvement_trends: Dict[str, Any] = Field(..., description="Progress over time")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle manager for the FastAPI application."""
    logger.info("Starting NEET Rank Predictor API")
    
    # Verify data files exist
    data_path = Path("src/data/mock")
    required_files = ["api_endpoint.json", "quiz_submission.json", "quiz_endpoint.json"]
    
    for file in required_files:
        if not (data_path / file).exists():
            logger.error(f"Required file {file} not found in {data_path}")
            sys.exit(1)
    
    logger.info("All required files found")
    yield
    logger.info("Shutting down NEET Rank Predictor API")

app = FastAPI(
    title="NEET Rank Predictor",
    description="""
    API for analyzing student performance and predicting NEET ranks.
    
    Features:
    - Performance Analysis by Topics and Difficulty Levels
    - Insight Generation and Recommendations
    - Rank Prediction and College Suggestions
    - Performance Visualizations
    """,
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
try:
    quiz_client = QuizClient()
    data_processor = DataProcessor()
    performance_analyzer = PerformanceAnalyzer()
    insight_generator = InsightGenerator()
    rank_predictor = RankPredictor()
    chart_generator = ChartGenerator()
except Exception as e:
    logger.error(f"Error initializing components: {str(e)}")
    sys.exit(1)

@app.get("/",
         description="Root endpoint with API information")
async def root():
    """Root endpoint returning API information."""
    return {
        "name": "NEET Rank Predictor API",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat(),
        "endpoints": [
            "/analysis/{user_id}",
            "/insights/{user_id}",
            "/predictions/{user_id}",
            "/visualizations/{user_id}",
            "/summary/{user_id}"
        ]
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "components": {
            "quiz_client": "ok",
            "data_processor": "ok",
            "performance_analyzer": "ok",
            "rank_predictor": "ok",
            "chart_generator": "ok"
        }
    }

@app.get("/analysis/{user_id}",
         response_model=QuizAnalysisResponse)
async def analyze_performance(user_id: str):
    """Analyze student performance based on quiz history."""
    try:
        logger.info(f"Analyzing performance for user {user_id}")
        
        quiz_history = await quiz_client.get_historical_quiz_data(user_id)
        current_quiz = await quiz_client.get_current_quiz_submission(user_id)
        
        if not quiz_history and not current_quiz:
            logger.warning(f"No quiz data found for user {user_id}")
            raise HTTPException(status_code=404, detail="No quiz data found for user")
        
        processed_history = data_processor.process_historical_data(quiz_history)
        if current_quiz:
            processed_current = data_processor.preprocess_quiz_submission(current_quiz)
            processed_history.append(processed_current)
        
        performance = performance_analyzer.analyze_student_performance(processed_history)
        
        # Convert all values to ensure JSON serialization
        response_data = {
            "user_id": str(user_id),
            "topic_wise_accuracy": {
                str(topic): float(accuracy)
                for topic, accuracy in performance.topic_wise_accuracy.items()
            },
            "difficulty_analysis": {
                str(topic): {
                    "easy": float(analysis.easy),
                    "medium": float(analysis.medium),
                    "hard": float(analysis.hard)
                }
                for topic, analysis in performance.difficulty_analysis.items()
            },
            "weak_areas": [str(area) for area in performance.weak_areas],
            "improvement_trends": {
                str(topic): [float(score) for score in scores]
                for topic, scores in performance.improvement_trends.items()
            }
        }
        
        return JSONResponse(content=response_data)
        
    except Exception as e:
        logger.error(f"Error analyzing performance for user {user_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/insights/{user_id}",
         response_model=InsightResponse)
async def get_insights(user_id: str):
    """Generate insights and recommendations."""
    try:
        logger.info(f"Generating insights for user {user_id}")
        
        quiz_history = await quiz_client.get_historical_quiz_data(user_id)
        if not quiz_history:
            raise HTTPException(status_code=404, detail="No quiz history found for user")
        
        processed_history = data_processor.process_historical_data(quiz_history)
        raw_report = insight_generator.generate_comprehensive_report(processed_history)
        
        # Convert values to ensure JSON serialization
        report = {
            "overall_statistics": {
                k: float(v) if isinstance(v, (int, float)) else str(v)
                for k, v in raw_report["overall_statistics"].items()
            },
            "topic_insights": {
                str(topic): {
                    "score": float(data["score"]),
                    "status": str(data["status"]),
                    "recommendations": [str(r) for r in data["recommendations"]]
                }
                for topic, data in raw_report["topic_insights"].items()
            },
            "weak_areas": [
                {k: str(v) for k, v in area.items()}
                for area in raw_report["weak_areas"]
            ],
            "recommendations": [
                {k: str(v) for k, v in rec.items()}
                for rec in raw_report["recommendations"]
            ],
            "uncovered_topics": [str(topic) for topic in raw_report["uncovered_topics"]]
        }
        
        return JSONResponse(content=report)
        
    except Exception as e:
        logger.error(f"Error generating insights for user {user_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/predictions/{user_id}",
         response_model=RankPredictionResponse)
async def predict_rank(user_id: str):
    """Predict NEET rank and recommend colleges."""
    try:
        logger.info(f"Predicting rank for user {user_id}")
        
        quiz_history = await quiz_client.get_historical_quiz_data(user_id)
        if not quiz_history:
            raise HTTPException(status_code=404, detail="No quiz history found for user")
        
        processed_history = data_processor.process_historical_data(quiz_history)
        performance = performance_analyzer.analyze_student_performance(processed_history)
        
        predicted_rank = rank_predictor.predict_rank(performance)
        recommended_colleges = rank_predictor.predict_colleges(predicted_rank)
        
        response_data = {
            "user_id": str(user_id),
            "predicted_rank": int(predicted_rank),
            "rank_range": f"{predicted_rank-500} to {predicted_rank+500}",
            "confidence_score": float(0.85),
            "recommended_colleges": [
                {
                    "name": str(college),
                    "probability": float(0.9 - (idx * 0.1)),
                    "cutoff_range": f"≤ {predicted_rank + (idx * 1000)}"
                }
                for idx, college in enumerate(recommended_colleges)
            ]
        }
        
        return JSONResponse(content=response_data)
        
    except Exception as e:
        logger.error(f"Error predicting rank for user {user_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/visualizations/{user_id}",
         response_model=VisualizationResponse,
         tags=["Progress Tracking"],
         summary="View Your Performance Charts",
         description="Get visual representations of your performance and progress")
async def get_visualizations(
    user_id: str = Path(..., description="Your student ID")
):
    """Generate visual representations of student performance."""
    try:
        logger.info(f"Generating visualizations for student {user_id}")
        
        # Fetch quiz data
        quiz_history = await quiz_client.get_historical_quiz_data(user_id)
        current_quiz = await quiz_client.get_current_quiz_submission(user_id)
        
        if not quiz_history and not current_quiz:
            raise HTTPException(
                status_code=404,
                detail="No quiz data found. Please complete at least one quiz first."
            )
        
        if current_quiz:
            quiz_history.append(current_quiz)
            
        processed_history = data_processor.process_historical_data(quiz_history)
        performance = performance_analyzer.analyze_student_performance(processed_history)
        
        # Generate visualization data
        charts = {
            "performance_trend_chart": chart_generator.generate_performance_trend(quiz_history),
            "topic_performance_chart": chart_generator.generate_topic_performance(
                performance.topic_wise_accuracy
            ),
            "weak_areas_chart": chart_generator.generate_weak_areas_chart(
                {topic: acc for topic, acc in performance.topic_wise_accuracy.items() 
                 if topic in performance.weak_areas}
            ),
            "improvement_trends_chart": chart_generator.generate_improvement_chart(
                performance.improvement_trends
            ),
            "difficulty_distribution_chart": {
                'type': 'bar',
                'data': [],  # We'll calculate this from quiz_history
                'axes': {
                    'x': {'label': 'Difficulty Level', 'dataKey': 'difficulty'},
                    'y': {'label': 'Questions Count'}
                },
                'series': [
                    {'name': 'Total Questions', 'dataKey': 'total', 'color': '#64748b'},
                    {'name': 'Correct Answers', 'dataKey': 'correct', 'color': '#2563eb'}
                ]
            }
        }
        
        # Calculate difficulty distribution data
        difficulty_stats = {
            'Easy': {'total': 0, 'correct': 0},
            'Medium': {'total': 0, 'correct': 0},
            'Hard': {'total': 0, 'correct': 0}
        }
        
        for quiz in quiz_history:
            for question in quiz['questions']:
                level = question['difficulty']
                difficulty_stats[level]['total'] += 1
                if question['is_correct']:
                    difficulty_stats[level]['correct'] += 1
        
        charts['difficulty_distribution_chart']['data'] = [
            {
                'difficulty': level,
                'total': stats['total'],
                'correct': stats['correct'],
                'accuracy': round((stats['correct'] / stats['total'] * 100), 2) if stats['total'] > 0 else 0
            }
            for level, stats in difficulty_stats.items()
        ]
        
        # Ensure all numeric values are properly formatted
        for chart in charts.values():
            chart['data'] = [
                {k: (round(v, 2) if isinstance(v, float) else v) 
                 for k, v in item.items()}
                for item in chart['data']
            ]
        
        return JSONResponse(content=charts)
        
    except Exception as e:
        logger.error(f"Error generating visualizations: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Could not generate visualizations. Please try again."
        )
@app.get("/summary/{user_id}")
async def get_summary(user_id: str):
    """Get a comprehensive summary of student performance and predictions."""
    try:
        logger.info(f"Generating summary for user {user_id}")
        
        analysis = await analyze_performance(user_id)
        insights = await get_insights(user_id)
        predictions = await predict_rank(user_id)
        visualizations = await get_visualizations(user_id)
        
        return JSONResponse(content={
            "analysis": analysis,
            "insights": insights,
            "predictions": predictions,
            "visualizations": visualizations,
            "generated_at": datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error generating summary for user {user_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000,
        log_level="info"
    )