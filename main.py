import pygame
import time

GREEN = (0,255,0)
RED = (255,0,0)
TILE_SIZE = 32
window = pygame.display.set_mode((1080,720))

class Player:
	def __init__(self, x, y, w, h):
		self.x_pos = x
		self.y_pos = y
		self.width = w
		self.height = h
		self.surface = pygame.Surface((self.width, self.height))
		self.surface.fill(RED)
		self.direction = 0
		self.gravity = 0.8
		self.velocity_y = 0

	def draw(self, window):
		window.blit(self.surface, (self.x_pos, self.y_pos))

	def update(self, value):
		self.direction = value
		if value > 0:
			self.x_pos += 4
		elif value < 0:
			self.x_pos -= 4

		self.velocity_y += self.gravity
		self.y_pos += self.velocity_y

	def checkSlopeCollision(self, collider):
		if self.x_pos + self.width / 2 < collider[0] or self.x_pos > collider[0]:
			return False
		elif self.y_pos + self.height  < collider[1] or self.y_pos > collider[1]:
			return False
		else:
			return True


class Slope:
	def __init__(self, x, y, w, h):
		self.x_pos = x
		self.y_pos = y
		self.width = w
		self.height = h
		self.surface = pygame.Surface((self.width, self.height))
		self.surface.fill(GREEN)
		self.colliders = []
		self.generateColliders()

	def generateColliders(self):
		for i in range(TILE_SIZE + 1):
			pixel = [self.x_pos + i, self.y_pos + TILE_SIZE - i]
			self.colliders.append(pixel)

	def drawColliders(self, window):
		for i in range(len(self.colliders)):
			window.set_at(self.colliders[i],RED)

	def draw(self, window):
		window.blit(self.surface, (self.x_pos, self.y_pos))

stairs = []
num_stairs = 20
for i in range(num_stairs):
	rect = Slope(i * TILE_SIZE ,400 - i * TILE_SIZE,TILE_SIZE,TILE_SIZE)
	stairs.append(rect)


player = Player(0,0,32,32)

is_running = True
value = 0
while is_running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			is_running = False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_RIGHT:
				value = 1
			elif event.key == pygame.K_LEFT:
				value = -1
		elif event.type == pygame.KEYUP:
			if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
				value = 0
	
	for i in range(len(stairs)):
		for j in range(len(stairs[i].colliders)):
			if player.checkSlopeCollision(stairs[i].colliders[j]):
				player.y_pos = stairs[i].colliders[j][1] - player.height
				player.velocity_y = 0
				

	player.update(value)

	window.fill(0)
	
	player.draw(window)
	for i in range(num_stairs):
		#stairs[i].draw(window)
		stairs[i].drawColliders(window)
	pygame.display.update()
	time.sleep(10/1000)
