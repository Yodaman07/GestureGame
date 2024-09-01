from GestureScreen import GestureScreen
import pygame
# Gesture Game: Made by Ayaan Irshad

gs = GestureScreen()
gs.initUI(10)
while gs.running:
    gs.display()

gs.gd.cam.release()
pygame.quit()
