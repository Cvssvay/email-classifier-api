# models.py
import pickle
import os
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
import pandas as pd

def train_classifier(data_path='combined_emails_with_natural_pii.csv'):
    """
    Train a classifier on email data from CSV
    
    Args:
        data_path: Path to the CSV file containing email data
        
    Returns:
        Trained classifier and vectorizer
    """
    # Load data
    try:
        print(f"Loading data from {data_path}...")
        df = pd.read_csv(data_path)
        
        # Check and rename columns if needed
        if 'email' in df.columns and 'type' in df.columns:
            print("Renaming columns to match expected format...")
            df = df.rename(columns={'email': 'email_text', 'type': 'email_type'})
        
        print(f"Loaded {len(df)} emails for training")
        
    except Exception as e:
        print(f"Error loading CSV: {e}")
        # Fallback to default examples if CSV loading fails
        print("Using default examples for training...")
        examples = [
            {"email_type": "Incident", "email_text": "Die Datenanalyse-Plattform brach unerwartet ab, da die SpeicheroberflÃ¤che zu gering war"},
            {"email_type": "Request", "email_text": "I am contacting you to request information on data analytics tools that can be utilized with the Eclipse IDE for enhancing investment optimization."},
            {"email_type": "Problem", "email_text": "The integration stopped working unexpectedly, causing synchronization errors between our platforms."},
            {"email_type": "Request", "email_text": "I am seeking suggestions for tools that can aid in making data-driven decisions."},
            {"email_type": "Incident", "email_text": "Ein Medien-Daten-Sperrverhalten trat aufgrund unerlaubten Zugriffes auf."},
            {"email_type": "Request", "email_text": "Inquiring about best practices for securing medical data on a 2-in-1 Convertible Laptop."}
        ]
        df = pd.DataFrame(examples)
    
    # Prepare data
    X = df['email_text'].values
    y = df['email_type'].values
    
    print(f"Training with {len(X)} samples across {len(np.unique(y))} categories")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Creating TF-IDF vectorizer and Random Forest classifier...")
    # Create pipeline
    vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1, 2))
    classifier = RandomForestClassifier(n_estimators=200, random_state=42)
    
    # Train
    print("Fitting vectorizer on training data...")
    X_train_vec = vectorizer.fit_transform(X_train)
    
    print("Training the classifier...")
    classifier.fit(X_train_vec, y_train)
    
    # Save model
    print("Saving trained model and vectorizer...")
    with open('email_classifier.pkl', 'wb') as f:
        pickle.dump(classifier, f)
    
    with open('vectorizer.pkl', 'wb') as f:
        pickle.dump(vectorizer, f)
    
    # Evaluate
    X_test_vec = vectorizer.transform(X_test)
    accuracy = classifier.score(X_test_vec, y_test)
    print(f"Classifier accuracy: {accuracy:.4f}")
    
    return classifier, vectorizer

def load_classifier(csv_path=None):
    """
    Load the trained classifier and vectorizer or train new ones if needed
    
    Args:
        csv_path: Optional path to CSV file for training
        
    Returns:
        Tuple of (classifier, vectorizer)
    """
    try:
        print("Attempting to load pre-trained classifier and vectorizer...")
        with open('email_classifier.pkl', 'rb') as f:
            classifier = pickle.load(f)
        
        with open('vectorizer.pkl', 'rb') as f:
            vectorizer = pickle.load(f)
        
        print("Successfully loaded pre-trained models")
        
    except FileNotFoundError:
        print("Pre-trained models not found. Training new models...")
        if csv_path and os.path.exists(csv_path):
            print(f"Training with provided CSV file: {csv_path}")
            classifier, vectorizer = train_classifier(csv_path)
        else:
            print("CSV file not found. Training with default examples.")
            classifier, vectorizer = train_classifier()
    
    return classifier, vectorizer

def predict_category(email_text, classifier, vectorizer):
    """
    Predict the category of an email
    
    Args:
        email_text: Text of the email
        classifier: Trained classifier
        vectorizer: Trained vectorizer
        
    Returns:
        Predicted category
    """
    # Transform text
    X = vectorizer.transform([email_text])
    
    # Predict
    prediction = classifier.predict(X)[0]
    
    return prediction

# Map of categories (can be expanded)
EMAIL_CATEGORIES = {
    "Incident": "Incident report about a system or service failure",
    "Request": "Request for information or service",
    "Problem": "Problem with existing service or product",
    "Technical Support": "Technical issues requiring expert assistance",
    "Billing Issues": "Issues related to billing or payments",
    "Account Management": "Requests related to account operations"
}