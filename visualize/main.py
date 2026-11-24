import math
import pygame
from physics import make_rope, euler_step, verlet_step, rope_step, stretch

WIDTH = 800
HEIGHT = 600
ANCHOR_X = 400
ANCHOR_Y = 80
SCALE = 200
N = 30
SEG = 2.0 / (N - 1)
DT = 1 / 60
GRAB_RADIUS = 30
MAX_STRETCH = 30

def to_screen(pt):
    sx = ANCHOR_X + pt[0]*SCALE
    sy = ANCHOR_Y + pt[1]*SCALE
    return int(sx), int(sy)

def to_world(sx, sy):
    x = (sx - ANCHOR_X) / SCALE
    y = (sy - ANCHOR_Y) / SCALE
    return x, y

def grab_point(mx, my):
    x, y = to_world(mx, my)
    d = math.sqrt(x*x + y*y)
    reach = SEG * (N - 1)
    if d > reach:
        x = x / d * reach
        y = y / d * reach
    return [x, y]

def is_near_end(p, mx, my):
    ex, ey = to_screen(p[N-1])
    return (mx - ex)**2 + (my - ey)**2 < GRAB_RADIUS * GRAB_RADIUS

def method_name(step_func):
    if step_func == euler_step:
        return "Euler"
    return "Verlet"

def draw(screen, p):
    screen.fill((20, 24, 32))
    for i in range(N - 1):
        pygame.draw.line(screen, (120, 170, 255), to_screen(p[i]), to_screen(p[i+1]), 3)
    for i in range(N):
        pygame.draw.circle(screen, (230, 230, 240), to_screen(p[i]), 5)
    pygame.draw.circle(screen, (120, 220, 160), to_screen(p[N-1]), 11)

def draw_info(screen, font, p, iters, step_func):
    s = stretch(p, SEG)
    w = int(200 * min(s, MAX_STRETCH) / MAX_STRETCH)
    text = font.render(method_name(step_func) + "   iters " + str(iters), True, (220, 225, 235))
    screen.blit(text, (16, 14))
    pygame.draw.rect(screen, (50, 58, 74), (16, 44, 200, 14))
    pygame.draw.rect(screen, (230, 120, 100), (16, 44, w, 14))
    text = font.render(format(s, ".1f") + "%", True, (220, 225, 235))
    screen.blit(text, (226, 42))

def run(step_func, iters):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 24)
    p, v = make_rope(N, SEG)
    grabbing = False
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    step_func = euler_step
                elif event.key == pygame.K_v:
                    step_func = verlet_step
                elif event.key == pygame.K_UP:
                    iters = min(iters + 1, 50)
                elif event.key == pygame.K_DOWN:
                    iters = max(iters - 1, 1)
                elif event.key == pygame.K_r:
                    p, v = make_rope(N, SEG)
                    grabbing = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                if is_near_end(p, mx, my):
                    grabbing = True
            elif event.type == pygame.MOUSEBUTTONUP:
                grabbing = False
        grab = None
        if grabbing:
            mx, my = pygame.mouse.get_pos()
            grab = grab_point(mx, my)
        rope_step(p, v, DT, SEG, iters, step_func, grab)
        draw(screen, p)
        draw_info(screen, font, p, iters, step_func)
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()

run(verlet_step, 3)