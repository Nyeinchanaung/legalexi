# Automated NDA Legal Document.
Project Link: https://github.com/Nyeinchanaung/legalexi
#### Submitted by: Carbonara Group
- Sonakul Kamnuanchai (st124738)
- Patsachon Pattakulpong (st124952)
- Nyein Chan Aung (st125553)


# Overview

This project presents an **automated legal document generation system**, specifically designed to create **Non-Disclosure Agreements (NDAs)** using cutting-edge **Natural Language Processing (NLP)** and deep learning techniques.

The system integrates:
- **spaCy-based Named Entity Recognition (NER)** for extracting key legal entities,
- **Legal-BERT** for legal intent detection, and
- a **Qwen1.5-0.5B-Chat model fine-tuned via LoRA** on the Legal-Clause-Instructions dataset for clause-level legal reasoning.

Generated clauses are dynamically populated into a Jinja2-based NDA template, producing **fully customized and legally coherent contracts** based on user-provided natural language prompts.

### Key Contributions

- A hybrid pipeline that combines **rule-based extraction** and **model-driven reasoning** for accurate legal clause generation
- Fine-tuning of **Qwen1.5-0.5B-Chat** using **Low-Rank Adaptation (LoRA)** to enhance clause generation performance
- Comprehensive evaluation demonstrating that **Qwen1.5-0.5B-Chat outperforms GPT-2**, achieving a **BERTScore (F1) of 85.81%** compared to GPT-2’s 76.08%, validating its superior legal text generation capabilities
- Full-stack **Flask web application** providing a real-time, interactive interface for end-to-end legal document creation

#### This project demonstrates how advanced AI models can automate legal document drafting, reducing time and cost, improving accessibility, and ensuring precision and compliance in contract generation.
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


# Project Progress Summary

## Achievements So Far

