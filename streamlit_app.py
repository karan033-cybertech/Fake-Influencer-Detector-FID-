import streamlit as st
import requests
import json
from typing import Dict, Any
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import pytesseract
from PIL import Image
import io

# Configuration
API_BASE_URL = "http://localhost:8000"
APP_TITLE = "🚨 Fake Influencer Detector"
APP_DESCRIPTION = "Analyze investment-related text for potential fake influencer red flags"

def check_api_health() -> bool:
    """Check if the FastAPI backend is running"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        return response.status_code == 200 and response.json().get("model_loaded", False)
    except:
        return False

def analyze_text(text: str) -> Dict[str, Any]:
    """Send text to FastAPI backend for analysis"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/analyze_text",
            json={"text": text},
            timeout=10
        )
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API Error: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.ConnectionError:
        st.error("❌ Cannot connect to the API backend. Please make sure the FastAPI server is running on localhost:8000")
        return None
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        return None

def extract_text_from_image(image_file) -> str:
    """Extract text from uploaded image using OCR"""
    try:
        # Open the image using PIL
        image = Image.open(image_file)
        
        # Convert to RGB if necessary (for PNG images with transparency)
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Extract text using pytesseract
        extracted_text = pytesseract.image_to_string(image)
        
        return extracted_text.strip()
    except Exception as e:
        st.error(f"❌ Error extracting text from image: {str(e)}")
        return ""

def get_risk_color(risk_score: int) -> str:
    """Get color based on risk score"""
    if risk_score >= 70:
        return "#FF4444"  # Red for high risk
    elif risk_score >= 40:
        return "#FFAA00"  # Orange for medium risk
    else:
        return "#00AA44"  # Green for low risk

def get_risk_emoji(risk_level: str) -> str:
    """Get emoji based on risk level"""
    if risk_level == "HIGH RISK":
        return "🚨"
    elif risk_level == "MEDIUM RISK":
        return "⚠️"
    else:
        return "✅"

