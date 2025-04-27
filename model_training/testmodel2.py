import os
import warnings

os.environ["BITSANDBYTES_NOWARNING"] = "1"
warnings.filterwarnings("ignore")

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel

base_model_name = "../models/model_nlp_merged_small" 
lora_adapter_path = "../models/legal_clause_lora_adapter"

print("🔵 Loading Base Model...")
tokenizer = AutoTokenizer.from_pretrained(base_model_name, trust_remote_code=True)
base_model = AutoModelForCausalLM.from_pretrained(
    base_model_name,
    torch_dtype=torch.float32,
    device_map=None
)
print("✅ Loaded base model.")

print("🔵 Loading LoRA Adapter...")
model = PeftModel.from_pretrained(base_model, lora_adapter_path)
print("✅ LoRA adapter loaded and attached to base model.")

# ------------------ 3. Final Perfect Prompt Builder ------------------
def build_clause_prompt_template(party1, party2, date, duration, clause_type, agreement_type):
    examples = {
        "confidentiality": (
            "{party1} (Disclosing Party) and {party2} (Receiving Party) agree that all confidential information disclosed as of {date} shall remain protected for a period of {duration}. "
            "The Receiving Party shall not disclose, copy, or use any confidential information without prior written consent from the Disclosing Party. "
            "Reasonable efforts shall be made by the Receiving Party to maintain the confidentiality of such information."
        ),
        "termination": (
            "{party1} and {party2} agree that this agreement may be terminated effective from {date} by providing written notice under the agreed conditions. "
            "Either party may terminate the agreement upon material breach by the other party, subject to any cure periods specified herein. "
            "Termination shall not relieve either party of any obligations accrued prior to the date of termination."
        ),
        "payment": (
            "{party1} (Employee) shall receive salary payments from {party2} (Employer) effective from {date}. "
            "Payments shall be made monthly, in accordance with the Employer's standard payroll practices, subject to applicable deductions. "
            "Adjustments to salary or benefits will be communicated in writing."
        ),
        "non_compete": (
            "{party1} agrees not to engage, directly or indirectly, in any competing business activities with {party2} effective from {date} for a period of {duration}. "
            "This restriction includes providing services to competitors or starting a competing business. "
            "Violation of this non-compete clause shall entitle {party2} to seek injunctive relief."
        ),
        "data_privacy": (
            "{party1} and {party2} agree to protect all personal and confidential data shared between the parties, effective from {date}. "
            "No data shall be transferred, disclosed, or used without prior consent, except as required by law. "
            "The Receiving Party shall implement reasonable security measures to protect such data during and after the term of this agreement."
        )
    }

    if clause_type not in examples:
        raise ValueError(f"Unsupported clause_type '{clause_type}'.")

    example_text = examples[clause_type].format(party1=party1, party2=party2, date=date, duration=duration)

    prompt = (
        f"### Example Clause:\n"
        f"{example_text}\n\n"
        f"### Instruction:\n"
        f"You are drafting a {clause_type.replace('_', ' ')} clause.\n"
        f"- Start the paragraph by mentioning '{party1} (Disclosing Party)' and '{party2} (Receiving Party)'.\n"
        f"- Write in formal legal English.\n"
        f"- Do NOT create any heading or title.\n"
        f"- Only 3–5 complete sentences.\n"
        f"- Focus on confidentiality/data/privacy/termination/payment/non-compete terms only.\n"
        f"- Avoid repeating the same point twice.\n"
        f"- Use the Effective Date: {date}, and mention the confidentiality period or duration.\n\n"
        f"Now, write the full legal clause paragraph accordingly.\n\n"
        f"### Response:\n"
    )
    return prompt


# ------------------ 4. Inference Function ------------------
def generate_legal_clause(party1, party2, date, duration, clause_type, agreement_type):
    prompt = build_clause_prompt_template(party1, party2, date, duration, clause_type, agreement_type)
    inputs = tokenizer(prompt, return_tensors="pt").to("cpu")
    
    model.eval()
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=180,
            temperature=0.1,
            top_p=0.85,
            do_sample=True,
            repetition_penalty=1.05,
            no_repeat_ngram_size=3,
            pad_token_id=tokenizer.eos_token_id,
            eos_token_id=tokenizer.eos_token_id
        )

    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()

    # Remove echoed prompt if present
    if generated_text.lower().startswith(prompt.lower()):
        generated_text = generated_text[len(prompt):].strip()

    # ✨ Cut after 5 sentences maximum
    sentences = generated_text.split(".")
    if len(sentences) > 5:
        generated_text = ".".join(sentences[:5]).strip() + "."

    return generated_text

# ------------------ 5. Example Usage ------------------

# Example User Input
user_input = {
    "party1": "AlphaCorp",
    "party2": "BetaTech",
    "date": "2024-01-01",
    "duration": "2 years",
    "clause_type": "confidentiality",
    "agreement_type": "NDA"
}

# Generate Clause
generated_clause = generate_legal_clause(
    party1=user_input["party1"],
    party2=user_input["party2"],
    date=user_input["date"],
    duration=user_input["duration"],
    clause_type=user_input["clause_type"],
    agreement_type=user_input["agreement_type"]
)

# Print Result
print("\n✅ Generated Legal Clause:\n")
print(generated_clause)
