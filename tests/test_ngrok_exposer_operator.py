import pytest
from unittest.mock import patch, MagicMock
from airflow.utils.context import Context
from airflow_ollama.operators.ngrok_exposer_operator import NgrokExposerOperator

class TestNgrokExposerOperator:

    def setup_method(self):
        self.task_id = 'test_ngrok_task'
        self.port = 11434
        self.auth_token = 'test_auth_token'

    @patch('airflow_ollama.operators.ngrok_exposer_operator.subprocess.run')
    def test_install_ngrok(self, mock_run):
        operator = NgrokExposerOperator(
            task_id=self.task_id,
            port=self.port,
            auth_token=self.auth_token,
            install_ngrok=True
        )
        operator.execute(context=Context())
        
        mock_run.assert_any_call([
            "curl", "-O", "https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz"
        ], check=True)
        mock_run.assert_any_call(["tar", "xvzf", "ngrok-v3-stable-linux-amd64.tgz"], check=True)

    @patch('airflow_ollama.operators.ngrok_exposer_operator.subprocess.run')
    def test_set_auth_token(self, mock_run):
        operator = NgrokExposerOperator(
            task_id=self.task_id,
            port=self.port,
            auth_token=self.auth_token
        )
        operator.execute(context=Context())
        
        mock_run.assert_any_call(["./ngrok", "authtoken", self.auth_token], check=True)

    @patch('airflow_ollama.operators.ngrok_exposer_operator.subprocess.run')
    def test_start_ngrok(self, mock_run):
        operator = NgrokExposerOperator(
            task_id=self.task_id,
            port=self.port,
            auth_token=self.auth_token
        )
        operator.execute(context=Context())
        
        mock_run.assert_any_call(f"nohup ./ngrok http {self.port} --log=stdout > ngrok.log 2>&1 &", shell=True, check=True)

    @patch('airflow_ollama.operators.ngrok_exposer_operator.subprocess.run')
    def test_execute_all_steps(self, mock_run):
        operator = NgrokExposerOperator(
            task_id=self.task_id,
            port=self.port,
            auth_token=self.auth_token,
            install_ngrok=True
        )
        operator.execute(context=Context())
        
        assert mock_run.call_count == 4  # install, extract, set auth token, start ngrok
