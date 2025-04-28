# helpers.py
import spacy
from spacy.matcher import Matcher
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline, GPT2Tokenizer, GPT2LMHeadModel
import torch
from peft import PeftModel
import re

nlp = spacy.load("en_core_web_sm")
# Path to the merged model (adjust for DigitalOcean deployment if needed)
gen_model_path = "models/best_legal_bert_contract_classifier_unknow"  # Hugging Face repo for deployment
# For local testing: model_path = "./model_nlp_merged_small"

# Load model with float32 for CPU compatibility
try:
    gen_model = AutoModelForCausalLM.from_pretrained(
        gen_model_path,
        torch_dtype=torch.float32,
        device_map=None
    ).to("cpu")
    print("Model loaded on CPU.")
except Exception as e:
    print(f"Error loading model: {e}")
    raise

# Load tokenizer separately
tokenizer = AutoTokenizer.from_pretrained(
    "Qwen/Qwen1.5-0.5B-Chat",
    trust_remote_code=True
)

# Load base model
print("🔵 Loading Base Model...")
model = AutoModelForCausalLM.from_pretrained(
    "Qwen/Qwen1.5-0.5B-Chat",
    trust_remote_code=True,
    device_map="auto",
    torch_dtype=torch.bfloat16,   # assuming you trained with bf16
)
print("✅ Base Model Loaded.")
# Load LoRA Adapter
print("🔵 Loading LoRA Adapter...")
model = PeftModel.from_pretrained(
    model,
    "models/qwen_lora_adapter"  # your adapter folder
)
print("✅ LoRA Adapter Loaded and Attached.")

# Keyward Matching for Contract Types
# This is a simple heuristic to classify contract types based on keywords.

# def classify_contract_type(prompt):
#     prompt = prompt.lower()
#     if "nda" in prompt or "non-disclosure" in prompt:
#         return "NDA"
#     elif "employment" in prompt or "job" in prompt:
#         return "Employment Agreement"
#     elif "service" in prompt or "work" in prompt:
#         return "Service Agreement"
#     return "NDA"

# use of legal bert for contract classification


# tokenizer = AutoTokenizer.from_pretrained("nlpaueb/legal-bert-base-uncased")
# model = AutoModelForSequenceClassification.from_pretrained("nlpaueb/legal-bert-base-uncased", num_labels=3)  # 3 contract types

# def classify_contract_type(prompt):
#     inputs = tokenizer(prompt, return_tensors="pt", truncation=True, padding=True)
#     with torch.no_grad():  # No training, just inference
#         outputs = model(**inputs)
#     logits = outputs.logits
#     predicted_class = torch.argmax(logits, dim=1).item()
#     contract_types = ["NDA", "Employment Agreement", "Service Agreement"]
#     return contract_types[predicted_class]

# Load model and tokenizer
def load_model():
    model_path = "models/best_legal_bert_contract_classifier_unknow"
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    classifier = pipeline(
        "text-classification",
        model=model_path,
        tokenizer=tokenizer,
        device=0 if torch.cuda.is_available() else -1
    )
    return classifier


def classify_contract_type(prompt):
    model = load_model()
    return model(prompt)[0]['label']


def extract_entities(prompt):
    doc = nlp(prompt)
    entities = {"parties": [], "dates": [], "duration": None, "description": None, "salary": None, "position": None}
    
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
    
    # Extract duration (e.g., "2-year", "12 months", etc.)
    # Create a matcher for durations like "2 years", "12 months", etc.
    matcher = Matcher(nlp.vocab)
    pattern = [{"LOWER": {"in": ["year", "month"]}}, {"LIKE_NUM": True}]
    matcher.add("DURATION", [pattern])

    matches = matcher(doc)
    for match_id, start, end in matches:
        span = doc[start:end]
        entities["duration"] = span.text
    
    # Extract salary (looking for numerical values followed by currency, "per month", etc.)
    for ent in doc.ents:
        if ent.label_ == "MONEY":
            entities["salary"] = ent.text
    
    # Extract position (heuristic: noun phrase related to roles or positions)
    for np in doc.noun_chunks:
        # Check for common patterns (e.g., words like "manager", "engineer", etc.)
        if any(role in np.text.lower() for role in ["manager", "engineer", "director", "officer", "developer"]):
            entities["position"] = np.text
    
    # Extract service description (heuristic: noun phrase after "for" or "to")
    for token in doc:
        if token.lower_ in ["for", "to"] and token.head.pos_ == "NOUN":
            description = " ".join(t.text for t in token.head.subtree if t.pos_ in ["NOUN", "ADJ", "VERB"])
            if not any(kw in description.lower() for kw in contract_keywords):
                entities["description"] = description
    
    return entities

