import os
import subprocess
import time
import requests
from pathlib import Path
from airflow.models import BaseOperator, Variable
from airflow.utils.decorators import apply_defaults
from typing import Optional

class NgrokExposerOperator(BaseOperator):
    @apply_defaults
    def __init__(
        self,
        port: int,
        auth_token: str,
        install_ngrok: bool = False,
        ngrok_path: Optional[str] = None,
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.port = port
        self.auth_token = auth_token
        self.install_ngrok = install_ngrok
        self.ngrok_path = ngrok_path or './ngrok'

    def execute(self, context):
        if self.install_ngrok:
            self._install_ngrok()
        self._set_auth_token()
        self._start_ngrok()
        ngrok_url = self._get_ngrok_url()
        self._set_airflow_variable(ngrok_url)

    def _install_ngrok(self):
        self.log.info("Installing ngrok...")
        install_cmd = [
            "curl", "-O", "https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz"
        ]
        subprocess.run(install_cmd, check=True)
        
        extract_cmd = ["tar", "xvzf", "ngrok-v3-stable-linux-amd64.tgz"]
        subprocess.run(extract_cmd, check=True)
        
        os.remove("ngrok-v3-stable-linux-amd64.tgz")
        os.chmod(self.ngrok_path, 0o755)
        self.log.info("ngrok installed successfully.")

    def _set_auth_token(self):
        self.log.info("Setting ngrok auth token...")
        auth_cmd = [self.ngrok_path, "authtoken", self.auth_token]
        subprocess.run(auth_cmd, check=True)
        self.log.info("ngrok auth token set successfully.")

    def _start_ngrok(self):
        self.log.info(f"Starting ngrok to expose port {self.port}...")
        ngrok_cmd = f'nohup {self.ngrok_path} http {self.port} --host-header="localhost:11434" --log=stdout > ngrok.log 2>&1 &'
        subprocess.run(ngrok_cmd, shell=True, check=True)
        self.log.info(f"ngrok started in the background, exposing port {self.port}.")

    def _get_ngrok_url(self):
        self.log.info("Fetching Ngrok URL...")
        retries = 5
        while retries > 0:
            try:
                response = requests.get("http://localhost:4040/api/tunnels")
                data = response.json()
                ngrok_url = data['tunnels'][0]['public_url']
                self.log.info(f"Ngrok URL fetched successfully: {ngrok_url}")
                return ngrok_url
            except Exception as e:
                self.log.warning(f"Failed to fetch Ngrok URL. Retrying... Error: {str(e)}")
                retries -= 1
                time.sleep(2)
        
        raise Exception("Failed to fetch Ngrok URL after multiple attempts")

    def _set_airflow_variable(self, ngrok_url):
        self.log.info("Setting Airflow variable OLLAMA_URL...")
        Variable.set("OLLAMA_URL", ngrok_url)
        self.log.info(f"Airflow variable OLLAMA_URL set to: {ngrok_url}")
