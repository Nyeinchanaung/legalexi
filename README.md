# Automated Legal Document Generation Templates, Distilling legal complexity into clear, actionable insights.
#### Submitted by: Group 8
- Sonakul Kamnuanchai (st124738)
- Patsachon Pattakulpong (st124952)
- Nyein Chan Aung (st125553)

## Overview
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
## Related Works

This project builds upon a growing body of research in legal Natural Language Processing (NLP), template-based generation, and domain-specific large language models (LLMs).

### 1. Template-Based Document Generation

Jinja2 has been widely used for prompt engineering and document automation. Liu et al. (2022) introduced [PromptSource](https://aclanthology.org/2022.acl-demo.9/), a template-based framework that facilitates dynamic natural language prompt generation for language model fine-tuning. Our project adopts a similar template-driven approach to structure legal content in Non-Disclosure Agreements (NDAs).

### 2. Transformer Models for Legal Text

Legal-BERT has demonstrated strong performance in classifying legal clauses and understanding domain-specific context. Limsopatham (2021) highlighted its ability to effectively segment and interpret legal texts ([paper](https://aclanthology.org/2021.nllp-1.22/)). Additionally, Narendra et al. (2024) leveraged clause segmentation and natural language inference to improve legal contract comparison, showcasing the practical potential of large language models ([paper](https://aclanthology.org/2024.nllp-1.11/)).

### 3. Evaluation with BERTScore

BERTScore is a widely adopted metric for evaluating semantic similarity between generated and reference texts. Hanna and Bojar (2021) conducted a fine-grained analysis showing its strengths in capturing meaning while pointing out its weaknesses in legal subtleties like function word usage ([paper](https://aclanthology.org/2021.wmt-1.59/)). We use BERTScore in our system to validate clause generation quality.

### 4. Domain-Specific LLMs

Recent work on open-source LLMs fine-tuned for specific industries demonstrates the power of instruction tuning. Examples include PIXIU for finance ([Xie et al., 2023](https://arxiv.org/abs/2309.12345)), HuaTuo for medicine ([Wang et al., 2023](https://arxiv.org/abs/2304.06975)), and AuditWen for auditing ([Huang et al., 2025](https://aclanthology.org/2025.llmfinlegal-1.30/)). Our project follows this line by fine-tuning Qwen-7B on the ContractNLI dataset ([Koreeda & Manning, 2021](https://aclanthology.org/2021.findings-emnlp.164/)) to generate legally accurate NDA clauses.

---

This combination of template rendering, legal clause modeling, and domain-adapted LLMs forms the backbone of our automated NDA generation system.

## References

- Wenyuan Gu, Jiale Han, Haowen Wang, Xiang Li, and Bo Cheng. 2025. *Explain-Analyze-Generate: A Sequential Multi-Agent Collaboration Method for Complex Reasoning.* Proceedings of the 31st International Conference on Computational Linguistics (COLING 2025).
- Sagar Joshi, Sumanth Balaji, Aparna Garimella, and Vasudeva Varma. 2022. *Graph-based Keyword Planning for Legal Clause Generation from Topics.* Proceedings of the Natural Legal Language Processing Workshop 2022.
- Nut Limsopatham. 2021. *Effectively Leveraging BERT for Legal Document Classification.* Proceedings of the Natural Legal Language Processing Workshop 2021.
- Savinay Narendra, Kaushal Shetty, and Adwait Ratnaparkhi. 2024. *Enhancing Contract Negotiations with LLM-Based Legal Document Comparison.* Proceedings of the Natural Legal Language Processing Workshop 2024.
- William Watson, Nicole Cho, Nishan Srishankar, Zhen Zeng, Lucas Cecchi, Daniel Scott, Suchetha Siddagangappa, Rachneet Kaur, Tucker Balch, and Manuela Veloso. 2025. *LAW: Legal Agentic Workflows for Custody and Fund Services Contracts.* Proceedings of the 31st International Conference on Computational Linguistics: Industry Track.
- Sina Zarrieß and Kyle Richardson. 2013. *An Automatic Method for Building a Data-to-Text Generator.* Proceedings of the 14th European Workshop on Natural Language Generation.

---









