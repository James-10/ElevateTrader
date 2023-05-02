"""Config module for elevate_trader"""
import os
from pydantic import (
    BaseSettings
)

from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

from utils.logging import get_logger

LOGGER = get_logger()


AZURE_CLIENT_SECRET = os.environ.get("AZURE_CLIENT_SECRET")

if AZURE_CLIENT_SECRET:
    LOGGER.info("Retrieving secrets from AZ KeyVaults")
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=os.environ.get("VAULT_URL"), credential=credential)
    secrets_iter = client.list_properties_of_secrets()

    secrets_dict = {}
    
    for secret in secrets_iter:
        secret_obj = client.get_secret(secret.name)
        secrets_dict.update({secret.name.replace("-", "_"): secret_obj.value })
    
    os.environ.update(secrets_dict)



class Settings(BaseSettings):
    database_uri: str = ""
    jpy_multiplier: int = 1000
    other_multiplier: int = 100000
    std_lot_contract: int = 100000
    fxchoice_path: str = ""
    cryptorocket_path: str = ""
    vaultmarkets_path: str = ""

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


Config = Settings()

if __name__ == "__main__":
    print(Config.fxchoice_path)