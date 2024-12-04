import time
import os
from moviepy.editor import *

def main():
    print(os.listdir())

    files = os.listdir("/")
    volume = "/" + next((s for s in files if "vidData" in s), None)

    clip = VideoFileClip(volume + "/vidtest.mp4").rotate(180)
    print("rotated clip")
    clip.write_videofile(volume + "/result.mp4",fps=60,codec='mpeg4')
    print("done writing")
    print(os.listdir(volume))

if __name__ == "__main__":
    main()