required_fields = {
    "Non-Disclosure Agreement (NDA)": ["disclosing_party", "receiving_party", "effective_date", "confidentiality_period"],
    "Employment Contract": ["employee_name", "employer_name", "start_date", "position", "salary"],
    "Service Agreement": ["client_name", "provider_name", "start_date", "end_date", "service_description"],
}

def map_entities_to_fields(contract_type, entities):
    data = {}
    missing = []
    
    # Handle Non-Disclosure Agreement (NDA)
    if contract_type == "Non-Disclosure Agreement (NDA)":
        parties = entities.get("parties", [])
        if parties:
            data["disclosing_party"] = parties[0]
            data["receiving_party"] = parties[1] if len(parties) > 1 else None
        dates = entities.get("dates", [])
        data["effective_date"] = dates[0] if dates else None
        data["confidentiality_period"] = entities.get("duration")  # Duration (e.g., "2 years")
        
    # Handle Employment Contract
    elif contract_type == "Employment Contract":
        parties = entities.get("parties", [])
        if parties:
            data["employee_name"] = parties[0]
            data["employer_name"] = parties[1] if len(parties) > 1 else None
        dates = entities.get("dates", [])
        data["start_date"] = dates[0] if dates else None
        data["position"] = entities.get("position")  # Position (e.g., "Software Engineer")
        data["salary"] = entities.get("salary")  # Salary (e.g., "$80,000 per year")
        
    # Handle Service Agreement
    elif contract_type == "Service Agreement":
        parties = entities.get("parties", [])
        if parties:
            data["client_name"] = parties[0]
            data["provider_name"] = parties[1] if len(parties) > 1 else None
        dates = entities.get("dates", [])
        data["start_date"] = dates[0] if dates else None
        data["end_date"] = dates[1] if len(dates) > 1 else None
        data["service_description"] = entities.get("description")  # Service description
        
    # Check for missing required fields
    for field in required_fields[contract_type]:
        if not data.get(field):
            missing.append(field)
    
    return data, missing



# dynamic clauses generation
# Load your legal BERT model for dynamic clause generation

# def generate_dynamic_clauses(contract_type, data):
#     # Load GPT-2 for clause generation
#     gpt2_tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
#     gpt2_model = GPT2LMHeadModel.from_pretrained("gpt2")
#     clauses = {}
#     if contract_type == "Non-Disclosure Agreement (NDA)":
#         # Example using your legal gtp2 model
#         inputs = gpt2_tokenizer(
#             f"Generate confidentiality definition for {data['disclosing_party']} and {data['receiving_party']}",
#             return_tensors="pt"
#         )
#         outputs = gpt2_model.generate(inputs)
#         clauses['definition'] = gpt2_tokenizer.decode(outputs[0], skip_special_tokens=True)
        
#     elif contract_type == "Employment Agreement":
#         # Similar logic for employment terms
#         pass
        
#     return clauses

# helpers.py (update the clause_prompts dictionary)
# def generate_dynamic_clauses(contract_type, clause_type, data=None):
#     data = data or {}
#     party1 = data.get("disclosing_party") or data.get("employee_name") or data.get("client_name") or "Party A"
#     party2 = data.get("receiving_party") or data.get("employer_name") or data.get("provider_name") or "Party B"
#     date = data.get("effective_date") or data.get("start_date") or "the effective date"
#     duration = data.get("confidentiality_period") or data.get("end_date") or "the term of this agreement"

