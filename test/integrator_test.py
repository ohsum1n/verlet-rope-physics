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

run(euler_step, 0.5, 3)
run(verlet_step, 0.5, 3)
run(euler_step, 0.1, 3)
run(verlet_step, 0.1, 3)
run(euler_step, 0.01, 3)
run(verlet_step, 0.01, 3)