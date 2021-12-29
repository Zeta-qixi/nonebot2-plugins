import cv2
import mediapipe
import os

from PIL import Image
from io import BytesIO
import requests


PATH =os.path.dirname(__file__)+'/data/'
IMAGE_PATH = PATH + 'out.png'
IMAGE_INPUT =  PATH + 'in.png'
mp_face_detection = mediapipe.solutions.face_detection
mp_drawing = mediapipe.solutions.drawing_utils



def get_detection_res(**kargs):
    url = kargs.get('url', None)
    res = requests.get(url)
    img = Image.open(BytesIO(res.content))
    img.save(IMAGE_INPUT)

    with mp_face_detection.FaceDetection(
        model_selection=1, min_detection_confidence=0.4) as face_detection:
    
        image = cv2.imread(IMAGE_INPUT)
        # Convert the BGR image to RGB and process it with MediaPipe Face Detection.
        results = face_detection.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        # Draw face detections of each face.
        if not results.detections:
            return False

        annotated_image = image.copy()
        for detection in results.detections:
            mp_drawing.draw_detection(annotated_image, detection)
        cv2.imwrite(IMAGE_PATH, annotated_image)

        return True