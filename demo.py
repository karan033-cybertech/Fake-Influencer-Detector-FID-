from fake_influencer_detector import FakeInfluencerDetector

def demo_usage():
    """Demonstrate how to use the saved model"""
    print("=== Fake Influencer Detector Demo ===\n")
    
    # Initialize detector
    detector = FakeInfluencerDetector()
    
    try:
        # Load the saved model
        detector.load_model('model.pkl')
        
        # Test with some new examples
        test_texts = [
            "This investment opportunity will make you rich beyond your wildest dreams!",
            "Consider consulting with a certified financial planner for retirement planning.",
            "Don't wait! This is your last chance to get in on the ground floor!",
            "Diversify your investments across different asset classes to manage risk.",
            "I'm not a financial advisor, but this investment is guaranteed to work!",
            "Research thoroughly before making any investment decisions.",
            "Join my exclusive investment group for insider tips and massive profits!",
            "Focus on long-term investment strategies rather than short-term gains."
        ]
        
        print("Analyzing investment-related text for fake influencer red flags...\n")
        
        # Make predictions
        predictions, probabilities = detector.predict(test_texts)
        
        # Display results
        for i, (text, pred, prob) in enumerate(zip(test_texts, predictions, probabilities)):
            confidence = max(prob)
            risk_level = "🚨 HIGH RISK" if pred == "risky" else "✅ SAFE"
            
            print(f"Text {i+1}: {text}")
            print(f"Assessment: {risk_level}")
            print(f"Confidence: {confidence:.1%}")
            print("-" * 80)
        
        print("\n=== Analysis Complete ===")
        print("The model has successfully identified potentially risky vs. safe investment advice!")
        
    except FileNotFoundError:
        print("Error: model.pkl not found!")
        print("Please run 'fake_influencer_detector.py' first to train and save the model.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    demo_usage()
