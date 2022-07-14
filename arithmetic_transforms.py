# ===================================================================

# Example : point transforms on a video file or live camera stream
# specified on the command line (e.g. python arithmetic_transforms.py video_file)
# or from an attached web camera

# Author : Amir Atapour Abarghouei, amir.atapour-abarghouei@durham.ac.uk

# Copyright (c) 2022 Amir Atapour Abarghouei

# License : LGPL - http://www.gnu.org/licenses/lgpl.html

# ===================================================================

import cv2
import argparse
import math
import numpy as np

# ===================================================================

keep_processing = True

# parse command line arguments for camera ID or video file

parser = argparse.ArgumentParser(
    description='Perform arithmetic point transforms on camera/video image')

parser.add_argument(
    "--camera",
    type=int,
    help="specify camera to use",
    default=0)

parser.add_argument(
    'video_file',
    metavar='video_file',
    type=str,
    nargs='?',
    help='specify optional video file')

args = parser.parse_args()

# ===================================================================

# define video capture object

print("Starting camera stream")
cap = cv2.VideoCapture()

# define display window name

window_name = "Live Camera Input - Arithmetic Transforms"  # window name

# if command line arguments are provided try to read video_file
# otherwise default to capture from attached H/W camera

if (((args.video_file) and (cap.open(str(args.video_file))))
        or (cap.open(args.camera))):

    # create window by name (note flags for resizable or not)

    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

    # keep old frame at every time step (used for XOR)

    old_frame = None

    while (keep_processing):

        # if video file or camera successfully open then read frame from video

        if (cap.isOpened):
            ret, bgr_frame = cap.read()

            # when we reach the end of the video (file) exit cleanly

            if (ret == 0):
                keep_processing = False
                continue

        # start a timer (to see how long processing and display takes)

        start_t = cv2.getTickCount()

        # *******************************

        # parameters for rescaling the image for easier processing

        scale_percent = 50 # percent of original size
        width = int(bgr_frame.shape[1] * scale_percent/100)
        height = int(bgr_frame.shape[0] * scale_percent/100)
        dim = (width, height)

        # parameters for overlaying text labels on the displayed images

        font = cv2.FONT_HERSHEY_COMPLEX
        bottomLeftCornerOfText = (10, height-15)
        fontScale = 2
        fontColor = (123,49,126)
        lineType  = 3

        # rescale image

        bgr_frame = cv2.resize(bgr_frame, dim, interpolation=cv2.INTER_AREA)

        # convert the image to grayscale

        frame = cv2.cvtColor(bgr_frame, cv2.COLOR_BGR2GRAY)

        # convert to 3 channel to stack with other images

        frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)

        # placeholder images that need to be overwritten

        placeholder = np.full(frame.shape, 0, dtype=np.uint8)
        font, line, color = cv2.FONT_HERSHEY_PLAIN, cv2.LINE_AA, (255,255,255)
        cv2.putText(placeholder, 'To be created by YOU!', (30, height//2), cv2.FONT_HERSHEY_PLAIN, 3, (255,255,255), 1, cv2.LINE_AA)
        half = placeholder.copy()
        diff_frame = placeholder.copy()



        # THIS IS THE PORTION OF THE CODE YOU NEED TO EDIT:

        # =======================================================
        # *******************************************************
        # =======================================================

        # divide the image (frame) by half
        # half = ....

        # keep the old frame to enable the difference operation
        # a variable called 'old_frame' was defined earlier in line 67
        # the initial value of this variable in None
        # you can now check to see if the value in None, then we don't have an old frame yet
        
        # calculate the absolute difference between the old frame and the current frame
        # https://docs.opencv.org/3.4/d2/de8/group__core__array.html#ga6fef31bc8c4071cbc114a758a2b79c14

        # if old_frame is not None:
        #     diff_frame = ....
        # else:
        #     diff_frame = ....
        # old_frame = ....

        # =======================================================
        # *******************************************************
        # =======================================================



        # overlay corresponding labels on the images

        cv2.putText(bgr_frame,'Colour Input', 
            bottomLeftCornerOfText, 
            font, 
            fontScale,
            fontColor,
            lineType)
        cv2.putText(frame,'Grayscale Input', 
            bottomLeftCornerOfText, 
            font, 
            fontScale,
            fontColor,
            lineType)
        cv2.putText(half,'Grayscale / 2', 
            bottomLeftCornerOfText, 
            font, 
            fontScale,
            fontColor,
            lineType)
        cv2.putText(diff_frame,'| current - previous |', 
            bottomLeftCornerOfText, 
            font, 
            fontScale,
            fontColor,
            lineType)

        # stack the images into a grid

        im_1 = cv2.hconcat([bgr_frame, frame])
        im_2 = cv2.hconcat([half, diff_frame])
        output = cv2.vconcat([im_1, im_2])

        # *******************************

        # display image

        cv2.imshow(window_name, output)
        
        # stop the timer and convert to ms. (to see how long processing and
        # display takes)

        stop_t = ((cv2.getTickCount() - start_t) /
                  cv2.getTickFrequency()) * 1000

        # start the event loop - essential

        # cv2.waitKey() is a keyboard binding function (argument is the time in
        # ms). It waits for specified milliseconds for any keyboard event.
        # If you press any key in that time, the program continues.
        # If 0 is passed, it waits indefinitely for a key stroke.
        # (bitwise and with 0xFF to extract least significant byte of
        # multi-byte response)

        # wait 40ms or less depending on processing time taken (i.e. 1000ms /
        # 25 fps = 40 ms)

        key = cv2.waitKey(max(2, 40 - int(math.ceil(stop_t)))) & 0xFF

        # It can also be set to detect specific key strokes by recording which
        # key is pressed

        # e.g. if user presses "x" then exit

        if (key == ord('x')):
            keep_processing = False

    # close all windows

    cv2.destroyAllWindows()

else:
    print("No video file specified or camera connected.")

# ===================================================================
