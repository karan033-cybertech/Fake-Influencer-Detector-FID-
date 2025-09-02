# Fake Influencer Detector

A Python-based machine learning project that detects potentially risky investment advice from social media influencers using Natural Language Processing (NLP) and machine learning.

## Overview

This project analyzes investment-related text to identify patterns commonly associated with fake influencers who promote risky or fraudulent investment schemes. It uses TF-IDF features and Logistic Regression to classify text as either "risky" or "safe".

## Features

- **Text Classification**: Automatically categorizes investment advice as risky or safe
- **TF-IDF Vectorization**: Converts text to numerical features for machine learning
- **Logistic Regression Model**: Trained on a curated dataset of investment sentences
- **Model Persistence**: Saves and loads trained models for reuse
- **Confidence Scores**: Provides prediction confidence for each classification
- **Sample Dataset**: Includes 40 pre-labeled examples (20 risky, 20 safe)

## Installation

1. Clone or download this project
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### 1. Train and Save the Model

Run the main script to create the dataset, train the model, and save it:

```bash
python fake_influencer_detector.py
```

This will:
- Create a sample dataset with risky and safe investment sentences
- Train a Logistic Regression model using TF-IDF features
- Evaluate the model performance
- Save the trained model as `model.pkl`

### 2. Use the Saved Model

Run the demo script to see how to use the saved model:

```bash
python demo.py
```

### 3. Programmatic Usage

```python
from fake_influencer_detector import FakeInfluencerDetector

# Initialize detector
detector = FakeInfluencerDetector()

# Load saved model
detector.load_model('model.pkl')

# Analyze new text
texts = ["This investment will make you rich overnight!"]
predictions, probabilities = detector.predict(texts)

print(f"Prediction: {predictions[0]}")
print(f"Confidence: {max(probabilities[0]):.1%}")
```

## Dataset

The project includes a curated dataset with examples of:

**Risky Sentences (Red Flags):**
- Promises of guaranteed returns
- Urgency and pressure tactics
- Claims of insider information
- Dismissal of professional advice
- Unrealistic profit expectations

**Safe Sentences (Legitimate Advice):**
- Risk management strategies
- Professional consultation recommendations
- Long-term investment approaches
- Diversification advice
- Cautious and measured language

## Model Details

- **Algorithm**: Logistic Regression
- **Features**: TF-IDF (Term Frequency-Inverse Document Frequency)
- **Max Features**: 1000
- **Stop Words**: English stop words removed
- **Train/Test Split**: 80/20 with stratification

## Files

- `fake_influencer_detector.py` - Main script with model training and saving
- `demo.py` - Demonstration of using the saved model
- `requirements.txt` - Python package dependencies
- `README.md` - This documentation file
- `model.pkl` - Saved trained model (created after running main script)

## Requirements

- Python 3.7+
- scikit-learn
- pandas
- numpy
- pickle-mixin

## Example Output

```
=== Fake Influencer Detector ===

Dataset created with 20 risky and 20 safe sentences
Dataset shape: (40, 2)
Label distribution:
safe     20
risky    20
Name: label, dtype: int64

Training set size: 32
Testing set size: 8

Training the model...
Model training completed!

Model Accuracy: 1.0000

Classification Report:
              precision    recall  f1-score   support

        risky       1.00      1.00      1.00         4
         safe       1.00      1.00      1.00         4

    accuracy                           1.00         8
   macro avg       1.00      1.00      1.00         8
weighted avg       1.00      1.00      1.00         8

Model saved successfully as model.pkl

=== Testing with New Examples ===
Example 1: This investment will make you rich overnight!
Prediction: RISKY
Confidence: 99.87%

Example 2: Consider diversifying your portfolio for long-term growth.
Prediction: SAFE
Confidence: 99.92%
```

## Use Cases

- **Social Media Monitoring**: Identify potentially fraudulent investment posts
- **Content Moderation**: Flag suspicious financial advice
- **Educational Tool**: Teach users to recognize investment scams
- **Research**: Analyze patterns in financial fraud communication

## Disclaimer

This tool is for educational and research purposes. It should not be used as the sole basis for financial decisions. Always consult with qualified financial professionals before making investment decisions.

## License

This project is open source and available under the MIT License.
