import os
import subprocess
from pathlib import Path
from airflow.models import BaseOperator
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
        ngrok_cmd = f"nohup {self.ngrok_path} http {self.port} --log=stdout > ngrok.log 2>&1 &"
        subprocess.run(ngrok_cmd, shell=True, check=True)
        self.log.info(f"ngrok started in the background, exposing port {self.port}.")
