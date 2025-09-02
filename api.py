from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pickle
from typing import List, Dict, Any
import re

# Initialize FastAPI app
app = FastAPI(
    title="Fake Influencer Detector API",
    description="API for detecting potentially risky investment advice from social media influencers",
    version="1.0.0"
)

# Pydantic models for request/response
class TextRequest(BaseModel):
    text: str

class AnalysisResponse(BaseModel):
    risk_score: int
    flagged_words: List[str]
    prediction: str
    confidence: float
    risk_level: str

class FakeInfluencerDetectorAPI:
    def __init__(self):
        self.model = None
        self.vectorizer = None
        self.is_loaded = False
        self.risky_keywords = [
            "guaranteed", "guarantee", "guarantees", "guaranteeing",
            "rich", "richer", "richest", "wealth", "wealthy",
            "millionaire", "billionaire", "overnight", "quick",
            "fast", "rapid", "immediate", "instant", "urgent",
            "hurry", "rush", "limited time", "last chance",
            "don't miss", "act now", "before it's too late",
            "insider", "secret", "exclusive", "exclusively",
            "explode", "moon", "rocket", "skyrocket", "surge",
            "breakthrough", "revolutionary", "game-changing",
            "no risk", "risk-free", "safe", "profitable",
            "profit", "profits", "profiting", "earn", "earning",
            "earns", "earned", "return", "returns", "returning",
            "returned", "double", "triple", "quadruple", "10x",
            "100x", "1000x", "500%", "1000%", "million",
            "billion", "trillion", "formula", "strategy", "method",
            "technique", "system", "program", "course", "training"
        ]
    
    def load_model(self, model_path: str = "model.pkl") -> bool:
        """Load the trained model and vectorizer"""
        try:
            with open(model_path, 'rb') as f:
                model_data = pickle.load(f)
            
            self.vectorizer = model_data['vectorizer']
            self.model = model_data['model']
            self.is_loaded = True
            print(f"Model loaded successfully from {model_path}")
            return True
        except Exception as e:
            print(f"Error loading model: {e}")
            return False
    
    def extract_flagged_words(self, text: str) -> List[str]:
        """Extract potentially risky words from the text"""
        text_lower = text.lower()
        flagged = []
        
        for keyword in self.risky_keywords:
            if keyword.lower() in text_lower:
                # Find all occurrences of the keyword
                pattern = re.compile(rf'\b{re.escape(keyword)}\b', re.IGNORECASE)
                if pattern.search(text):
                    flagged.append(keyword)
        
        return list(set(flagged))  # Remove duplicates
    
    def calculate_risk_score(self, text: str, flagged_words: List[str], confidence: float) -> int:
        """Calculate a risk score from 0-100 based on various factors"""
        base_score = 0
        
        # Base score from flagged words (50 points max) - Increased weight
        word_score = min(len(flagged_words) * 12, 50)  # Increased from 8 to 12
        base_score += word_score
        
        # Urgency and pressure indicators (35 points max) - Increased weight
        urgency_indicators = ["!", "urgent", "hurry", "rush", "now", "today", "limited", "quick", "fast", "overnight", "7 days", "30 days"]
        urgency_count = sum(1 for indicator in urgency_indicators if indicator.lower() in text.lower())
        urgency_score = min(urgency_count * 7, 35)  # Increased from 5 to 7
        base_score += urgency_score
        
        # Confidence-based adjustment (15 points max) - Reduced weight
        if confidence > 0.7:
            confidence_score = 15
        elif confidence > 0.5:
            confidence_score = 10
        else:
            confidence_score = 5
        base_score += confidence_score
        
        # Bonus points for high-risk combinations
        if len(flagged_words) >= 2 and any(word in text.lower() for word in ["guaranteed", "guarantee", "100%", "profit"]):
            base_score += 15
        
        # Additional bonus for time pressure and urgency
        time_pressure_words = ["7 days", "30 days", "overnight", "quick", "fast", "immediate"]
        if any(word in text.lower() for word in time_pressure_words):
            base_score += 10
        
        # Bonus for unrealistic returns
        if any(word in text.lower() for word in ["100%", "millionaire", "rich", "overnight"]):
            base_score += 10
        
        # Cap at 100
        return min(base_score, 100)
    
    def analyze_text(self, text: str) -> Dict[str, Any]:
        """Analyze text and return comprehensive results"""
        if not self.is_loaded:
            raise ValueError("Model not loaded. Please load the model first.")
        
        # Extract flagged words
        flagged_words = self.extract_flagged_words(text)
        
        # Make prediction using the model
        try:
            # Transform text using the loaded vectorizer
            features = self.vectorizer.transform([text])
            prediction = self.model.predict(features)[0]
            probabilities = self.model.predict_proba(features)[0]
            confidence = max(probabilities)
            
            # Calculate risk score
            risk_score = self.calculate_risk_score(text, flagged_words, confidence)
            
            # Determine risk level
            if risk_score >= 70:
                risk_level = "HIGH RISK"
            elif risk_score >= 40:
                risk_level = "MEDIUM RISK"
            else:
                risk_level = "LOW RISK"
            
            return {
                "risk_score": risk_score,
                "flagged_words": flagged_words,
                "prediction": prediction,
                "confidence": round(confidence, 3),
                "risk_level": risk_level
            }
            
        except Exception as e:
            raise ValueError(f"Error during prediction: {e}")

# Initialize the detector
detector = FakeInfluencerDetectorAPI()

@app.on_event("startup")
async def startup_event():
    """Load the model when the application starts"""
    success = detector.load_model()
    if not success:
        print("Warning: Failed to load model. API may not function properly.")

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Fake Influencer Detector API",
        "version": "1.0.0",
        "status": "Model loaded" if detector.is_loaded else "Model not loaded",
        "endpoints": {
            "/analyze_text": "POST - Analyze investment text for risk",
            "/health": "GET - Check API health status"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy" if detector.is_loaded else "unhealthy",
        "model_loaded": detector.is_loaded,
        "timestamp": "2024-01-01T00:00:00Z"
    }

@app.post("/analyze_text", response_model=AnalysisResponse)
async def analyze_text(request: TextRequest):
    """Analyze investment text for potential risk indicators"""
    try:
        if not detector.is_loaded:
            raise HTTPException(status_code=503, detail="Model not loaded. Please try again later.")
        
        if not request.text or len(request.text.strip()) == 0:
            raise HTTPException(status_code=400, detail="Text cannot be empty")
        
        # Analyze the text
        result = detector.analyze_text(request.text)
        
        return AnalysisResponse(**result)
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/model_info")
async def model_info():
    """Get information about the loaded model"""
    if not detector.is_loaded:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    return {
        "model_type": type(detector.model).__name__,
        "vectorizer_type": type(detector.vectorizer).__name__,
        "max_features": detector.vectorizer.max_features if hasattr(detector.vectorizer, 'max_features') else "Unknown",
        "vocabulary_size": len(detector.vectorizer.vocabulary_) if hasattr(detector.vectorizer, 'vocabulary_') else "Unknown"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
