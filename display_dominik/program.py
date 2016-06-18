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

import pykinect
from pykinect import nui
from pykinect.nui import JointId
from pykinect.nui import SkeletonTrackingState
from pykinect.nui.structs import TransformSmoothParameters

import pygame
from pygame.color import THECOLORS
from pygame.locals import *

import PyIgnition, sys, random

hippieColorPalette = [(253,0,255),(253,255,0),(0,255,56),(0,249,255),(60,0,255)];
neonColorPalette = [(255,240,1),(253,25,153),(153,252,32),(0,230,254),(161,14,236)];

def GetRandomColor():
	return (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255));
	
def GetColorFromPalette(index, palette):
	if index == -1:
		return palette[random.randrange(0,len(palette))];
	else:
		if index >= 0 and index < len(palette):
			return palette[index]
	
colorPalette, framerate, sourceCount, effectCount, backColour, screenSize, screen, clock, surf1, surf2, effects, sources;
		
def InitializeOutput():
	colorPalette = neonColorPalette;
	framerate = 30;
	sourceCount = 1;
	effectCount = 2;
	backColour = (0, 0, 0)
	screenSize = (800, 600)

	screen = pygame.display.set_mode(screenSize)
	pygame.display.set_caption("Body Lights!")
	clock = pygame.time.Clock()

	surf1 = pygame.Surface(screenSize)
	surf1.fill(backColour)
	surf1.set_colorkey(backColour)

	surf2 = pygame.Surface(screenSize)
	surf2.fill(backColour)
	surf2.set_colorkey(backColour)

	surf1.set_alpha(150)
	surf2.set_alpha(150)

	effects = []
	sources = []

	for i in range (0, effectCount):
		curSurf = surf1;
		if(i % 2 == 0):
			curSurf = surf2;
		
		effect = PyIgnition.ParticleEffect(curSurf, (0, 0), screenSize)
		gravity = effect.CreateDirectedGravity(strength = 0.0, direction = [0.01, 0])
		wind = effect.CreateDirectedGravity(strength = 0.0, direction = [0.01, 0])
		effects.append(effect);
	
		for i in range (0, sourceCount):
			source = effect.CreateSource((300, 500), initspeed = 2.0, initdirection = 0.0, initspeedrandrange = 0.0, initdirectionrandrange = 0.0, particlesperframe = 5, particlelife = 50, drawtype = PyIgnition.DRAWTYPE_CIRCLE, colour = (255, 200, 100), radius = 3.0)
			color1 = GetColorFromPalette(-1, colorPalette)
			source.CreateParticleKeyframe(10, colour = color1, radius = 16.0)
			color2 = GetColorFromPalette(-1, colorPalette)
			source.CreateParticleKeyframe(30, colour = color2, radius = 24.0)
			color3 = GetColorFromPalette(-1, colorPalette)
			source.CreateParticleKeyframe(60, colour = color3, radius = 80.0)
			source.CreateParticleKeyframe(80, colour = backColour, radius = 200.0)
			sources.append(source)

def UpdateOutput(pos1, pos2):
	screen.fill(backColour)

	index = 0;
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
				
	#for i in range(0, sourceCount):
	#	sources[i].SetPos(pygame.mouse.get_pos())	
	#	if sources[0].curframe % framerate == 0:
	#		sources[i].ConsolidateKeyframes()	
	#		if(i == index):
	#			index = index + 1;
	#			if(index == sourceCount):
	#				index = 0;
	#				break
	
	sources[0].SetPos(pos1)
	sources[1].SetPos(pos2)
		
	#for i in range(0, effectCount):
	effects[0].Update()
	effects[0].Redraw()
	effects[1].Update()
	effects[1].Redraw()
	
	screen.blit(surf1, (0,0,screenSize[0],screenSize[1]))
	screen.blit(surf2, (0,0,screenSize[0],screenSize[1]))
	pygame.display.flip()
	pygame.display.update()
	
	clock.tick(framerate)
			
KINECTEVENT = pygame.USEREVENT
DEPTH_WINSIZE = 800,600
VIDEO_WINSIZE = 640,480
pygame.init()
InitializeOutput();

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

LEFT_ARM = (JointId.ShoulderCenter,
            JointId.ShoulderLeft,
            JointId.ElbowLeft,
            JointId.WristLeft,
            JointId.HandLeft)
RIGHT_ARM = (JointId.ShoulderCenter,
             JointId.ShoulderRight,
             JointId.ElbowRight,
             JointId.WristRight,
             JointId.HandRight)
LEFT_LEG = (JointId.HipCenter,
            JointId.HipLeft,
            JointId.KneeLeft,
            JointId.AnkleLeft,
            JointId.FootLeft)
RIGHT_LEG = (JointId.HipCenter,
             JointId.HipRight,
             JointId.KneeRight,
             JointId.AnkleRight,
             JointId.FootRight)
SPINE = (JointId.HipCenter,
         JointId.Spine,
         JointId.ShoulderCenter,
         JointId.Head)

skeleton_to_depth_image = nui.SkeletonEngine.skeleton_to_depth_image

movement = open('log.txt','w')

def draw_skeleton_data(pSkelton, index, position, width = 2):

    handPos = skeleton_to_depth_image(pSkelton.SkeletonPositions[position],dispInfo.current_w,dispInfo.current_w)

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

def get_draw_data(pSkelton):
	posLeft, posRight;
	
	handLeft = skeleton_to_depth_image(pSkelton.SkeletonPositions[JointId.HandLeft],dispInfo.current_w,dispInfo.current_w)
	posLeft = (int(handLeft[0]), int(handLeft[1]));
	handRight = skeleton_to_depth_image(pSkelton.SkeletonPositions[JointId.HandRight],dispInfo.current_w,dispInfo.current_w);
	posRight = (int(handRight[0]), int(handRight[1]));
    handPos = skeleton_to_depth_image(pSkelton.SkeletonPositions[position],dispInfo.current_w,dispInfo.current_w)
  
  	return posLeft, posRight;

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
    print('     d - Switch to depth view')
    print('     v - Switch to video view')
    print('     s - Toggle displaing of the skeleton')
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
            skeletons = e.skeletons
            if draw_skeleton:
                pos1, pos2 = get_skeleton_data(skeletons[0])
                UpdateOutput(pos1, pos2);
        elif e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                done = True
                break
            elif e.key == K_d:
                with screen_lock:
                    screen = pygame.display.set_mode(DEPTH_WINSIZE,0,16)
                    video_display = False
            elif e.key == K_v:
                with screen_lock:
                    screen = pygame.display.set_mode(VIDEO_WINSIZE,0,32)
                    video_display = True
            elif e.key == K_s:
                draw_skeleton = not draw_skeleton
            elif e.key == K_u:
                kinect.camera.elevation_angle = kinect.camera.elevation_angle + 2
            elif e.key == K_j:
                kinect.camera.elevation_angle = kinect.camera.elevation_angle - 2
            elif e.key == K_x:
                kinect.camera.elevation_angle = 2

    movement.close()
