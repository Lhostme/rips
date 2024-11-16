import time
import os
from moviepy.editor import *

def main():
    print(os.listdir())
    clip = VideoFileClip("./vidData/ss13.mp4").rotate(180)
    print("rotated clip")
    clip.write_videofile('./vidData;D/result.avi',fps=25,codec='mpeg4')
    print("done writing")
    print(os.listdir("./vidData;D"))

if __name__ == "__main__":
    main()
