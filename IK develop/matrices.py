from spatialmath import SE3
import roboticstoolbox as rtb
import swift
import numpy as np
robot = rtb.models.DH.Panda()
#print(robot)

T = robot.fkine(robot.qz)
print(T)

# IK
1.408,1.421,1.002

T = SE3(0.7, 0.2, 0.1) * SE3.OA([1, 1, 1], [0, 0, -1])

sol = robot.ikine_LMS(T,q0=np.array([0,0,0,0,0,0,0]))  # solve IK, ignore additional outputs
print(sol)  # display joint angles
# FK shows that desired end-effector pose was achieved
print(robot.fkine(sol.q))

