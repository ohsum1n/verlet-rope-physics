import math
import time

g = 9.8

def make_rope(n, seg):
    p = []
    v = []
    for i in range(n):
        p.append([0.0, i * seg])
        v.append([0.0, 0.0])
    return p, v

def acc(x, y):
    ax = 0.0
    ay = g
    return ax, ay

def euler_step(x, y, vx, vy, dt):
    ax, ay = acc(x, y)
    x_new = x + vx*dt
    y_new = y + vy*dt
    vx_new = vx + ax*dt
    vy_new = vy + ay*dt
    return x_new, y_new, vx_new, vy_new

def verlet_step(x, y, vx, vy, dt):
    ax, ay = acc(x, y)
    x_new = x + vx*dt + 0.5*ax*dt*dt
    y_new = y + vy*dt + 0.5*ay*dt*dt
    ax_new, ay_new = acc(x_new, y_new)
    vx_new = vx + 0.5*(ax + ax_new)*dt
    vy_new = vy + 0.5*(ay + ay_new)*dt
    return x_new, y_new, vx_new, vy_new

def constrain(p, seg, iters, pin_end):
    n = len(p)
    for _ in range(iters):
        for i in range(n - 1):
            dx = p[i+1][0] - p[i][0]
            dy = p[i+1][1] - p[i][1]
            d = math.sqrt(dx*dx + dy*dy)
            if d == 0:
                continue
            diff = (d - seg) / d
            if i == 0:
                p[i+1][0] -= dx * diff
                p[i+1][1] -= dy * diff
            elif pin_end and i == n - 2:
                p[i][0] += dx * diff
                p[i][1] += dy * diff
            else:
                p[i][0] += 0.5 * dx * diff
                p[i][1] += 0.5 * dy * diff
                p[i+1][0] -= 0.5 * dx * diff
                p[i+1][1] -= 0.5 * dy * diff

def rope_step(p, v, dt, seg, iters, step_func, grab):
    n = len(p)
    p_new = [[0.0, 0.0] for _ in range(n)]
    v_new = [[0.0, 0.0] for _ in range(n)]
    for i in range(1, n):
        if grab is not None and i == n - 1:
            p_new[i] = [grab[0], grab[1]]
            v_new[i] = [(grab[0] - p[i][0]) / dt, (grab[1] - p[i][1]) / dt]
        else:
            x, y, vx, vy = step_func(p[i][0], p[i][1], v[i][0], v[i][1], dt)
            p_new[i] = [x, y]
            v_new[i] = [vx, vy]
    p_pre = [q[:] for q in p_new]
    constrain(p_new, seg, iters, grab is not None)
    for i in range(1, n):
        v[i][0] = v_new[i][0] + (p_new[i][0] - p_pre[i][0]) / dt
        v[i][1] = v_new[i][1] + (p_new[i][1] - p_pre[i][1]) / dt
        p[i] = p_new[i]

def rope_step_sub(p, v, dt, seg, iters, step_func, grab, sub):
    sx = p[-1][0]
    sy = p[-1][1]
    goal = grab
    for k in range(sub):
        if grab is not None:
            goal = [sx + (grab[0] - sx) * (k + 1) / sub, sy + (grab[1] - sy) * (k + 1) / sub]
        rope_step(p, v, dt / sub, seg, iters, step_func, goal)

def energy(p, v):
    e = 0.0
    for i in range(1, len(p)):
        e += 0.5 * (v[i][0]*v[i][0] + v[i][1]*v[i][1]) - g * p[i][1]
    return e

def stretch(p, seg):
    total = 0.0
    for i in range(len(p) - 1):
        dx = p[i+1][0] - p[i][0]
        dy = p[i+1][1] - p[i][1]
        total += math.sqrt(dx*dx + dy*dy)
    return (total / (seg * (len(p) - 1)) - 1) * 100

def find_best(n, length, dt, target):
    seg = length / (n - 1)
    best = None
    for iters in range(1, 11):
        for sub in range(1, 11):
            p, v = make_rope(n, seg)
            worst = 0.0
            total = 0.0
            gx = 0.0
            move = 0.1
            for i in range(180):
                grab = None
                if i >= 60:
                    gx += move
                    if abs(gx) > 1.2:
                        move = -move
                    grab = [gx, 1.5]
                start = time.perf_counter()
                rope_step_sub(p, v, dt, seg, iters, verlet_step, grab, sub)
                total += time.perf_counter() - start
                worst = max(worst, stretch(p, seg))
            ms = total / 180 * 1000
            if worst <= target and (best is None or ms < best[3]):
                best = (iters, sub, worst, ms)
    return best

if __name__ == "__main__":
    seg = 2.0 / 29
    for iters, sub in [(20, 1), (10, 2), (5, 4), (2, 10), (1, 20)]:
        p, v = make_rope(30, seg)
        for i in range(300):
            rope_step_sub(p, v, 1/60, seg, iters, verlet_step, None, sub)
        print(iters, sub, round(stretch(p, seg), 2))
    for n in [10, 30, 60, 100]:
        print(n, find_best(n, 2.0, 1/60, 5))