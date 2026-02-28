# digital-tissue-automate

Automated function for fetching latest version of a model, calculate metrics and send them to a new model.

## Reference
### KPIs Structure

1. **Liveability** - Capacity to support everyday wellbeing
   - Daylight Potential
   - Green Space Index

2. **Interconnection** - Connections between people and programs
   - Program Diversity Index
   - Circulation Efficiency

3. **Adaptability** - Capacity of spaces to transform
   - Occupancy Efficiency
   - Net Floor Area Ratio

4. **Sustainability** - Environmental performance
   - Envelope Efficiency
   - Carbon Efficiency

## Setup

### Prerequisites

- [uv](https://github.com/astral-sh/uv)
- Python 3.8+

### Installation

1. **Clone the repository:**
   ```
   git clone <your-repo-url>
   ```

2. **Install dependencies:**
   ```
   pip install uv
   ```
   ```
   uv sync
   ```

3. **Set environment variables**  
   (recommended: create a `.env` file in the project root):
   ```
   WORKSPACE_ID=your_workspace_id
   PROJECT_ID=your_project_id
   SOURCE_MODEL=your_source_model
   TARGET_MODEL=your_target_model
   ```
    For authentication, the `.env` file must include:
    - `SPECKLE_TOKEN="your_token"`
    - `SPECKLE_SERVER=https://app.speckle.systems`

   You can test authentication by running the `get_client.py` file:
   ```
   uv python src/adapters/get_client.py
   
### Running the Project

To run the main script:
```
uv python src/main.py
```
Replace `src/main.py` with your actual entry point if different.

### Running the tests

To run the main script:
```
uv pip install -e .
pytest
```
### Linting the files
```
pylint --rcfile=pylintrc src
pylint --rcfile=tests/pylintrc tests
```


