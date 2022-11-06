import numpy as np
import roboticstoolbox as rtb
from spatialmath import SE3

#panda dobot using DH parameters

link1 = rtb.RevoluteMDH(a =1)

link2 = rtb.RevoluteMDH(alpha = -np.pi/2,a=1)

link3 = rtb.RevoluteMDH(a = 1)

#list of links
links = [link1,link2, link3]
#create robot objects using dh parameters

robot = rtb.DHRobot(links)
#forward kinematics 
T=robot.fkine(np.array([0.785398,1.5708,0]))
print(T)

#final pose
Tf = SE3.Trans(1.707,0.7071,-1) *SE3.OA([1,  0, 0], [0, 0, 1])

#solution test (still failure)
sol = robot.ikine_min(Tf,q0=np.array([0,0,0]))
print(sol)

print(robot.fkine(sol.q))