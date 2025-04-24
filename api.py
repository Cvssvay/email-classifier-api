# api.py
from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
import uvicorn
from utils import mask_pii
from models import load_classifier, predict_category
import spacy

# Initialize FastAPI app
app = FastAPI(
    title="Email Classification API",
    description="API for classifying emails and masking PII",
    version="1.0.0"
)

# Load models
try:
    print("Loading spaCy models...")
    nlp_en = spacy.load("en_core_web_md")
    nlp_de = spacy.load("de_core_news_md")
    print("spaCy models loaded successfully")
except:
    # Install if needed
    print("Installing required spaCy models...")
    import os
    os.system("python -m spacy download en_core_web_md")
    os.system("python -m spacy download de_core_news_md")
    nlp_en = spacy.load("en_core_web_md")
    nlp_de = spacy.load("de_core_news_md")
    print("spaCy models installed and loaded successfully")

# Load classifier (check for CSV file)
print("Loading email classifier...")
classifier, vectorizer = load_classifier('combined_emails_with_natural_pii.csv')

class EmailRequest(BaseModel):
    email_body: str

@app.post("/")
async def process_email(request: EmailRequest):
    """
    Process an email: mask PII and classify it
    """
    if not request.email_body:
        raise HTTPException(status_code=400, detail="Email body cannot be empty")
    
    try:
        # Extract and mask PII
        masked_email, entities = mask_pii(request.email_body, nlp_en, nlp_de)
        
        # Classify the masked email
        category = predict_category(masked_email, classifier, vectorizer)
        
        # Format response according to requirements
        response = {
            "input_email_body": request.email_body,
            "list_of_masked_entities": entities,
            "masked_email": masked_email,
            "category_of_the_email": category
        }
        
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing email: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)