#     clause_prompts = {
#         "confidentiality": {
#             "NDA": f"Generate a confidentiality clause for an NDA between {party1} (Disclosing Party) and {party2} (Receiving Party), effective from {date}, with a confidentiality period of {duration}.",
#             "Employment Agreement": f"Generate a confidentiality clause for an Employment Agreement between {party1} (Employee) and {party2} (Employer), effective from {date}.",
#             "Service Agreement": f"Generate a confidentiality clause for a Service Agreement between {party1} (Client) and {party2} (Provider), effective from {date} until {duration}."
#         },
#         "termination": {
#             "NDA": f"Generate a termination clause for an NDA between {party1} and {party2}, effective from {date}, specifying conditions for termination.",
#             "Employment Agreement": f"Generate a termination clause for an Employment Agreement between {party1} (Employee) and {party2} (Employer), effective from {date}, including notice period and conditions.",
#             "Service Agreement": f"Generate a termination clause for a Service Agreement between {party1} (Client) and {party2} (Provider), effective from {date} until {duration}, including termination conditions."
#         },
#         "data_privacy": {
#             "NDA": f"Generate a data privacy clause for an NDA between {party1} and {party2}, effective from {date}, including consent, transfer, and protection of personal data.",
#             "Employment Agreement": f"Generate a data privacy clause for an Employment Agreement between {party1} (Employee) and {party2} (Employer), effective from {date}, addressing employee data handling and consent.",
#             "Service Agreement": f"Generate a data privacy clause for a Service Agreement between {party1} (Client) and {party2} (Provider), effective from {date}, covering data sharing, consent, and security measures."
#         },
#         "payment": {
#             "Employment Agreement": f"Generate a payment clause for an Employment Agreement between {party1} (Employee) and {party2} (Employer), effective from {date}, specifying salary and payment schedule.",
#             "Service Agreement": f"Generate a payment clause for a Service Agreement between {party1} (Client) and {party2} (Provider), effective from {date}, detailing payment terms and schedule."
#         },
#         "non_compete": {
#             "NDA": f"Generate a non-compete clause for an NDA between {party1} and {party2}, effective from {date}, restricting {party2} from engaging in competing activities for {duration}.",
#             "Employment Agreement": f"Generate a non-compete clause for an Employment Agreement between {party1} (Employee) and {party2} (Employer), effective from {date}, restricting the Employee from working with competitors for a specified period after termination.",
#             "Service Agreement": f"Generate a non-compete clause for a Service Agreement between {party1} (Client) and {party2} (Provider), effective from {date}, restricting the Provider from offering similar services to competitors for {duration}."
#         }
#     }

#     if clause_type not in clause_prompts or contract_type not in clause_prompts[clause_type]:
#         return f"Error: Clause type '{clause_type}' not supported for {contract_type}."

#     prompt = clause_prompts[clause_type][contract_type]
#     inputs = gen_tokenizer(prompt, return_tensors="pt").to("cpu")
#     with torch.no_grad():
#         outputs = gen_model.generate(
#             **inputs,
#             max_length=300,
#             temperature=0.7,
#             top_p=0.95,
#             do_sample=True
#         )
#     return gen_tokenizer.decode(outputs[0], skip_special_tokens=True)

