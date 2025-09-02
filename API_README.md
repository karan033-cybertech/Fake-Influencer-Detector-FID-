# Fake Influencer Detector - FastAPI Backend

A FastAPI-based REST API for the Fake Influencer Detector that analyzes investment text for potential risk indicators.

## 🚀 Features

- **RESTful API**: Clean, modern API design with FastAPI
- **Model Integration**: Loads and uses the trained `model.pkl` file
- **Risk Scoring**: Calculates risk scores from 0-100 based on multiple factors
- **Word Detection**: Identifies potentially risky keywords in text
- **Real-time Analysis**: Fast text processing and analysis
- **Comprehensive Response**: Returns detailed analysis including confidence scores
- **Health Monitoring**: Built-in health check endpoints
- **Interactive Documentation**: Auto-generated API docs with Swagger UI

## 📋 Requirements

- Python 3.7+
- FastAPI
- Uvicorn (ASGI server)
- scikit-learn
- pandas
- numpy
- pydantic

## 🛠️ Installation

1. **Install API dependencies:**
   ```bash
   pip install -r requirements_api.txt
   ```

2. **Ensure the model file exists:**
   - Run `python fake_influencer_detector.py` first to generate `model.pkl`
   - The API will automatically load this model on startup

## 🚀 Quick Start

### 1. Start the API Server

```bash
python api.py
```

The server will start on `http://localhost:8000`

### 2. Access API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### 3. Test the API

```bash
python test_api.py
```

## 📡 API Endpoints

### Root Endpoint
```
GET /
```
Returns API information and available endpoints.

### Health Check
```
GET /health
```
Returns API health status and model loading status.

### Model Information
```
GET /model_info
```
Returns details about the loaded machine learning model.

### Text Analysis (Main Endpoint)
```
POST /analyze_text
```

**Request Body:**
```json
{
  "text": "Your investment text here"
}
```

**Response:**
```json
{
  "risk_score": 75,
  "flagged_words": ["guaranteed", "rich", "quick"],
  "prediction": "risky",
  "confidence": 0.823,
  "risk_level": "HIGH RISK"
}
```

## 🔍 Risk Scoring Algorithm

The API calculates risk scores (0-100) based on multiple factors:

1. **Flagged Words (40 points max)**: Each risky keyword adds up to 8 points
2. **Urgency Indicators (30 points max)**: Exclamation marks, urgency words add up to 5 points each
3. **Model Confidence (30 points max)**: Higher confidence in risky predictions increases score

**Risk Levels:**
- **0-39**: LOW RISK
- **40-69**: MEDIUM RISK  
- **70-100**: HIGH RISK

## 🚨 Risky Keywords Detected

The API automatically flags these types of words:

- **Guarantees**: "guaranteed", "guarantee", "risk-free"
- **Wealth Promises**: "rich", "millionaire", "billionaire"
- **Urgency**: "hurry", "rush", "limited time", "act now"
- **Insider Claims**: "insider", "secret", "exclusive"
- **Unrealistic Returns**: "500%", "1000x", "overnight"
- **Pressure Tactics**: "don't miss", "last chance", "before it's too late"

## 📊 Example Usage

### Using curl

```bash
# Analyze risky text
curl -X POST "http://localhost:8000/analyze_text" \
     -H "Content-Type: application/json" \
     -d '{"text": "Get rich quick with this guaranteed 500% return investment!"}'

# Analyze safe text
curl -X POST "http://localhost:8000/analyze_text" \
     -H "Content-Type: application/json" \
     -d '{"text": "Consider diversifying your portfolio to manage risk effectively."}'
```

### Using Python requests

```python
import requests

# Analyze text
response = requests.post(
    "http://localhost:8000/analyze_text",
    json={"text": "Your investment text here"}
)

if response.status_code == 200:
    result = response.json()
    print(f"Risk Score: {result['risk_score']}/100")
    print(f"Risk Level: {result['risk_level']}")
    print(f"Flagged Words: {result['flagged_words']}")
```

### Using JavaScript fetch

```javascript
// Analyze text
fetch('http://localhost:8000/analyze_text', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        text: 'Your investment text here'
    })
})
.then(response => response.json())
.then(data => {
    console.log(`Risk Score: ${data.risk_score}/100`);
    console.log(`Risk Level: ${data.risk_level}`);
    console.log(`Flagged Words: ${data.flagged_words.join(', ')}`);
});
```

## 🧪 Testing

### Automated Testing
```bash
python test_api.py
```

### Manual Testing
1. Start the server: `python api.py`
2. Open http://localhost:8000/docs in your browser
3. Use the interactive Swagger UI to test endpoints
4. Try different text inputs to see risk analysis

## 🔧 Configuration

### Environment Variables
- `HOST`: Server host (default: 0.0.0.0)
- `PORT`: Server port (default: 8000)

### Model Path
- Default model path: `model.pkl`
- Can be modified in the `FakeInfluencerDetectorAPI.load_model()` method

## 📈 Performance

- **Response Time**: Typically < 100ms for text analysis
- **Concurrent Requests**: Handles multiple simultaneous requests
- **Memory Usage**: Efficient model loading and text processing
- **Scalability**: Can be deployed with multiple workers using Uvicorn

## 🚀 Deployment

### Production Deployment
```bash
# Install production dependencies
pip install gunicorn uvicorn[standard]

# Run with multiple workers
gunicorn api:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Docker Deployment
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements_api.txt .
RUN pip install -r requirements_api.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 🔍 Troubleshooting

### Common Issues

1. **Model not loaded error**
   - Ensure `model.pkl` exists in the project directory
   - Check file permissions
   - Verify the model file is not corrupted

2. **Import errors**
   - Install all requirements: `pip install -r requirements_api.txt`
   - Check Python version compatibility

3. **Port already in use**
   - Change port in `api.py` or kill existing process
   - Use: `lsof -ti:8000 | xargs kill -9`

### Debug Mode
```bash
# Run with debug logging
uvicorn api:app --reload --log-level debug
```

## 📚 API Documentation

- **Interactive Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/openapi.json

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## ⚠️ Disclaimer

This tool is for educational and research purposes. It should not be used as the sole basis for financial decisions. Always consult with qualified financial professionals before making investment decisions.
