from numpy import *
from matplotlib.pyplot import *
from scipy.integrate import ode
import pdb
import os
import sys

'''
This file solves the one-body problem and shows a 2d animated gif. 
'''
# single body problem with 
# Y = [x,y,vx,vy]
# f1b is the RHS for a single body
def f1b(t,Y):
	x,y,vx,vy = Y
	n = (x**2+y**2)**1.5
	return array([vx,vy,-.5*x/n,-.5*y/n])

# two body problem with 
# Y = [x1,y1,x2,y2,vx1,vy1,vx2,vy2]
# f2b is the RHS for two body problem
def f2b(t,Y):
	x1,y1,x2,y2,vx1,vy1,vx2,vy2 = Y
	M = .5
	m = .01
	X1 = array([x1,y1])
	X2 = array([x2,y2])
	d3 = linalg.norm(X2 - X1)**3
	return array([vx1,vy1,vx2,vy2,M*(x2-x1)/d3,M*(y2-y1)/d3,\
								  m*(x1-x2)/d3,m*(y1-y2)/d3])

t0 = 0
tfinal = .74
y01b = array([.25,0.0,0.0,.45])
y02b = array([.35,0,0,0,0,.5,0,-.01]) # w/ m = .01, dt = .005,tfinal = .74
#y02b = array([.35,0,0,0,0,.5,0,-.5]) # w/ m = .5, dt = .005, tfinal = .62
dt = .002

# define single body or two body problem
f = f2b
y0 = y02b
test = ode(f).set_integrator('dopri5',atol=1e-8)
test.set_initial_value(y0,t0)

fig = figure() # initialize figure
ax = fig.add_subplot(111) # subplot for position of walkers
frame_count = 0
print '\nCapturing frames...'
while test.successful() and test.t < tfinal:
	# integrate
	test.integrate(test.t+dt)
	# plot position
	#ax.cla()
	ax.plot(test.y[0],test.y[1],'b.',markersize=6)
	ax.plot(test.y[2],test.y[3],'oy',markersize=10)
	ax.set_xlim([-.15,.5])
	ax.set_ylim([-.25,.25])
	ax.set_title('One-body orbit ')
	# record frames
	fname = '_tmp%03d.png' %frame_count # file name
	frame_count += 1 # iterate frame count
	if frame_count%20 == 0: print '%i out of %i' %(frame_count,tfinal/dt)
	fig.savefig(fname)

pdb.set_trace()

# converting png to animated gif
print '\nConverting png files to animated gif (this maye take some time)...\n'
os.system("convert -delay 2 -loop 0 *.png " + "orbit2b2.gif")
os.system("rm *.png *.pyc") # clean up files
os.system("animate orbit2b2.gif") # play animates gif

#pdb.set_trace()
