import pytest
from pathway_service.position_calculator import Position, PositionCalculator


@pytest.mark.parametrize("box_points,expected_position", [
    # Center
    ((480, 0, 720, 200), Position(x=50, width=20, height=25)),
    # Left
    ((180, 0, 420, 200), Position(x=25, width=20, height=25)),
    # Right
    ((960, 0, 1200, 200), Position(x=90, width=20, height=25)),
])
def test_compute_position(box_points, expected_position):
    calculator = create_position_calculator()
    position = calculator.compute_position(box_points=box_points)
    assert position == expected_position


def create_position_calculator():
    return PositionCalculator(width=1200, height=800)
