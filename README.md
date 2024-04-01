# Digit_Recognition_module


The provided code is a Python script that implements a number matching game using hand gestures captured via webcam.

Imports necessary libraries including OpenCV (cv2), a hand tracking module (HandTrackingModule), os, time, random, playsound, threading, and some modules for database interaction and analytics.
Defines a function correct() to play a correct sound.
Defines the main function number_matching_game() which runs the number matching game.
Initializes variables and constants including the hand detector, video capture, finger labels (mapping finger configurations to numbers), game duration, image duration, and initializes i and j variables.
Enters a main game loop where it continuously captures video frames from the webcam.
Within the loop, it generates random numbers i and j and displays them on the screen along with the live webcam feed.
It detects hands in the webcam feed and maps the finger configurations to labels using finger_labels.
Concatenates the finger counts for left and right hands to form numbers and checks if the sum matches the current i + j.
If the sum matches, it plays a correct sound, increments the score, generates new random numbers i and j, and continues the game loop.
Displays the current score on the screen.
Terminates the game loop if the 'q' key is pressed.
After the game loop ends (when time exceeds game_duration), it releases the video capture, displays the final score on a full-screen window, waits for 5 seconds, inserts the gameplay data into a database, and displays the user dashboard related to the game.
Overall, this code implements a simple number matching game using hand gestures and provides a score based on the accuracy and speed of the player's responses
