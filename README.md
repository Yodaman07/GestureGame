# Gesture Game
This is a maze game that gives you randomly generated mazes to complete using hand gestures

**Made By: Ayaan Irshad**

## How to Install
With the project open, run `pip3 -r requirements.txt` to install all nescessary packages, and then run `pip3 main.py` to run the game.

## How to play
There are 4 main gestures in the game:
* **Controls**
  * `Open_Palm` = Right
  * `Closed_Fist` = Left
  * `Thumbs_Down` = Down
  * `Victory` = Up
  * `ILoveYou` = Reset position to the start

Tip: Sometimes the model is tricky to detect your hand movements. I would suggest starting with your palm open and when it is being detected, move into the other hand positions from there.

## Maze
The maze is randomly generated every time and uses a **depth first backtracking** algorithm.

Here are some good resources for learning about maze generation algorithms:

[Wikipedia on Maze Gen Algorithms](https://en.wikipedia.org/wiki/Maze_generation_algorithm)

[Github demonstrations](https://github.com/john-science/mazelib/blob/main/docs/MAZE_GEN_ALGOS.md)

[Stack Overflow Discussion]( https://stackoverflow.com/questions/38502/whats-a-good-algorithm-to-generate-a-maze)

## Gesture Detection
Using Google's mediapipe library, I am able to detect 8 different hand gestures ([page with model info](https://ai.google.dev/edge/mediapipe/solutions/vision/gesture_recognizer#custom_models), I am using the HandGestureClassifier).
The hand wireframe isn't shown on the screen, but the results are detected and shown in the icons on screen.

Google provides steps for setting up the basic code to detect your gestures [here](https://ai.google.dev/edge/mediapipe/solutions/vision/gesture_recognizer/python#live-stream)
(You are analysing each frame of an OpenCV livestream, and then calling a callback function with the data from the result to see if gestures are detected or not)


### Gestures from the model

The model can detect 8 gestures as stated above. These can be seen below:
* Gestures:
  * `Unknown`
  * `Closed_Fist`
  * `Open_Palm`
  * `Pointing_Up`
  * `Thumb_Down`
  * `Thumb_Up`
  * `Victory`
  * `ILoveYou`

## Icons
The hollow icons used were not made by me, they were all from
[flaticon.com](https://www.flaticon.com/). The icons with a `_f` after the name are modified versions of the hollow icons just filled in using photoshop.

