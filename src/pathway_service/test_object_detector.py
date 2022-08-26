
from pathway_service.object_detector import ObjectDetector
from pathway_service.position_calculator import Position


def test_detect_objects():
    with open("src/pathway_service/beatles.jpg", "rb") as f:
        picture_data = f.read()
        detected_objects = ObjectDetector().detect_objects(
            image_data=picture_data, filtered_types=["person"])
        assert len(detected_objects) == 4
        assert detected_objects[0].position == Position(
            x=11, width=13, height=42)
        assert detected_objects[1].position == Position(
            x=31, width=13, height=42)
        assert detected_objects[2].position == Position(
            x=45, width=15, height=41)
        assert detected_objects[3].position == Position(
            x=68, width=14, height=39)
