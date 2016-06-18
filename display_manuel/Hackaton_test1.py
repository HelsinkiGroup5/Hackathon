# PyIgnition test

import PyIgnition, pygame, sys, random


screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("PyIgnition demo: fire")
clock = pygame.time.Clock()

fire = PyIgnition.ParticleEffect(screen, (0, 0), (800, 600))
fire2 = PyIgnition.ParticleEffect(screen, (0, 0), (800, 600))
gravity2 = fire2.CreateDirectedGravity(strength = 0.1, direction = [0, -1])
gravity = fire.CreateDirectedGravity(strength = -0.01, direction = [0, -1])
wind = fire.CreateDirectedGravity(strength = 0.01, direction = [1, 0])
wind2 = fire2.CreateDirectedGravity(strength = 0.01, direction = [-1, 0])
source = fire.CreateSource((300, 500), initspeed = .5, initdirection = 0.0, initspeedrandrange = 1.0, initdirectionrandrange = 0.5, particlesperframe = 10, particlelife = 100, drawtype = PyIgnition.DRAWTYPE_CIRCLE, colour = (255, 200, 100,150), radius = 3.0)
source.CreateParticleKeyframe(10, colour = (random.randrange(0,255), random.randrange(0,255), random.randrange(0,255), 150), radius = 4.0)
source.CreateParticleKeyframe(30, colour = (150, 0, 0,30), radius = 6.0)
source.CreateParticleKeyframe(60, colour = (50, 20, 20,10), radius = 20.0)
source.CreateParticleKeyframe(80, colour = (0, 0, 0, 0), radius = 50.0)
source2 = fire2.CreateSource((300, 500), initspeed = .05, initdirection = 0.0, initspeedrandrange = 1.0, initdirectionrandrange = 0.5, particlesperframe = 10, particlelife = 100, drawtype = PyIgnition.DRAWTYPE_CIRCLE, colour = (255, 200, 100,150), radius = 3.0)
source2.CreateParticleKeyframe(10, colour = (random.randrange(0,255), random.randrange(0,255), random.randrange(0,255), 150), radius = 4.0)

#rect = fire.CreateRectangle((400, 100), (200, 100, 100), bounce = 0.2, width = 100, height = 20)
#rect.CreateKeyframe(frame = 500, pos = (400, 250), width = 200, height = 30)
#fire.CreateCircle((350, 200), (200, 100, 100), bounce = 0.2, radius = 25)
#fire.CreateCircle((450, 200), (200, 100, 100), bounce = 0.2, radius = 25)

# Test shizz for generic keyframe creation function
#source.CreateParticleKeyframe(2, colour = (0, 0, 255))
#source.CreateParticleKeyframe(5, colour = (0, 0, 0))
#source.CreateParticleKeyframe(0, colour = (255, 255, 255))
#source.CreateParticleKeyframe(0, colour = (0, 255, 0))
#source.CreateParticleKeyframe(80, colour = (255, 255, 255), radius = 1.0)

fire.SaveToFile("Fire.ppe")
fire2.SaveToFile("Fire.ppe")


while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
	screen.fill((0, 0, 0))
	x,y = pygame.mouse.get_pos()
	r_col = x/3.5
	g_col = 255-y/2.5
	b_col = x/4.5*y/2.5/255*1
	screen.fill((r_col, g_col, b_col))
	#print r_col, g_col, b_col
	mov_x,mov_y = pygame.mouse.get_rel()
	mov =  abs(mov_x)*abs(mov_y)/2+50
	print abs(mov_x), abs(mov_y), mov
	if mov > 400:
		mov = 400
	source.CreateParticleKeyframe(80, colour = (r_col, g_col, b_col, 0), radius = mov)

	source.SetPos(pygame.mouse.get_pos())
	source2.SetPos(pygame.mouse.get_pos())

	if source.curframe % 30 == 0:
		source.ConsolidateKeyframes()
	fire.Update()
	fire.Redraw()
	fire2.Update()
	fire2.Redraw()
	pygame.display.update()
	clock.tick(30)
