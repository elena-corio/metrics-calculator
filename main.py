"""This module contains the function's business logic.

Use the automation_context module to wrap your function in an Automate context helper.
"""

import sys
import os

# Add src directory to Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from pydantic import Field
from speckle_automate import (
    AutomateBase,
    AutomationContext,
    execute_automate_function,
)

from application.run_application import run_application


class FunctionInputs(AutomateBase):
    """Input parameters for the metrics calculator function.
    
    These values are configured in the Speckle Automate UI.
    """
    
    project_id: str = Field(
        title="Project ID",
        description="The ID of the Speckle project"
    )
    
    source_model_id: str = Field(
        title="Source Model ID",
        description="The ID of the source model to fetch and analyze"
    )
    
    target_model_id: str = Field(
        title="Target Model ID",
        description="The ID of the target model where results will be sent"
    )


def automate_function(
    automate_context: AutomationContext,
    function_inputs: FunctionInputs,
) -> None:
    """Speckle Automate function for calculating KPI metrics.
    
    Fetches a model, calculates KPIs (Daylight Potential, Green Space Index, 
    Program Diversity, etc.), and sends results to a target model.

    Args:
        automate_context: A context-helper object that carries relevant information
            about the runtime context of this function.
        function_inputs: User-defined inputs containing source and target model IDs.
    """
    try:
        run_application(
            automate_context=automate_context,
            project_id=automate_context.automation_run_data.project_id,
            source_model_id=automate_context.automation_run_data.model_id,
            target_model_id=function_inputs.target_model_id
        )
        automate_context.mark_run_success("Metrics calculated and sent successfully.")
    except Exception as e:
        automate_context.mark_run_failed(f"Error calculating metrics: {str(e)}")
        raise


# make sure to call the function with the executor
if __name__ == "__main__":
    # NOTE: always pass in the automate function by its reference; do not invoke it!
    
    # Pass in the function reference with the inputs schema to the executor
    execute_automate_function(automate_function, FunctionInputs)
