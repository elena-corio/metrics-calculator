"""
Calculate program diversity index based on the distribution of program types among units.
"""

from domain.model.elements import Unit

# program_i_units_count	= count(program_i_units)
# program_i_frequencies	= Sum(program_i_units_count) **2
# program_diversity_index = 1 - program_frequencies / (program_units_count**2)

def count_programs(units: list[Unit]) -> dict[str, int]:
    """
    Count the number of units for each program type.
    """
    program_counts = {}
    for unit in units:
        program_counts[unit.program] = program_counts.get(unit.program, 0) + 1
    return program_counts

def calculate_program_frequencies(program_counts: dict[str, int]) -> int:
    """
    Calculate the sum of squares of the number of units for each program type.
    """
    return sum(count ** 2 for count in program_counts.values())

def calculate_program_diversity_index(units: list[Unit]) -> float:
    """
    Calculate the program diversity index for a list of units.
    """
    program_counts = count_programs(units)
    total_units = len(units)
    if total_units == 0:
        return 0.0
    program_frequencies = calculate_program_frequencies(program_counts)
    return 1 - (program_frequencies / (total_units ** 2))
