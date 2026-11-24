import math

G = 9.8
L = 1.0

def acc(x, y):
    ax = 0.0
    ay = G
    return ax, ay

def energy(x, y, vx, vy):
    return 0.5 * (vx*vx + vy*vy) - G * y

def constrain(x, y, vx, vy):
    d = math.sqrt(x*x + y*y)
    nx = x / d
    ny = y / d
    x = nx * L
    y = ny * L
    vr = vx*nx + vy*ny
    vx = vx - vr * nx
    vy = vy - vr * ny
    return x, y, vx, vy

def euler_step(x, y, vx, vy, dt):
    ax, ay = acc(x, y)
    x_new = x + vx*dt
    y_new = y + vy*dt
    vx_new = vx + ax*dt
    vy_new = vy + ay*dt
    return constrain(x_new, y_new, vx_new, vy_new)

def verlet_step(x, y, vx, vy, dt):
    ax, ay = acc(x, y)
    x_new = x + vx*dt + 0.5*ax*dt*dt
    y_new = y + vy*dt + 0.5*ay*dt*dt
    ax_new, ay_new = acc(x_new, y_new)
    vx_new = vx + 0.5*(ax + ax_new)*dt
    vy_new = vy + 0.5*(ay + ay_new)*dt
    return constrain(x_new, y_new, vx_new, vy_new)

def run(step_func, dt, steps):
    x, y, vx, vy = 1.0, 0.0, 0.0, 0.0
    print(0, x, y, vx, vy, energy(x, y, vx, vy), math.sqrt(x*x + y*y))
    for i in range(1, steps + 1):
        x, y, vx, vy = step_func(x, y, vx, vy, dt)
        print(i, round(x, 5), round(y, 5), round(vx, 5), round(vy, 5),
              round(energy(x, y, vx, vy), 5), round(math.sqrt(x*x + y*y), 5))

run(euler_step, 0.05, 3)
run(verlet_step, 0.05, 3)