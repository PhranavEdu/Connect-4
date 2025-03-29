import pygame
import sys
pygame.init()
width=600
height=400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Connect Four Homepage")

blue = (0, 255, 255)
black = (0, 0, 0)
gray = (200, 200, 200)
red = (255, 0, 0)

font_large = pygame.font.SysFont("Arial", 48)
font_small = pygame.font.SysFont("Arial", 32)
text = font_large.render("CONNECT FOUR", True, gray)
rect = text.get_rect(center=(width // 2, 50))
class Button:
    def __init__(self, text, x, y, width, height, color, hover_color):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.font = font_small

    def draw(self, screen):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_x, mouse_y):
            pygame.draw.rect(screen, self.hover_color, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)

        text_surface = self.font.render(self.text, True, gray)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_hovered(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        return self.rect.collidepoint(mouse_x, mouse_y)
play_button = Button("Play", 200, 150, 200, 50, black, red)
exit_button = Button("Exit", 200, 250, 200, 50, black, red)
running = True
while running:
    screen.fill(black)
    screen.blit(text, rect)
    play_button.draw(screen)
    exit_button.draw(screen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if play_button.is_hovered():
                print("Play button")
            if exit_button.is_hovered():
                running = False

    pygame.display.flip()

pygame.quit()
sys.exit()