from spatialmath import SE3
import roboticstoolbox as rtb
import swift

robot = rtb.models.DH.Panda()
#print(robot)

T = robot.fkine(robot.qz)
print(T)

# IK
1.408,1.421,1.002

T = SE3(0.7, 0.2, 0.1) * SE3.OA([0, 1, 0], [0, 0, -1])

sol = robot.ikine_LMS(T)  # solve IK, ignore additional outputs
print(sol.q)  # display joint angles
# FK shows that desired end-effector pose was achieved
print(robot.fkine(sol.q))

