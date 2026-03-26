def test_calculate_program_diversity_index_chunked_average():
    # 30 units: 15 at level 0, 15 at level 15
    # First chunk: 10 LIVING, 5 WORKING
    # Second chunk: 5 LIVING, 10 WORKING
    units = [
        make_unit(level=0, program=ProgramType.LIVING) for _ in range(10)
    ] + [
        make_unit(level=0, program=ProgramType.WORKING) for _ in range(5)
    ] + [
        make_unit(level=15, program=ProgramType.LIVING) for _ in range(5)
    ] + [
        make_unit(level=15, program=ProgramType.WORKING) for _ in range(10)
    ]
    # Chunk 1: 10 LIVING, 5 WORKING: 1 - ((10^2 + 5^2)/15^2) = 1 - (100+25)/225 = 1 - 125/225 = 0.4444...
    # Chunk 2: 5 LIVING, 10 WORKING: same as above
    expected = 0.4444444444444444
    result = calculate_program_diversity_index(units)
    assert abs(result - expected) < 1e-6, f"Expected {expected}, got {result}"

def test_calculate_program_diversity_index_irregular_chunks():
    # 10 units at level 0, 5 at level 20 (different chunk sizes)
    units = [
        make_unit(level=0, program=ProgramType.LIVING) for _ in range(7)
    ] + [
        make_unit(level=0, program=ProgramType.WORKING) for _ in range(3)
    ] + [
        make_unit(level=20, program=ProgramType.LIVING) for _ in range(2)
    ] + [
        make_unit(level=20, program=ProgramType.WORKING) for _ in range(3)
    ]
    # Chunk 1: 7 LIVING, 3 WORKING: 1 - ((49+9)/100) = 1 - 58/100 = 0.42
    # Chunk 2: 2 LIVING, 3 WORKING: 1 - ((4+9)/25) = 1 - 13/25 = 0.48
    expected = (0.42 + 0.48) / 2
    result = calculate_program_diversity_index(units)
    assert abs(result - expected) < 1e-6, f"Expected {expected}, got {result}"
from domain.model.fixture import make_unit
from domain.metrics.program_diversity import calculate_program_diversity_index
from domain.model.types import ProgramType

def test_calculate_program_diversity_index_single_program():
    units = [make_unit(), make_unit(), make_unit()]
    # All same program (LIVING), diversity index should be 0
    assert calculate_program_diversity_index(units) == 0.0

def test_calculate_program_diversity_index_multiple_programs():
    units = [
        make_unit(program=ProgramType.LIVING), 
        make_unit(program=ProgramType.LIVING), 
        make_unit(program=ProgramType.WORKING), 
        make_unit(program=ProgramType.WORKING)
        ]
    # 2 of LIVING, 2 of WORKING, diversity index = 1 - (2^2 + 2^2) / 4^2 = 1 - (4+4)/16 = 0.5
    assert calculate_program_diversity_index(units) == 0.5

def test_calculate_program_diversity_index_empty():
    units = []
    assert calculate_program_diversity_index(units) == 0.0
