import math

G = 9.8

def make_rope(n, seg):
    p = []
    v = []
    for i in range(n):
        p.append([i * seg, 0.0])
        v.append([0.0, 0.0])
    return p, v

def acc(x, y):
    ax = 0.0
    ay = G
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

def constrain(p, seg, iters):
    n = len(p)
    for _ in range(iters):
        for i in range(n - 1):
            dx = p[i+1][0] - p[i][0]
            dy = p[i+1][1] - p[i][1]
            d = math.sqrt(dx*dx + dy*dy)
            diff = (d - seg) / d
            if i == 0:
                p[i+1][0] -= dx * diff
                p[i+1][1] -= dy * diff
            else:
                p[i][0] += 0.5 * dx * diff
                p[i][1] += 0.5 * dy * diff
                p[i+1][0] -= 0.5 * dx * diff
                p[i+1][1] -= 0.5 * dy * diff

def rope_step(p, v, dt, seg, iters, step_func):
    n = len(p)
    p_new = [[0.0, 0.0] for _ in range(n)]
    v_new = [[0.0, 0.0] for _ in range(n)]
    for i in range(1, n):
        x, y, vx, vy = step_func(p[i][0], p[i][1], v[i][0], v[i][1], dt)
        p_new[i] = [x, y]
        v_new[i] = [vx, vy]
    p_pre = [q[:] for q in p_new]
    constrain(p_new, seg, iters)
    for i in range(1, n):
        v[i][0] = v_new[i][0] + (p_new[i][0] - p_pre[i][0]) / dt
        v[i][1] = v_new[i][1] + (p_new[i][1] - p_pre[i][1]) / dt
        p[i] = p_new[i]

def energy(p, v):
    e = 0.0
    for i in range(1, len(p)):
        e += 0.5 * (v[i][0]*v[i][0] + v[i][1]*v[i][1]) - G * p[i][1]
    return e

def stretch(p, seg):
    total = 0.0
    for i in range(len(p) - 1):
        dx = p[i+1][0] - p[i][0]
        dy = p[i+1][1] - p[i][1]
        total += math.sqrt(dx*dx + dy*dy)
    return (total / (seg * (len(p) - 1)) - 1) * 100

def run(step_func, dt, steps, n, seg, iters):
    p, v = make_rope(n, seg)
    print(0, p[1], p[n-1], energy(p, v), stretch(p, seg))
    for i in range(1, steps + 1):
        rope_step(p, v, dt, seg, iters, step_func)
        print(i, [round(a, 5) for a in p[1]], [round(a, 5) for a in p[n-1]],
              round(energy(p, v), 5), round(stretch(p, seg), 5))

run(euler_step, 0.05, 3, 4, 0.5, 10)
run(verlet_step, 0.05, 3, 4, 0.5, 10)