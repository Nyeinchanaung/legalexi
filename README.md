# legalexi
## Automated Legal Document Generation:
### Distilling legal complexity into clear, actionable insights.
#### Submitted by: Group 8
- Sonakul Kamnuanchai (st124738)
- Patsachon Pattakulpong (st124952)
- Nyein Chan Aung (st125553)
#### Submitted to: Dr. Chaklam Silpasuwanchai 
# Project Proposal
## Abstract
Legal contracts are inherently complex and often require specialized expertise to draft, which can create a significant barrier for individuals and small businesses that lack access to affordable legal services. This project proposes the development of a natural language processing (NLP)-based system aimed at automating legal document generation. The system will utilize pre-trained contract templates and integrate user-provided information—such as names, dates, and specific terms—to produce customized, legally compliant documents. 
The methodology includes training an NLP model on a comprehensive dataset of legal contracts to capture their structural and linguistic patterns, followed by fine-tuning the model to incorporate user-specific details seamlessly. The anticipated outcomes are a significant reduction in the time and cost associated with contract drafting, enhanced accessibility to legal services, and the creation of clear, actionable contracts. By transforming complex legal language into user-friendly documents, this project seeks to democratize access to legal resources, empowering a broader audience to create reliable agreements without needing extensive legal consultation.
## Introduction
Legal contracts are important for both businesses and personal agreements. They provide clarity, mutual understanding, and legal protection for everyone involved. However, the complicated language and structure of legal documents can make them hard to understand for people without legal training. This confusion can lead to mistakes and problems, especially for individuals and small businesses that may not have the money to hire lawyers. Because of this, many people use generic templates or skip formal agreements, putting themselves at risk of legal issues.

Natural language processing (NLP) offers a solution. By using NLP to automate the creation of legal documents, we can turn complex legal language into simple, clear information. This makes legal resources easier to use and more affordable. This project aims to develop an NLP-powered system that creates customized legal contracts. Combining existing templates with specific user information will make the drafting process easier while ensuring the documents are legally valid and tailored to individual needs.

This project is important because it can help more people access legal tools. By cutting down on the time, cost, and expertise needed to create contracts, this system will allow individuals and small businesses to draft reliable agreements without needing extensive legal help. In today’s digital world, where efficiency and accessibility are key, this project meets the growing demand for legal automation.

This work's main question is: How can we use NLP to create legally valid contracts that match user input and are easy to understand for those without legal training? This introduction explains the problem, proposes a solution, highlights the project's importance, and focuses on future research.

## Problem & Motivation
Legal contracts are essential for formalizing agreements, but their complexity often makes them difficult for people without specialized legal knowledge to understand. The technical language and intricate structure of these documents can be overwhelming for non-experts. This creates a significant barrier for individuals and small businesses that cannot afford to hire legal professionals. Without accessible legal support, many resort to using generic, one-size-fits-all templates or forgo formal contracts altogether. This puts them at risk of legal issues, such as misunderstandings or disputes, due to poorly drafted or nonexistent agreements.
The motivation for this project is to leverage natural language processing (NLP) to simplify and automate the creation of legal contracts, making them more accessible and affordable. By developing an NLP-powered system that generates customized contracts using pre-trained templates and user inputs, the project aims to achieve the following goals:
- Reduce Time and Cost: Streamline the drafting process to save users valuable time and money.
- Enhanced Accessibility: Provide an easy-to-use tool that empowers individuals and small businesses to create legal documents without needing expert knowledge.
- Ensure Clarity and Compliance: Produce contracts that are both understandable and legally sound.
This initiative seeks to bridge the gap between legal expertise and everyday users, enabling more people to confidently formalize their agreements. It also aligns with the growing demand for efficient, technology-driven solutions in an increasingly digital world.

## Prior related work (Papers)
### Paper 1: "An Automatic Method for Building a Data-to-Text Generator"  ###

### Paper 2:  ###

### Paper 3:  ###

### Paper 4: ###

### Paper 5: ###

### Paper 6:  ###

### Paper 7: ###

## Methodology
This project proposes a hybrid approach to automating legal contract generation, specifically focusing on Non-Disclosure Agreements (NDAs), by integrating Natural Language Processing (NLP) with template-based methods. The system will use a fine-tuned Legal-BERT model to classify user inputs into required clause types and Jinja2 to fill clause templates with extracted details. The methodology is divided into three core components: dataset preparation, NLP model fine-tuning for clause classification, and dynamic contract generation. The following subsections detail the dataset and experimental design to evaluate the system’s performance.

### Dataset ###
To enable the development and testing of the automated legal document generation system, a dataset of legal contract templates, clauses, and user input examples will be curated from publicly available resources. This ensures accessibility, compliance with legal standards, and feasibility within the project’s scope.
<br/>
**Source:** <br/>
- Legal Contract Templates and Clauses: Collected from free legal template repositories such as Law Insider and Rocket Lawyer, which offer a variety of NDA templates and clause examples.
- User Input Examples: Manually created synthetic inputs based on common NDA scenarios, supplemented by paraphrased examples to increase variety.

