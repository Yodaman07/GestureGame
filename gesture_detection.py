import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import cv2 as cv


# https://ai.google.dev/edge/mediapipe/solutions/vision/gesture_recognizer#custom_models
# https://ai.google.dev/edge/mediapipe/solutions/vision/gesture_recognizer/python#live-stream
# https://stackoverflow.com/questions/47743246/getting-timestamp-of-each-frame-in-a-video <-- I didn't use the code but the idea helped for getting the timestamp
def print_result(result: vision.GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int):
    if result.gestures != []:
        data = result.gestures[0][0]
        name = data.category_name
        confidence = data.score
        if name != "None":
            print(f"Name: {name}, Confidence: {round(confidence * 100, 2)}%, Timestamp: {timestamp_ms}")
    else:
        pass
        # print(f"No pose detected, timestamp: {timestamp_ms}")


base_options = python.BaseOptions(model_asset_path="model/gesture_recognizer.task")
options = vision.GestureRecognizerOptions(base_options=base_options, running_mode=vision.RunningMode.LIVE_STREAM,
                                          result_callback=print_result)
recognizer = vision.GestureRecognizer.create_from_options(options)

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
    recognizer.recognize_async(mp_img, 100 * frame_count)

    cv.imshow("stream", frame)
    # https://stackoverflow.com/questions/5217519/what-does-opencvs-cvwaitkey-function-do <-- how waitKey works
    if cv.waitKey(1) == ord("q"):  # gets the unicode value for q
        break

cam.release()
cv.destroyAllWindows()
