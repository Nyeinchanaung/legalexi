from jinja2 import Environment, FileSystemLoader

# Set up the Jinja2 environment to load templates from the 'templates' folder
env = Environment(loader=FileSystemLoader('templates'))

def render_contract(contract_type, data):
    # Map contract types to their template files
    template_mapping = {
        "NDA": "nda_template.jinja",
        "Employment Agreement": "employment_template.jinja"
        # Add more contract types as needed
    }
    
    if contract_type not in template_mapping:
        raise ValueError(f"Unsupported contract type: {contract_type}")
    
    # Load the template and render it with the data
    template_name = template_mapping[contract_type]
    template = env.get_template(template_name)
    return template.render(data)

# sample_data = {
#     "effective_date": "2023-11-01",
#     "disclosing_party": "Company A",
#     "disclosing_party_address": "123 Main St",
#     "receiving_party": "Company B",
#     "receiving_party_address": "456 Elm St",
#     "signature_date": "2023-11-02"
# }

# rendered = render_contract("NDA", sample_data)
# print(rendered)  # Or save to a file to review