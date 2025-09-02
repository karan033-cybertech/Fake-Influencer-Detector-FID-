# 🚨 Fake Influencer Detector - Streamlit Frontend

A beautiful, interactive web interface for the Fake Influencer Detector that connects to the FastAPI backend to analyze investment text for potential fake influencer red flags.

## ✨ Features

- **🎨 Modern UI**: Clean, responsive design with intuitive navigation
- **📝 Text Input**: Large text area for easy input of investment-related text
- **🚀 Real-time Analysis**: Instant connection to FastAPI backend for analysis
- **📊 Visual Results**: Interactive charts and progress bars for risk assessment
- **🔍 Word Highlighting**: Red highlighting of flagged risky words in text
- **📈 Risk Breakdown**: Detailed analysis of risk factors and scoring
- **💾 Report Download**: Export analysis results as JSON reports
- **📱 Responsive Design**: Works on desktop and mobile devices

## 🎯 What It Detects

The frontend displays comprehensive analysis including:

- **Risk Score (0-100)**: Visual gauge with color coding
- **Risk Level**: LOW/MEDIUM/HIGH with appropriate emojis
- **Flagged Words**: Red-highlighted risky keywords
- **Model Confidence**: Prediction confidence percentage
- **Risk Breakdown**: Component scores for different risk factors
- **Text Analysis**: Character count, word count, sentence count

## 🛠️ Installation

### Prerequisites

1. **FastAPI Backend Running**: Make sure the API server is running on localhost:8000
2. **Python 3.7+**: Required for Streamlit and dependencies

### Setup

1. **Install Streamlit dependencies:**
   ```bash
   pip install -r requirements_streamlit.txt
   ```

2. **Ensure FastAPI backend is running:**
   ```bash
   python api.py
   ```

3. **Start the Streamlit app:**
   ```bash
   streamlit run streamlit_app.py
   ```

4. **Open your browser** and navigate to: `http://localhost:8501`

## 🚀 Quick Start

### 1. Start the Backend
```bash
# Terminal 1: Start FastAPI backend
python api.py
```

### 2. Start the Frontend
```bash
# Terminal 2: Start Streamlit frontend
streamlit run streamlit_app.py
```

### 3. Use the App
1. Open `http://localhost:8501` in your browser
2. Enter investment-related text in the text area
3. Click "🚀 Analyze Text"
4. View results in the interactive dashboard

## 📱 Interface Overview

### Main Components

1. **Header Section**
   - App title with gradient styling
   - Description and navigation

2. **Sidebar**
   - API connection status
   - Model information
   - How-to instructions
   - Risk level explanations

3. **Text Input Area**
   - Large text area for input
   - Placeholder examples
   - Submit button

4. **Quick Stats Panel**
   - Risk level with emoji
   - Risk score metric
   - Confidence percentage
   - Prediction result
   - Flagged words count

5. **Results Dashboard**
   - **Overview Tab**: Risk gauge and assessment
   - **Risk Analysis Tab**: Charts and breakdowns
   - **Text Details Tab**: Highlighted text and analysis

### Color Coding

- **🟢 Green (0-39)**: LOW RISK - Safe investment advice
- **🟡 Orange (40-69)**: MEDIUM RISK - Some concerning elements
- **🔴 Red (70-100)**: HIGH RISK - Multiple red flags detected

## 🔧 Configuration

### Streamlit Settings

The app uses a custom configuration file (`.streamlit/config.toml`):

- **Port**: 8501 (default)
- **Theme**: Custom red-based color scheme
- **Server**: Localhost only for security

### API Connection

- **Base URL**: `http://localhost:8000`
- **Timeout**: 10 seconds for analysis requests
- **Health Check**: Automatic API status monitoring

## 📊 Example Usage

### High-Risk Text Example
```
"Get rich quick with this guaranteed 500% return investment! 
Don't miss out on this once-in-a-lifetime opportunity!"
```

**Expected Results:**
- Risk Score: 65-85/100
- Risk Level: MEDIUM-HIGH RISK
- Flagged Words: "guaranteed", "rich", "quick", "return", "don't miss"
- Prediction: RISKY

### Low-Risk Text Example
```
"Consider diversifying your portfolio to manage risk effectively. 
Consult with a certified financial advisor."
```

**Expected Results:**
- Risk Score: 15-25/100
- Risk Level: LOW RISK
- Flagged Words: None
- Prediction: SAFE

## 🧪 Testing

### Manual Testing
1. Start both backend and frontend
2. Test with various text inputs
3. Verify API connection status
4. Check all visualization components

### Automated Testing
The app includes built-in error handling for:
- API connection failures
- Invalid responses
- Network timeouts
- Empty text submissions

## 🔍 Troubleshooting

### Common Issues

1. **"API Backend Not Connected"**
   - Ensure `python api.py` is running
   - Check if port 8000 is available
   - Verify no firewall blocking

2. **"Model Not Loaded"**
   - Check if `model.pkl` exists
   - Restart the API server
   - Check API logs for errors

3. **Streamlit Connection Issues**
   - Verify port 8501 is free
   - Check browser console for errors
   - Restart Streamlit app

4. **Analysis Not Working**
   - Check API health endpoint
   - Verify text input is not empty
   - Check network connectivity

### Debug Mode

```bash
# Run with debug logging
streamlit run streamlit_app.py --logger.level debug
```

## 📈 Performance

- **Response Time**: < 2 seconds for typical analysis
- **Memory Usage**: Efficient with session state management
- **Concurrent Users**: Supports multiple simultaneous users
- **Real-time Updates**: Instant feedback and results

## 🚀 Deployment

### Local Development
```bash
streamlit run streamlit_app.py --server.port 8501
```

### Production Deployment
```bash
# Install production dependencies
pip install gunicorn streamlit

# Run with multiple workers
streamlit run streamlit_app.py --server.port 8501 --server.address 0.0.0.0
```

### Docker Deployment
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements_streamlit.txt .
RUN pip install -r requirements_streamlit.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "streamlit_app.py", "--server.port", "8501"]
```

## 🔒 Security Features

- **Localhost Only**: Default configuration restricts access to local machine
- **Input Validation**: Sanitizes user input before processing
- **Error Handling**: Graceful handling of malicious inputs
- **Session Management**: Secure session state handling

## 📚 API Integration

The frontend integrates seamlessly with the FastAPI backend:

- **Health Monitoring**: Automatic API status checking
- **Error Handling**: Graceful fallbacks for API failures
- **Real-time Communication**: Direct HTTP requests to backend
- **Response Processing**: Parses and displays API results

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## ⚠️ Disclaimer

This tool is for educational and research purposes. It should not be used as the sole basis for financial decisions. Always consult with qualified financial professionals before making investment decisions.

## 🆘 Support

If you encounter issues:

1. Check the troubleshooting section
2. Verify API backend is running
3. Check browser console for errors
4. Review Streamlit logs
5. Ensure all dependencies are installed

---

**🚨 Fake Influencer Detector Frontend** - Making investment fraud detection accessible and user-friendly!
