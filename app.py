# -*- coding: utf-8 -*-

from flask import Flask, request, render_template, send_file
from io import BytesIO
import json
from helpers import classify_contract_type, extract_entities, map_entities_to_fields, generate_legal_clause
import pdfkit
from datetime import datetime
import tempfile
import logging
import shutil
import os
import subprocess


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

def generate_missing_fields_message(contract_type, data, missing):
    """Generate a natural language reply for missing fields."""
    if not missing:
        return None
    
    # Base message
    known_party = data.get("disclosing_party") or data.get("employee_name") or data.get("client_name") or "the parties"
    message = f"You would like to generate an {contract_type} contract for {known_party}. I still need some more information. "
    
    # Add specific questions for missing fields
    questions = []
    if "receiving_party" in missing:
        questions.append("Who is the receiving party?")
    if "effective_date" in missing or "start_date" in missing:
        questions.append("What is the effective or start date?")
    if "confidentiality_period" in missing:
        questions.append("What is the confidentiality period?")
    if "position" in missing:
        questions.append("What is the position?")
    if "salary" in missing:
        questions.append("What is the salary?")
    if "end_date" in missing:
        questions.append("What is the end date?")
    if "service_description" in missing:
        questions.append("What is the service description?")
    
    message += " ".join(questions)
    return message

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        prompt = request.form['prompt']
        contract_type = classify_contract_type(prompt)

        if contract_type == "unknown":
            return render_template('index.html', error="Unknown contract type. Please provide a valid contract type in your prompt.")
        else:
            entities = extract_entities(prompt)
            data, missing = map_entities_to_fields(contract_type, entities)
            contract_id = get_contract_id(contract_type)
        
            json_data = json.dumps(data)
            print("Sending to index.html for validation:", {"contract_type": contract_type, "data": data, "missing": missing})
            
            # Generate reply if fields are missing
            reply = generate_missing_fields_message(contract_type, data, missing)
            if reply:
                return render_template('index.html', 
                                    contract_type=contract_type, 
                                    original_data_json=json_data, 
                                    original_data=data, 
                                    missing=missing, 
                                    reply=reply,
                                    contract_id=contract_id,
                                    step="validate")
            else:
                return render_template('index.html', 
                                    contract_type=contract_type, 
                                    original_data_json=json_data, 
                                    original_data=data,
                                    missing=missing,
                                    contract_id=contract_id,
                                    step="validate")
    return render_template('index.html')

# @app.route('/validate', methods=['POST'])
# def validate():
#     contract_type = request.form['contract_type']
#     raw_data = request.form['original_data']
#     print("Received in /validate:", raw_data)
    
#     try:
#         original_data = json.loads(raw_data)
#         print("Parsed original_data:", original_data)
#     except json.JSONDecodeError as e:
#         print("JSONDecodeError:", e, "Raw data:", raw_data)
#         return "Error: Invalid data format", 400
    
#     corrected_data = request.form.to_dict()
#     corrected_data.pop('contract_type')
#     corrected_data.pop('original_data')
#     corrected_data.pop('submit')
    
#     full_data = {**original_data, **corrected_data}
#     missing = [field for field in map_entities_to_fields(contract_type, {})[1] if not full_data.get(field)]
    
#     if missing:
#         json_data = json.dumps(full_data)
#         reply = generate_missing_fields_message(contract_type, full_data, missing)
#         print("Sending to index.html for missing fields:", {"contract_type": contract_type, "data": full_data, "missing": missing})
#         return render_template('index.html', 
#                              contract_type=contract_type, 
#                              original_data_json=json_data, 
#                              original_data=full_data, 
#                              missing=missing, 
#                              reply=reply, 
#                              step="missing")
#     else:
#         print("Collected data before template generation:", full_data)
#         if(contract_type == "Non-Disclosure Agreement (NDA)"):
#             template_name = "nda_template.html"
#             full_data["dynamic_clauses"] = "Dynamic clauses for NDA"
#         elif(contract_type == "Employment Contract"):
#             template_name = "employment_contract.html"
#             full_data["dynamic_clauses"] = "Dynamic clauses for Employment Contract"
#         elif(contract_type == "Service Agreement"):
#             template_name = "employment_contract.html"
#             full_data["dynamic_clauses"] = "Dynamic clauses for Service Agreement"
#         # Add more contract types and their dynamic clauses as needed
#         # Render the appropriate template based on contract type
#         return render_template(template_name, **full_data)

