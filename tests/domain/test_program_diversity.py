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
