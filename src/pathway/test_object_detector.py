
import pytest
from pathway.object_detector import ObjectDetector

@pytest.mark.skip(reason="🚧 work in progress")
def test_detect_objects():
  with open("src/pathway/beatles.jpg", "rb") as f:
    picture_data = f.read()
    detected_objects = ObjectDetector().detect_objects(picture_data=picture_data)
    assert len(detected_objects) == 4
    # @todo check 4 beatles detected with right positions