#!/usr/bin/env python3
"""
Test client for the Fake Influencer Detector FastAPI
"""

import requests
import json
import time

# API base URL
BASE_URL = "http://localhost:8000"

def test_api_endpoints():
    """Test all API endpoints"""
    print("=== Testing Fake Influencer Detector API ===\n")
    
    # Test 1: Root endpoint
    print("1. Testing root endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Root endpoint working: {data['message']}")
            print(f"   Status: {data['status']}")
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API. Make sure the server is running.")
        return False
    
    # Test 2: Health check
    print("\n2. Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check: {data['status']}")
            print(f"   Model loaded: {data['model_loaded']}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health check error: {e}")
    
    # Test 3: Model info
    print("\n3. Testing model info endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/model_info")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Model info retrieved:")
            print(f"   Model type: {data['model_type']}")
            print(f"   Vectorizer: {data['vectorizer_type']}")
            print(f"   Max features: {data['max_features']}")
            print(f"   Vocabulary size: {data['vocabulary_size']}")
        else:
            print(f"❌ Model info failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Model info error: {e}")
    
    # Test 4: Text analysis with risky text
    print("\n4. Testing text analysis with risky investment text...")
    risky_text = "Get rich quick with this guaranteed 500% return investment! Don't miss out on this once-in-a-lifetime opportunity!"
    
    try:
        response = requests.post(
            f"{BASE_URL}/analyze_text",
            json={"text": risky_text}
        )
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Risky text analysis successful:")
            print(f"   Risk Score: {data['risk_score']}/100")
            print(f"   Risk Level: {data['risk_level']}")
            print(f"   Prediction: {data['prediction'].upper()}")
            print(f"   Confidence: {data['confidence']:.1%}")
            print(f"   Flagged Words: {', '.join(data['flagged_words'])}")
        else:
            print(f"❌ Risky text analysis failed: {response.status_code}")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Risky text analysis error: {e}")
    
    # Test 5: Text analysis with safe text
    print("\n5. Testing text analysis with safe investment text...")
    safe_text = "Consider diversifying your portfolio to manage risk effectively. Consult with a certified financial advisor."
    
    try:
        response = requests.post(
            f"{BASE_URL}/analyze_text",
            json={"text": safe_text}
        )
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Safe text analysis successful:")
            print(f"   Risk Score: {data['risk_score']}/100")
            print(f"   Risk Level: {data['risk_level']}")
            print(f"   Prediction: {data['prediction'].upper()}")
            print(f"   Confidence: {data['confidence']:.1%}")
            print(f"   Flagged Words: {', '.join(data['flagged_words']) if data['flagged_words'] else 'None'}")
        else:
            print(f"❌ Safe text analysis failed: {response.status_code}")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Safe text analysis error: {e}")
    
    # Test 6: Edge case - empty text
    print("\n6. Testing edge case - empty text...")
    try:
        response = requests.post(
            f"{BASE_URL}/analyze_text",
            json={"text": ""}
        )
        if response.status_code == 400:
            print("✅ Empty text properly rejected with 400 status")
        else:
            print(f"❌ Empty text not properly handled: {response.status_code}")
    except Exception as e:
        print(f"❌ Empty text test error: {e}")
    
    print("\n=== API Testing Complete ===")
    return True

def interactive_test():
    """Interactive testing mode"""
    print("\n=== Interactive Testing Mode ===")
    print("Enter investment text to analyze (or 'quit' to exit):")
    
    while True:
        user_text = input("\nEnter text: ").strip()
        
        if user_text.lower() in ['quit', 'exit', 'q']:
            break
        
        if not user_text:
            print("Please enter some text to analyze.")
            continue
        
        try:
            response = requests.post(
                f"{BASE_URL}/analyze_text",
                json={"text": user_text}
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"\n📊 Analysis Results:")
                print(f"   Risk Score: {data['risk_score']}/100")
                print(f"   Risk Level: {data['risk_level']}")
                print(f"   Prediction: {data['prediction'].upper()}")
                print(f"   Confidence: {data['confidence']:.1%}")
                if data['flagged_words']:
                    print(f"   🚨 Flagged Words: {', '.join(data['flagged_words'])}")
                else:
                    print(f"   ✅ No flagged words detected")
            else:
                print(f"❌ Analysis failed: {response.status_code}")
                print(f"   Error: {response.text}")
                
        except Exception as e:
            print(f"❌ Error during analysis: {e}")

if __name__ == "__main__":
    print("Fake Influencer Detector API Test Client")
    print("Make sure the API server is running on http://localhost:8000")
    print("=" * 50)
    
    # Test basic endpoints
    if test_api_endpoints():
        # If basic tests pass, offer interactive mode
        try:
            interactive_test()
        except KeyboardInterrupt:
            print("\n\nExiting interactive mode...")
    else:
        print("\n❌ Basic API tests failed. Please check if the server is running.")
        print("To start the server, run: python api.py")
