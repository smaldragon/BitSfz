import pygame
from colors import *
pygame.init()
screen = pygame.display.set_mode((384,384),pygame.RESIZABLE)
pygame.display.set_caption("SFZ-Chip")

font = pygame.font.Font("fonts/monogram-extended.ttf",16)
screen.blit(font.render(".Amplitude",True,COLORS[3]),(0,100))