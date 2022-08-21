
from pathway.object_detector import ObjectDetector
from pathway.position_calculator import Position

def test_detect_objects():
  with open("src/pathway/beatles.jpg", "rb") as f:
    picture_data = f.read()
    detected_objects = ObjectDetector().detect_objects(picture_data=picture_data, filtered_types=["person"])
    assert len(detected_objects) == 4
    assert detected_objects[0].position == Position(x=-77, width=13, height=42)
    assert detected_objects[1].position == Position(x=-37, width=13, height=42)
    assert detected_objects[2].position == Position(x=-10, width=15, height=41)
    assert detected_objects[3].position == Position(x=37, width=14, height=39)