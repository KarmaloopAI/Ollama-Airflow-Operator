from datetime import datetime, timedelta
from airflow import DAG
from custom_operators import OllamaOperator, NgrokExposerOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'ollama_llmodel_setup',
    default_args=default_args,
    description='Install ollama and ngrok, pull gemma, expose port, and run gemma',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2024, 6, 21),
    catchup=False,
)

install_and_start_ollama = OllamaOperator(
    task_id='install_and_start_ollama',
    model_name='gemma',
    install_ollama=True,
    run_model=False,
    dag=dag,
)

expose_ollama_port = NgrokExposerOperator(
    task_id='expose_ollama_port',
    port=11434,
    auth_token='your_ngrok_auth_token',
    install_ngrok=True,
    dag=dag,
)

run_llmodel = OllamaOperator(
    task_id='run_llmodel',
    model_name='gemma',
    install_ollama=False,
    run_model=True,
    dag=dag,
)

install_and_start_ollama >> expose_ollama_port >> run_llmodel
