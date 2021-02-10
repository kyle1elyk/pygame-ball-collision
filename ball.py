import pygame



class Ball(object):
	def __init__(self, **args):
		for key in args:
			self.__dict__[key] = args[key]
		
	def draw(self, surface):
		if "width" in self.__dict__:
			pygame.draw.circle(surface, self.color, [round(self.pos[0]), round(self.pos[1])], self.radius, self.width)
			return
		pygame.draw.circle(surface, self.color, [round(self.pos[0]), round(self.pos[1])], self.radius)