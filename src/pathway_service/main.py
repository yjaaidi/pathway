from fastapi import FastAPI, File, status

from pathway_service.object_detector import ObjectDetector
import os
import uvicorn  # type:ignore

app = FastAPI()

object_detector = ObjectDetector()


@app.post("/images", status_code=status.HTTP_201_CREATED)
async def processImage(image: bytes = File()):
    items = object_detector.detect_objects(
        image_data=image, filtered_types=["person"])
    return {'items': items}


def start(reload=False):
    uvicorn.run("pathway_service.main:app",
                host="0.0.0.0", port=int(os.environ.get('PORT', 8000)), reload=reload, workers=1)


def start_dev():
    start(reload=True)
