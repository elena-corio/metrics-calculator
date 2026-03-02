
# digital-tissue-automate

Automated function for fetching the latest version of a model, calculating KPIs, and sending results to a new model via Speckle Automate.

## KPIs Structure

1. **Liveability**: Daylight Potential, Green Space Index
2. **Interconnection**: Program Diversity Index, Circulation Efficiency
3. **Adaptability**: Occupancy Efficiency, Net Floor Area Ratio
4. **Sustainability**: Envelope Efficiency, Carbon Efficiency

## Setup & Installation

### Prerequisites
- Python 3.10+
- [uv](https://github.com/astral-sh/uv) (recommended for dependency management)
- Docker (for containerized deployment)

### Install dependencies

Using **uv** (recommended):
```bash
uv sync
```
If you previously used Poetry, you can migrate dependencies to `pyproject.toml` and use `uv sync`.

Using **pip** (alternative):
```bash
pip install -e ".[dev]"
```

### Environment Variables
Create a `.env` file in the project root:
```
SPECKLE_TOKEN=your_personal_access_token
SPECKLE_SERVER_URL=https://app.speckle.systems
SPECKLE_PROJECT_ID=your_project_id
SPECKLE_AUTOMATION_ID=your_test_automation_id
```

**Note:** Workspace ID, source model ID, and target model ID are stored in `src/config.py` as they are specific to this function's domain logic.

## Commands

### Run main script (will not work with speckle automate)
```bash
python main.py
```

### Run as Speckle Automate contract
```bash
python main.py '<automation_context_json>' '<function_inputs_json>' <token>
```

### Run tests
```bash
uv pip install -e .
pytest
```

### Lint code
```bash
pylint --rcfile=pylintrc src
pylint --rcfile=tests/pylintrc tests
```

## Docker Usage

### Build Docker image
```bash
docker build -t digital-tissue-automate .
```

### Run Docker container (Speckle Automate contract)
```bash
docker run --rm digital-tissue-automate \
   python src/main.py '<automation_context_json>' '<function_inputs_json>' <token>
```

## Deployment & Automation

- To deploy as a Speckle Automate function, publish a GitHub release and ensure your Docker image is built and pushed to your registry (see `.github/workflows/main.yml`).
- Register your function at [Speckle Automate](https://automate.speckle.dev/).

## Resources
- [SpecklePy Guide](https://speckle.guide/dev/python.html)
- [Speckle Automate](https://automate.speckle.dev/)


