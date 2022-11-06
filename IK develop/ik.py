import numpy as np
import roboticstoolbox as rtb
from spatialmath import SE3

#panda dobot using DH parameters

link1 = rtb.RevoluteMDH(d =1, qlim =np.array([np.pi/2,-np.pi/2]))

link2 = rtb.RevoluteMDH(alpha = np.pi/2)

link3 = rtb.RevoluteMDH(a = 1)
link4 = rtb.RevoluteMDH(a = 1)

#list of links
links = [link1,link2, link3,link4]
#create robot objects using dh parameters

robot = rtb.DHRobot(links)
#forward kinematics 
T=robot.fkine(np.array([-np.pi/4, np.pi,0,0]))
print(T)

#final pose
Tf = SE3.Trans(-1.414,1.414,1) *SE3.OA([1,  0, 0], [0, 0, 1])

#solution test (still failure)
sol = robot.ikine_LMS(Tf)#,q0=np.array([0,0,0,0]),qlim=False)
print(sol)

print(robot.fkine(sol.q))