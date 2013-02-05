from numpy import *
from matplotlib.pyplot import *
from scipy.integrate import ode
import pdb

def f(t,Y):
	x = Y[0]
	y = Y[1]
	vx = Y[2]
	vy = Y[3]
	n = (x**2+y**2)**1.5
	return array([vx,vy,-2*x/n,-2*y/n])

t0 = 0
tfinal = 1
y0 = array([.5,0.0,0.0,.2])
dt = .002

test = ode(f).set_integrator('dopri5',atol=1e-6)
test.set_initial_value(y0,t0)

while test.successful() and test.t < tfinal:
	test.integrate(test.t+dt)
	plot(test.y[0],test.y[1],'k.')
plot(0,0,'or')

pdb.set_trace()
