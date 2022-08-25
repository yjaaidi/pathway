
from io import BytesIO
from numpy.typing import NDArray
from PIL import Image


def frame_to_jpg(frame: NDArray) -> bytes:
    image = Image.fromarray(frame.astype('uint8'), 'RGB')
    image_buffer = BytesIO()
    image.save(image_buffer, format='JPEG')
    return image_buffer.getvalue()
