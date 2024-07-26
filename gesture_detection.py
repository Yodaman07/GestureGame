import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import cv2 as cv


# https://ai.google.dev/edge/mediapipe/solutions/vision/gesture_recognizer#custom_models
# https://ai.google.dev/edge/mediapipe/solutions/vision/gesture_recognizer/python#live-stream
# https://stackoverflow.com/questions/47743246/getting-timestamp-of-each-frame-in-a-video <-- I didn't use the code but the idea helped for getting the timestamp


class GestureDetector:
    def __init__(self, gestureSpace):
        self.recognizer: vision.GestureRecognizer = None
        self.maxGestureCount = gestureSpace
        self.gestures: [] = []

        self.configRecognizer("model/gesture_recognizer.task")

    def print_result(self, result: vision.GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int):
        if result.gestures != []:
            data = result.gestures[0][0]
            name = data.category_name
            confidence = data.score
            if name != "None":
                gestureData = {"Name": name, "Confidence": round(confidence * 100, 2), "Timestamp": timestamp_ms}
                if not self.gestures:
                    self.gestures.append(gestureData)
                    return

                if len(self.gestures) < 10:
                    self.gestures.append(gestureData)
                else:
                    self.gestures[0:9] = self.gestures[1:10]  # shifts list values to make space for the newest one
                    self.gestures[-1] = gestureData

        else:
            pass
            # print(f"No pose detected, timestamp: {timestamp_ms}")

    def configRecognizer(self, model_path):
        base_options = python.BaseOptions(model_asset_path=model_path)
        options = vision.GestureRecognizerOptions(base_options=base_options,
                                                  running_mode=vision.RunningMode.LIVE_STREAM,
                                                  result_callback=self.print_result)
        self.recognizer = vision.GestureRecognizer.create_from_options(options)

    def run(self):
        cam = cv.VideoCapture(0)

        if not cam.isOpened():
            print("Unable to access camera")  # kill the program if the camera is not accessed
            cam.release()
            exit()

        frame_count = 0
        while True:
            frame_count += 1
            retrieved, frame = cam.read()

            if not retrieved:
                print("Stream has likely ended")
                break

            mp_img = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
            self.recognizer.recognize_async(mp_img, frame_count) # TODO Fix the timestamp ms thing instead of just returning the frame count

            cv.imshow("stream", frame)
            # https://stackoverflow.com/questions/5217519/what-does-opencvs-cvwaitkey-function-do <-- how waitKey works
            if cv.waitKey(1) == ord("q"):  # gets the unicode value for q
                break

        cam.release()
        cv.destroyAllWindows()


g = GestureDetector(10)
g.run()
print(g.gestures)
# TODO: Fix issue where you can only get the gestures after you finish the program. Run simultaneously or smth
