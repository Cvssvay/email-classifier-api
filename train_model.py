# train_model.py
from models import train_classifier
import argparse

def main():
    parser = argparse.ArgumentParser(description='Train Email Classification Model')
    parser.add_argument('--csv', type=str, default='combined_emails_with_natural_pii.csv', 
                        help='Path to CSV file containing email data (default: email_data.csv)')
    
    args = parser.parse_args()
    
    print(f"Training model with data from: {args.csv}")
    classifier, vectorizer = train_classifier(args.csv)
    print("Model training complete!")
    print("The trained model and vectorizer have been saved to the current directory.")
    print("You can now run the API server with: uvicorn api:app --reload")

if __name__ == "__main__":
    main()