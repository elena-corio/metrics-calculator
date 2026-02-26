from enum import Enum

class ProgramType(str, Enum):
    LIVING = "Living"
    WORKING = "Working"
    LEARNING = "Learning"
    COMMERCE = "Commerce"
    LEISURE = "Leisure"
    HEALTH = "Health"
    COMMUNITY = "Community"
    CIRCULATION = "Circulation"
    SUPPORT = "Support"

class MaterialType(str, Enum):
    CONCRETE = "Concrete"
    STEEL = "Steel"
    TIMBER = "Timber"
    GLASS = "Glass"
    PLASTIC = "Plastic"
    COMPOSITE = "Composite"
    
class SectionType(str, Enum):
    BOX = "Box"
    CIRCLE = "Circle"