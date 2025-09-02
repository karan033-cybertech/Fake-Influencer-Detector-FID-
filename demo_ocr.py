#!/usr/bin/env python3
"""
Demo script for OCR functionality
This script demonstrates how to use the image text extraction feature
"""

import pytesseract
from PIL import Image
import requests
import json

# Configuration
API_BASE_URL = "http://localhost:8000"

def extract_text_from_image_demo(image_path: str) -> str:
    """Demo function to extract text from an image file"""
    try:
        # Open the image using PIL
        image = Image.open(image_path)
        
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Extract text using pytesseract
        extracted_text = pytesseract.image_to_string(image)
        
        return extracted_text.strip()
    except Exception as e:
        print(f"❌ Error extracting text from image: {str(e)}")
        return ""

def analyze_text_demo(text: str) -> dict:
    """Demo function to analyze text using the API"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/analyze_text",
            json={"text": text},
            timeout=10
        )
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ API Error: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to the API backend. Please make sure the FastAPI server is running on localhost:8000")
        return None
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None

def demo_ocr_pipeline():
    """Demonstrate the complete OCR pipeline"""
    print("🚀 OCR Pipeline Demo")
    print("=" * 50)
    
    # Check if Tesseract is available
    try:
        tesseract_version = pytesseract.get_tesseract_version()
        print(f"✅ Tesseract version: {tesseract_version}")
    except Exception as e:
        print(f"❌ Tesseract not available: {str(e)}")
        print("📝 Please install Tesseract OCR first (see WINDOWS_TESSERACT_INSTALL.md)")
        return
    
    # Example 1: Test with a sample text
    print("\n📝 Example 1: Direct Text Analysis")
    print("-" * 40)
    
    sample_text = "Get rich quick with this guaranteed 500% return investment! Don't miss out on this once-in-a-lifetime opportunity!"
    print(f"Sample text: {sample_text}")
    
    result = analyze_text_demo(sample_text)
    if result:
        print(f"✅ Analysis complete!")
        print(f"   Risk Score: {result['risk_score']}/100")
        print(f"   Risk Level: {result['risk_level']}")
        print(f"   Flagged Words: {', '.join(result['flagged_words'])}")
    
    # Example 2: OCR from image (if image path provided)
    print("\n🖼️ Example 2: Image OCR (if image file exists)")
    print("-" * 40)
    
    # You can test this by providing an image path
    # image_path = "path/to/your/image.png"
    # if os.path.exists(image_path):
    #     print(f"Processing image: {image_path}")
    #     extracted_text = extract_text_from_image_demo(image_path)
    #     if extracted_text:
    #         print(f"Extracted text: {extracted_text[:100]}...")
    #         result = analyze_text_demo(extracted_text)
    #         if result:
    #             print(f"✅ OCR Analysis complete!")
    #             print(f"   Risk Score: {result['risk_score']}/100")
    #             print(f"   Risk Level: {result['risk_level']}")
    #     else:
    #         print("❌ No text extracted from image")
    # else:
    #     print("No test image found. To test OCR:")
    #     print("1. Save an image with text to your project directory")
    #     print("2. Update the image_path variable in this script")
    #     print("3. Run the script again")
    
    print("\n📋 To test with actual images:")
    print("1. Run the Streamlit app: streamlit run streamlit_app.py")
    print("2. Go to the '🖼️ Image Upload' tab")
    print("3. Upload an image and test OCR extraction")
    print("4. Analyze the extracted text for fake influencer detection")

def test_api_connection():
    """Test if the API backend is running"""
    print("🔌 Testing API Connection")
    print("-" * 30)
    
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            health_data = response.json()
            print(f"✅ API Backend Connected")
            print(f"   Status: {health_data.get('status', 'Unknown')}")
            print(f"   Model Loaded: {health_data.get('model_loaded', False)}")
            return True
        else:
            print(f"❌ API Error: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API backend")
        print("📝 Make sure to run: python api.py")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    print("🧪 Fake Influencer Detector - OCR Demo")
    print("=" * 60)
    
    # Test API connection first
    api_connected = test_api_connection()
    
    if api_connected:
        # Run OCR demo
        demo_ocr_pipeline()
    else:
        print("\n🔧 Setup Instructions:")
        print("1. Start the API backend: python api.py")
        print("2. Install Tesseract OCR (see WINDOWS_TESSERACT_INSTALL.md)")
        print("3. Run this demo again: python demo_ocr.py")
    
    print("\n" + "=" * 60)
    print("�� Demo completed!")
