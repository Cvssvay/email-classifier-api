FROM python:3.12.5

# Set working directory
WORKDIR /app

# Install dependencies
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt

# Download spaCy models
RUN python -m spacy download en_core_web_md
RUN python -m spacy download de_core_news_md

# Copy app code
COPY . .

# Expose port 7860 (Hugging Face default)
EXPOSE 7860

# Run the FastAPI app with uvicorn
CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "7860"]
