# utils.py
import re
import spacy
from typing import List, Dict, Tuple, Any

# Define patterns for various entities
PATTERNS = {
    "email": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
    "phone_number": r'(\+\d{1,3}[-\.\s])?\(?\d{3}\)?[-\.\s]?\d{3}[-\.\s]?\d{4}|\+\d{1,3}[-\.\s]\d{1,4}[-\.\s]\d{1,4}[-\.\s]\d{1,4}',
    "dob": r'\b\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4}\b',
    "aadhar_num": r'\b\d{4}\s\d{4}\s\d{4}\b|\b\d{12}\b',
    "credit_debit_no": r'\b(?:\d{4}[- ]?){3}\d{4}\b|\b\d{16}\b',
    "cvv_no": r'\bCVV\s*:?\s*\d{3,4}\b|\bcvv\s*:?\s*\d{3,4}\b|\bCVV\s*number\s*:?\s*\d{3,4}\b|\bcvv\s*number\s*:?\s*\d{3,4}\b',
    "expiry_no": r'\b(0[1-9]|1[0-2])[\/\-](\d{2}|\d{4})\b|\bexpiry\s*:?\s*(0[1-9]|1[0-2])[\/\-](\d{2}|\d{4})\b'
}

def extract_entities(text: str, nlp_en, nlp_de) -> List[Dict[str, Any]]:
    """
    Extract all entities from the text using regex patterns and NER
    
    Args:
        text: Email text
        nlp_en: English language model
        nlp_de: German language model
        
    Returns:
        List of dictionaries containing entity information
    """
    entities = []
    
    # Check language - simple check for German characters
    is_german = any(char in text for char in 'äöüÄÖÜß')
    
    # Use appropriate NLP model
    nlp = nlp_de if is_german else nlp_en
    
    # Process with spaCy for names
    doc = nlp(text)
    
    # Extract names using NER
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            # Check if this looks like a full name (at least two parts)
            if len(ent.text.split()) > 1:
                start_idx = text.find(ent.text)
                if start_idx != -1:
                    entities.append({
                        "position": [start_idx, start_idx + len(ent.text)],
                        "classification": "full_name",
                        "entity": ent.text
                    })
    
    # Extract from specific patterns like "My name is..."
    name_patterns = [
        r'(?:my name is|I am|I\'m|This is) ([A-Z][a-z]+ [A-Z][a-z]+)',
        r'(?:mein Name ist|Ich bin|das ist) ([A-Z][a-z]+ [A-Z][a-z]+)'
    ]
    
    for pattern in name_patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            name = match.group(1)
            start_idx = match.start(1)
            entities.append({
                "position": [start_idx, start_idx + len(name)],
                "classification": "full_name",
                "entity": name
            })
    
    # Extract other entities using regex
    for entity_type, pattern in PATTERNS.items():
        matches = re.finditer(pattern, text)
        for match in matches:
            entity_value = match.group(0)
            start_idx = match.start()
            entities.append({
                "position": [start_idx, start_idx + len(entity_value)],
                "classification": entity_type,
                "entity": entity_value
            })
    
    # Sort entities by position
    entities.sort(key=lambda x: x["position"][0])
    
    return entities

def mask_pii(text: str, nlp_en, nlp_de) -> Tuple[str, List[Dict[str, Any]]]:
    """
    Mask PII in the text
    
    Args:
        text: Email text
        nlp_en: English language model
        nlp_de: German language model
        
    Returns:
        Masked text and a list of extracted entities
    """
    entities = extract_entities(text, nlp_en, nlp_de)
    
    # Sort entities in reverse order to avoid index shifting when replacing
    entities_reversed = sorted(entities, key=lambda x: x["position"][0], reverse=True)
    
    masked_text = text
    for entity in entities_reversed:
        start, end = entity["position"]
        entity_type = entity["classification"]
        masked_text = masked_text[:start] + f"[{entity_type}]" + masked_text[end:]
    
    return masked_text, entities