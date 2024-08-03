from GestureScreen import GestureScreen
import pygame

gs = GestureScreen()
gs.initUI(10)
while gs.running:
    gs.display()

gs.gd.cam.release()
pygame.quit()
