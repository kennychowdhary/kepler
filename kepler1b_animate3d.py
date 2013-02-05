from numpy import *
from matplotlib.pyplot import *
from mpl_toolkits.mplot3d import Axes3D
from scipy.integrate import ode
import pdb
import os
import sys

'''1 body problem in 3d setting '''

def f(t,Y):
	x = Y[0]
	y = Y[1]
	z = Y[2]
	vx = Y[3]
	vy = Y[4]
	vz = Y[5]
	n = (x**2+y**2+z**2)**1.5
	return array([vx,vy,vz,-.15*x/n,-.15*y/n,-.15*z/n])

t0 = 0
tfinal = .95
y0 = array([.25,0.0,0.0,0.0,.45,0.25])
dt = .01
N = round(tfinal/dt)

run1 = ode(f).set_integrator('dopri5',atol=1e-6)
run1.set_initial_value(y0,t0)
X = zeros(N)
Y = zeros(N)
Z = zeros(N)
count = 0
while run1.successful() and run1.t < tfinal:
	# integrate
	run1.integrate(run1.t+dt)
	X[count] = run1.y[0]
	Y[count] = run1.y[1]
	Z[count] = run1.y[2]
	count += 1

# define center of orbit
x0 = zeros(1)
y0 = zeros(1)
z0 = zeros(1)

fig = figure() # initialize figure
ax = fig.gca(projection='3d') # subplot for position of walkers
frame_count = 0
decay = lambda r,c0,i: exp(-r*abs(c0-i))
r = .1250
for i in arange(N):
	ax.cla() 
	# plot all with decay transparency
	for j in arange(i):
		ax.plot(array([X[j]]),array([Y[j]]),array([Z[j]]),'b.',markersize=8,alpha=decay(r,i,j)) # plot on axis
	# plot current position
	ax.plot(array([X[i]]),array([Y[i]]),array([Z[i]]),'b.',markersize=12)
	ax.plot(x0,y0,z0,'oy',markersize=24)
	ax.set_xlim([-.1,.3])
	ax.set_ylim([-.15,.15])
	ax.set_zlim([-.15,.15])
	ax.set_title('One-body orbit')
	# record frames
	fname = '_tmp%03d.png' %frame_count # file name
	frame_count += 1 # iterate frame count
	if frame_count%10 == 0: print '%i out of %i' %(frame_count,tfinal/dt)
	fig.savefig(fname)

# converting png to animated gif
print '\nConverting png files to animated gif (this maye take some time)...\n'
os.system("convert -delay 3 -loop 0 *.png " + "orbit3d.gif")
os.system("rm *.png *.pyc") # clean up files
os.system("animate orbit3d.gif") # play animates gif

pdb.set_trace()
