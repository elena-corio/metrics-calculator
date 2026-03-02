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


def automate_function(automate_context: AutomationContext) -> None:
    """Speckle Automate function for calculating KPI metrics.
    
    Fetches the latest version of a model, calculates KPIs (Daylight Potential, 
    Green Space Index, Program Diversity, etc.), and sends results to a new model.

    Args:
        automate_context: A context-helper object that carries relevant information
            about the runtime context of this function.
            It gives access to the Speckle project data that triggered this run.
    """
    try:
        run_application(automate_context)
        automate_context.mark_run_success("Metrics calculated and sent successfully.")
    except Exception as e:
        automate_context.mark_run_failed(f"Error calculating metrics: {str(e)}")
        raise


# make sure to call the function with the executor
if __name__ == "__main__":
    # NOTE: always pass in the automate function by its reference; do not invoke it!
    
    # Pass in the function reference to the executor (no inputs needed)
    execute_automate_function(automate_function)
