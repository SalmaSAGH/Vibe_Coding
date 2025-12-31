# Smart Agriculture Decision Support System

## 🌱 Overview

This project is a **Smart Agriculture Decision Support System** developed as part of a laboratory exercise on "Vibe Coding" - human-AI collaborative software development. The system provides farmers with actionable irrigation and fertilization recommendations based on IoT sensor data.

### Key Features

- 📊 **Real-time Sensor Monitoring**: Track soil moisture, temperature, and humidity
- 🤖 **AI-Powered Recommendations**: Get irrigation and fertilization advice
- 📈 **Historical Analysis**: Review trends and patterns over time
- ⚠️ **Alert System**: Receive warnings about critical conditions
- 🎯 **Explainable Decisions**: Understand the reasoning behind recommendations

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│         PRESENTATION LAYER (Streamlit)              │
│  - Dashboard UI                                     │
│  - Data Visualization                               │
└────────────────┬────────────────────────────────────┘
                 │ HTTP/REST
┌────────────────┴────────────────────────────────────┐
│           APPLICATION LAYER (FastAPI)               │
│  - API Endpoints                                    │
│  - Request Validation                               │
└────────────────┬────────────────────────────────────┘
                 │
┌────────────────┴────────────────────────────────────┐
│              BUSINESS LOGIC LAYER                   │
│  - Decision Engine (Strategy Pattern)               │
│  - Irrigation Strategy                              │
│  - Alert System                                     │
└────────────────┬────────────────────────────────────┘
                 │
┌────────────────┴────────────────────────────────────┐
│            DATA ACCESS LAYER                        │
│  - Repository Pattern                               │
│  - Data Service                                     │
└────────────────┬────────────────────────────────────┘
                 │
┌────────────────┴────────────────────────────────────┐
│           PERSISTENCE LAYER (SQLite)                │
│  - Sensor Data                                      │
│  - Recommendations History                          │
└─────────────────────────────────────────────────────┘
```

---

## 📋 Prerequisites

- Python 3.8+
- pip
- Virtual environment (recommended)

---

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd smart-agri-vibe-lab
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

**requirements.txt:**
```
fastapi==0.104.1
uvicorn[standard]==0.24.0
streamlit==1.28.1
pydantic==2.5.0
pydantic-settings==2.1.0
plotly==5.18.0
pandas==2.1.3
requests==2.31.0
python-dotenv==1.0.0
sqlalchemy==2.0.23
slowapi==0.1.9
pytest==7.4.3
httpx==0.25.1
```

### 4. Setup Environment Variables

Create a `.env` file in the project root:

```bash
# Database
DATABASE_URL=sqlite:///data/agri.db

# Security
API_KEYS=["dev-key-123","test-key-456"]
ALLOWED_ORIGINS=["http://localhost:8501"]

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/agri_system.log

# Agricultural Thresholds (Tomatoes)
SOIL_MOISTURE_CRITICAL=20.0
SOIL_MOISTURE_LOW=40.0
SOIL_MOISTURE_OPTIMAL_MIN=60.0
SOIL_MOISTURE_OPTIMAL_MAX=80.0
SOIL_MOISTURE_EXCESS=85.0

TEMP_OPTIMAL_MIN=15.0
TEMP_OPTIMAL_MAX=30.0
TEMP_HIGH=30.0
TEMP_EXTREME=35.0

HUMIDITY_LOW=40.0

# Plot Configuration
DEFAULT_PLOT_AREA_M2=100.0
ROOT_DEPTH_M=0.3
```

### 5. Initialize Database

```bash
python -c "from backend.database import init_db; init_db()"
```

---

## 🎮 Running the Application

### Start Backend API

```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: `http://localhost:8000`

API documentation (Swagger): `http://localhost:8000/docs`

### Start Frontend Dashboard

In a new terminal:

```bash
cd frontend
streamlit run app.py
```

The dashboard will open automatically at: `http://localhost:8501`

---

## 📡 API Usage

### Authentication

All API endpoints (except `/health`) require authentication via API key:

```bash
curl -H "X-API-Key: dev-key-123" http://localhost:8000/api/sensors/list
```

