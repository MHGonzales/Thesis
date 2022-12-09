import numpy as np
import roboticstoolbox as rtb
from spatialmath import SE3


l0 = 1
#joint 1
e1 = rtb.ET.tz(l0)
e2 = rtb.ET.Rz()

#joint 2
e3 = rtb.ET.Rx(-90,unit = "deg")
e4 = rtb.ET.Rz()

#joint 3
e5 = rtb.ET.tx(l0)
e6 = rtb.ET.Rz()

#joint 4
e7 = rtb.ET.tx(l0)



link1 = rtb.Link(e1*e2,name='link1')
link2 = rtb.Link(e3*e4,name = 'link2',parent ='link1')
link3 = rtb.Link(e5*e6,name = 'link3',parent ='link2')
link4 = rtb.Link(e7,name = 'link4',parent ='link3')

links = [link1,link2,link3,link4]

robot = rtb.ERobot(links)
print(f"Robot has {robot.n} joints")
#forward kinematics 
T=robot.fkine(np.array([np.pi/4, -np.pi/4,0]))
print(T)

#final pose
Tf = SE3.Trans(1,1,2.4142 ) *SE3.OA([0,0,1], [1,1,0])
print(Tf)
#solution test (still failure)
sol = robot.ikine_LMS(Tf,q0=np.array([0,0,0]),mask= np.array([1,1,1,0,0,0]))
print(sol)

print(robot.fkine(sol.q))