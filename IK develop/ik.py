import numpy as np
import roboticstoolbox as rtb
from spatialmath import SE3
import swift
#panda dobot using DH parameters


link1 = rtb.DHLink(d =1, qlim =np.array([np.pi/2,-np.pi/2]),mdh=True)

link2 = rtb.DHLink(alpha = np.pi/2,mdh=True)

link3 = rtb.DHLink(a = 1,mdh=True)
link4 = rtb.DHLink(a = 1,mdh=True,)

#list of links ,offset = -link2.theta -link3.theta,

links = [link1,link2, link3,link4]
#create robot objects using dh parameters

robot = rtb.DHRobot(links)
print(robot)
#forward kinematics 
T=robot.fkine(np.array([0, 0,0,0]))
print(T)

#final pose
Tf = SE3.Trans(2,0,1) *SE3.OA([0,  1, 0], [0, 0, 1])

#solution test (still failure)
sol = robot.ikine_LMS(Tf,q0=np.array([0,0,0,0]),mask= np.array([1,1,1,1,0,0]))
print(sol)

print(robot.fkine(sol.q))
qtraj = rtb.jtraj(np.array([0,0,np.pi/2,0]), sol.q, 50)
robot.plot(qtraj.q, movie="panda1.gif")
