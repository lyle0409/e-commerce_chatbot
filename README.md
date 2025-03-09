# Agentic E-commerce Chatbot

## Introduction
This project develops a complete NLP pipeline, from data crawling using BeautifulSoup4 and LLM tools to preprocessing via rule-based methods and GPT normalization.** The pipeline includes training and evaluating various models, such as SVM, LSTM, and Transformer, followed by deployment.

Additionally, an agentic chatbot powered by GPT-4o-mini is built, utilizing function-calling capabilities and tailored tools to enhance functionality and address specific use cases. The chatbot supports prompt engineering for product-specific needs, including time queries, persona-based interactions, and specialized problem-solving.

## Feartures
- **Data Crawling**: Extracts web data using `BeautifulSoup4` and LLM-assisted parsing.
- **Preprocessing**:
  - Rule-based text cleaning.
  - GPT normalization for consistency.
- **Chatbot Development**:
  - Powered by `GPT-4o-mini`.
  - Function-calling for dynamic response generation.
  - Domain-specific expertise.
- **Deployment**: Scalable and efficient deployment of the best-performing model.

## Installation
### Prerequisites
- Python `>=3.8`
- Install dependencies:
  ```bash
  pip install -r requirements.txt

## Run
- replace OPENAI_API_KEY with your key
```bash
  docker compose build
docker compose up
  ```

Now your `README.md` will be updated directly on GitHub! 🚀
