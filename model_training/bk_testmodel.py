import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

# Path to the merged model folder downloaded from Google Drive
model_path = "./model_nlp_merged_small"

# Load tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)

# Load model with float32 to ensure CPU compatibility
model = AutoModelForCausalLM.from_pretrained(
    model_path,
    torch_dtype=torch.float32,
    device_map=None
).to("cpu")

# Run inference
prompt = "Generate a clause about data privacy including consent, transfer, and personal data."
inputs = tokenizer(prompt, return_tensors="pt").to("cpu")

with torch.no_grad():
    outputs = model.generate(
        **inputs,
        max_length=300,
        temperature=0.7,
        top_p=0.95,
        do_sample=True
    )

# Decode output
generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
print("\nGenerated Clause:\n")
print(generated_text)
