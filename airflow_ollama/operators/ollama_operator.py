import os
import subprocess
from pathlib import Path
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from typing import Optional

class OllamaOperator(BaseOperator):
    @apply_defaults
    def __init__(
        self,
        model_name: str,
        install_ollama: bool = False,
        run_model: bool = False,
        ollama_path: Optional[str] = None,
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.model_name = model_name
        self.install_ollama = install_ollama
        self.run_model = run_model
        self.ollama_path = ollama_path or './ollama'

    def execute(self, context):
        if self.install_ollama:
            self._install_ollama()
        self._start_ollama_server()
        self._pull_model()
        if self.run_model:
            self._run_model()

    def _install_ollama(self):
        self.log.info("Installing Ollama...")
        install_cmd = [
            "curl", "-L", "https://ollama.com/download/ollama-linux-amd64",
            "-o", self.ollama_path
        ]
        subprocess.run(install_cmd, check=True)
        os.chmod(self.ollama_path, 0o755)
        self.log.info("Ollama installed successfully.")

    def _start_ollama_server(self):
        self.log.info("Starting Ollama server...")
        server_cmd = f"nohup {self.ollama_path} serve > ollama.log 2>&1 &"
        subprocess.run(server_cmd, shell=True, check=True)
        self.log.info("Ollama server started in the background.")

    def _pull_model(self):
        self.log.info(f"Pulling model: {self.model_name}")
        pull_cmd = [self.ollama_path, "pull", self.model_name]
        subprocess.run(pull_cmd, check=True)
        self.log.info(f"Model {self.model_name} pulled successfully.")

    def _run_model(self):
        self.log.info(f"Running model: {self.model_name}")
        run_cmd = [self.ollama_path, "run", self.model_name]
        subprocess.run(run_cmd, check=True)
        self.log.info(f"Model {self.model_name} completed execution.")
