 # ############################################################################
 #
 # Copyright (c) Microsoft Corporation.
 #
 # Available under the Microsoft PyKinect 1.0 Alpha license.  See LICENSE.txt
 # for more information.
 #
 # ###########################################################################/

 # ############################################################################
 #
 # Modifications made to code by the awesome group 5 of the 2016 Aalto
 # university summer school on design interaction.
 #
 # This code is for the saturday hackathon
 #
 # ###########################################################################/

import thread
import itertools
import ctypes
import random
import datetime
import time
from pprint import pprint
import OSC

import pykinect
from pykinect import nui
from pykinect.nui import JointId
from pykinect.nui import SkeletonTrackingState
from pykinect.nui.structs import TransformSmoothParameters

import pygame
from pygame.color import THECOLORS
from pygame.locals import *

KINECTEVENT = pygame.USEREVENT
DEPTH_WINSIZE = 800,600
VIDEO_WINSIZE = 640,480
pygame.init()

c = OSC.OSCClient()

SMOOTH_PARAMS_SMOOTHING = 0.7
SMOOTH_PARAMS_CORRECTION = 0.4
SMOOTH_PARAMS_PREDICTION = 0.7
SMOOTH_PARAMS_JITTER_RADIUS = 0.1
SMOOTH_PARAMS_MAX_DEVIATION_RADIUS = 0.1
SMOOTH_PARAMS = TransformSmoothParameters(SMOOTH_PARAMS_SMOOTHING,
                                          SMOOTH_PARAMS_CORRECTION,
                                          SMOOTH_PARAMS_PREDICTION,
                                          SMOOTH_PARAMS_JITTER_RADIUS,
                                          SMOOTH_PARAMS_MAX_DEVIATION_RADIUS)

SKELETON_COLORS = [THECOLORS["red"],
                   THECOLORS["blue"],
                   THECOLORS["green"],
                   THECOLORS["orange"],
                   THECOLORS["purple"],
                   THECOLORS["yellow"],
                   THECOLORS["violet"]]

skeleton_to_depth_image = nui.SkeletonEngine.skeleton_to_depth_image

movement = open('log.txt','w')

def draw_skeleton_data(pSkelton, index, position, width = 2):

    handPos = skeleton_to_depth_image(pSkelton.SkeletonPositions[position],dispInfo.current_w,dispInfo.current_w)

    if position == JointId.HandRight:
        oscmsg.append('1')
    else:
        oscmsg.append('0')

    oscmsg.append(handPos[0])
    oscmsg.append(handPos[1])


    #xDummy = random.randrange(0,DEPTH_WINSIZE[0])
    #yDummy = random.randrange(0,DEPTH_WINSIZE[1])

    #print str(xDummy) + " " + str(yDummy)#

    #oscmsg.append(random.randrange(0,DEPTH_WINSIZE[0]))
    #oscmsg.append(random.randrange(0,DEPTH_WINSIZE[1]))

    c.send(oscmsg)
    oscmsg.clearData()

    log_hand_pos(int(handPos[0]),int(handPos[1]),position)

    pygame.draw.circle(screen, SKELETON_COLORS[random.randint(0,len(SKELETON_COLORS)-1)], (int(handPos[0]),int(handPos[1])), 10, 0)


# recipe to get address of surface: http://archives.seul.org/pygame/users/Apr-2008/msg00218.html
if hasattr(ctypes.pythonapi, 'Py_InitModule4'):
   Py_ssize_t = ctypes.c_int
elif hasattr(ctypes.pythonapi, 'Py_InitModule4_64'):
   Py_ssize_t = ctypes.c_int64
else:
   raise TypeError("Cannot determine type of Py_ssize_t")

_PyObject_AsWriteBuffer = ctypes.pythonapi.PyObject_AsWriteBuffer
_PyObject_AsWriteBuffer.restype = ctypes.c_int
_PyObject_AsWriteBuffer.argtypes = [ctypes.py_object,
                                  ctypes.POINTER(ctypes.c_void_p),
                                  ctypes.POINTER(Py_ssize_t)]

