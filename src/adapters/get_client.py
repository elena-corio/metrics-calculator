"""
Get a SpeckleClient instance authenticated with a token.

"""
import os
from dotenv import load_dotenv
from specklepy.api.client import SpeckleClient


def get_client() -> SpeckleClient:
    """
    Authenticate and return a SpeckleClient instance.
    Requires SPECKLE_TOKEN in environment or .env file.
    """
    # Load environment variables from a local .env file, if present
    load_dotenv()

    # Get token and server host from environment
    token = os.environ.get("SPECKLE_TOKEN")
    server_host = os.environ.get("SPECKLE_SERVER", "app.speckle.systems")

    if not token:
        raise ValueError("Set SPECKLE_TOKEN in your .env file and re-run.")

    # Authenticate
    speckle_client = SpeckleClient(host=server_host)
    speckle_client.authenticate_with_token(token)

    return speckle_client


if __name__ == "__main__":
    # Test authentication when running this script directly
    client = get_client()
    user = client.active_user.get()
    print(f"✓ Logged in as {user.name} on {client.url}")
