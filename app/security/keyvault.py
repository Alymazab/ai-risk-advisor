"""
Azure Key Vault helper.
Only responsible for retrieving secrets.
"""

import os
from functools import lru_cache

from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient


load_dotenv()

VAULT_URL = os.getenv("AZURE_KEY_VAULT_URL")

if not VAULT_URL:
    raise ValueError("AZURE_KEY_VAULT_URL is missing from .env")


credential = DefaultAzureCredential()
client = SecretClient(vault_url=VAULT_URL, credential=credential)


@lru_cache(maxsize=20)
def get_secret(secret_name: str) -> str:
    return client.get_secret(secret_name).value