@app.route('/validate', methods=['POST'])
def validate():
    contract_type = request.form['contract_type']
    contract_id = request.form['contract_id']
    raw_data = request.form['original_data']
    print("Received in /validate:", raw_data)
    
    try:
        original_data = json.loads(raw_data)
        print("Parsed original_data:", original_data)
    except json.JSONDecodeError as e:
        print("JSONDecodeError:", e, "Raw data:", raw_data)
        return "Error: Invalid data format", 400
    
    corrected_data = request.form.to_dict()
    corrected_data.pop('contract_type')
    corrected_data.pop('original_data')
    corrected_data.pop('submit')
    
    full_data = {**original_data, **corrected_data}
    missing = [field for field in map_entities_to_fields(contract_type, {})[1] if not full_data.get(field)]
    
    if missing:
        json_data = json.dumps(full_data)
        reply = generate_missing_fields_message(contract_type, full_data, missing)
        print("Sending to index.html for missing fields:", {"contract_type": contract_type, "data": full_data, "missing": missing})
        return render_template('index.html', 
                             contract_type=contract_type, 
                             original_data_json=json_data, 
                             original_data=full_data, 
                             missing=missing, 
                             reply=reply, 
                             contract_id = contract_id,
                             step="missing")
    else:
        json_data = json.dumps(full_data)
        reply = generate_missing_fields_message(contract_type, full_data, missing)
        print("Sending to index.html for missing fields:", {"contract_type": contract_type, "data": full_data})
        return render_template('index.html', 
                             contract_type=contract_type, 
                             original_data_json=json_data, 
                             original_data=full_data, 
                             reply=reply, 
                             contract_id = contract_id,
                             step="template_selection")

    # else:
    #     print("Collected data before template generation:", full_data)
    #     if(contract_type == "Non-Disclosure Agreement (NDA)"):
    #         template_name = "nda_template.html"
    #         full_data["dynamic_clauses"] = "Dynamic clauses for NDA"
    #     elif(contract_type == "Employment Contract"):
    #         template_name = "employment_contract.html"
    #         full_data["dynamic_clauses"] = "Dynamic clauses for Employment Contract"
    #     elif(contract_type == "Service Agreement"):
    #         template_name = "employment_contract.html"
    #         full_data["dynamic_clauses"] = "Dynamic clauses for Service Agreement"
    #     # Add more contract types and their dynamic clauses as needed
    #     # Render the appropriate template based on contract type
    #     return render_template(template_name, **full_data)

