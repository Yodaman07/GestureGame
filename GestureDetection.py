import mediapipe as mp
import numpy as np
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import cv2 as cv


# https://ai.google.dev/edge/mediapipe/solutions/vision/gesture_recognizer#custom_models
# https://ai.google.dev/edge/mediapipe/solutions/vision/gesture_recognizer/python#live-stream
# https://stackoverflow.com/questions/47743246/getting-timestamp-of-each-frame-in-a-video <-- I didn't use the code but the idea helped for getting the timestamp

# TODO improve accuracy of the gesture detector/draw the results
class GestureDetector:
    def __init__(self, gestureSpace):
        self.recognizer: vision.GestureRecognizer = None
        self.maxGestureCount = gestureSpace
        self.gestures: [] = []
        # https: // ai.google.dev / edge / mediapipe / solutions / vision / gesture_recognizer
        self.possibleGestures = ["None", "Closed_Fist", "Open_Palm", "Pointing_Up", "Thumb_Down", "Thumb_Up",
                                 "Victory", "ILoveYou"]

        self.frame_count: int = 0
        self.cam: cv.VideoCapture = None
        self.shrinkFactor = 5  # factor to shrink the camera image from
        # DO NOT CHANGE
        self.width: int = 0
        self.height: int = 0

        self.configRecognizer("model/gesture_recognizer.task")

    def print_result(self, result: vision.GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int):
        if result.gestures != []:
            data = result.gestures[0][0]
            name = data.category_name
            confidence = data.score
            gestureData = {"Name": name, "Confidence": round(confidence * 100, 2), "Timestamp": timestamp_ms}
            # print(gestureData)
            self.appendGestureData(gestureData)

        else:
            gestureData = {"Name": None, "Confidence": None, "Timestamp": timestamp_ms}
            # print(gestureData)
            self.appendGestureData(gestureData)

    def appendGestureData(self, gestureData):
        if not self.gestures:
            self.gestures.append(gestureData)
            return

        if len(self.gestures) < 10:
            self.gestures.append(gestureData)
        else:
            self.gestures[0:9] = self.gestures[1:10]  # shifts list values to make space for the newest one
            self.gestures[-1] = gestureData

    def configRecognizer(self, model_path):
        base_options = python.BaseOptions(model_asset_path=model_path)
        options = vision.GestureRecognizerOptions(base_options=base_options,
                                                  running_mode=vision.RunningMode.LIVE_STREAM,
                                                  result_callback=self.print_result)
        self.recognizer = vision.GestureRecognizer.create_from_options(options)

    def initStream(self):
        self.cam = cv.VideoCapture(0)

        if not self.cam.isOpened():
            print("Unable to access camera")  # kill the program if the camera is not accessed
            self.cam.release()
            exit()

        self.width = int(self.cam.get(cv.CAP_PROP_FRAME_WIDTH) / self.shrinkFactor)
        self.height = int(self.cam.get(cv.CAP_PROP_FRAME_HEIGHT) / self.shrinkFactor)

        self.frame_count = 0

    def getCurrentFrame(self) -> np.array:  # camera information to get called every frame <-- must be put in a while loop
        self.frame_count += 1
        retrieved, frame = self.cam.read()

        mp_img = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
        self.recognizer.recognize_async(mp_img, self.frame_count) # TODO Fix the timestamp ms thing instead of just returning the frame count

        frame = cv.resize(frame, (int(self.width), int(self.height)))
        if not retrieved:
            print("Stream has likely ended")
            return
        return frame
