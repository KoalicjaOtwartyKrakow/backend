"""Module containing functions to retrieve secrets from Google Secrets Manager."""
import os
from google.cloud import secretmanager


def access_secret_version_or_none(secret_id, version_id="latest"):
    """
    Retrieve secret from Google Secret Manager. Or none, if running locally, aka
    detected by whether PROJECT_ID is set.

    Args:
        secret_id (string): Name of secret.
        version_id (str, optional): Version of secret. Defaults to "latest".

    Returns:
        Secret variable or None when running locally
    """
    project_id = os.environ.get("PROJECT_ID")

    if not project_id:
        return None

    # Create the Secret Manager client.
    client = secretmanager.SecretManagerServiceClient()

    # Build the resource name of the secret version.
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"

    # Access the secret version.
    response = client.access_secret_version(name=name)

    # Return the decoded payload.
    return response.payload.data.decode("UTF-8")
