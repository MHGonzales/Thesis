import numpy as np
import roboticstoolbox as rtb
from spatialmath import SE3

#panda dobot using DH parameters
q1 =0
q2 = 0
q3 = 0
q4 = -q2 -q3

link1 = rtb.DHLink(d =1, qlim =np.array([np.pi/2,-np.pi/2]),mdh=True,theta=q1)

link2 = rtb.DHLink(alpha = np.pi/2,mdh=True,theta=q2)

link3 = rtb.DHLink(a = 1,mdh=True,theta=q3)
link4 = rtb.DHLink(a = 1,mdh=True,theta=q4)
link4.offset = -link2.theta - link3.theta
#list of links

links = [link1,link2, link3,link4]
#create robot objects using dh parameters

robot = rtb.DHRobot(links)
#forward kinematics 
T=robot.fkine(np.array([np.pi/4, -np.pi/4,0,0]))
#print(link4.theta)

#final pose
Tf = SE3.Trans(1,1,2.4142) *SE3.OA([0,  1, 0], [0, 0, 1])

#solution test (still failure)
sol = robot.ikine_LMS(Tf,q0=np.array([0,0,0,0]),mask= np.array([1,1,1,0,1,0]))
print(sol.q)

print(robot.fkine(sol.q))