def build_clause_prompt_template(fields, clause_type, agreement_type):
    # Define examples for each contract type and clause
    examples = {
        "Non-Disclosure Agreement (NDA)": {
            "purpose": (
                "WHEREAS, {disclosing_party} possesses proprietary information relating to its business operations; "
                "and WHEREAS, {disclosing_party} and {receiving_party} desire to explore a potential business relationship."
            ),
            "confidential_information": (
                "Confidential Information shall mean any data or information, oral or written, disclosed by {disclosing_party} to {receiving_party} as of {effective_date}, including but not limited to: "
                "- Information expressly marked as confidential; "
                "- Trade secrets, business plans, and technical data; "
                "- Any information the Receiving Party should reasonably consider confidential."
            ),
            "obligations": (
                "{receiving_party} (Receiving Party) shall, effective from {effective_date}: "
                "- Hold the Confidential Information in strict confidence; "
                "- Not disclose such information without prior written consent from {disclosing_party}; "
                "- Use the information solely for the purpose of the agreement."
            ),
            "term": (
                "This Agreement shall remain in effect for {confidentiality_period} from the Effective Date of {effective_date}, unless terminated earlier by mutual agreement."
            ),
            "termination": (
                "Upon termination effective from {effective_date}, {receiving_party} shall cease use of Confidential Information and, within thirty (30) days, return or destroy all materials provided by {disclosing_party}."
            ),
            "non_compete": (
                "{receiving_party} shall not engage in activities competitive with {disclosing_party}’s business for one (1) year post-termination, effective from {effective_date}."
            ),
            "governing_law": (
                "This Agreement is governed by the laws of the Country of Thailand."
            ),
            "data_privacy": (
                "{receiving_party} shall comply with applicable data protection laws when handling Confidential Information shared by {disclosing_party} as of {effective_date}."
            ),
        },
        "Employment Contract": {
            "position_and_duties": (
                "{employee_name} shall serve as {position} and perform duties as directed by {employer_name}, effective from {start_date}."
            ),
            "compensation": (
                "{employer_name} shall pay {employee_name} a salary of {salary} per annum, payable monthly, effective from {start_date}, subject to applicable deductions."
            ),
            "term_of_employment": (
                "Employment shall commence on {start_date} and continue until terminated by either party in accordance with this Agreement."
            ),
            "confidentiality": (
                "{employee_name} shall not disclose confidential information of {employer_name} during or after employment, effective from {start_date}."
            ),
            "termination": (
                "Either {employer_name} or {employee_name} may terminate this Agreement with thirty (30) days’ written notice, effective from {start_date}, or immediately for cause."
            ),
            "non_compete": (
                "{employee_name} shall not engage in competitive activities within the same industry as {employer_name} for one (1) year after termination, effective from {start_date}."
            ),
            "governing_law": (
                "This Agreement is governed by the laws of the Country of Thailand."
            ),
            "benefits": (
                "{employee_name} is entitled to health insurance and {vacation_days} vacation days as per {employer_name}’s policies, effective from {start_date}."
            ),
        },
        "Service Agreement": {
            "scope_of_services": (
                "{provider_name} shall provide the following services to {client_name}, effective from {start_date}: "
                "- {service_description}; "
                "- Additional services as mutually agreed."
            ),
            "term_of_agreement": (
                "This Agreement shall commence on {start_date} and continue until {end_date}, unless terminated earlier."
            ),
            "payment_terms": (
                "{client_name} shall pay {provider_name} for services rendered, effective from {start_date}, per the agreed schedule."
            ),
            "confidentiality": (
                "{provider_name} shall not disclose confidential information of {client_name} obtained during the performance of services, effective from {start_date}."
            ),
            "termination": (
                "Either {client_name} or {provider_name} may terminate this Agreement with thirty (30) days’ written notice, effective from {start_date}, or immediately for material breach."
            ),
            "indemnification": (
                "{provider_name} shall indemnify {client_name} against claims arising from the performance of services, effective from {start_date}."
            ),
            "governing_law": (
                "This Agreement is governed by the laws of the Country of Thailand."
            ),
            "independent_contractor_status": (
                "{provider_name} is an independent contractor and not an employee of {client_name}, effective from {start_date}."
            ),
        },
    }

    # Validate agreement_type and clause_type
    if agreement_type not in examples or clause_type not in examples[agreement_type]:
        raise ValueError(f"Unsupported agreement_type '{agreement_type}' or clause_type '{clause_type}'.")

    # Format the example text with provided fields
    try:
        example_text = examples[agreement_type][clause_type].format(**fields)
    except KeyError as e:
        raise ValueError(f"Missing required field: {e}")

    # Build the prompt
    prompt = (
        f"### Example Clause:\n"
        f"{example_text}\n\n"
        f"### Instruction:\n"
        f"You are drafting a {clause_type.replace('_', ' ')} clause for a {agreement_type}.\n"
        f"- Write in formal legal English.\n"
        f"- Do NOT include any headings or titles.\n"
        f"- Bullet point with correct number if necessary for clarity (e.g., for lists of obligations or services).\n"
        f"- END the clause formally and completely.\n"
        f"- DO NOT add address or location.\n"
        f"- Avoid redundancy and repetition.\n"
        f"- Incorporate the following details where applicable:\n"
        f"  - Parties: {fields.get('party1', '')} and {fields.get('party2', '')}\n"
        f"  - Effective Date: {fields.get('effective_date', fields.get('start_date', ''))}\n"
        f"  - Duration/Period: {fields.get('confidentiality_period', fields.get('end_date', ''))}\n"
        f"Now, write the full legal clause paragraph accordingly.\n\n"
        f"### Response:\n"
    )
    # prompt = (
    #     f"### Example Clause:\n"
    #     f"{example_text}\n\n"
    #     f"### Instruction:\n"
    #     f"You are drafting a {clause_type.replace('_', ' ')} clause for a {agreement_type}.\n"
    #     f"- Write in formal legal English.\n"
    #     f"- Do NOT include any headings or titles.\n"
    #     f"- END the clause completely.\n"
    #     f"- DO NOT add address or location.\n"
    #     f"- Avoid redundancy and repetition.\n"
    #     f"Now, write the full legal clause sentence by setence accordingly.\n\n"
    #     f"### Response:\n"
    # )

    print("Example Text:\n", example_text, "\nPrompt:\n", prompt)
    return prompt

