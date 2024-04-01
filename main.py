import cv2
import random
from cvzone.HandTrackingModule import HandDetector
import os
import time
from playsound import playsound
import threading
import sys
current_directory = os.getcwd()
current_path = os.path.abspath(os.path.join(current_directory))
sys.path.append(current_path)
from insert_into_database import insert_gameplay_data
from dashboard_analytics import user_dashboard
# Function to play correct sound
def correct():
    playsound(os.getcwd()+'/arithmetic_module/assets/correct.mp3')

# Function to display the number matching game
def number_matching_game():
    score = 0
    detector = HandDetector(maxHands=2, detectionCon=0.8)
    cap = cv2.VideoCapture(0)

    finger_labels = {
        tuple([0, 0, 0, 0, 0]): "0",
        tuple([0, 1, 0, 0, 0]): "1",
        tuple([0, 1, 1, 0, 0]): "2",
        tuple([1, 1, 1, 0, 0]): "3",
        tuple([0, 1, 1, 1, 1]): "4",
        tuple([1, 1, 1, 1, 1]): "5",
        tuple([0, 1, 1, 1, 0]): "6",
        tuple([0, 1, 1, 0, 1]): "7",
        tuple([0, 1, 0, 1, 1]): "8",
        tuple([0, 0, 1, 1, 1]): "9",
        tuple([1, 0, 0, 0, 0]): "10"
    }

    # Initialize variables
    start_time = time.time()
    game_duration = 30  # 20 seconds
    image_duration = 30  # 30 seconds per-pair of images (i and j)
    i, j = None, None  # Initialize i and j

    # Create a full-screen window named "BG"
    cv2.namedWindow("BG", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("BG", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    # Main game loop
    while time.time() - start_time < game_duration:
        if i is None or j is None or time.time() - start_time >= image_duration:
            # Generate random numbers i and j
            i = random.randint(0, 9)
            j = random.randint(0, 9)
            start_time = time.time()  # Reset the start time for image duration

        # Load background image
        imgBG = cv2.imread(os.getcwd() + "/digits_recognition/assets/BG.png")
        imgBG = cv2.resize(imgBG, (1920, 1080))

        # Check if the video capture was opened successfully
        if not cap.isOpened():
            print("Error: Video capture not opened.")
            break

        # Capturing live video
        success, img = cap.read()
        if not success:
            print("Error: Unable to capture frame.")
            break

        # Flip the frame horizontally for a more natural view
        img = cv2.flip(img, 1)

        # Detect hands in the frame
        hands, img = detector.findHands(img)

        count_left = ""
        count_right = ""

        if hands:
            for hand in hands:
                finger_up = detector.fingersUp(hand)

                # Get the corresponding labels for finger configurations
                label = finger_labels.get(tuple(finger_up), "")

                # Concatenate the finger counts for left and right hands
                if hand["type"] == "Left":
                    count_left += label
                elif hand["type"] == "Right":
                    count_right += label

                if count_right + count_left == str(i) + str(j):
                    t1 = threading.Thread(target=correct)
                    t1.start()
                    score+=10
                    i = random.randint(0, 9)
                    j = random.randint(0, 9)

        # Display the count on the top part of the left half
        # cv2.putText(img, f"Count: {count_right + count_left}", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7,
        #             (255, 255, 255), 2)


        # Display images i and j
        image_directory = os.getcwd() + "/digits_recognition/assets"
        try:
            image_i = cv2.imread(os.path.join(image_directory, f"{i}.png"))
            image_j = cv2.imread(os.path.join(image_directory, f"{j}.png"))

            if image_i is not None and image_j is not None:
                image_i = cv2.resize(image_i, (360, 710))
                image_j = cv2.resize(image_j, (360, 710))
            else:
                print("Error loading one or both images. Please check file paths and file integrity.")
                continue
        except Exception as e:
            print(f"Error loading or resizing images: {e}")
            continue

        # Overlay images onto the background
        img = cv2.resize(img, (740, 710))
        imgBG[290:1000, 80:820] = img
        imgBG[290:1000, 1105:1465] = image_i
        imgBG[290:1000, 1475:1835] = image_j
        # Display the timer in white font, bold, on the top-right corner
        current_time = int(time.time() - start_time)
        # timer_text = f"{game_duration - current_time}"
        # cv2.putText(imgBG, timer_text, (1600,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.putText(imgBG,str(int(game_duration - current_time)),(1770,70),cv2.FONT_HERSHEY_SIMPLEX,1.5,(0,0,0),5)

        # Display the composed frame
        cv2.imshow("BG", imgBG)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release video capture and destroy windows when the game is finished
    cap.release()
    cv2.destroyAllWindows()
    cv2.namedWindow('DISPLAY SCREEN', cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty('DISPLAY SCREEN', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    score_img = cv2.imread(os.getcwd() + "/arithmetic_module/assets/score.png")
    cv2.putText(score_img, "Score", (750, 500), cv2.FONT_HERSHEY_SIMPLEX, 5, (14, 53, 138), 10)
    cv2.putText(score_img, str(score), (900, 700), cv2.FONT_HERSHEY_SIMPLEX, 5, (14, 53, 138), 10)
    cv2.imshow("DISPLAY SCREEN", score_img)
    cv2.waitKey(5000)
    cv2.destroyAllWindows()
    insert_gameplay_data(score,"digits_sign_learning")
    user_dashboard("digits_sign_learning")
    # display dashboard

# Call the function to run the game
number_matching_game()