def surface_to_array(surface):
   buffer_interface = surface.get_buffer()
   address = ctypes.c_void_p()
   size = Py_ssize_t()
   _PyObject_AsWriteBuffer(buffer_interface,
                          ctypes.byref(address), ctypes.byref(size))
   bytes = (ctypes.c_byte * size.value).from_address(address.value)
   bytes.object = buffer_interface
   return bytes

def draw_skeletons(skeletons):
    for index, data in enumerate(skeletons):

        # Draw left and right hand
        draw_skeleton_data(data, index, JointId.HandRight)
        draw_skeleton_data(data, index, JointId.HandLeft)

def depth_frame_ready(frame):
    if video_display:
        return

    with screen_lock:
        address = surface_to_array(screen)
        del address
        if skeletons is not None and draw_skeleton:
            draw_skeletons(skeletons)
        pygame.display.update()


def video_frame_ready(frame):
    if not video_display:
        return

    with screen_lock:
        address = surface_to_array(screen)
        del address
        if skeletons is not None and draw_skeleton:
            draw_skeletons(skeletons)
        pygame.display.update()

def log_hand_pos(hand_x, hand_y, position):
    # We have some frames where we don't get the x,y coords, we'll just ignore those
    if(hand_x != 0 and hand_y != 0):
        ts = time.clock()
        movement.write("Time: " +  str(ts) +  " Hand: " + str(position) + " X-coord: " + str(hand_x) + " Y-coord: " + str(hand_y))
        movement.write("\n")

if __name__ == '__main__':
    full_screen = True
    draw_skeleton = True
    video_display = False

    c.connect(('10.100.29.119', 57120))   # localhost, port 57120
    oscmsg = OSC.OSCMessage()
    oscmsg.setAddress("/startup")

    screen_lock = thread.allocate()

    screen = pygame.display.set_mode(DEPTH_WINSIZE,0,16)
    pygame.display.set_caption('Super Awesome Light Body Control Thing')
    skeletons = None
    screen.fill(THECOLORS["black"])

    kinect = nui.Runtime()
    kinect.skeleton_engine.enabled = True

    def post_frame(frame):
        try:
            pygame.event.post(pygame.event.Event(KINECTEVENT, skeletons = frame.SkeletonData))
        except:
            # event queue full
            pass

    kinect.skeleton_frame_ready += post_frame

    kinect.depth_frame_ready += depth_frame_ready
    kinect.video_frame_ready += video_frame_ready

    kinect.video_stream.open(nui.ImageStreamType.Video, 2, nui.ImageResolution.Resolution640x480, nui.ImageType.Color)
    kinect.depth_stream.open(nui.ImageStreamType.Depth, 2, nui.ImageResolution.Resolution320x240, nui.ImageType.Depth)

    print len(SKELETON_COLORS)

    print('Controls: ')
    print('     u - Increase elevation angle')
    print('     j - Decrease elevation angle')

    # main game loop
    done = False

    while not done:
        e = pygame.event.wait()
        dispInfo = pygame.display.Info()
        if e.type == pygame.QUIT:
            done = True
            break
        elif e.type == KINECTEVENT:
            #kinect._nui.NuiTransformSmooth(e.skeletom_frame,SMOOTH_PARAMS)
            #kinect._nui.NuiTransformSmooth(e.skeleton_frame, SMOOTH_PARAMS
            #print str(e.skeletom_frame)
            skeletons = e.skeletons
            if draw_skeleton:
                draw_skeletons(skeletons)
                pygame.display.update()
        elif e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                done = True
                break
            elif e.key == K_u:
                kinect.camera.elevation_angle = kinect.camera.elevation_angle + 2
            elif e.key == K_j:
                kinect.camera.elevation_angle = kinect.camera.elevation_angle - 2
            elif e.key == K_x:
                kinect.camera.elevation_angle = 2

    movement.close()
