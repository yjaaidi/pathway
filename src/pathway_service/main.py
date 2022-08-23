from fastapi import Depends, FastAPI, File

from pathway_service.object_detector import ObjectDetector
import uvicorn

app = FastAPI()

object_detector = ObjectDetector()


@app.post("/images")
async def processImage(image: bytes = File()):
    items = object_detector.detect_objects(
        image_data=image, filtered_types=["person"])
    return {'items': items}


def start():
    uvicorn.run("pathway_service.main:app",
                host="0.0.0.0", port=8000, reload=True)
