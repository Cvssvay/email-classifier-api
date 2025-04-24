# Email Classification System

This project implements an email classification system with PII masking capabilities. The system classifies support emails into different categories while ensuring that personal information is masked before processing.

## Features

- Email classification into categories (Incident, Request, Problem, etc.)
- Personal Information Masking (PII) without using LLMs
- API for processing emails

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/email-classification.git
cd email-classification
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Download the required spaCy models:
```bash
python -m spacy download en_core_web_md
python -m spacy download de_core_news_md
```

## Usage

### Running the API locally

```bash
uvicorn api:app --host 0.0.0.0 --port 8000
```

### Using the API

The API accepts POST requests with a JSON body:

```json
{
  "email_body": "Your email content here"
}
```

Example curl command:

```bash
curl -X POST "http://localhost:8000/" \
     -H "Content-Type: application/json" \
     -d '{"email_body": "Hello, my name is John Doe, and my email is johndoe@example.com. I am experiencing issues with my account."}'
```

### API Response

The API returns a JSON with the following structure:

```json
{
  "input_email_body": "Original email text",
  "list_of_masked_entities": [
    {
      "position": [start_index, end_index],
      "classification": "entity_type",
      "entity": "original_entity_value"
    }
  ],
  "masked_email": "Masked email text",
  "category_of_the_email": "Predicted category"
}
```

## Project Structure

- `app.py`: Main application entry point
- `api.py`: FastAPI implementation
- `models.py`: Classification model training and inference
- `utils.py`: Utility functions for PII masking and entity extraction
- `requirements.txt`: Dependencies

## Deployment

### Deploying to Hugging Face Spaces

1. Create a new Space on Hugging Face
2. Select "Gradio" or "FastAPI" as the Space SDK
3. Connect your GitHub repository
4. Configure the build settings to use the requirements.txt file

## License

This project is licensed under the MIT License - see the LICENSE file for details.