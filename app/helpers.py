# helpers.py
import spacy
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# Keyward Matching for Contract Types
# This is a simple heuristic to classify contract types based on keywords.

def classify_contract_type(prompt):
    prompt = prompt.lower()
    if "nda" in prompt or "non-disclosure" in prompt:
        return "NDA"
    elif "employment" in prompt or "job" in prompt:
        return "Employment Agreement"
    elif "service" in prompt or "work" in prompt:
        return "Service Agreement"
    return "NDA"

# use of legal bert for contract classification


nlp = spacy.load("en_core_web_sm")
tokenizer = AutoTokenizer.from_pretrained("nlpaueb/legal-bert-base-uncased")
model = AutoModelForSequenceClassification.from_pretrained("nlpaueb/legal-bert-base-uncased", num_labels=3)  # 3 contract types

# def classify_contract_type(prompt):
#     inputs = tokenizer(prompt, return_tensors="pt", truncation=True, padding=True)
#     with torch.no_grad():  # No training, just inference
#         outputs = model(**inputs)
#     logits = outputs.logits
#     predicted_class = torch.argmax(logits, dim=1).item()
#     contract_types = ["NDA", "Employment Agreement", "Service Agreement"]
#     return contract_types[predicted_class]

def extract_entities(prompt):
    doc = nlp(prompt)
    entities = {"parties": [], "dates": [], "duration": None, "description": None}
    
    # Contract type keywords to exclude from entities
    contract_keywords = ["nda", "non-disclosure", "employment", "job", "service", "work", "agreement"]
    
    # Extract parties (ORG or PERSON, excluding contract keywords)
    for ent in doc.ents:
        text = ent.text.lower()
        if ent.label_ in ["ORG", "PERSON"] and not any(kw in text for kw in contract_keywords):
            entities["parties"].append(ent.text)
    
    # Extract dates
    for ent in doc.ents:
        if ent.label_ == "DATE":
            entities["dates"].append(ent.text)
    
    # Extract duration (e.g., "2-year")
    for token in doc:
        if token.text.endswith("-year"):
            entities["duration"] = token.text
    
    # Extract service description (heuristic: noun phrase after "for" or "to")
    for token in doc:
        if token.lower_ in ["for", "to"] and token.head.pos_ == "NOUN":
            description = " ".join(t.text for t in token.head.subtree if t.pos_ in ["NOUN", "ADJ", "VERB"])
            if not any(kw in description.lower() for kw in contract_keywords):
                entities["description"] = description
    
    return entities

required_fields = {
    "NDA": ["disclosing_party", "receiving_party", "effective_date", "confidentiality_period"],
    "Employment Agreement": ["employee_name", "employer_name", "start_date", "position", "salary"],
    "Service Agreement": ["client_name", "provider_name", "start_date", "end_date", "service_description"]
}

def map_entities_to_fields(contract_type, entities):
    data = {}
    missing = []
    if contract_type == "NDA":
        parties = entities.get("parties", [])
        if parties:
            data["disclosing_party"] = parties[0]
            data["receiving_party"] = parties[1] if len(parties) > 1 else None
        dates = entities.get("dates", [])
        data["effective_date"] = dates[0] if dates else None
        data["confidentiality_period"] = entities.get("duration")
    elif contract_type == "Employment Agreement":
        parties = entities.get("parties", [])
        if parties:
            data["employee_name"] = parties[0]
            data["employer_name"] = parties[1] if len(parties) > 1 else None
        dates = entities.get("dates", [])
        data["start_date"] = dates[0] if dates else None
    elif contract_type == "Service Agreement":
        parties = entities.get("parties", [])
        if parties:
            data["client_name"] = parties[0]
            data["provider_name"] = parties[1] if len(parties) > 1 else None
        dates = entities.get("dates", [])
        data["start_date"] = dates[0] if dates else None
        data["end_date"] = dates[1] if len(dates) > 1 else None
        data["service_description"] = entities.get("description")
    for field in required_fields[contract_type]:
        if not data.get(field):
            missing.append(field)
    return data, missing