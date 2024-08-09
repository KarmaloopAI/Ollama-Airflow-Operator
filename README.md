# Ollama-Airflow-Operator: Because AI, Airflow, and Alliteration Are Awesome!

> 🤖 "Airflow + Ollama = Magic" - Some Data Scientist, probably

Welcome to the Ollama-Airflow-Operator, where we make running LLMs as easy as pie (and potentially more delicious)!

## What's This All About?

Ever wished you could orchestrate Large Language Models (LLMs) with the ease of scheduling a tweet? Well, now you can! This Airflow plugin lets you manage Ollama (the cool kid in the LLM playground) **with no external compute dependencies**. That is the key.

### Here is why

In the wild world of enterprise AI, Data Engineers often find themselves in a peculiar predicament. They have the skills, the ideas, and the burning desire to leverage LLMs for innovative solutions. But alas! They're often stymied by the lack of access to dedicated LLM endpoints in their organizations.

Enter the Ollama-Airflow-Operator – a glimmer of hope in the dark night of corporate red tape. Born from the frustration of Data Engineers who dared to dream, this plugin turns the tables on the traditional AI deployment model.

With this operator, Data Engineers can now leverage their existing Airflow infrastructure to spin up LLM endpoints on demand. No need for external compute resources or endpoints. No more waiting for IT approvals. Just pure, unadulterated LLM power at your fingertips.

### Is this the only reason?
No. Imagine the future of Agents. There are tools after tools and frameworks after frameworks that are showing up. But nothing stands as tall as Airflow in the world of task orchestration. Any AI Agent will first and foremost be an orchestrated workflow, and that is where the power of Airflow comes in. Pair it up with Ollama - and Data Engineers can now make magic happen say with enriching data in ways not possible previously, or making sense of unstructured data and the possibilities are limitless.

## Getting Started

Get ready to embark on your LLM journey with Airflow! Here's how to get started:

### 1. Installation

First, install the Ollama-Airflow-Operator package:

```bash
pip install airflow-ollama
```
OR
```bash
pip install git+https://github.com/KarmaloopAI/Ollama-Airflow-Operator.git
```

### 2. Import the Operators
This should be same as any other operators you use in your Airflow DAGs
```python
from airflow import DAG
from airflow.utils.dates import days_ago
from airflow_ollama.operators.ollama_operator import OllamaOperator
from airflow_ollama.operators.ngrok_exposer_operator import NgrokExposerOperator
```

### 3. Use it in your DAGs
Here is an example of how to use it.
```python
with DAG('ollama_llm_setup', start_date=days_ago(1), schedule_interval=None) as dag:
    
    install_ollama = OllamaOperator(
        task_id='install_ollama',
        install_ollama=True,
        model_name='gemma:2b',  # Choose your model
        run_model=False
    )

    expose_ollama = NgrokExposerOperator(
        task_id='expose_ollama',
        port=11434,  # Default Ollama port
        auth_token='your_ngrok_auth_token'
    )

    run_model = OllamaOperator(
        task_id='run_model',
        model_name='gemma:2b',
        run_model=True
    )

    install_ollama >> expose_ollama >> run_model
```

### About the Author
Hello, my name is [Abi Chatterjee](https://www.linkedin.com/in/abi-chatterjee/) and you may reach me via [LinkedIn](https://www.linkedin.com/in/abi-chatterjee/)

I am in love with LLMs, for the better or worse, and have been finding innovative ways of building LLM and GenAi solutions.
