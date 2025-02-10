# Performance thresholds
WEAK_PERFORMANCE_THRESHOLD = 0.4  # 40%
AVERAGE_PERFORMANCE_THRESHOLD = 0.6  # 60%
GOOD_PERFORMANCE_THRESHOLD = 0.75  # 75%

# Topic categories
NEET_TOPICS = [
    "Human Physiology",
    "Body Fluids and Circulation",
    "Reproduction",
    "Reproductive Health",
    "Principles of Inheritance and Variation",
    "Microbes in Human Welfare",
    "Human Health and Disease",
    "Structural Organisation in Animals"
]

# College cutoff ranks (sample data)
COLLEGE_CUTOFFS = {
    "AIIMS New Delhi": 50,
    "JIPMER Puducherry": 200,
    "CMC Vellore": 500,
    "AFMC Pune": 1000,
    "Maulana Azad Medical College": 2000
}

# Performance improvement thresholds
SIGNIFICANT_IMPROVEMENT = 0.1  # 10%
MODERATE_IMPROVEMENT = 0.05  # 5%

# Time-based analysis constants
RECENT_ACTIVITY_DAYS = 30
TREND_ANALYSIS_MINIMUM_QUIZZES = 5

# Model parameters
FEATURE_WEIGHTS = {
    'accuracy': 0.4,
    'consistency': 0.2,
    'improvement': 0.2,
    'topic_coverage': 0.2
}