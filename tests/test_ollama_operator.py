import pytest
from unittest.mock import patch, MagicMock
from airflow.utils.context import Context
from airflow_ollama.operators.ollama_operator import OllamaOperator

class TestOllamaOperator:

    def setup_method(self):
        self.task_id = 'test_ollama_task'
        self.model_name = 'test_model'

    @patch('airflow_ollama.operators.ollama_operator.subprocess.run')
    def test_install_ollama(self, mock_run):
        operator = OllamaOperator(
            task_id=self.task_id,
            model_name=self.model_name,
            install_ollama=True
        )
        operator.execute(context=Context())
        
        mock_run.assert_any_call([
            "curl", "-L", "https://ollama.com/download/ollama-linux-amd64",
            "-o", "./ollama"
        ], check=True)

    @patch('airflow_ollama.operators.ollama_operator.subprocess.run')
    def test_start_ollama_server(self, mock_run):
        operator = OllamaOperator(
            task_id=self.task_id,
            model_name=self.model_name
        )
        operator.execute(context=Context())
        
        mock_run.assert_any_call("nohup ./ollama serve > ollama.log 2>&1 &", shell=True, check=True)

    @patch('airflow_ollama.operators.ollama_operator.subprocess.run')
    def test_pull_model(self, mock_run):
        operator = OllamaOperator(
            task_id=self.task_id,
            model_name=self.model_name
        )
        operator.execute(context=Context())
        
        mock_run.assert_any_call(["./ollama", "pull", self.model_name], check=True)

    @patch('airflow_ollama.operators.ollama_operator.subprocess.run')
    def test_run_model(self, mock_run):
        operator = OllamaOperator(
            task_id=self.task_id,
            model_name=self.model_name,
            run_model=True
        )
        operator.execute(context=Context())
        
        mock_run.assert_any_call(["./ollama", "run", self.model_name], check=True)

    @patch('airflow_ollama.operators.ollama_operator.subprocess.run')
    def test_execute_all_steps(self, mock_run):
        operator = OllamaOperator(
            task_id=self.task_id,
            model_name=self.model_name,
            install_ollama=True,
            run_model=True
        )
        operator.execute(context=Context())
        
        assert mock_run.call_count == 4  # install, start server, pull model, run model