@app.route('/generate', methods=['POST'])
def generate():
    contract_type = request.form['contract_type']
    full_data = json.loads(request.form['original_data'])
    template_choice = request.form['template_choice']
    contract_id = request.form['contract_id']

    required_fields = {
        "Non-Disclosure Agreement (NDA)": ["disclosing_party", "receiving_party", "effective_date", "confidentiality_period"],
        "Employment Contract": ["employee_name", "employer_name", "start_date", "position", "salary"],
        "Service Agreement": ["client_name", "provider_name", "start_date", "end_date", "service_description"],
    }

    # Validate required fields
    if contract_type not in required_fields:
        return {"error": f"Unsupported contract type: {contract_type}"}, 400
    missing_fields = [field for field in required_fields[contract_type] if field not in full_data or not full_data[field]]
    if missing_fields:
        return {"error": f"Missing required fields: {', '.join(missing_fields)}"}, 400

    print("Received in /generate:", full_data)

    if template_choice == 'dynamic':
        # Define standard clauses for each contract type
        standard_clauses = {
            "Non-Disclosure Agreement (NDA)": [
                "purpose", "confidential_information", "obligations", "term",
                "termination","non_compete", "governing_law", "data_privacy"
            ],
            "Employment Contract": [
                "position_and_duties", "compensation", "term_of_employment",
                "confidentiality", "termination", "non_compete", "governing_law", "benefits"
            ],
            "Service Agreement": [
                "scope_of_services", "term_of_agreement", "payment_terms",
                "confidentiality", "termination", "indemnification", "governing_law", "independent_contractor_status"
            ],
        }

        # Include optional clauses if fields are provided
        optional_clauses = {
            "Non-Disclosure Agreement (NDA)": ["non_compete"],
            "Employment Contract": ["non_compete"],
            "Service Agreement": ["indemnification"],
        }

        # Build fields dictionary based on contract type
        fields = {}
        dynamic_contract_template = "dynamic_nda_template_1.html"
        if contract_type == "Non-Disclosure Agreement (NDA)":
            fields = {
                "disclosing_party": full_data["disclosing_party"],
                "receiving_party": full_data["receiving_party"],
                "effective_date": full_data["effective_date"],
                "confidentiality_period": full_data["confidentiality_period"],
                "party1": full_data["disclosing_party"],
                "party2": full_data["receiving_party"],
            }
            dynamic_contract_template = "dynamic_nda_template_1.html"
        elif contract_type == "Employment Contract":
            fields = {
                "employee_name": full_data["employee_name"],
                "employer_name": full_data["employer_name"],
                "start_date": full_data["start_date"],
                "position": full_data["position"],
                "salary": full_data["salary"],
                "vacation_days": full_data.get("vacation_days", "15"),  # Default for benefits clause
                "party1": full_data["employee_name"],
                "party2": full_data["employer_name"],
            }
            dynamic_contract_template = "dynamic_emp_template_1.html"
        elif contract_type == "Service Agreement":
            fields = {
                "client_name": full_data["client_name"],
                "provider_name": full_data["provider_name"],
                "start_date": full_data["start_date"],
                "end_date": full_data["end_date"],
                "service_description": full_data["service_description"],
                "party1": full_data["client_name"],
                "party2": full_data["provider_name"],
            }
            dynamic_contract_template = "dynamic_sa_template_1.html"

        # Generate dynamic clauses
        dynamic_clauses = {}
        download =True,
        for clause in standard_clauses[contract_type]:
            dynamic_clauses[clause] = generate_legal_clause(fields, clause, contract_type)

        # Generate optional clauses if fields are provided
        for clause in optional_clauses.get(contract_type, []):
            if full_data.get(clause):
                dynamic_clauses[clause] = generate_legal_clause(fields, clause, contract_type)

        full_data.update(dynamic_clauses)
        print("Dynamic clauses generated:", dynamic_clauses)

        # Render the dynamic template
        return render_template(
            dynamic_contract_template,
            contract_type=contract_type,
            original_data_json=json.dumps(full_data),
            full_data=full_data,
            contract_id=contract_id,
            download = True,
            generation_date="2025-04-28"  # Adjust as needed
        )
    else:
        # Render static template
        return render_template(
            f"{contract_id}_template_{template_choice}.html",
            download=True,
            original_data_json=json.dumps(full_data),
            **full_data
        )
    # return jsonify({"html": rendered_html})
    
# def generate():
#     contract_type = request.form['contract_type']
#     full_data = json.loads(request.form['original_data'])
#     template_choice = request.form['template_choice']
#     contract_id = request.form['contract_id']

#     required_fields = {
#     "Non-Disclosure Agreement (NDA)": ["disclosing_party", "receiving_party", "effective_date", "confidentiality_period"],
#     "Employment Contract": ["employee_name", "employer_name", "start_date", "position", "salary"],
#     "Service Agreement": ["client_name", "provider_name", "start_date", "end_date", "service_description"],
#     }
    
