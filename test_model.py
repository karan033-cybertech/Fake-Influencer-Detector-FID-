#!/usr/bin/env python3
"""
Simple test script for the Fake Influencer Detector model
"""

from fake_influencer_detector import FakeInfluencerDetector

def test_model():
    """Test the saved model with various inputs"""
    print("=== Testing Saved Model ===\n")
    
    # Initialize detector
    detector = FakeInfluencerDetector()
    
    try:
        # Load the saved model
        detector.load_model('model.pkl')
        print("✅ Model loaded successfully!")
        
        # Test cases
        test_cases = [
            # Clearly risky cases
            ("Get rich quick scheme!", "risky"),
            ("Guaranteed 1000% returns!", "risky"),
            ("Don't miss this opportunity!", "risky"),
            
            # Clearly safe cases
            ("Diversify your investments.", "safe"),
            ("Consult a financial advisor.", "safe"),
            ("Consider long-term strategies.", "safe"),
            
            # Edge cases
            ("This might be interesting.", "safe"),
            ("Investment opportunity here.", "safe"),
        ]
        
        print("\nTesting model predictions...\n")
        
        correct_predictions = 0
        total_predictions = len(test_cases)
        
        for text, expected in test_cases:
            prediction, probability = detector.predict([text])
            confidence = max(probability[0])
            
            # Determine if prediction is correct
            is_correct = prediction[0] == expected
            if is_correct:
                correct_predictions += 1
                status = "✅"
            else:
                status = "❌"
            
            print(f"{status} Text: {text}")
            print(f"   Expected: {expected.upper()}")
            print(f"   Predicted: {prediction[0].upper()}")
            print(f"   Confidence: {confidence:.1%}")
            print()
        
        # Calculate accuracy
        accuracy = correct_predictions / total_predictions
        print(f"Test Results: {correct_predictions}/{total_predictions} correct ({accuracy:.1%})")
        
        if accuracy >= 0.7:
            print("🎉 Model is working well!")
        else:
            print("⚠️  Model may need improvement")
            
    except FileNotFoundError:
        print("❌ Error: model.pkl not found!")
        print("Please run 'fake_influencer_detector.py' first to train and save the model.")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_model()
