import math
import pygame
from physics import make_rope, euler_step, verlet_step, rope_step_sub, stretch, find_best

width = 800
height = 600
anchor_x = 400
anchor_y = 80
scale = 200
length = 2.0
dt = 1 / 60
grab_radius = 30
max_stretch = 30
target = 5

def to_screen(pt):
    return int(anchor_x + pt[0] * scale), int(anchor_y + pt[1] * scale)

def to_world(sx, sy):
    return (sx - anchor_x) / scale, (sy - anchor_y) / scale

def grab_point(mx, my):
    x, y = to_world(mx, my)
    d = math.sqrt(x*x + y*y)
    if d > length:
        x = x * length / d
        y = y * length / d
    return [x, y]

def is_near_end(p, mx, my):
    ex, ey = to_screen(p[-1])
    return (ex - mx) ** 2 + (ey - my) ** 2 < grab_radius ** 2

def method_name(step_func):
    if step_func == euler_step:
        return "Euler"
    return "Verlet"

def draw(screen, p):
    points = [to_screen(q) for q in p]
    pygame.draw.lines(screen, (120, 170, 255), False, points, 3)
    pygame.draw.circle(screen, (110, 220, 130), points[-1], 8)

def draw_info(screen, font, p, seg, n, iters, sub, step_func, message):
    s = stretch(p, seg)
    w = int(200 * min(s, max_stretch) / max_stretch)
    text = method_name(step_func) + "   points " + str(n) + "   iters " + str(iters) + "   sub " + str(sub)
    screen.blit(font.render(text, True, (220, 225, 235)), (16, 14))
    pygame.draw.rect(screen, (50, 58, 74), (16, 44, 200, 14))
    pygame.draw.rect(screen, (230, 120, 100), (16, 44, w, 14))
    screen.blit(font.render(format(s, ".1f") + "%", True, (220, 225, 235)), (226, 42))
    screen.blit(font.render(message, True, (160, 200, 170)), (16, 70))

def run(step_func, n, iters, sub):
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    font = pygame.font.SysFont(None, 26)
    clock = pygame.time.Clock()
    seg = length / (n - 1)
    p, v = make_rope(n, seg)
    grabbing = False
    message = "T: find best iters/sub"
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if is_near_end(p, event.pos[0], event.pos[1]):
                    grabbing = True
            elif event.type == pygame.MOUSEBUTTONUP:
                grabbing = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    iters = min(iters + 1, 50)
                elif event.key == pygame.K_DOWN:
                    iters = max(iters - 1, 1)
                elif event.key == pygame.K_RIGHT:
                    sub = min(sub + 1, 20)
                elif event.key == pygame.K_LEFT:
                    sub = max(sub - 1, 1)
                elif event.key == pygame.K_e:
                    step_func = euler_step
                elif event.key == pygame.K_v:
                    step_func = verlet_step
                elif event.key == pygame.K_EQUALS:
                    n = min(n + 1, 50)
                    seg = length / (n - 1)
                    p, v = make_rope(n, seg)
                elif event.key == pygame.K_MINUS:
                    n = max(n - 1, 2)
                    seg = length / (n - 1)
                    p, v = make_rope(n, seg)
                elif event.key == pygame.K_r:
                    p, v = make_rope(n, seg)
                elif event.key == pygame.K_t:
                    screen.fill((24, 28, 38))
                    draw(screen, p)
                    draw_info(screen, font, p, seg, n, iters, sub, step_func, "searching...")
                    pygame.display.flip()
                    best = find_best(n, length, dt, target)
                    if best is None:
                        message = "no combo reaches " + str(target) + "%"
                    else:
                        iters = best[0]
                        sub = best[1]
                        message = "best: iters " + str(iters) + " sub " + str(sub) + "  (" + format(best[2], ".1f") + "%, " + format(best[3], ".2f") + " ms)"
        grab = None
        if grabbing:
            mx, my = pygame.mouse.get_pos()
            grab = grab_point(mx, my)
        rope_step_sub(p, v, dt, seg, iters, step_func, grab, sub)
        screen.fill((24, 28, 38))
        draw(screen, p)
        draw_info(screen, font, p, seg, n, iters, sub, step_func, message)
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()

run(verlet_step, 30, 3, 1)