#     print("Received in /generate:", full_data)
#     if template_choice == 'dynamic':
#         # Generate dynamic clauses for all required types
#         # dynamic_clauses = {
#         #     "confidentiality": generate_dynamic_clauses(contract_type, "confidentiality", full_data),
#         #     "data_privacy": generate_dynamic_clauses(contract_type, "data_privacy", full_data),
#         #     "termination": generate_dynamic_clauses(contract_type, "termination", full_data),
#         # }
#         # generate_legal_clause(party1, party2, date, duration, clause_type, agreement_type):
#         dynamic_clauses = {
#             "confidentiality": generate_legal_clause(
#                 full_data['disclosing_party'], 
#                 full_data['receiving_party'],
#                 full_data['effective_date'], 
#                 full_data['confidentiality_period'], 
#                 "confidentiality",
#                 'Non-Disclosure Agreement (NDA)'),
#             "data_privacy": generate_legal_clause(
#                 full_data['disclosing_party'], 
#                 full_data['receiving_party'],
#                 full_data['effective_date'], 
#                 full_data['confidentiality_period'], 
#                 "data_privacy",
#                 'Non-Disclosure Agreement (NDA)'),
#             "termination": generate_legal_clause(
#                 full_data['disclosing_party'], 
#                 full_data['receiving_party'],
#                 full_data['effective_date'], 
#                 full_data['confidentiality_period'], 
#                 "termination",
#                 'Non-Disclosure Agreement (NDA)'),
#         }
#         if contract_type in ["Employment Contract"]:
#             dynamic_clauses["payment"] = generate_legal_clause(
#                 full_data['employee_name'], 
#                 full_data['employer_name'],
#                 full_data['start_date'], 
#                 full_data['position'], 
#                 full_data['salary'], 
#                 "payment",
#                 'Employment Contract'),
        
#         full_data.update(dynamic_clauses)
#         print("Dynamic clauses generated:", dynamic_clauses)
#         # Render the template with dynamic clauses
#         return render_template('dynamic_contract_template.html',
#                              contract_type=contract_type,
#                              full_data_json=json.dumps(full_data),
#                              full_data=full_data,
#                              contract_id=contract_id)
#     else:
#         return render_template(
#             f"{contract_id}_template_{template_choice}.html",
#             download=True,
#             original_data_json=json.dumps(full_data),
#             **full_data)
    
# @app.route('/generate_dynamic', methods=['POST'])
# def generate_dynamic():
#     contract_type = request.form['contract_type']
#     full_data = json.loads(request.form['full_data'])
#     template_choice = request.form['template_choice']
    
#     if template_choice == 'dynamic':
#         # Generate dynamic clauses using your model
#         dynamic_clauses = generate_dynamic_clauses(contract_type, full_data)
#         full_data.update(dynamic_clauses)
        
#         return render_template('dynamic_nda_template.html',
#                              contract_type=contract_type,
#                              full_data_json=json.dumps(full_data),
#                              full_data=full_data)
#     else:
#         #return render_template(f'{contract_type.lower()}_template.html', **full_data)
#         if(contract_type == "Non-Disclosure Agreement (NDA)"):
#             template_name = "nda_template.html"
#             full_data["dynamic_clauses"] = "Dynamic clauses for NDA"
#         elif(contract_type == "Employment Contract"):
#             template_name = "employment_contract.html"
#             full_data["dynamic_clauses"] = "Dynamic clauses for Employment Contract"
#         elif(contract_type == "Service Agreement"):
#             template_name = "employment_contract.html"
#             full_data["dynamic_clauses"] = "Dynamic clauses for Service Agreement"
#         # Add more contract types and their dynamic clauses as needed
#         # Render the appropriate template based on contract type
#         return render_template(template_name, **full_data)

@app.route('/submit_missing', methods=['POST'])
def submit_missing():
    contract_type = request.form['contract_type']
    raw_data = request.form['original_data']
    print("Received in /submit_missing:", raw_data)
    
    try:
        original_data = json.loads(raw_data)
        print("Parsed original_data:", original_data)
    except json.JSONDecodeError as e:
        print("JSONDecodeError:", e, "Raw data:", raw_data)
        return "Error: Invalid data format", 400
    
    new_data = request.form.to_dict()
    new_data.pop('contract_type')
    new_data.pop('original_data')
    contract_id = get_contract_id(contract_type)

    full_data = {**original_data, **new_data}
    missing = [field for field in map_entities_to_fields(contract_type, {})[1] if not full_data.get(field)]
    
    print("Collected data before template generation:", full_data)
    #return render_template(f'{contract_type.lower()}_template.html', **full_data)
    json_data = json.dumps(full_data)
    reply = generate_missing_fields_message(contract_type, full_data, missing)
    print("Sending to index.html for missing fields:", {"contract_type": contract_type, "data": full_data})
    return render_template('index.html', 
                             contract_type=contract_type, 
                             original_data_json=json_data, 
                             original_data=full_data, 
                             reply=reply, 
                             contract_id = contract_id,
                             step="template_selection")

