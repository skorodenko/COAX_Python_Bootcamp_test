import cv2
import uuid
import tempfile
from PIL import Image
from pathlib import Path
from natsort import natsorted


def video2jpgs(url_to_video: str, frame_folder: str, k: int = 1, f: float = 1):
    """Extracts frames from a video

    url_to_video: url to video file
    frame_folder: path to frames
    k: take only every k-th frame, omiting k-1 frames, to decrease gif size, takes every frame by default
    f: resizing coeficient, doesn't resize by default
    """
    video_capture = cv2.VideoCapture(url_to_video)
    still_reading, image = video_capture.read()
    frame_count = 0
    while still_reading:
        # Take every k-th frame
        if frame_count % k == 0:
            image = cv2.resize(image, None, fx=f, fy=f, interpolation=cv2.INTER_AREA)
            cv2.imwrite(f"{frame_folder}/{frame_count}.jpg", image)
        still_reading, image = video_capture.read()
        frame_count += 1


def jpgs2gif(frame_folder, output_file):
    """Converts all jpgs from a folder to a gif

    frame_folder: path to frames
    output_file: path to output file
    """
    images = Path(frame_folder).glob("*.jpg")
    images = [Path(p) for p in natsorted([str(p) for p in images])]

    frames = [Image.open(image) for image in images]
    frames[0].save(
        output_file,
        format="GIF",
        append_images=frames[1:],
        save_all=True,
        duration=10,
        loop=0,
    )


def tiktok2gif(
    url_to_video: str = None, /, output: Path = Path("."), k: int = 10, f: float = 1 / 3
) -> Path:
    """Converts tiktok video from specified url to gif

    url_to_video: url to video file
    output: Path object, indicates output folder, working directory by default
    k: take only every k-th frame, omiting k-1 frames, to decrease gif size, 10 by default
    f: resizing coeficient, 1/3 by default

    returns path to created gif
    """
    if url_to_video == None:
        raise ValueError("url_to_video should not be None")

    output_file = output / f"{uuid.uuid4().hex}.gif"

    with tempfile.TemporaryDirectory() as tmpdir:
        video2jpgs(url_to_video, tmpdir, k, f)
        jpgs2gif(tmpdir, output_file)

    return output_file