### Submit Sensor Data

```bash
curl -X POST http://localhost:8000/api/sensors/data \
  -H "Content-Type: application/json" \
  -H "X-API-Key: dev-key-123" \
  -d '{
    "sensor_id": "FIELD_A_01",
    "soil_moisture": 45.5,
    "temperature": 28.3,
    "humidity": 62.1
  }'
```

### Get Recommendations

```bash
curl -H "X-API-Key: dev-key-123" \
  http://localhost:8000/api/recommendations/FIELD_A_01
```

### Get Sensor History

```bash
curl -H "X-API-Key: dev-key-123" \
  "http://localhost:8000/api/sensors/history/FIELD_A_01?limit=50"
```

---

## 🧪 Testing

### Run Unit Tests

```bash
pytest tests/ -v
```

### Run Specific Test File

```bash
pytest tests/test_decision_engine.py -v
```

### Run with Coverage

```bash
pytest tests/ --cov=backend --cov-report=html
```

View coverage report: `open htmlcov/index.html`

---

## 📁 Project Structure

```
smart-agri-vibe-lab/
│
├── report/                          # Lab reports (Phases 1-7)
│   ├── phase1_vibe_coding.md
│   ├── phase2_architecture.md
│   ├── phase3_backend_review.md
│   ├── phase4_decision_logic.md
│   ├── phase5_frontend_ux.md
│   ├── phase6_refactoring.md
│   └── phase7_reflection.md
│
├── prompts/                         # AI prompts used
│   ├── architecture_prompt.txt
│   ├── backend_prompt.txt
│   ├── rules_prompt.txt
│   └── frontend_prompt.txt
│
├── backend/                         # FastAPI backend
│   ├── main.py                      # API entry point
│   ├── database.py                  # Database connection
│   ├── models.py                    # Data models
│   │
│   ├── config/
│   │   └── settings.py              # Configuration management
│   │
│   ├── middleware/
│   │   ├── auth.py                  # Authentication
│   │   └── error_handler.py         # Error handling
│   │
│   ├── services/
│   │   ├── decision_engine.py       # Main decision logic
│   │   ├── data_service.py          # Data access layer
│   │   ├── strategy_factory.py      # Strategy factory
│   │   │
│   │   └── strategies/
│   │       ├── irrigation_strategy.py
│   │       ├── alert_strategy.py
│   │       └── fertilization_strategy.py
│   │
│   ├── routers/                     # API route modules
│   │   ├── sensors.py
│   │   └── recommendations.py
│   │
│   └── utils/
│       └── logger.py                # Logging configuration
│
├── frontend/                        # Streamlit frontend
│   └── app.py                       # Dashboard application
│
├── tests/                           # Test suite
│   ├── test_decision_engine.py
│   ├── test_api_endpoints.py
│   ├── test_data_service.py
│   └── conftest.py                  # Test fixtures
│
├── data/                            # Data storage
│   └── agri.db                      # SQLite database
│
├── logs/                            # Application logs
│   └── agri_system.log
│
├── .env                             # Environment variables (not in git)
├── .env.example                     # Environment template
├── .gitignore                       # Git ignore rules
├── requirements.txt                 # Python dependencies
└── README.md                        # This file
```

---

## ⚙️ Configuration

### Crop-Specific Settings

To configure for different crops, modify `.env`:

**For Lettuce:**
```bash
SOIL_MOISTURE_LOW=50.0
SOIL_MOISTURE_OPTIMAL_MIN=70.0
SOIL_MOISTURE_OPTIMAL_MAX=85.0
```

**For Peppers:**
```bash
SOIL_MOISTURE_LOW=35.0
SOIL_MOISTURE_OPTIMAL_MIN=55.0
SOIL_MOISTURE_OPTIMAL_MAX=75.0
TEMP_EXTREME=38.0
```

### Adding New API Keys

```bash
# In .env
API_KEYS=["dev-key-123","prod-key-789","sensor-network-key-abc"]
```

### Changing Plot Size

