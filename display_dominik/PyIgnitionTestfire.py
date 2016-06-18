# PyIgnition test

import PyIgnition, pygame, sys, random

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
		source = effect.CreateSource((300, 500), initspeed = 1.0, initdirection = 0.0, initspeedrandrange = 0.0, initdirectionrandrange = 0.0, particlesperframe = 1, particlelife = 100, drawtype = PyIgnition.DRAWTYPE_CIRCLE, colour = (255, 200, 100), radius = 3.0)
		color1 = GetColorFromPalette(-1, colorPalette)
		source.CreateParticleKeyframe(10, colour = color1, radius = 16.0)
		color2 = GetColorFromPalette(-1, colorPalette)
		source.CreateParticleKeyframe(30, colour = color2, radius = 24.0)
		color3 = GetColorFromPalette(-1, colorPalette)
		source.CreateParticleKeyframe(60, colour = color3, radius = 80.0)
		source.CreateParticleKeyframe(80, colour = backColour, radius = 200.0)
		sources.append(source)

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
	
	sources[0].SetPos(pygame.mouse.get_pos())
	sources[1].SetPos(pygame.mouse.get_pos())
		
	for i in range(0, effectCount):
		effects[i].Update()
		effects[i].Redraw()
	
	screen.blit(surf1, (0,0,screenSize[0],screenSize[1]))
	screen.blit(surf2, (0,0,screenSize[0],screenSize[1]))
	pygame.display.flip()
	pygame.display.update()
	
	clock.tick(framerate)