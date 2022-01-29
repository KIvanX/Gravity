import pygame
import math
from random import randint
from time import time

class Object:
    def __init__(self, name, m, x, y, vx, vy):
        self.name, self.m, self.x, self.y, self.vx, self.vy = name, m, x, y, vx, vy


pygame.init()
window = pygame.display.set_mode((1200, 550))
pygame.display.set_caption('Гравитация')
Fon = pygame.image.load('Fon.jpg')
Obj_fon = pygame.image.load('obj2.png')
Boom = pygame.image.load('Boom.png')
Moon = pygame.image.load('Moon.png')
window.blit(Fon, (0, 0))
clock = pygame.time.Clock()

sys = [Object('Moon', 5000000, 0, 30000, 0, 0), Object('A1', 100000, 0, 0, -30, 0)]
for i in range(30):
    sys.append(Object('E' + str(i), randint(1, 10), randint(-300, 1500), randint(-300, 850), randint(-50, 50),
                      randint(-50, 50)))

delay = 10
boom = []
koef = 0.03
M_clk, K_clk = False, 0
M_sdv_x = M_sdv_y = M_clk_x = M_clk_y = 0
game, t, tsr = True, 0, 0
while game:
    t += 1

    clock.tick()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                M_clk = True
                pos = pygame.mouse.get_pos()
                M_clk_x = pos[0] / koef
                M_clk_y = pos[1] / koef
            if event.button == 4:
                koef += koef*0.15
            if event.button == 5:
                koef -= koef*0.15
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                M_clk = False
                pos = pygame.mouse.get_pos()
                M_sdv_x += (M_clk_x - pos[0]/koef)
                M_sdv_y += (M_clk_y - pos[1]/koef)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                K_clk = 1
            if event.key == pygame.K_DOWN:
                K_clk = -1
        if event.type == pygame.KEYUP:
            if event.key in [pygame.K_UP, pygame.K_DOWN]:
                K_clk = 0

    t1 = time()
    M_x, M_y = M_sdv_x, M_sdv_y
    if M_clk:
        pos = pygame.mouse.get_pos()
        M_x = M_sdv_x + (M_clk_x - pos[0]/koef)
        M_y = M_sdv_y + (M_clk_y - pos[1]/koef)

    if K_clk:
        delay += delay * K_clk * 0.001

    if t % int(delay) == 0:
        window.blit(Fon, (0, 0))
    for obj1 in sys:
        for obj2 in sys:
            if obj1 == obj2:
                continue
            S = math.sqrt((obj1.x - obj2.x)*(obj1.x - obj2.x) + (obj1.y - obj2.y)*(obj1.y - obj2.y))
            if S < (math.sqrt(obj1.m) + math.sqrt(obj2.m)) * 0.8:
                obj1, obj2 = (obj2, obj1) if obj1.m < obj2.m else (obj1, obj2)
                obj1.vx += obj2.vx * obj2.m / obj1.m
                obj1.vy += obj2.vy * obj2.m / obj1.m
                obj1.m += obj2.m * 0.99
                boom.append([obj2.x, obj2.y, 1, int(math.sqrt(obj2.m))])
                sys.pop(sys.index(obj2))
            else:
                obj1.vx += 6.67 * obj2.m / (S * S * S) * (obj2.x - obj1.x)
                obj1.vy += 6.67 * obj2.m / (S * S * S) * (obj2.y - obj1.y)

        obj1.x += obj1.vx
        obj1.y += obj1.vy
        if t % int(delay) == 0:
            new_fon = pygame.transform.scale(Obj_fon, (int(math.sqrt(obj1.m)*2*koef), int(math.sqrt(obj1.m) * 2 * koef)))
            if obj1.name == 'Moon':
                obj1.x, obj1.y = 0, 30000
                new_fon = pygame.transform.scale(Moon, (int(math.sqrt(obj1.m) * 2 * koef), int(math.sqrt(obj1.m) * 2 * koef)))
            x = (obj1.x - int(math.sqrt(obj1.m)) - M_x) * koef - (koef-1)*600
            y = (obj1.y - int(math.sqrt(obj1.m)) - M_y) * koef - (koef-1)*225
            window.blit(new_fon, (x, y))
            font = pygame.font.SysFont('arial', int(math.sqrt(math.sqrt(obj1.m)*2*koef))+15)
            text = font.render(obj1.name, True, (250, 230, 200))
            window.blit(text, (x+int(math.sqrt(obj1.m) * koef), y+int(math.sqrt(obj1.m) * koef)))

    for b in boom:
        b[2] += 0.5
        r = int(b[2] * b[3] / 2) if b[2] < 20 else int(20 * b[3] / 2)
        if t % int(delay)  == 0:
            new_boom = pygame.transform.scale(Boom, (int(r*koef), int(r*koef)))
            new_boom.set_alpha(250 - int(b[2] - 20) * 20)
            window.blit(new_boom, ((b[0] - r / 2 - M_x)*koef-(koef-1)*600,
                                   (b[1] - r / 2 - M_y)*koef-(koef-1)*225))
        if b[2] >= 30.0:
            boom.pop(boom.index(b))
    tsr = ((time()-t1)*1000 + tsr) / 2
    print(int(delay) , tsr)

    if t % int(delay)  == 0:
        pygame.display.flip()

