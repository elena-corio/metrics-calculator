### Backend (Hexagonal/Clean Architecture)

```
domain/                   Core business logic (models, calculations, rules)
├── models/           
├── metrics/         
└── rules/

application/              Orchestration layer
├── metrics_service.py      
└── metrics_workflow.py     

adapters/                 Speckle integration
├── get_client.py
├── get_latest_version.py
├── create_version.py
├── receive_data.py
├── send_data.py
└── mappers.py      
   
```

### Metric Calculation Flow

```
Speckle Project
    ↓
get_client() → SpecklePy client
    ↓
get_latest_version() → Fetch last evrsion in source model
    ↓
receive_data() → Download and deserialize model
    ↓
mappers.py → Convert Speckle objects to Domain models
    ↓
metrics_service.calculate_all_metrics(model)
    ├── daylight_potential()
    ├── green_space_index()
    ├── program_diversity_index()
    ├── circulation_efficiency()
    ├── occupancy_efficiency()
    ├── net_floor_area_ratio()
    ├── envelope_efficiency()
    └── carbon_efficiency()
    ↓
create_version() → Create new version in target model
    ↓
send_data() → Send data to new target model
    → 