def create_risk_gauge(risk_score: int, risk_level: str):
    """Create a gauge chart for risk score"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=risk_score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': f"Risk Score: {risk_score}/100"},
        delta={'reference': 50},
        gauge={
            'axis': {'range': [None, 100]},
            'bar': {'color': get_risk_color(risk_score)},
            'steps': [
                {'range': [0, 39], 'color': "#00AA44"},
                {'range': [40, 69], 'color': "#FFAA00"},
                {'range': [70, 100], 'color': "#FF4444"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 70
            }
        }
    ))
    
    fig.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=40, b=20),
        font=dict(size=14)
    )
    
    return fig

def highlight_flagged_words(text: str, flagged_words: list) -> str:
    """Highlight flagged words in the text with HTML styling"""
    if not flagged_words:
        return text
    
    highlighted_text = text
    for word in flagged_words:
        # Case-insensitive replacement with HTML highlighting
        import re
        pattern = re.compile(re.escape(word), re.IGNORECASE)
        highlighted_text = pattern.sub(
            f'<span style="background-color: #FF4444; color: white; padding: 2px 4px; border-radius: 3px; font-weight: bold;">{word}</span>',
            highlighted_text
        )
    
    return highlighted_text

def main():
    # Page configuration
    st.set_page_config(
        page_title=APP_TITLE,
        page_icon="🚨",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS
    st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 1rem;
        background: linear-gradient(90deg, #FF4444, #FFAA00, #00AA44);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .risk-high { color: #FF4444; font-weight: bold; }
    .risk-medium { color: #FFAA00; font-weight: bold; }
    .risk-low { color: #00AA44; font-weight: bold; }
    .flagged-word { 
        background-color: #FF4444; 
        color: white; 
        padding: 2px 6px; 
        border-radius: 4px; 
        font-weight: bold;
        margin: 2px;
        display: inline-block;
    }
    .stProgress > div > div > div > div {
        background-color: #FF4444;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown(f'<h1 class="main-header">{APP_TITLE}</h1>', unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center; color: #666;'>{APP_DESCRIPTION}</h3>", unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("🔧 API Status")
        
        # Check API health
        if check_api_health():
            st.success("✅ API Backend Connected")
            st.success("✅ Model Loaded")
            
            # Get model info
            try:
                model_info = requests.get(f"{API_BASE_URL}/model_info").json()
                st.info(f"**Model Type:** {model_info['model_type']}")
                st.info(f"**Vectorizer:** {model_info['vectorizer_type']}")
                st.info(f"**Features:** {model_info['max_features']}")
                st.info(f"**Vocabulary:** {model_info['vocabulary_size']}")
            except:
                st.warning("Could not retrieve model info")
        else:
            st.error("❌ API Backend Not Connected")
            st.error("❌ Model Not Loaded")
            st.markdown("""
            **To fix this:**
            1. Make sure the FastAPI server is running
            2. Run: `python api.py`
            3. Check if port 8000 is available
            """)
        
        st.markdown("---")
        st.markdown("**How it works:**")
        st.markdown("""
        1. **Text Input:** Enter investment-related text directly
        2. **Image Upload:** Upload screenshots/images for OCR text extraction
        3. Submit for analysis
        4. Get risk score and flagged words
        5. Review detailed analysis
        """)
        
        st.markdown("**Risk Levels:**")
        st.markdown("- 🟢 **LOW (0-39):** Likely safe advice")
        st.markdown("- 🟡 **MEDIUM (40-69):** Some concerning elements")
        st.markdown("- 🔴 **HIGH (70-100):** Multiple red flags")
        
        st.markdown("---")
        st.markdown("**📸 Image Upload Tips:**")
        st.markdown("- Use clear, high-resolution images")
        st.markdown("- Ensure text is readable and well-lit")
        st.markdown("- Avoid blurry or low-quality screenshots")
        st.markdown("- Supported formats: PNG, JPG, JPEG, BMP, TIFF")
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📝 Text Analysis")
        
        # Create tabs for text input and image upload
        tab1, tab2 = st.tabs(["📝 Text Input", "🖼️ Image Upload"])
        
        with tab1:
            # Text input
            user_text = st.text_area(
                "Enter investment-related text to analyze:",
                height=150,
                placeholder="Example: Get rich quick with this guaranteed 500% return investment! Don't miss out on this once-in-a-lifetime opportunity!"
            )
            
            # Submit button for text
            if st.button("🚀 Analyze Text", type="primary", use_container_width=True):
                if user_text.strip():
                    with st.spinner("Analyzing text..."):
                        result = analyze_text(user_text.strip())
                        
                        if result:
                            # Store result in session state
                            st.session_state.analysis_result = result
                            st.session_state.analyzed_text = user_text.strip()
                            st.rerun()
                else:
                    st.warning("Please enter some text to analyze.")
        
        with tab2:
            st.subheader("📸 Upload Screenshot or Image")
            st.markdown("Upload an image containing text to analyze. The app will extract text using OCR and analyze it for potential fake influencer red flags.")
            
            # Image upload
            uploaded_file = st.file_uploader(
                "Choose an image file",
                type=['png', 'jpg', 'jpeg', 'bmp', 'tiff'],
                help="Supported formats: PNG, JPG, JPEG, BMP, TIFF"
            )
            
            if uploaded_file is not None:
                # Display the uploaded image
                st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
                
                # Extract text button
                if st.button("🔍 Extract Text from Image", type="primary", use_container_width=True):
                    with st.spinner("Extracting text from image..."):
                        extracted_text = extract_text_from_image(uploaded_file)
                        
                        if extracted_text:
                            st.success("✅ Text extracted successfully!")
                            st.subheader("Extracted Text:")
                            st.text_area("Extracted Text", extracted_text, height=150, disabled=True)
                            
                            # Analyze extracted text button
                            if st.button("🚀 Analyze Extracted Text", type="primary", use_container_width=True):
                                with st.spinner("Analyzing extracted text..."):
                                    result = analyze_text(extracted_text)
                                    
                                    if result:
                                        # Store result in session state
                                        st.session_state.analysis_result = result
                                        st.session_state.analyzed_text = extracted_text
                                        st.rerun()
                        else:
                            st.error("❌ No text could be extracted from the image. Please try a different image or check if the image contains clear, readable text.")
    
    with col2:
        st.header("📊 Quick Stats")
        
        if 'analysis_result' in st.session_state:
            result = st.session_state.analysis_result
            
            # Risk level display
            risk_emoji = get_risk_emoji(result['risk_level'])
            st.markdown(f"### {risk_emoji} {result['risk_level']}")
            
            # Risk score
            st.metric("Risk Score", f"{result['risk_score']}/100")
            
            # Confidence
            st.metric("Confidence", f"{result['confidence']:.1%}")
            
            # Prediction
            prediction_emoji = "🚨" if result['prediction'] == "risky" else "✅"
            st.markdown(f"**Prediction:** {prediction_emoji} {result['prediction'].upper()}")
            
            # Flagged words count
            flagged_count = len(result['flagged_words'])
            st.metric("Flagged Words", flagged_count)
    
    # Results section
    if 'analysis_result' in st.session_state:
        st.markdown("---")
        st.header("📊 Analysis Results")
        
        result = st.session_state.analysis_result
        analyzed_text = st.session_state.analyzed_text
        
        # Create tabs for different views
        tab1, tab2, tab3 = st.tabs(["🎯 Overview", "📈 Risk Analysis", "🔍 Text Details"])
        
        with tab1:
            col1, col2 = st.columns([1, 1])
            
            with col1:
                # Risk gauge
                st.plotly_chart(create_risk_gauge(result['risk_score'], result['risk_level']), use_container_width=True)
            
            with col2:
                # Risk breakdown
                st.subheader("Risk Breakdown")
                
                # Flagged words score
                word_score = min(len(result['flagged_words']) * 8, 40)
                st.metric("Flagged Words Score", f"{word_score}/40")
                
                # Confidence score
                confidence_score = 30 if result['confidence'] > 0.7 else (20 if result['confidence'] > 0.5 else 10)
                st.metric("Confidence Score", f"{confidence_score}/30")
                
                # Overall assessment
                st.markdown("### Assessment")
                if result['risk_score'] >= 70:
                    st.error("🚨 **HIGH RISK** - Multiple red flags detected. Exercise extreme caution.")
                elif result['risk_score'] >= 40:
                    st.warning("⚠️ **MEDIUM RISK** - Some concerning elements. Proceed with caution.")
                else:
                    st.success("✅ **LOW RISK** - Text appears to contain legitimate advice.")
        
        with tab2:
            col1, col2 = st.columns([1, 1])
            
            with col1:
                # Risk score bar chart
                st.subheader("Risk Score Breakdown")
                
                categories = ["Flagged Words", "Urgency Indicators", "Model Confidence"]
                scores = [
                    min(len(result['flagged_words']) * 8, 40),
                    0,  # This would need to be calculated in the API
                    30 if result['confidence'] > 0.7 else (20 if result['confidence'] > 0.5 else 10)
                ]
                
                fig = px.bar(
                    x=categories,
                    y=scores,
                    color=scores,
                    color_continuous_scale=["green", "orange", "red"],
                    title="Risk Score Components"
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Confidence distribution
                st.subheader("Model Confidence")
                
                confidence_data = {
                    'Category': ['Safe', 'Risky'],
                    'Probability': [1 - result['confidence'], result['confidence']]
                }
                
                fig = px.pie(
                    confidence_data,
                    values='Probability',
                    names='Category',
                    title="Prediction Confidence",
                    color_discrete_map={'Safe': '#00AA44', 'Risky': '#FF4444'}
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.subheader("Original Text with Highlights")
                
                if result['flagged_words']:
                    highlighted_text = highlight_flagged_words(analyzed_text, result['flagged_words'])
                    st.markdown(highlighted_text, unsafe_allow_html=True)
                    
                    st.markdown("---")
                    st.markdown("**🚨 Flagged Words Detected:**")
                    for word in result['flagged_words']:
                        st.markdown(f'<span class="flagged-word">{word}</span>', unsafe_allow_html=True)
                else:
                    st.success("✅ No flagged words detected in this text.")
                    st.markdown(analyzed_text)
            
            with col2:
                st.subheader("Analysis Details")
                
                st.markdown(f"**Text Length:** {len(analyzed_text)} characters")
                st.markdown(f"**Words:** {len(analyzed_text.split())}")
                st.markdown(f"**Sentences:** {len([s for s in analyzed_text.split('.') if s.strip()])}")
                
                if result['flagged_words']:
                    st.markdown("**Risk Factors:**")
                    for word in result['flagged_words']:
                        st.markdown(f"- {word}")
        
        # Download results
        st.markdown("---")
        col1, col2 = st.columns([1, 1])
        
        with col1:
            if st.button("📥 Download Analysis Report", use_container_width=True):
                # Create report
                report = {
                    "timestamp": datetime.now().isoformat(),
                    "text_analyzed": analyzed_text,
                    "analysis_results": result
                }
                
                # Convert to JSON string
                report_json = json.dumps(report, indent=2)
                
                # Create download button
                st.download_button(
                    label="📄 Download JSON Report",
                    data=report_json,
                    file_name=f"fake_influencer_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
        
        with col2:
            if st.button("🔄 Analyze New Text", use_container_width=True):
                # Clear session state
                del st.session_state.analysis_result
                del st.session_state.analyzed_text
                st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>🚨 <strong>Fake Influencer Detector</strong> - Powered by Machine Learning</p>
        <p>⚠️ This tool is for educational purposes only. Always consult financial professionals.</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