def get_contract_id(contract_type):
    """Get the contract ID based on the contract type."""
    if contract_type == "Non-Disclosure Agreement (NDA)":
        return "nda"
    elif contract_type == "Employment Contract":
        return "emp"
    elif contract_type == "Service Agreement":
        return "sa"
    # Add more contract types and their IDs as needed
    return None


# Attempt to find wkhtmltopdf in PATH
def find_wkhtmltopdf():
    wkhtmltopdf_path = shutil.which('wkhtmltopdf')
    if wkhtmltopdf_path:
        logger.info(f"wkhtmltopdf found at: {wkhtmltopdf_path}")
        return wkhtmltopdf_path
    logger.error("wkhtmltopdf not found in PATH. Please install wkhtmltopdf: https://wkhtmltopdf.org/downloads.html")
    return None

# Specify the path to wkhtmltopdf executable (update this based on your system)
# Examples: '/usr/bin/wkhtmltopdf' (Linux), '/opt/homebrew/bin/wkhtmltopdf' (macOS), 'C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe' (Windows)
WKHTMLTOPDF_PATH = find_wkhtmltopdf()
# Configure pdfkit with wkhtmltopdf path
try:
    configuration = pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_PATH) if WKHTMLTOPDF_PATH else pdfkit.configuration()
except Exception as e:
    logger.error(f"Failed to configure pdfkit: {str(e)}")
    configuration = None

@app.route('/download_pdf/<template_choice>', methods=['POST'])
def download_pdf(template_choice):
    # Extract form data
    contract_id = request.form.get('contract_id')
    original_data_json = request.form.get('original_data_json')
    original_data = json.loads(original_data_json) if original_data_json else {}
    #full_data = request.form.get('original_data_json')
    logger.info(f"Generating PDF for template {template_choice} with data: {original_data}")

    template_file = f"{contract_id}_template_{template_choice}.html"
    print("Template file:", template_file)

  # Render the template with provided data
    if not template_file:
        logger.error(f"Invalid template choice: {template_choice}")
        return "Invalid template choice", 400

    # Render the template with provided data
    try:
        rendered_html = render_template(template_file, full_data = original_data, **original_data, generation_date=datetime.now().strftime('%Y-%m-%d'))
        logger.info(f"Template file: {template_file}")
        logger.info(f"Rendered HTML (full): {rendered_html}")
    except Exception as e:
        logger.error(f"Template rendering failed: {str(e)}")
        return "Error rendering template", 500

    # Convert rendered HTML to PDF using a temporary file
    pdf_output = BytesIO()
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            pdfkit.from_string(rendered_html, temp_file.name, configuration=configuration, options={
                'page-size': 'Letter',
                'margin-top': '0.5in',
                'margin-bottom': '0.5in',
                'margin-left': '0.5in',
                'margin-right': '0.5in',
                'encoding': 'UTF-8',
                'no-outline': None,
                '--disable-smart-shrinking': None,
                '--enable-local-file-access': None,
                '--load-error-handling': 'ignore',
                '--zoom': '1.2',  # Slightly increase zoom for layout accuracy
                '--dpi': '300',  # High resolution for fonts and CSS
                '--javascript-delay': '1000'  # Wait for any dynamic rendering
            })
            # Read the temporary file into BytesIO
            with open(temp_file.name, 'rb') as f:
                pdf_output.write(f.read())
        # Clean up the temporary file
        os.unlink(temp_file.name)
    except Exception as e:
        logger.error(f"PDF generation failed: {str(e)}")
        return f"Error generating PDF: {str(e)}", 500

    # Prepare the PDF for download
    pdf_output.seek(0)
    filename = f"{contract_id}_{template_choice}.pdf"
    return send_file(
        pdf_output,
        mimetype='application/pdf',
        as_attachment=True,
        download_name=filename
    )

# def get_template_name(contract_id, template_choice):  
#     """Get the template name based on contract ID and template choice."""
#     return f"{contract_id}_template_{template_choice}.html"

# if __name__ == '__main__':
#     app.run(debug=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)