import pygame, sys
from pygame.locals import *
from Quadtree import Quadtree, Rectangle
from ball import Ball

from math import pi, sqrt, asin, sin, cos
from random import randrange, uniform
import time
import ctypes
fullscreen = True

SIZE = (300, 1200)




player_scale = 0.01

target = None

def input(events):
	for event in events:
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		elif event.type == MOUSEBUTTONUP and event.button == 5:
			balls[0].radius = max(1, balls[0].radius - 3)
			
		elif event.type == MOUSEBUTTONUP and event.button == 4:
			balls[0].radius += 3
		elif event.type == MOUSEBUTTONUP and event.button == 1:
			cpos = event.pos
			return_objects = []
			
			this = Rectangle(cpos[0] - 1, cpos[1] - 1, 2, 2, balls[0])
			root_tree.retrieve(return_objects, this)
			print(len(return_objects))
			global target
			
			if target is not None:
				target.width = 0
			
			target = None
			for that in return_objects:
				if target is None and that.ball.r_id != 0:
					if that.x <= cpos[0] <= that.x + that.w and that.y <= cpos[1] <= that.y + that.h:
						target = that.ball
						target.width = 2
						print(f'Target {target.r_id}')
					else:
						print(f'No target {that.ball.pos} vs {cpos}')
	
	if target:
		ab = [target.pos[0] - balls[0].pos[0], target.pos[1] - balls[0].pos[1]]
	
		
		
		ab_w = sqrt(ab[0]**2 + ab[1]**2)
		
		ab = [ab[0] / ab_w * player_scale, ab[1] / ab_w*player_scale]
		# ab = [ab[0] / ab_w * player_scale * (2 * ab_w / SIZE[0]), ab[1] / ab_w*player_scale * (2 * ab_w / SIZE[0])]
		
		for k in range(0, 2):
			balls[0].vel[k] += ab[k]
	
	
	if pygame.mouse.get_pressed()[0]:
		cpos = pygame.mouse.get_pos()
		
		
		if not target:
			ab = [cpos[0] - balls[0].pos[0], cpos[1] - balls[0].pos[1]]
			
			
			ab_w = sqrt(ab[0]**2 + ab[1]**2)
			
			ab = [ab[0] / ab_w * player_scale, ab[1] / ab_w*player_scale]
			# ab = [ab[0] / ab_w * player_scale * (2 * ab_w / SIZE[0]), ab[1] / ab_w*player_scale * (2 * ab_w / SIZE[0])]
			
			for k in range(0, 2):
				balls[0].vel[k] += ab[k]


	keys_pressed = pygame.key.get_pressed()

	if keys_pressed[K_LEFT] or keys_pressed[K_a]:
		#player_move(x = -5)
		balls[0].vel[0] += -player_scale
		pass

	if keys_pressed[K_RIGHT] or keys_pressed[K_d]:
		#player_move(x = +5)
		balls[0].vel[0] += +player_scale
		pass

	if keys_pressed[K_UP] or keys_pressed[K_w]:
		#player_move(y = -5)
		balls[0].vel[1] += -player_scale
		pass

	if keys_pressed[K_DOWN] or keys_pressed[K_s]:
		#player_move(y = +5)
		balls[0].vel[1] += +player_scale
		pass
		
	if keys_pressed[K_SPACE]:
		#player_move(y = +5)
		balls[0].vel[0] = 0
		balls[0].vel[1] = 0
		pass
		
	if keys_pressed[K_ESCAPE]:
		pygame.quit()
		sys.exit()

def collide(ball_a, ball_b, distance):
	
	if distance == 0:
		print (f'{ball_a} and {ball_b} dist 0')
		ball_a.color = (ball_a.color[0], 255, ball_a.color[2])
		ball_b.color = (ball_b.color[0], 255, ball_b.color[2])
		return
	theta = asin((ball_b.pos[1] - ball_a.pos[1]) / distance)
	M = 1 / (ball_a.mass + ball_b.mass)
	e = .2
	vp = [[ball_a.vel[0] * cos(theta) + ball_a.vel[1] * sin(theta), ball_b.vel[0] * cos(theta) + ball_b.vel[1] * sin(theta)], [0, 0]]
	vn = [ball_a.vel[0] * -sin(theta) + ball_a.vel[1] * cos(theta), ball_b.vel[0] * -sin(theta) + ball_b.vel[1] * cos(theta)]
	
	vp[1][0] = M * (vp[0][0] * (ball_a.mass - e * ball_b.mass) + vp[0][1] * (1 + e) * ball_b.mass)
	vp[1][1] = M * (vp[0][0] * (1 + e) * ball_a.mass + vp[0][1] * (ball_b.mass - e * ball_a.mass))
	
	ball_a.vel = [vp[1][0] * cos(theta) - vn[0] * sin(theta),
				  vp[1][0] * sin(theta) + vn[0] * cos(theta)]

	ball_b.vel = [vp[1][1] * cos(theta) - vn[1] * sin(theta),
				  vp[1][1] * sin(theta) + vn[1] * cos(theta)]

	
	overlap = ball_a.radius + ball_b.radius - distance
	ab = [ball_a.pos[0] - ball_b.pos[0], ball_a.pos[1] - ball_b.pos[1]]
	ba = [ball_b.pos[0] - ball_a.pos[0], ball_b.pos[1] - ball_a.pos[1]]
	
	ab_w = sqrt(ab[0]**2 + ab[1]**2)
	ba_w = sqrt(ba[0]**2 + ba[1]**2)
	o2 = (overlap / 2) * (ball_a.mass / (ball_a.mass + ball_b.mass))
	o3 = (overlap / 2) * (ball_b.mass / (ball_a.mass + ball_b.mass))
	ab = [ab[0] / ab_w * o2, ab[1] / ab_w* o2]
	ba = [ba[0] / ba_w * o3, ba[1] / ba_w * o3]
	# print(f'ab:{ab}, overlap:{overlap}')
	for k in range(0, 2):
		ball_a.pos[k] += ab[k]
		ball_b.pos[k] += ba[k]
	"""
	ti = time.time()
	tc = 0
	
	while False and sqrt((ball_a.pos[0] - ball_b.pos[0]) ** 2 + (ball_a.pos[1] - ball_b.pos[1]) ** 2) <= ball_a.radius + ball_b.radius:
		if (ball_a.vel[0] == 0 and ball_a.vel[1] == 0) and (ball_b.vel[0] == 0 and ball_b.vel[1] == 0):
			continue
		for k in range(0, 2):
			ball_a.pos[k] += ball_a.vel[k] * edt
			ball_b.pos[k] += ball_b.vel[k] * edt
		tc += 1
	
	tf = time.time()
	if (tf - ti) *1000 > 5:
		print(f"!!! {(tf-ti)*1000:.1f}ms : {tc}")
	"""
