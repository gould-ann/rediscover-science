import pygame
import sys

class Option:
	hovered = False
	#creates initial box
	def __init__(self, text, pos):
		self.text = text
		self.pos = pos
		self.set_rect()
		self.draw()
	
	def draw(self):
		self.set_rend()
		screen.blit(self.rend, self.rect)
		
	def set_rend(self):
		self.rend = menu_font.render(self.text, True, self.get_color())
		
	def get_color(self):
		if self.hovered:
			return (255, 255, 255)
		else:
			return (100, 100, 100)
		
	def set_rect(self):
		self.set_rend()
		self.rect = self.rend.get_rect()
		self.rect.topleft = self.pos

pygame.init()
screenX = 480
screenY = 320
screen = pygame.display.set_mode((screenX, screenY))
menu_font = pygame.font.Font(None, 40)
options = [Option("Redicover Science", (screenX/5, screenY)),
		   Option("Save this person", (screenX/4, screenY/3)), 
		   Option("Save another person", (screenX/4, screenY/3+50)),
		   Option("Save Devin Uner", (screenX/4, screenY/3+100))]

while True:
	pygame.event.pump()
	event = pygame.event.get()
	for my_event in event:
		if my_event.type == pygame.QUIT:
			sys.exit()

	screen.fill((57, 82, 54)) #colored background
	for option in options:
		if option.rect.collidepoint(pygame.mouse.get_pos()):
			option.hovered = True
			for my_event in event:
				if my_event.type == pygame.MOUSEBUTTONUP:
					pos = pygame.mouse.get_pos()
					print option.text
		else:
			option.hovered = False
		option.draw()
	pygame.display.update()