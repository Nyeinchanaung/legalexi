# Automated Legal Document Generation Templates, Distilling legal complexity into clear, actionable insights.
#### Submitted by: Group 8
- Sonakul Kamnuanchai (st124738)
- Patsachon Pattakulpong (st124952)
- Nyein Chan Aung (st125553)

# Overview
This project presents an **automated legal document generation system**, specifically designed to create **Non-Disclosure Agreements (NDAs)** using cutting-edge **Natural Language Processing (NLP)** and deep learning techniques.

The system integrates:
- **spaCy-based Named Entity Recognition (NER)** for extracting key legal entities,
- **Legal-BERT** for legal intent detection, and
- a **Qwen-7B model fine-tuned via LoRA** on the ContractNLI dataset for clause-level legal reasoning.
Generated clauses are dynamically populated into a Jinja2-based NDA template, producing **fully customized and legally compliant documents**.

### Key Contributions

- A hybrid pipeline that combines **rule-based extraction** and **model-driven reasoning** for legal clause generation
- Fine-tuning of **Qwen-7B** using **Low-Rank Adaptation (LoRA)** to improve clause-level classification performance
- Full-stack **Flask web interface** to support real-time, end-to-end document generation and interaction
- High semantic accuracy demonstrated with **BERTScore (F1: 80.05%)**, reflecting the quality and legal coherence of the generated contracts  

This project showcases how legal document automation can reduce time and cost, improve accessibility, and ensure clarity and compliance—all through the power of NLP.
---
# Related Works

This project integrates insights from recent advancements in template-based document generation, transformer models for legal clause analysis, evaluation techniques for generated text, and domain-specific large language models (LLMs).

### 1. Template-Based Document Generation

Template-driven systems have proven effective in automating structured document generation. A widely adopted tool in this domain is **Jinja2**, which enables dynamic text generation by replacing placeholders with input data. Its utility in NLP has been notably demonstrated in the **PromptSource** framework developed by Liu et al. (2022), where Jinja2 was used to dynamically generate natural language prompts for fine-tuning large language models. Inspired by this, our system applies a similar approach to automate legal contract creation, dynamically inserting legal clauses and user-specific entities into pre-built NDA templates.

### 2. Transformer Models and Clause Analysis

Transformer-based models, especially domain-adapted versions like **Legal-BERT**, have shown great potential in handling legal documents. Limsopatham (2021) demonstrated Legal-BERT’s ability to segment and interpret legal language effectively. Complementing this, Narendra et al. (2024) proposed methods to enhance contract understanding using clause segmentation and Natural Language Inference (NLI), improving contract comparison and clause-level classification. These approaches guide our own integration of Legal-BERT for intent detection and Qwen-7B for clause generation.

### 3. Evaluation Methods for Legal Document Generation

Evaluation of legal text generation requires metrics that account for contextual fidelity and legal phrasing. Cao et al. (2020) proposed integrating BERT with score-based features to detect grammatical and semantic errors in generated content. Meanwhile, BERTScore—studied extensively by Hanna and Bojar (2021)—has become a key metric for measuring semantic similarity between generated and reference clauses. Although effective at detecting major discrepancies, it is less sensitive to subtle legal phrasings, prompting the need for complementary qualitative review. We use BERTScore to measure the semantic consistency of our generated NDA clauses.

### 4. Open-Source Large Language Models

The evolution of open-source LLMs such as **LLaMA** (Touvron et al., 2023), **Alpaca** (Taori et al., 2023), **Baichuan** (Yang et al., 2023), and **Qwen-VL** (Bai et al., 2023) has democratized access to high-performing models for diverse NLP tasks. Recent trends have focused on domain-specific fine-tuning. For instance, **PIXIU** (Xie et al., 2023) specializes in financial NLP, while **HuaTuo** (Wang et al., 2023) targets medical applications. In line with this trend, Huang et al. (2025) developed **AuditWen**, a Qwen-7B-based model fine-tuned for audit-specific tasks. Inspired by these models, our project fine-tunes Qwen-7B using **LoRA** on the **ContractNLI** dataset to generate legal clauses tailored for NDA contracts.

