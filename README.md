# Automated Legal Document Generation Templates, Distilling legal complexity into clear, actionable insights.
#### Submitted by: Group 8
- Sonakul Kamnuanchai (st124738)
- Patsachon Pattakulpong (st124952)
- Nyein Chan Aung (st125553)

## Overview
This project presents an **automated legal document generation system**, specifically designed to create **Non-Disclosure Agreements (NDAs)** using cutting-edge **Natural Language Processing (NLP)** and deep learning techniques.

The system integrates
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

## References

- Wenyuan Gu, Jiale Han, Haowen Wang, Xiang Li, and Bo Cheng. 2025. *Explain-Analyze-Generate: A Sequential Multi-Agent Collaboration Method for Complex Reasoning.* Proceedings of the 31st International Conference on Computational Linguistics (COLING 2025).
- Sagar Joshi, Sumanth Balaji, Aparna Garimella, and Vasudeva Varma. 2022. *Graph-based Keyword Planning for Legal Clause Generation from Topics.* Proceedings of the Natural Legal Language Processing Workshop 2022.
- Nut Limsopatham. 2021. *Effectively Leveraging BERT for Legal Document Classification.* Proceedings of the Natural Legal Language Processing Workshop 2021.
- Savinay Narendra, Kaushal Shetty, and Adwait Ratnaparkhi. 2024. *Enhancing Contract Negotiations with LLM-Based Legal Document Comparison.* Proceedings of the Natural Legal Language Processing Workshop 2024.
- William Watson, Nicole Cho, Nishan Srishankar, Zhen Zeng, Lucas Cecchi, Daniel Scott, Suchetha Siddagangappa, Rachneet Kaur, Tucker Balch, and Manuela Veloso. 2025. *LAW: Legal Agentic Workflows for Custody and Fund Services Contracts.* Proceedings of the 31st International Conference on Computational Linguistics: Industry Track.
- Sina Zarrieß and Kyle Richardson. 2013. *An Automatic Method for Building a Data-to-Text Generator.* Proceedings of the 14th European Workshop on Natural Language Generation.

---









