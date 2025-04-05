# helpers.py
import spacy

nlp = spacy.load("en_core_web_sm")

def classify_contract_type(prompt):
    prompt = prompt.lower()
    if "nda" in prompt or "non-disclosure" in prompt:
        return "NDA"
    elif "employment" in prompt or "job" in prompt:
        return "Employment Agreement"
    elif "service" in prompt or "work" in prompt:
        return "Service Agreement"
    return "NDA"

def extract_entities(prompt):
    doc = nlp(prompt)
    entities = {"parties": [], "dates": [], "duration": None}
    for ent in doc.ents:
        if ent.label_ in ["ORG", "PERSON"]:
            entities["parties"].append(ent.text)
        elif ent.label_ == "DATE":
            entities["dates"].append(ent.text)
    for token in doc:
        if token.text.endswith("-year"):
            entities["duration"] = token.text
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
        if entities["parties"]:
            data["disclosing_party"] = entities["parties"][0]
            data["receiving_party"] = entities["parties"][1] if len(entities["parties"]) > 1 else None
        data["effective_date"] = entities["dates"][0] if entities["dates"] else None
        data["confidentiality_period"] = entities["duration"]
    # Add other contract types as needed
    for field in required_fields[contract_type]:
        if not data.get(field):
            missing.append(field)
    return data, missing