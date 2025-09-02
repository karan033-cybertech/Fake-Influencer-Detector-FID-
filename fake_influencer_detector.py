import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import pickle
import warnings
warnings.filterwarnings('ignore')

class FakeInfluencerDetector:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        self.model = LogisticRegression(random_state=42)
        self.is_trained = False
    
    def create_sample_dataset(self):
        """Create a sample dataset with risky and safe investment sentences"""
        
        # Risky investment sentences (fake influencer red flags)
        risky_sentences = [
            "Get rich quick with this guaranteed 500% return investment!",
            "Don't miss out on this once-in-a-lifetime opportunity!",
            "This investment will make you a millionaire in 30 days!",
            "Trust me, this is the next Bitcoin!",
            "I've made millions with this strategy, you can too!",
            "This is insider information, act fast before it's too late!",
            "No risk involved, guaranteed profits!",
            "Join my exclusive investment group for massive returns!",
            "This company is about to explode, buy now!",
            "I'm giving away my secret investment formula!",
            "This is the easiest way to make money online!",
            "Don't listen to financial advisors, they don't know anything!",
            "This investment is 100% safe and profitable!",
            "I'm sharing this because I care about your financial future!",
            "This is the investment opportunity of the century!",
            "Act now or regret forever!",
            "This will change your life forever!",
            "I'm not a financial advisor, but trust me on this!",
            "This is the secret the rich don't want you to know!",
            "Double your money in just one week!"
        ]
        
        # Safe investment sentences (legitimate financial advice)
        safe_sentences = [
            "Diversify your portfolio to manage risk effectively.",
            "Consider your investment timeline and risk tolerance.",
            "Research companies before investing in their stock.",
            "Consult with a certified financial advisor.",
            "Past performance doesn't guarantee future results.",
            "Invest in index funds for long-term growth.",
            "Consider dollar-cost averaging for regular investments.",
            "Emergency funds should be prioritized before investing.",
            "Understand the fees associated with investment products.",
            "Rebalance your portfolio periodically.",
            "Consider tax implications of your investment decisions.",
            "Don't invest money you can't afford to lose.",
            "Focus on long-term investment strategies.",
            "Avoid making emotional investment decisions.",
            "Consider environmental, social, and governance factors.",
            "Review your investment plan annually.",
            "Understand the difference between stocks and bonds.",
            "Consider international diversification.",
            "Invest in what you understand.",
            "Patience is key in successful investing.",
            "Seek professional advice for complex financial decisions."
        ]
        
        # Create DataFrame
        data = {
            'text': risky_sentences + safe_sentences,
            'label': ['risky'] * len(risky_sentences) + ['safe'] * len(safe_sentences)
        }
        
        self.dataset = pd.DataFrame(data)
        print(f"Dataset created with {len(risky_sentences)} risky and {len(safe_sentences)} safe sentences")
        return self.dataset
    
    def prepare_features(self, texts, fit_vectorizer=False):
        """Convert text to TF-IDF features"""
        if fit_vectorizer:
            # Fit and transform for training data
            features = self.vectorizer.fit_transform(texts)
        else:
            # Transform for new data
            features = self.vectorizer.transform(texts)
        return features
    
    def train(self, X_train, y_train):
        """Train the logistic regression model"""
        print("Training the model...")
        self.model.fit(X_train, y_train)
        self.is_trained = True
        print("Model training completed!")
    
    def predict(self, texts):
        """Predict whether texts are risky or safe"""
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")
        
        features = self.vectorizer.transform(texts)
        predictions = self.model.predict(features)
        probabilities = self.model.predict_proba(features)
        
        return predictions, probabilities
    
    def evaluate(self, X_test, y_test):
        """Evaluate model performance"""
        predictions = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)
        
        print(f"\nModel Accuracy: {accuracy:.4f}")
        print("\nClassification Report:")
        print(classification_report(y_test, predictions))
        
        return accuracy
    
    def save_model(self, filename='model.pkl'):
        """Save the trained model and vectorizer"""
        if not self.is_trained:
            raise ValueError("Model must be trained before saving")
        
        model_data = {
            'vectorizer': self.vectorizer,
            'model': self.model,
            'is_trained': self.is_trained
        }
        
        with open(filename, 'wb') as f:
            pickle.dump(model_data, f)
        
        print(f"Model saved successfully as {filename}")
    
    def load_model(self, filename='model.pkl'):
        """Load a saved model and vectorizer"""
        with open(filename, 'rb') as f:
            model_data = pickle.load(f)
        
        self.vectorizer = model_data['vectorizer']
        self.model = model_data['model']
        self.is_trained = model_data['is_trained']
        
        print(f"Model loaded successfully from {filename}")

def main():
    """Main function to run the Fake Influencer Detector"""
    print("=== Fake Influencer Detector ===\n")
    
    # Initialize detector
    detector = FakeInfluencerDetector()
    
    # Create sample dataset
    dataset = detector.create_sample_dataset()
    print(f"Dataset shape: {dataset.shape}")
    print(f"Label distribution:\n{dataset['label'].value_counts()}\n")
    
    # Split data into training and testing sets
    X = dataset['text']
    y = dataset['label']
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"Training set size: {len(X_train)}")
    print(f"Testing set size: {len(X_test)}\n")
    
    # Prepare features
    X_train_features = detector.prepare_features(X_train, fit_vectorizer=True)
    X_test_features = detector.prepare_features(X_test, fit_vectorizer=False)
    
    # Train the model
    detector.train(X_train_features, y_train)
    
    # Evaluate the model
    accuracy = detector.evaluate(X_test_features, y_test)
    
    # Save the model
    detector.save_model()
    
    # Test with some new examples
    print("\n=== Testing with New Examples ===")
    test_examples = [
        "This investment will make you rich overnight!",
        "Consider diversifying your portfolio for long-term growth.",
        "Don't miss this amazing opportunity to get rich!",
        "Consult with a financial advisor before making investment decisions."
    ]
    
    predictions, probabilities = detector.predict(test_examples)
    
    for i, (text, pred, prob) in enumerate(zip(test_examples, predictions, probabilities)):
        confidence = max(prob)
        print(f"\nExample {i+1}: {text}")
        print(f"Prediction: {pred.upper()}")
        print(f"Confidence: {confidence:.2%}")
    
    print("\n=== Model Training and Saving Complete ===")
    print("The model has been saved as 'model.pkl' and is ready for use!")

if __name__ == "__main__":
    main()
