from numpy import *
from matplotlib.pyplot import *
from scipy.integrate import ode
import pdb
import os
import sys

'''
This file solves the one-body problem and shows a 2d animated gif. 
'''

# Compute RHS of ODE
def f(t,Y):
	x,y,vx,vy = Y # define individual values
	d3 = (x**2+y**2)**1.5 # ||x||^3
	M = .5
	return array([vx,vy,-M*x/d3,-M*y/d3])

# initial parameters
t0 = 0 # initial start time
tfinal = .95 # final start time
dt = .008 # time step to solution (dopri5 algorithm uses adaptive)
y0 = array([.25,0.0,0.0,.45]) # initial position and velocity

# initiate integrator object
test = ode(f).set_integrator('dopri5',atol=1e-6) # prescribe tolerance for adaptive time step
test.set_initial_value(y0,t0) # set initial time and initial value

fig = figure() # initialize figure
ax = fig.add_subplot(111) # name of the plot
frame_count = 0
print 'Capturing frames...'
while test.successful() and test.t < tfinal:
	# integrate
	test.integrate(test.t+dt)
	# plot position
	ax.cla()
	ax.plot(test.y[0],test.y[1],'b.',markersize=6)
	ax.plot(0,0,'oy',markersize=12)
	ax.set_xlim([-.1,.3])
	ax.set_ylim([-.15,.15])
	ax.set_title('One-body orbit')
	# record frames
	fname = '_tmp%03d.png' %frame_count # file name
	frame_count += 1 # iterate frame count
	if frame_count%20 == 0: print '%i out of %i' %(frame_count,tfinal/dt)
	fig.savefig(fname)

# converting png to animated gif
print '\nConverting png files to animated gif (this maye take some time)...\n'
os.system("convert -delay 5 -loop 0 *.png " + "orbit.gif")
os.system("rm *.png *.pyc") # clean up files
os.system("animate orbit.gif") # play animates gif

#pdb.set_trace()
