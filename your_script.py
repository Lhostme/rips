import time
import os
import cv2

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/sample', methods=['POST'])
def sample():
    print(os.listdir())
    reqArgs = request.get_json()
    print("args: ", reqArgs)

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
    print("width: ", frameWidth)
    print("height: ", frameHeight)
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

        for arg in reqArgs:
            if (arg == "topText" or arg == "bottomText" or arg == "centerText"):
                putText(reqArgs[arg], frame, frameWidth, frameHeight, arg)

        # Write the frame to the output video
        output.write(frame)

    # Release resources
    capture.release()
    output.release()

    print("done writing")
    print(os.listdir(volume))

    return jsonify({"result":outputPath})

def putText(text, frame, frameWidth, frameHeight, position):
    # Add text to the frame
    if not text:
        text = "OpenCV Text Example"
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    color = (0, 255, 0)  # Green
    thickness = 1
    (text_width, text_height), baseline = cv2.getTextSize(text, font, font_scale, thickness)
    xVal = round(frameWidth / 2)
    if position == "topText":
        position = (xVal - round(text_width / 2), text_height + 10)  # Coordinates (x, y) for the text
    elif position == "bottomText":
        position = (xVal - round(text_width / 2), frameHeight - text_height - 10)
    else:
        yVal = round(frameHeight / 2)
        position = (xVal - round(text_width / 2), yVal) # Center text
    cv2.putText(frame, text, position, font, font_scale, color, thickness)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
