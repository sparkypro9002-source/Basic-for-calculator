import pygame

pygame.init()
screen = pygame.display.set_mode((225, 400))


def sq(x, y):
    pygame.draw.rect(screen, "red", (x, y, 50, 50))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()


    sq(5,125);  sq(5,180);  sq(5,235);  sq(5,290);  sq(5,345)
    sq(60,125); sq(60,180); sq(60,235); sq(60,290); sq(60,345)
    sq(115,125);sq(115,180);sq(115,235);sq(115,290);sq(115,345)
    sq(170,125);sq(170,180);sq(170,235);sq(170,290);sq(170,345)
    
    pygame.draw.rect(screen, "white", (5, 5, 215, 115))
    pygame.display.flip()


