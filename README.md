# NEET Rank Predictor Backend 🚀

A powerful backend system for analyzing NEET exam performance and predicting ranks based on quiz history. 📊

![API Documentation](https://github.com/akashgh003/backend_NEET-rank-predict/blob/main/Screenshot_10-2-2025_23427_localhost.jpeg)

## Features ⭐

- **Performance Analysis** 📈
  - Topic-wise performance tracking
  - Difficulty level analysis
  - Progress monitoring
  - Weak area identification

- **Intelligent Insights** 🧠
  - Personalized recommendations
  - Study pattern analysis
  - Improvement suggestions
  - Performance trends

- **Rank Prediction** 🎯
  - AI-powered rank prediction
  - College admission chances
  - Cutoff analysis
  - Performance benchmarking

## Tech Stack 🛠️

- **Framework:** FastAPI 🚅
- **Language:** Python 3.9+ 🐍
- **Data Processing:** Pandas, NumPy 📊
- **Visualization:** Chart.js data formats 📉
- **Documentation:** Swagger UI / OpenAPI 📚
- **Testing:** pytest 🧪
- **Development:** uvicorn 🦄

## Project Structure 📁

```
neet-rank-predictor/
├── src/
│   ├── analysis/
│   │   ├── insights.py
│   │   └── performance.py
│   ├── data/
│   │   ├── quiz_client.py
│   │   └── data_processor.py
│   ├── models/
│   │   ├── predictor.py
│   │   └── student.py
│   └── visualization/
│       └── charts.py
├── tests/
├── app.py
└── requirements.txt
```

## Setup and Installation 🚀

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/neet-rank-predictor.git
   cd neet-rank-predictor
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the API documentation**
   - Open [http://localhost:8000/docs](http://localhost:8000/docs) in your browser
   - Interactive API documentation will be available

## API Endpoints 🌐

### Student Reports 📋
- `GET /student-report/{user_id}`
  - Complete performance analysis
  - Study recommendations
  - Rank predictions

### Progress Tracking 📈
- `GET /visualizations/{user_id}`
  - Performance trend charts
  - Topic-wise analysis
  - Difficulty distribution

### College Predictions 🎓
- `GET /predictions/{user_id}`
  - NEET rank prediction
  - College admission chances
  - Cutoff analysis

## Sample Usage 💻

```python
# Example: Get student performance report
import requests

api_url = "http://localhost:8000"
user_id = "student123"

# Get complete analysis
response = requests.get(f"{api_url}/student-report/{user_id}")
analysis = response.json()

# Get visualizations
viz_response = requests.get(f"{api_url}/visualizations/{user_id}")
charts = viz_response.json()

print(f"Student Performance Report for {user_id}")
print(f"Overall Score: {analysis['overview']['average_score']}%")
print(f"Predicted Rank Range: {analysis['predicted_rank_range']}")
```

## Contributing 🤝

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Testing 🧪

Run the test suite:
```bash
pytest tests/
```


## Acknowledgments 🙏

- NEET exam pattern and scoring system
- Historical NEET rank data
- Educational analytics research

## Contact 📧

GitHub ID - [@akashgh003](https://github.com/akashgh003)

Project Link: [https://github.com/yourusername/neet-rank-predictor](https://github.com/yourusername/neet-rank-predictor)

---

⭐ Star this repository if you find it helpful!
