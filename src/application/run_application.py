from specklepy.transports.server import ServerTransport

from adapters.domain_to_speckle import create_and_send_speckle_model, model_to_speckle
from adapters.new_version import create_version
from adapters.latest_version import get_latest_version
from adapters.speckle_to_domain import receive_and_convert_data
from adapters.speckle_client import get_client
from domain.rules.loader import load_rulebook
from config import PROJECT_ID


def run_application():
    """
    Main function to run the application.
    """
    # Load the rulebook to calculate metrics
    rulebook = load_rulebook()
    
    # Initializes the client and server transport to receive data.
    client  = get_client()
    transport = ServerTransport(stream_id=PROJECT_ID, client=client)
    
    # Get the latest version of source model and 
    version = get_latest_version(client)
    
    # Receive data, converting it to the domain model.
    domain_model = receive_and_convert_data(version, transport)
    
    # Convert the domain model to a Speckle model and send it to the target model.
    object_id = create_and_send_speckle_model(domain_model = domain_model, rulebook=rulebook, transport=transport)
    print(f"✓ Created and sent Speckle model with object ID: {object_id}")
    
    # Create a new version in target model 
    create_version(client, object_id)