def acc(y):
    a = -y
    return a

def energy(y, v):
    return (y*y + v*v) / 2

def euler_step(y, v, dt):
    a = acc(y)
    y_new = y + v*dt
    v_new = v + a*dt
    return y_new, v_new

def verlet_step(y, v, dt):
    a = acc(y)
    y_new = y + v*dt + 0.5*a*dt*dt
    a_new = acc(y_new)
    v_new = v + 0.5*(a + a_new)*dt
    return y_new, v_new
    
def run(step_func, dt, steps):
    y = 1.0
    v = 0.0
    print(0, y, v, energy(y, v))
    for i in range(1, steps + 1):
        y, v = step_func(y, v, dt)
        print(i, y, v, energy(y, v))

y1 = 1.0
v1 = 0.0
y2 = 1.0
v2 = 0.0
dt = 1 / 60
print(0, energy(y1, v1), energy(y2, v2))
for i in range(1, 10801):
    y1, v1 = euler_step(y1, v1, dt)
    y2, v2 = verlet_step(y2, v2, dt)
    if i % 600 == 0:
        print(i, energy(y1, v1), energy(y2, v2))