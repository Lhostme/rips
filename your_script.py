import os
import cv2

from flask import Flask, request, jsonify
from moviepy import VideoFileClip

app = Flask(__name__)

@app.route('/process', methods=['POST'])
def process():
    print(os.listdir())
    reqArgs = request.get_json()
    print("args: ", reqArgs)

    if (not "input" in reqArgs or not reqArgs["input"]): return jsonify({"error": "Input file required"})
    if (not "output"in reqArgs or not reqArgs["output"]): return jsonify({"error": "Output file required"})
    files = os.listdir("/")
    volume = "/" + next((s for s in files if "vidData" in s), None)
    # print("volume", volume)

    total_size = 0
    for dirpath, dirnames, filenames in os.walk(volume):
        for file in filenames:
            file_path = os.path.join(dirpath, file)
            # Skip if it's a broken symlink
            if not os.path.islink(file_path):
                total_size += os.path.getsize(file_path)

    if (total_size >= 5000000000):
        return jsonify({"error":"Max storage space reached"})

    # Set video input/output location
    inputPath = volume + "/" + reqArgs["input"]
    outputPath = volume + "/" + reqArgs["output"]

    # Open the input video
    capture = cv2.VideoCapture(inputPath)
    if not capture.isOpened():
        return jsonify({"error": "Could not open video file"})

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

        textColour = [255,255,255]
        thickness = 1
        fontScale = 1
        if (reqArgs["rgb"] and len(reqArgs["rgb"]) == 3): textColour = reqArgs["rgb"]
        if ("thickness" in reqArgs): thickness = reqArgs["thickness"]
        if ("fontScale" in reqArgs): fontScale = reqArgs["fontScale"]
        if ("topText" in reqArgs):
            putText(reqArgs["topText"], frame, frameWidth, frameHeight, "topText", textColour, fontScale, thickness)
        if ("bottomText" in reqArgs):
            putText(reqArgs["bottomText"], frame, frameWidth, frameHeight, "bottomText", textColour, fontScale, thickness)
        if ("centerText" in reqArgs):
            putText(reqArgs["centerText"], frame, frameWidth, frameHeight, "centerText", textColour, fontScale, thickness)


        # Write the frame to the output video
        output.write(frame)

    # Release resources
    capture.release()
    output.release()

    if ("gifify" in reqArgs and reqArgs["gifify"] == True):
        videoClip = VideoFileClip(outputPath)
        outputPath = outputPath[:outputPath.find('.')] + ".gif"
        videoClip.write_gif(outputPath)

    print("done writing")
    print(os.listdir(volume))

    return jsonify({"result":outputPath})

@app.route('/help', methods=['GET'])
def help():
    return jsonify({
        "Add Text": {
            "route": "/process",
            "parameters": {
                "bottomText":"Text at bottom center",
                "topText":"Text at top center",
                "centerText":"Text in center",
                "textColour": "Array of 3 numbers representing rgb",
                "thickness": "Width of the stroke used to create the text",
                "fontScale": "Number from 0 to 1 to change relative size of text"
            }
        },
        "List Files": {
            "route": "/lsVolume"
        }
    })

@app.route('/lsVolume', methods=['GET'])
def lsVolume():
    files = os.listdir("/")
    volume = "/" + next((s for s in files if "vidData" in s), None)
    return jsonify({"files": os.listdir(volume)})

def putText(text, frame, frameWidth, frameHeight, position, textColour, fontScale, thickness):
    # Add text to the frame
    if not text:
        text = ""
    font = cv2.FONT_HERSHEY_SIMPLEX
    color = (textColour[2], textColour[1], textColour[0])
    (text_width, text_height), baseline = cv2.getTextSize(text, font, fontScale, thickness)
    xVal = round(frameWidth / 2)
    if position == "topText":
        position = (xVal - round(text_width / 2), text_height + 10)  # Coordinates (x, y) for the text
    elif position == "bottomText":
        position = (xVal - round(text_width / 2), frameHeight - text_height - 10)
    else:
        yVal = round(frameHeight / 2)
        position = (xVal - round(text_width / 2), yVal) # Center text
    cv2.putText(frame, text, position, font, fontScale, color, thickness)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