#### 1. System Architecture Designed
![experiment-design-carbov5](https://github.com/user-attachments/assets/c4c7d815-8ac0-4845-bf6b-e1497ca350d0)
<p align="center"> Figure 1: Expirement Design</p> 

A modular NLP pipeline has been created, integrating the following components:
- **spaCy** for Named Entity Recognition (NER)
- **Legal-BERT** for contract intent classification
- **Qwen1.5-0.5B-Chat** (fine-tuned via LoRA) for clause-level generation
- **Jinja2** for dynamic NDA templating
- **Flask** for a web-based user interface

#### 2. NER and Clause Detection Implemented

- Custom rules developed in spaCy to identify legal entities such as party names and durations
- Legal-BERT tested on identifying contract types and classifying clause intents

#### 3. Model Fine-Tuning Completed

- Qwen1.5-0.5B-Chat fine-tuned on the **Legal-Clause-Instructions** dataset using **LoRA** for efficient domain adaptation
- GPT-2 model fine-tuned as a baseline for performance comparison

#### 4. Evaluation Conducted

- Evaluated using **BERTScore** for semantic alignment between generated and reference clauses
- **Qwen1.5-0.5B-Chat** achieved an F1 score of **80.05%**, outperforming GPT-2’s **75.58%**

#### 5. Template-Based NDA Generation Operational

- Jinja2 templates developed for Non-Disclosure Agreements
- Generated clauses and user inputs dynamically integrated into the legal templates

#### 6. Web Interface Prototyped

- Flask backend developed to handle:
  - User prompt submission
  - Contract generation
  - Document download
- Basic user interface functional; UX improvements planned


![Home page : user prompt](https://github.com/user-attachments/assets/56711025-ac43-4112-a502-03dc60185d33)
<p align="center"> Figure 2: Home page : User prompt </p> 

![Progress : collecting data](https://github.com/user-attachments/assets/02c144f2-8730-4f9a-9259-9ed8d5905170)
<p align="center"> Figure 3: Progress : Collecting additional data </p> 

![Result: generated contract by Jinja](https://github.com/user-attachments/assets/73916f99-0126-49de-a5da-48e6b551a527)
<p align="center"> Figure 3: Result : Contract generated by Jinja Template</p> 

---

### Experiment Highlights

- **Dataset**:  
  A curated subset of the Legal-Clause-Instructions dataset, consisting of Training 4,557 samples and Test 507 samples.

- **Evaluation Metrics**:  
  Performance was assessed using evaluation loss and BERTScore metrics, including Precision, Recall, and F1 score, to measure semantic alignment and output quality.

- **Best Performing Model**:  
  The fine-tuned **Qwen1.5-0.5B-Chat** model with LoRA achieved the highest performance, reaching a **BERTScore (F1) of 0.8581**, outperforming the GPT-2 baseline (F1: 0.7608).

---
# Results
We evaluated the performance of GPT-2 and Qwen (LoRA) models on legal clause generation using the Legal-Clause-Instructions dataset. Evaluation was performed using standard language modeling loss and BERTScore.

#### Evaluation Metrics

<div align="center">

| Metric            | Qwen              | GPT-2             |
|:------------------:|:------------------:|:------------------:|
| **Eval Loss**      | **0.473**          | 0.478             |
| **BERTScore (P)**  | **0.8415**         | 0.7315            |
| **BERTScore (R)**  | **0.8764**         | 0.7936            |
| **BERTScore (F1)** | **0.8581**         | 0.7608            |

</div>

<p align="center"> Table 1: Evaluation results comparing Qwen and GPT-2 on legal clause generation.</p>

#### Analysis
- **Qwen1.5-0.5B-Chat** outperformed **GPT-2** across all metrics, achieving higher precision, recall, and F1 score.
- The lower evaluation loss indicates that Qwen produces outputs more closely aligned with the ground truth clauses.
- These results validate the choice of using Qwen1.5-0.5B-Chat as the generation backbone for the system.
- The system is capable of producing **legally coherent**, **highly accurate**, and **customizable NDA contracts** from simple natural language prompts.

##### Legal-Bert Model Result
- Query: I need nda between Company A and B organization
- Predicted: Non-Disclosure Agreement (NDA) (Confidence: 1.00)
- 
- Query: Create an agreement for a consultant to audit our development team
- Predicted: Service Agreement (Confidence: 1.00)
- 
- Query: We need employee agreement to hire software engineer
- Predicted: Employment Contract (Confidence: 1.00)
- 
- Query: How are you?
- Predicted: unknown (Confidence: 1.00)

##### Generation Model Result
Example Text:
 WHEREAS, the Asian Institute possesses proprietary information relating to its business operations; and WHEREAS, the Asian Institute and ABC Organisation desire to explore a potential business relationship. 
Prompt:
##### Example Clause:
WHEREAS, the Asian Institute possesses proprietary information relating to its business operations; and WHEREAS, the Asian Institute and ABC Organisation desire to explore a potential business relationship.

##### Instruction:
You are drafting a purpose clause for a Non-Disclosure Agreement (NDA).
- Write in formal legal English.
- Do NOT include any headings or titles.
- Bullet point for each line.
- END the clause completely.
- DO NOT add address or location.
- Avoid redundancy and repetition.
Now, write the full legal clause sentence by setence accordingly.

##### Response:

`Generated Text:`

1. Definition of Confidential Information: "Confidential Information" means any and all information disclosed by the Asian Institute to the ABC Organisation, whether in writing, orally, or by any other means, that is designated as confidential or that reasonably should be understood to be confidential given the nature of the information and the circumstances of disclosure. Confidential Information includes, but is not limited to, trade secrets, business plans, financial information, customer lists, and any other information that is not generally known to the public.

2. Obligations of the Receiving Party: The Receiving Party agrees to hold the Confidential Information in strict confidence and not to disclose it to any third party without the prior written consent of the Asian Institute. The Receiving Party shall use the Confidential Information solely for the purpose of evaluating a potential business relationship between the two parties.

3. Exceptions: The obligations of the Receiving Party under this Agreement shall not apply to any information that: (a) is or becomes generally available to the public through no fault of the Receiving Party; (b) was in the possession of the Receiving Party prior to its disclosure by the Asian Institute; (c) is rightfully obtained by the Receiving Party from a third party without restriction on disclosure; or (d) is independently developed by the Receiving Party without reference to the Confidential Information.

# Conclusion

The development of the automated legal contract generation system successfully reached a key milestone with the implementation of two core components: a legal intent extraction module and a clause-level text generation module. The intent extraction module, leveraging Legal-BERT and spaCy, accurately interprets user input, while the generation module utilizes a fine-tuned Qwen1.5-0.5B-Chat model, trained with LoRA on the Legal-Clause-Instructions dataset, to produce high-quality legal clauses aligned with real-world contractual standards.

Evaluation results demonstrate that the Qwen model outperforms the GPT-2 baseline across all key metrics, achieving a precision of 84.15%, recall of 87.64%, and F1 score of 85.81%, compared to GPT-2’s precision of 73.15%, recall of 79.36%, and F1 score of 76.08%. These improvements validate Qwen as the preferred model, ensuring greater semantic accuracy, completeness, and reliability in automated contract drafting — critical factors in the legal domain.

While the two modules currently operate independently, both have been independently validated and are ready for integration. The next phase will involve merging these components into a cohesive, automated pipeline that allows users to generate fully customized Non-Disclosure Agreements (NDAs) from natural language prompts. This integration marks an important step toward realizing the system’s ultimate goal: fully automated, precise, and trustworthy legal content creation.

# Limitations

Despite promising results, the current system has several limitations:

- **Scope limited to NDAs:**  
  The system is currently tailored specifically for Non-Disclosure Agreements and may require substantial retraining or templating to handle other types of contracts (e.g., employment agreements, service contracts).

- **Dependence on Input Quality:**  
  The quality and clarity of the generated contracts are heavily dependent on the quality of user prompts. Ambiguous or poorly structured prompts may result in less accurate or incomplete clauses.

- **Limited Legal Reasoning Depth:**  
  Although the fine-tuned Qwen1.5-0.5B-Chat model improves clause generation, it cannot yet perform deep legal reasoning or adapt to jurisdiction-specific legal variations without further customization.

- **Independent Module Operation:**  
  At this stage, the intent extraction and clause generation modules operate independently. Full integration into an end-to-end pipeline is planned for future development.

- **Dataset and Bias Constraints:**  
  The model’s training data may not cover all edge cases or diverse legal phrasing styles, potentially introducing bias or limitations in clause diversity.

These limitations highlight opportunities for future work, including expanding contract types, enhancing prompt engineering, integrating jurisdictional customization, and refining the model with broader legal datasets.


# References

- Wenyuan Gu, Jiale Han, Haowen Wang, Xiang Li, and Bo Cheng. 2025. *Explain-Analyze-Generate: A Sequential Multi-Agent Collaboration Method for Complex Reasoning.* Proceedings of the 31st International Conference on Computational Linguistics (COLING 2025).
- Sagar Joshi, Sumanth Balaji, Aparna Garimella, and Vasudeva Varma. 2022. *Graph-based Keyword Planning for Legal Clause Generation from Topics.* Proceedings of the Natural Legal Language Processing Workshop 2022.
- Nut Limsopatham. 2021. *Effectively Leveraging BERT for Legal Document Classification.* Proceedings of the Natural Legal Language Processing Workshop 2021.
- Savinay Narendra, Kaushal Shetty, and Adwait Ratnaparkhi. 2024. *Enhancing Contract Negotiations with LLM-Based Legal Document Comparison.* Proceedings of the Natural Legal Language Processing Workshop 2024.
- William Watson, Nicole Cho, Nishan Srishankar, Zhen Zeng, Lucas Cecchi, Daniel Scott, Suchetha Siddagangappa, Rachneet Kaur, Tucker Balch, and Manuela Veloso. 2025. *LAW: Legal Agentic Workflows for Custody and Fund Services Contracts.* Proceedings of the 31st International Conference on Computational Linguistics: Industry Track.
- Sina Zarrieß and Kyle Richardson. 2013. *An Automatic Method for Building a Data-to-Text Generator.* Proceedings of the 14th European Workshop on Natural Language Generation.

---