def generate_legal_clause(fields, clause_type, agreement_type):
    prompt = build_clause_prompt_template(fields, clause_type, agreement_type)

    inputs = tokenizer(prompt, return_tensors="pt").to("cpu")
    inputs = {k: v.to(model.device) for k, v in inputs.items()}
    
    model.eval()
    with torch.no_grad():
    # Generate output based on input
        outputs = model.generate(
            **inputs,                           # input_ids and attention_mask from the tokenizer
            max_new_tokens=256,                 # limit the number of tokens generated
            num_beams=4,                        # use beam search for better quality
            do_sample=True,                     # enable sampling (for more diverse outputs)
            temperature=0.5,                    # adjust temperature for creativity (lower = more deterministic)
            top_p=0.9,                          # nucleus sampling (keep top 90% probability mass)
            eos_token_id=tokenizer.eos_token_id, # end-of-sequence token to stop generation
            pad_token_id=tokenizer.pad_token_id, # padding token for correct handling
            early_stopping=True                 # stop early if beam search reaches end
        )
    
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()

    # Remove echoed prompt if present
    if generated_text.lower().startswith(prompt.lower()):
        generated_text = generated_text[len(prompt):].strip()

    # Remove any headings or titles from the generated text
    generated_text = "\n".join(line for line in generated_text.split("\n") if not (line.isupper() or line.endswith(":"))).strip()
    print("Generated Text:\n", generated_text)
    generated_text = clean_text(generated_text)
    print("Cleaned Text:\n", generated_text)
    return generated_text


def clean_text(text):
    # # Process the text using spaCy
    # doc = nlp(text)

    # # Split the text into sentences
    # sentences = list(doc.sents)
    
    # # Remove empty numbered sentences (e.g., "2." with no content after it)
    # sentences = [sent for sent in sentences if not (sent.text.strip().isdigit() or (sent.text.strip()[0].isdigit() and len(sent.text.strip()) <= 3))]

    # # Rebuild the text with bullet points and numbered sentences
    # cleaned_text = "<ul>"

    # for sent in sentences:
    #     sentence_text = sent.text.strip()

    #     # Check if the sentence ends with a colon (e.g., "Job Title and Responsibilities:")
    #     if sentence_text.endswith(":"):
    #         # Make the part before the colon bold
    #         part_before_colon = sentence_text.split(":", 1)[0]
    #         part_after_colon = sentence_text.split(":", 1)[1].strip()
    #         cleaned_text += f"<li><strong>{part_before_colon}:</strong> {part_after_colon}</li>"
    #     elif sentence_text and sentence_text[0].isdigit() and sentence_text[1] == ".":
    #         # For numbered sentences, retain the number and add it as part of the list item
    #         cleaned_text += f"<li>{sentence_text}</li>"
    #     else:
    #         # For unnumbered sentences, add a bullet point
    #         cleaned_text += f"<li>{sentence_text}</li>"

    # cleaned_text += "</ul>"
    
    # return cleaned_text
    
    # Normalize input text
    # Load spaCy English model
    nlp = spacy.load("en_core_web_sm")
    
    # Process the text with spaCy
    doc = nlp(text)
    
    # Get all sentences
    sentences = list(doc.sents)
    
    # If no sentences or only one sentence, return original text
    if len(sentences) <= 1:
        return text.strip()
    
    # Get the last sentence
    last_sentence = sentences[-1]
    
    # Check if the last sentence is incomplete
    # An incomplete sentence might lack a verb or end abruptly
    has_verb = any(token.pos_ == "VERB" for token in last_sentence)
    ends_with_punctuation = last_sentence.text.strip()[-1] in ".!?"
    
    # If the last sentence has no verb or doesn't end with punctuation, remove it
    if not has_verb or not ends_with_punctuation:
        # Reconstruct the text without the last sentence
        return text[:last_sentence.start_char].strip()
    
    # If the last sentence is complete, return the original text
    return text.strip()