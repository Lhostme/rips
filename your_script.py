import time
import os
import cv2

def main():
    print(os.listdir())

    files = os.listdir("/")
    volume = "/" + next((s for s in files if "vidData" in s), None)
    print("volume", volume)

    # Set video input/output location
    inputPath = volume + "/vidtest.mp4"
    outputPath = volume + "/result.mp4"

    # Open the input video
    capture = cv2.VideoCapture(inputPath)
    if not capture.isOpened():
        print("Error: Could not open video file.")
        exit()

    # Get video properties
    frameWidth = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    frameHeight = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(capture.get(cv2.CAP_PROP_FPS))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    # Create VideoWriter object
    output = cv2.VideoWriter(outputPath, fourcc, fps, (frameWidth, frameHeight))

    print("Writing text to file")
    # Loop through video frames
    while True:
        ret, frame = capture.read()
        if not ret:
            break

        # Add text to the frame
        text = "OpenCV Text Example"
        position = (50, 50)  # Coordinates (x, y) for the text
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1
        color = (0, 255, 0)  # Green
        thickness = 2
        cv2.putText(frame, text, position, font, font_scale, color, thickness)

        # Write the frame to the output video
        output.write(frame)

    # Release resources
    capture.release()
    output.release()

    print("done writing")
    print(os.listdir(volume))

if __name__ == "__main__":
    main()
