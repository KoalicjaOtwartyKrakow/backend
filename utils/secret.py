"""Module containing functions to retrieve secrets from Google Secrets Manager."""
import os
from google.cloud import secretmanager

PROJECT_ID = os.environ.get("PROJECT_ID", "<LOCAL>")


def access_secret_version(secret_id, version_id="latest"):
    """Retrieve secret from Google Secret Manager.

    Args:
        secret_id (string): Name of secret.
        version_id (str, optional): Version of secret. Defaults to "latest".

    Returns:
        Secret variable.
    """
    # Create the Secret Manager client.
    client = secretmanager.SecretManagerServiceClient()

    # Build the resource name of the secret version.
    name = f"projects/{PROJECT_ID}/secrets/{secret_id}/versions/{version_id}"

    # Access the secret version.
    response = client.access_secret_version(name=name)

    # Return the decoded payload.
    return response.payload.data.decode("UTF-8")