def hash2(k1, k2):
	if k1 < k2:
		return (k2+k1) * (k2 +k1 +1) / 2 + k1
	return (k1+k2) * (k1 +k2 +1) / 2 + k2

def draw_quad(surface, quad):
	pygame.draw.rect(surface, (0,0,0), pygame.Rect(quad.bounds.x, quad.bounds.y, quad.bounds.w ,quad.bounds.h), 1)
	
	for sub_quad in quad.nodes:
		if sub_quad:
			draw_quad(surface, sub_quad)

t   = 0
dt  = 0.00005
del_t = 1
edt = dt / 5
frame = 0
last = time.time()
collisions  = 0
pot_collisions  = 0
skipped_check  = 0

balls = []
root_tree = None

if __name__ == '__main__':
	pygame.init()
	
	window = pygame.display.set_mode(SIZE)
	
	if fullscreen:
		ctypes.windll.user32.SetProcessDPIAware()
		true_res = (ctypes.windll.user32.GetSystemMetrics(0),ctypes.windll.user32.GetSystemMetrics(1))
		
		SIZE = true_res
		pygame.display.set_mode(true_res, pygame.FULLSCREEN)

	pygame.display.set_caption("Ball")
	
	balls = [
		Ball(pos=[randrange(SIZE[0]),
			randrange(SIZE[1])],
			color=(0, 0, 0),
			radius=6,
			r_id=i,
			mass=1,
			vel=[uniform(-0.1,0.1), uniform(-0.1,0.1)]
			)
		for i in range(300)]

	balls[0].mass = 1000
	balls[0].radius = 5
	balls[0].color = (0,0,255)
	
	
	root_tree = Quadtree(0, Rectangle(0, 0, SIZE[0], SIZE[1], None))
	
	
	
	
	clock = pygame.time.Clock()
	while True:
		window.fill((255, 255, 255))
		collisions  = 0
		pot_collisions  = 0
		skipped_check = 0
		root_tree.clear()
		for ball in balls:
			ball.pos[0] += ball.vel[0] * dt #* (1/del_t)
			ball.pos[1] += ball.vel[1] * dt #* (1/del_t)
			root_tree.insert(Rectangle(ball.pos[0] - ball.radius, ball.pos[1] - ball.radius, ball.radius * 2, ball.radius * 2, ball))
			
		
		
		checked = {}

		return_objects = []
		for ball in balls:
			return_objects.clear()
			this = Rectangle(ball.pos[0] - ball.radius, ball.pos[1] - ball.radius, ball.radius * 2, ball.radius * 2, ball)
			root_tree.retrieve(return_objects, this)
			
			
			if not ball.radius < ball.pos[0] < SIZE[0] - ball.radius:
				ball.vel[0] *= -.9
				ball.pos[0] = max(min(ball.pos[0], SIZE[0] - ball.radius), ball.radius)
				
			if not ball.radius < ball.pos[1] < SIZE[1] - ball.radius:
				ball.vel[1] *= -.9
				ball.pos[1] = max(min(ball.pos[1], SIZE[1] - ball.radius), ball.radius)
			
			for that in return_objects:
				if this.ball.r_id != that.ball.r_id:
				
					#if not str(min(this.ball.r_id, that.ball.r_id)) + ":" + str(max(this.ball.r_id, that.ball.r_id)) in checked:
					if not hash2(this.ball.r_id, that.ball.r_id) in checked:
						checked[hash2(this.ball.r_id, that.ball.r_id)] = True
						pot_collisions += 1
						distance = sqrt((this.ball.pos[0] - that.ball.pos[0]) ** 2 + (this.ball.pos[1] - that.ball.pos[1]) ** 2)
						
						
						if distance <= this.ball.radius + that.ball.radius:
							this.ball.color = (255,this.ball.color[1],this.ball.color[2])
							that.ball.color = (255,that.ball.color[1],that.ball.color[2])
							# print(f"{this.ball.r_id} and {that.ball.r_id} -> {distance}")
							collide(this.ball, that.ball, distance)
							collisions += 1
					else:
						skipped_check += 1

		for ball in balls:
			ball.draw(window)
			ball.color = (ball.color[0] * 0.99 ,ball.color[1],ball.color[2])
			#ball.vel[1] += 9

		draw_quad(window, root_tree)
		del_t = time.time() - last
		dt = clock.tick(144)
		t += dt
		pygame.display.flip()
		input(pygame.event.get())
		
		
		if del_t*1000 > 10:
			print(f'{len(checked)}\t/{pot_collisions + skipped_check}\tC:{collisions}\tSC:{skipped_check}\t:{del_t*1000:.1f}ms')
		last = time.time()
		frame += 1