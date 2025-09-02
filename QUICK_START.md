# 🚀 Quick Start Guide: Image Upload & OCR

Get the image upload and OCR functionality working in 5 minutes!

## ⚡ Quick Setup (5 minutes)

### 1. **Install Tesseract OCR** ⏱️ 2 min
```powershell
# Option A: Download and install manually
# Go to: https://github.com/UB-Mannheim/tesseract/wiki
# Download: tesseract-ocr-w64-setup-5.3.1.20240401.exe
# Run as Administrator and follow the installer

# Option B: Using winget (Windows 10/11)
winget install UB-Mannheim.TesseractOCR

# Option C: Using Chocolatey
choco install tesseract
```

### 2. **Add to PATH** ⏱️ 1 min
```powershell
# Temporary (current session only)
$env:PATH += ";C:\Program Files\Tesseract-OCR"

# Permanent (recommended)
# Press Win+R, type 'sysdm.cpl', go to Advanced → Environment Variables
# Add 'C:\Program Files\Tesseract-OCR' to System PATH
```

### 3. **Test Installation** ⏱️ 1 min
```powershell
# Verify Tesseract is working
tesseract --version

# Test Python dependencies
python test_ocr.py
```

### 4. **Start the App** ⏱️ 1 min
```powershell
# Terminal 1: Start API backend
python api.py

# Terminal 2: Start Streamlit app
streamlit run streamlit_app.py
```

## 🎯 Test the Feature

### **Step-by-Step Testing**
1. **Open the app** in your browser (usually http://localhost:8501)
2. **Click "🖼️ Image Upload"** tab
3. **Upload an image** with clear text (PNG, JPG, etc.)
4. **Click "🔍 Extract Text from Image"**
5. **Review extracted text** and click "🚀 Analyze Extracted Text"
6. **View analysis results** - same as text input!

## 🔧 Troubleshooting

### **Common Issues & Quick Fixes**

#### ❌ "tesseract is not installed or it's not in your PATH"
```powershell
# Quick fix: Add to current session PATH
$env:PATH += ";C:\Program Files\Tesseract-OCR"

# Verify it works
tesseract --version
```

#### ❌ "Cannot connect to API backend"
```powershell
# Start the API backend
python api.py
```

#### ❌ "No text extracted from image"
- Use higher quality images (300+ DPI)
- Ensure good lighting and contrast
- Avoid blurry or low-quality screenshots

### **Still Having Issues?**
- **Check detailed guide**: `WINDOWS_TESSERACT_INSTALL.md`
- **Run test script**: `python test_ocr.py`
- **Verify dependencies**: `pip list | findstr pytesseract`

## 📱 Sample Images to Test

### **Good Test Images**
- Screenshots of social media posts
- Clear text documents
- High-resolution images with readable fonts
- Simple backgrounds

### **Avoid These**
- Blurry or low-resolution images
- Complex backgrounds
- Handwritten text (unless very clear)
- Images with heavy filters or effects

## 🎉 Success Indicators

### **✅ Everything is Working When:**
- `tesseract --version` shows version info
- `python test_ocr.py` runs without errors
- Streamlit app loads with "🖼️ Image Upload" tab
- You can upload an image and extract text
- Analysis results appear after OCR extraction

### **🚀 Ready to Use!**
Once you see the success indicators above, you can:
- Upload screenshots of investment advice
- Extract text from social media posts
- Analyze extracted text for fake influencer red flags
- Get the same detailed analysis as direct text input

## 📚 Need More Help?

### **Documentation Files**
- `IMAGE_UPLOAD_README.md` - Complete feature guide
- `WINDOWS_TESSERACT_INSTALL.md` - Detailed Windows setup
- `IMPLEMENTATION_SUMMARY.md` - Technical implementation details

### **Test Scripts**
- `test_ocr.py` - Basic functionality test
- `demo_ocr.py` - Complete pipeline demonstration

### **Quick Commands Reference**
```powershell
# Test OCR
python test_ocr.py

# Demo OCR pipeline
python demo_ocr.py

# Start API
python api.py

# Start Streamlit app
streamlit run streamlit_app.py

# Check Tesseract
tesseract --version

# Check Python packages
pip list | findstr pytesseract
```

---

**🎯 Goal**: Get image upload and OCR working in under 5 minutes!

**⏱️ Time**: Most users complete setup in 3-5 minutes

**🚨 If stuck**: Check the troubleshooting section above
