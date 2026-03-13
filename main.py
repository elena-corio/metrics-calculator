"""This module contains the function's business logic.

Use the automation_context module to wrap your function in an Automate context helper.
"""

import sys
import os

# Add src directory to Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from speckle_automate import (
    AutomationContext,
    execute_automate_function,
)

from application.run_application import run_application
from adapters.metric_model_setup import get_or_create_metrics_model
from adapters.validators import ValidationResult
from config import METRICS_MODEL_NAME


def automate_function(
    automate_context: AutomationContext
) -> None:
    """Speckle Automate function for calculating KPI metrics.
    
    Fetches a model, calculates KPIs (Daylight Potential, Green Space Index, 
    Program Diversity, etc.), and sends results to a dedicated 'metrics' model.

    Args:
        automate_context: A context-helper object that carries relevant information
            about the runtime context of this function, including project_id and model_id.
    """
    try:
        # Get or create the metrics model in the project
        target_model_id = get_or_create_metrics_model(
            client=automate_context.speckle_client,
            project_id=automate_context.automation_run_data.project_id,
            metrics_model_name=METRICS_MODEL_NAME
        )
        
        result = run_application(
            automate_context=automate_context,
            project_id=automate_context.automation_run_data.project_id,
            source_model_id=automate_context.automation_run_data.model_id,
            target_model_id=target_model_id
        )
        
        # Check if validation failed
        if isinstance(result, ValidationResult) and not result.is_valid:
            automate_context.mark_run_failed(
                status_message=result.message,
                results=result.to_dict()
            )
            return
        
        automate_context.mark_run_success("Metrics calculated and sent successfully.")
    except Exception as e:
        automate_context.mark_run_failed(f"Unexpected error: {str(e)}")
        raise


# make sure to call the function with the executor
if __name__ == "__main__":
    # NOTE: always pass in the automate function by its reference; do not invoke it!
    
    # Pass in the function reference to the executor
    execute_automate_function(automate_function)
