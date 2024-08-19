import os
import subprocess
import time
from pathlib import Path
from airflow.models import BaseOperator, Variable
from airflow.utils.decorators import apply_defaults
from typing import Optional

from requests import RequestException
import requests

class OllamaOperator(BaseOperator):
    @apply_defaults
    def __init__(
        self,
        model_name: str,
        install_ollama: bool = False,
        run_model: bool = False,
        ollama_path: Optional[str] = None,
        ollama_download_url: Optional[str] = None,
        server_url: str = "http://localhost:11434",
        max_retries: int = 3,
        retry_interval: int = 2,
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.model_name = model_name
        self.install_ollama = install_ollama
        self.run_model = run_model
        self.ollama_path = ollama_path or './ollama'
        self.ollama_download_url = ollama_download_url or "https://ollama.com/download/ollama-linux-amd64"
        self.server_url = server_url
        self.max_retries = max_retries
        self.retry_interval = retry_interval

    def execute(self, context):
        if self.install_ollama:
            self._install_ollama()
        
        self._start_ollama_server()
        self._pull_model()

        if self.run_model:
            self._run_model()

        self._control_loop()

    def _install_ollama(self):
        if os.path.exists(self.ollama_path) and os.access(self.ollama_path, os.X_OK):
            self.log.info("Ollama already exists and is executable. Skipping installation.")
            return

        self.log.info("Installing Ollama...")
        install_cmd = [
            "curl", "-L", self.ollama_download_url,
            "-o", self.ollama_path
        ]
        try:
            subprocess.run(install_cmd, check=True)
            os.chmod(self.ollama_path, 0o755)
            self.log.info("Ollama installed successfully.")
        except subprocess.CalledProcessError as e:
            self.log.error(f"Failed to download Ollama: {e}")
            raise
        except OSError as e:
            self.log.error(f"Failed to set executable permissions on Ollama: {e}")
            raise

    def _wait_for_ollama_server(self):
        self.log.info(f"Waiting for Ollama server to be ready at {self.server_url}")
        for attempt in range(self.max_retries):
            try:
                response = requests.get(f"{self.server_url}/api/tags")
                if response.status_code == 200:
                    self.log.info("Ollama server is ready")
                    return True
            except RequestException as e:
                self.log.info(f"Attempt {attempt + 1}/{self.max_retries}: Server not ready. Error: {str(e)}")
            
            time.sleep(self.retry_interval)
        
        self.log.error(f"Ollama server did not become ready after {self.max_retries} attempts")
        return False

    def _start_ollama_server(self):
        self.log.info("Starting Ollama server...")
        
        os.chdir(os.path.dirname(self.ollama_path))
        ollama_binary_name = os.path.basename(self.ollama_path)

        env = os.environ.copy()
        env['OLLAMA_ORIGINS'] = '*'

        server_cmd = f'nohup ./{ollama_binary_name} serve > ollama.log 2>&1 &'
        subprocess.run(server_cmd, shell=True, check=True, env=env)
        self.log.info("Ollama server started in the background.")

    def _pull_model(self):
        if not self._wait_for_ollama_server():
            raise RuntimeError("Ollama server is not ready. Cannot pull model.")
        
        self.log.info(f"Pulling model: {self.model_name}")
        os.chdir(os.path.dirname(self.ollama_path))
        ollama_binary_name = os.path.basename(self.ollama_path)
        pull_cmd = f'./{ollama_binary_name} pull {self.model_name}'
        try:
            self.log.info(f"Executing command: {pull_cmd}")
            result = subprocess.run(
                pull_cmd, 
                shell=True, 
                check=True, 
                capture_output=True, 
                text=True
            )
            self.log.info(f"Model {self.model_name} pulled successfully. Output:")
            self.log.info(result.stdout)
            if result.stderr:
                self.log.warning(f"Warnings during model pull: {result.stderr}")
        except subprocess.CalledProcessError as e:
            self.log.error(f"Failed to pull model {self.model_name}. Command '{e.cmd}' returned non-zero exit status {e.returncode}.")
            self.log.error(f"Error output:")
            self.log.error(e.stdout)
            self.log.error(e.stderr)
            # Log the current working directory and list its contents
            self.log.info(f"Current working directory: {os.getcwd()}")
            self.log.info(f"Directory contents: {os.listdir()}")

    def _run_model(self):
        self.log.info(f"Running model: {self.model_name}")
        os.chdir(os.path.dirname(self.ollama_path))
        ollama_binary_name = os.path.basename(self.ollama_path)
        run_cmd = [f'./{ollama_binary_name}', "run", self.model_name]
        subprocess.run(run_cmd, shell=True, check=True)
        self.log.info(f"Model {self.model_name} completed execution.")

    def _control_loop(self):
        self.log.info("Entering control loop...")
        while True:
            try:
                command = Variable.get("OLLAMA_CONTROL_COMMAND", default_var="KEEP_RUNNING")
            except KeyError:
                command = "KEEP_RUNNING"
            
            if command == "SHUTDOWN":
                self.log.info("Received SHUTDOWN command. Exiting control loop.")
                Variable.set("OLLAMA_CONTROL_COMMAND", "NONE")
                Variable.set("OLLAMA_URL", "")
                break
            
            self.log.info("Sleeping for 60 seconds...")
            time.sleep(60)

        self.log.info("Control loop ended. Task complete.")
