# app.py
from flask import Flask, request, render_template
import json
from helpers import classify_contract_type, extract_entities, map_entities_to_fields

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        prompt = request.form['prompt']
        contract_type = classify_contract_type(prompt)
        entities = extract_entities(prompt)
        data, missing = map_entities_to_fields(contract_type, entities)
        
        if missing:
            # Explicitly encode data as JSON and verify
            json_data = json.dumps(data)
            print("JSON data to send:", json_data)  # Debug before rendering
            return render_template('index.html', 
                                 contract_type=contract_type, 
                                 original_data_json=json_data,  # Pass as string
                                 missing=missing)
        else:
            return render_template(f'{contract_type.lower()}_template.html', **data)
    return render_template('index.html')

@app.route('/submit_missing', methods=['POST'])
def submit_missing():
    contract_type = request.form['contract_type']
    raw_data = request.form['original_data']
    print("Received in /submit_missing:", raw_data)  # Debug raw input
    
    try:
        original_data = json.loads(raw_data)
        print("Parsed original_data:", original_data)  # Debug parsed data
    except json.JSONDecodeError as e:
        print("JSONDecodeError:", e, "Raw data:", raw_data)
        return "Error: Invalid data format", 400
    
    new_data = request.form.to_dict()
    new_data.pop('contract_type')
    new_data.pop('original_data')
    full_data = {**original_data, **new_data}
    print("Full data to template:", full_data)  # Debug final data
    return render_template(f'{contract_type.lower()}_template.html', **full_data)

if __name__ == '__main__':
    app.run(debug=True)