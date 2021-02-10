class Quadtree():

	MAX_OBJECTS = 4 # amount before split
	MAX_LEVELS = 6   # Deepest level subnode
	
	def __init__(self, p_level, p_bounds):
		self.level = p_level
		self.objects = []
		self.bounds = p_bounds
		self.nodes = [None] * 4
	
	def clear(self):
		self.objects = []
		
		for i in range(4):
			if self.nodes[i]:
				self.nodes[i].clear()
			self.nodes[i] = None
	
	def split(self):
		sub_width = self.bounds.w // 2
		sub_height = self.bounds.h // 2
		x = self.bounds.x
		y = self.bounds.y
		
		self.nodes[0] = Quadtree(self.level + 1, Rectangle(x + sub_width, y, sub_width, sub_height, None))
		self.nodes[1] = Quadtree(self.level + 1, Rectangle(x, y, sub_width, sub_height, None))
		self.nodes[2] = Quadtree(self.level + 1, Rectangle(x, y + sub_height, sub_width, sub_height, None))
		self.nodes[3] = Quadtree(self.level + 1, Rectangle(x + sub_width, y + sub_height, sub_width, sub_height, None))
	
	def get_index(self, p_rect):
		index = -1
		vertical_midpoint = self.bounds.x + (self.bounds.w / 2)
		horizontal_midpoint = self.bounds.y + (self.bounds.h / 2)
		
		top_quad = p_rect.y < horizontal_midpoint and p_rect.y + p_rect.h < horizontal_midpoint
		bottom_quad = p_rect.y > horizontal_midpoint
		
		if p_rect.x < vertical_midpoint and p_rect.x + p_rect.w < vertical_midpoint:
			if top_quad:
				index = 1
			elif bottom_quad:
				index = 2
		elif p_rect.x > vertical_midpoint:
			if top_quad:
				index = 0
			elif bottom_quad:
				index = 3
		
		return index
	
	def insert(self, p_rect):
		if self.nodes[0]:
			index = self.get_index(p_rect)
			
			if index > -1:
				self.nodes[index].insert(p_rect)
				
				return
		
		self.objects.append(p_rect)
		
		if len(self.objects) > self.MAX_OBJECTS and self.level < self.MAX_LEVELS:
			if not self.nodes[0]:
				self.split()
			
			i = 0
			
			while i < len(self.objects):
				index = self.get_index(self.objects[i])
				if index > -1:
					self.nodes[index].insert(self.objects.pop(i))
				else:
					i = i + 1
	
	def retrieve(self, return_objects, p_rect):
		index = self.get_index(p_rect)
		if index > -1 and self.nodes[0]:
			self.nodes[index].retrieve(return_objects, p_rect)
		
		return_objects.extend(self.objects)
		
		return return_objects

class Rectangle():
	def __init__(self, x, y, w, h, ball):
		self.x = x
		self.y = y
		self.w = w
		self.h = h
		self.ball = ball