```bash
# In .env
DEFAULT_PLOT_AREA_M2=250.0  # For 250m² plot
ROOT_DEPTH_M=0.5            # For deeper-rooted crops
```

---

## 🐛 Troubleshooting

### Database Issues

**Error**: `no such table: sensor_readings`

**Solution**: Reinitialize database:
```bash
rm data/agri.db
python -c "from backend.database import init_db; init_db()"
```

### API Authentication Fails

**Error**: `401 Unauthorized`

**Solution**: Check API key in `.env` and request header match:
```bash
echo $API_KEYS  # Should show your keys
```

### Frontend Can't Connect to Backend

**Error**: `Connection refused`

**Solution**: Ensure backend is running on port 8000:
```bash
# Check if backend is running
curl http://localhost:8000/health

# If not, start backend
cd backend && uvicorn main:app --reload
```

### Import Errors

**Error**: `ModuleNotFoundError: No module named 'fastapi'`

**Solution**: Install dependencies:
```bash
pip install -r requirements.txt
```

---

## 📊 Sample Data

### Generate Test Data

```python
import requests

API_KEY = "dev-key-123"
BASE_URL = "http://localhost:8000/api"

# Submit sample readings
data_points = [
    {"sensor_id": "FIELD_A_01", "soil_moisture": 45.0, "temperature": 25.0, "humidity": 60.0},
    {"sensor_id": "FIELD_A_01", "soil_moisture": 42.0, "temperature": 27.0, "humidity": 58.0},
    {"sensor_id": "FIELD_A_01", "soil_moisture": 38.0, "temperature": 30.0, "humidity": 55.0},
    {"sensor_id": "FIELD_B_01", "soil_moisture": 70.0, "temperature": 22.0, "humidity": 65.0},
]

for data in data_points:
    response = requests.post(
        f"{BASE_URL}/sensors/data",
        json=data,
        headers={"X-API-Key": API_KEY}
    )
    print(f"Status: {response.status_code}, Data: {response.json()}")
```

---

## 🔒 Security Considerations

### Production Deployment Checklist

- [ ] **Change default API keys** in `.env`
- [ ] **Restrict CORS origins** to your domain only
- [ ] **Enable HTTPS** (use nginx/traefik as reverse proxy)
- [ ] **Set up rate limiting** (already configured via slowapi)
- [ ] **Regular security audits** of dependencies
- [ ] **Monitor logs** for suspicious activity
- [ ] **Backup database** regularly
- [ ] **Implement user authentication** (currently only API key auth)

### Environment Variables Security

Never commit `.env` file to git:

```bash
# .gitignore
.env
*.db
logs/
__pycache__/
```

---

## 📚 Documentation

### API Documentation

Once backend is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Decision Logic Documentation

See `report/phase4_decision_logic.md` for detailed explanation of irrigation and fertilization algorithms.

### Architecture Documentation

See `report/phase2_architecture.md` for system design rationale.

---

## 🤝 Contributing

This is a laboratory project, but improvements are welcome:

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

### Code Style

- Follow PEP 8 for Python code
- Use type hints
- Write docstrings for all functions
- Add tests for new features

---

## 📝 License

This project is for educational purposes. License: MIT

---

## 👥 Authors

- **Student Name** - ASEDS INE3
- **Instructor** - Software Engineering Course

---

## 🙏 Acknowledgments

- UC Davis Agricultural Guidelines
- FAO Irrigation Manual
- Anthropic Claude (AI assistance for vibe coding)
- FastAPI and Streamlit communities

---

## 📞 Support

For issues or questions:
- Open an issue on GitHub
- Contact: [your-email@example.com]
- Lab TA Office Hours: [time/location]

---

## 📈 Roadmap

### Phase 8 (Future Work)

- [ ] Weather API integration
- [ ] Multi-crop support
- [ ] Mobile app (React Native)
- [ ] Machine learning for personalized recommendations
- [ ] IoT sensor integration (MQTT)
- [ ] Multi-language support (Arabic, French)
- [ ] Farmer community features
- [ ] Crop yield prediction
- [ ] Pest detection via image recognition

---

**Built with ❤️ and 🤖 through Vibe Coding**