This combination of Jinja2 template rendering, transformer-based legal clause modeling, and instruction-tuned large language models forms the foundation of our end-to-end automated legal document generation system.


## Project Progress Summary

**Project Title**: Automated Legal Document Generation Using NLP and LLMs  
**Objective**: To develop an end-to-end system that generates customized, legally valid Non-Disclosure Agreements (NDAs) from natural language inputs.

---

# Achievements So Far

#### 1. System Architecture Designed

A modular NLP pipeline has been created, integrating the following components:
- **spaCy** for Named Entity Recognition (NER)
- **Legal-BERT** for contract intent classification
- **Qwen-7B** (fine-tuned via LoRA) for clause-level generation
- **Jinja2** for dynamic NDA templating
- **Flask** for a web-based user interface

#### 2. NER and Clause Detection Implemented

- Custom rules developed in spaCy to identify legal entities such as party names and durations
- Legal-BERT tested on identifying contract types and classifying clause intents

#### 3. Model Fine-Tuning Completed

- Qwen-7B fine-tuned on the **ContractNLI** dataset using **LoRA** for efficient domain adaptation
- GPT-2 model fine-tuned as a baseline for performance comparison

#### 4. Evaluation Conducted

- Evaluated using **BERTScore** for semantic alignment between generated and reference clauses
- **Qwen-7B** achieved an F1 score of **80.05%**, outperforming GPT-2’s **75.58%**

#### 5. Template-Based NDA Generation Operational

- Jinja2 templates developed for Non-Disclosure Agreements
- Generated clauses and user inputs dynamically integrated into the legal templates

#### 6. Web Interface Prototyped

- Flask backend developed to handle:
  - User prompt submission
  - Contract generation
  - Document download
- Basic user interface functional; UX improvements planned

---

### Experiment Highlights

- **Dataset**: Subset of ContractNLI containing 607 annotated NDA clauses
- **Evaluation Metrics**: Evaluation loss, BERTScore (Precision, Recall, F1)
- **Best Performing Model**: Qwen-7B with LoRA (F1 score: **0.8060**)

---

### Next Steps

- Integrate the NER and clause generation modules into a seamless, end-to-end pipeline
- Enhance the web interface with form validation and improved user experience
- Extend the system to support additional contract types such as employment and service agreements
- Implement user feedback mechanisms to support continuous system refinement
- Add document export options (PDF, DOCX) and version tracking for generated contracts

# References

- Wenyuan Gu, Jiale Han, Haowen Wang, Xiang Li, and Bo Cheng. 2025. *Explain-Analyze-Generate: A Sequential Multi-Agent Collaboration Method for Complex Reasoning.* Proceedings of the 31st International Conference on Computational Linguistics (COLING 2025).
- Sagar Joshi, Sumanth Balaji, Aparna Garimella, and Vasudeva Varma. 2022. *Graph-based Keyword Planning for Legal Clause Generation from Topics.* Proceedings of the Natural Legal Language Processing Workshop 2022.
- Nut Limsopatham. 2021. *Effectively Leveraging BERT for Legal Document Classification.* Proceedings of the Natural Legal Language Processing Workshop 2021.
- Savinay Narendra, Kaushal Shetty, and Adwait Ratnaparkhi. 2024. *Enhancing Contract Negotiations with LLM-Based Legal Document Comparison.* Proceedings of the Natural Legal Language Processing Workshop 2024.
- William Watson, Nicole Cho, Nishan Srishankar, Zhen Zeng, Lucas Cecchi, Daniel Scott, Suchetha Siddagangappa, Rachneet Kaur, Tucker Balch, and Manuela Veloso. 2025. *LAW: Legal Agentic Workflows for Custody and Fund Services Contracts.* Proceedings of the 31st International Conference on Computational Linguistics: Industry Track.
- Sina Zarrieß and Kyle Richardson. 2013. *An Automatic Method for Building a Data-to-Text Generator.* Proceedings of the 14th European Workshop on Natural Language Generation.

---