**Composition:** <br/>
The dataset will consist of three main elements:
- Predefined NDA Templates: A set of 5-10 NDA templates representing common scenarios (e.g., mutual NDAs, employee NDAs, vendor NDAs). These templates provide a structural foundation for the system.
- Clause Library: A collection of 20-30 individual clauses (e.g., confidentiality obligations, term and termination, governing law) extracted from the templates. Each clause will be tagged with metadata (e.g., "mutual" vs. "one-way" confidentiality) to indicate its applicability based on user inputs.
- Clause Classification Dataset: A dataset of 100 synthetic user inputs (e.g., "I need an NDA for sharing business plans with a partner") labeled with corresponding clause types (e.g., "confidentiality," "purpose," "duration"). This dataset will be used to fine-tune Legal-BERT for clause classification.
**Annotation:** <br/>
- Clauses will be manually annotated to identify placeholders (e.g., [Party A Name], [Effective Date]) and categorized by their function within the contract (e.g., "scope of confidentiality").
- The clause classification dataset will be annotated to map user inputs to required clauses, ensuring the fine-tuned model can accurately identify necessary clause types. Due to time and resource constraints, the dataset is intentionally limited in size but designed to offer sufficient variety for dynamic contract assembly.
<br/>

### Experimental Design ###
The experimental design evaluates the system’s ability to process user inputs accurately, classify required clauses using the fine-tuned Legal-BERT model, extract entities, and generate coherent, complete, and legally compliant NDAs. The evaluation is structured in three phases—NLP model fine-tuning, clause classification and entity extraction assessment, and contract generation evaluation—followed by an iterative refinement step.
<br/>
#### NLP Model Fine-Tuning for Clause Classification:
- The Legal-BERT model (nlpaueb/legal-bert-base-uncased) will be loaded using the Hugging Face Transformers library.
- The clause classification dataset (100 examples) will be formatted into input-output pairs, where inputs are user requests and outputs are clause type labels (e.g., "confidentiality").
- The model will be fine-tuned on this dataset using a GPU (e.g., via Google Colab) with a training split of 80% and a validation split of 20%. Training parameters will include a learning rate of 2e-5, batch size of 8, and 3 epochs to balance performance and resource constraints.
#### Contract Generation Evaluation: ####
- The system will generate NDAs using the same 50 user inputs from the clause classification and entity extraction assessment.
- The fine-tuned Legal-BERT model will classify required clauses, and spaCy will extract entities to populate the clause templates.
- Jinja2 will be used to insert extracted entities into the selected clause templates, assembling the final contract.
- Each generated contract will be reviewed against a checklist of essential NDA components (e.g., party names, effective date, confidentiality obligations).
- A panel of 3-5 peers will evaluate the contracts’ clarity and usability on a Likert scale (1-5) across criteria such as readability, completeness, and perceived legal reliability.

### Tools and Technologies ###
- Programming Language: Python 3.8+ for implementation.
- NLP Libraries: 1) Hugging Face Transformers for fine-tuning Legal-BERT. 2)spaCy for entity extraction using en_core_web_sm.
- Templating Engine: Jinja2 for dynamically inserting extracted entities into clause templates.
- User Interface: Streamlit for a simple web-based interface to collect inputs and display contracts.
- Hardware: Google Colab (free tier with GPU) for fine-tuning Legal-BERT.
- Version Control: Git for code management.
## Expected Results ##
The web app, built using web application framework, such as Django or Streamlit, is expected to provide an intuitive interface for users to input natural language requests and receive customized Non-Disclosure Agreements (NDAs), demonstrating the practical application of NLP techniques. Technically, the app should accurately process user inputs, leveraging the fine-tuned Legal-BERT model to achieve an 80% accuracy in classifying required clauses (e.g., confidentiality, purpose) and spaCy’s NER model to extract entities (e.g., names, dates) with 75% accuracy. Generated NDAs are anticipated to include 90% of essential components, with an error rate below 10% for missing or misplaced clauses, ensuring functional drafts. For example, an input like "Alice needs an NDA with Bob starting on January 1, 2025, for sharing business plans" should produce a complete NDA displayed on the app, with all critical clauses and entities correctly populated.<br/>
User experience is expected to be seamless, with the app enabling contract generation in under 5 minutes, supported by minimal clarification prompts (e.g., "Please specify the effective date") when entities are missed. Peer reviewers are anticipated to rate the generated NDAs at 4 out of 5 for clarity, completeness, and perceived legal reliability, confirming the app’s usability for non-experts. Practically, the web app should reduce NDA drafting time by 50% compared to manual methods, enhancing accessibility for small businesses and individuals. A disclaimer will be displayed to remind users to consult a legal professional, ensuring responsible use. Iterative refinement based on feedback is expected to improve clause classification and entity extraction accuracy by 5-10%, enhancing the app’s reliability for future iterations.

## Conclusion ##


## Reference ##












