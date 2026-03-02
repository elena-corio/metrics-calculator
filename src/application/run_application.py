from specklepy.transports.server import ServerTransport

from adapters.domain_to_speckle import create_and_send_speckle_model, model_to_speckle
from adapters.new_version import create_version
from adapters.latest_version import get_latest_version
from adapters.speckle_to_domain import receive_and_convert_data
from adapters.speckle_client import get_client
from domain.rules.loader import load_rulebook
from config import PROJECT_ID


def run_application(automate_context=None, function_inputs=None, token=None):
    """
    Main function to run the application.
    
    Args:
        automate_context: AutomationContext from Speckle Automate (preferred)
        function_inputs: Function inputs from Speckle Automate
        token: Optional token (not used when automate_context provided)
    """
    # Load the rulebook to calculate metrics
    rulebook = load_rulebook()
    
    # Use provided automate_context or create a standalone client
    if automate_context:
        # Use the pre-authenticated client from Speckle Automate
        client = automate_context.speckle_client
        # Receive the version that triggered this automation
        version = automate_context.receive_version()
    else:
        # Standalone mode (for local testing)
        client = get_client()
        version = get_latest_version(client)
    
    # Create transport for the project
    transport = ServerTransport(stream_id=PROJECT_ID, client=client)
    
    # Receive data, converting it to the domain model.
    domain_model = receive_and_convert_data(version, transport)
    
    # Convert the domain model to a Speckle model and send it to the target model.
    object_id = create_and_send_speckle_model(
        domain_model=domain_model, 
        rulebook=rulebook, 
        transport=transport
    )
    print(f"✓ Created and sent Speckle model with object ID: {object_id}")
    
    # Create a new version in target model 
    create_version(client, object_id)