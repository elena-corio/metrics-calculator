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
    Calculate the average program diversity index for units, chunked by every 15 levels.
    Each chunk contains all units whose level falls within a 15-level window (0-14, 15-29, etc).
    Returns the average diversity index across all non-empty chunks.
    """
    if not units:
        return 0.0

    # Group units by 15-level chunks
    from collections import defaultdict
    chunks = defaultdict(list)
    for unit in units:
        # Integer division to determine the chunk index
        chunk_idx = int(unit.level) // 15
        chunks[chunk_idx].append(unit)

    # Calculate diversity index for each chunk
    indices = []
    for chunk_units in chunks.values():
        program_counts = count_programs(chunk_units)
        total_units = len(chunk_units)
        if total_units == 0:
            continue
        program_frequencies = calculate_program_frequencies(program_counts)
        index = 1 - (program_frequencies / (total_units ** 2))
        indices.append(index)

    if not indices:
        return 0.0
    return sum(indices) / len(indices)
