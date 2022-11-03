import numpy as np
import roboticstoolbox as rtb
import spatialmath as sm

#change value to actual dobot link lengths
l0 = 1
l1 = 1
l2 = 1

#reference frames translation and rotation
e1 = rtb.ET.tz(l0)
e2 = rtb.ET.Rz()
e3 = rtb.ET.Ry()
e4 = rtb.ET.tz(l1)
e5 = rtb.ET.Ry()
e6 = rtb.ET.tz(l2)
#forward kinematics
ets = rtb.ETS([e1, e2, e3, e4, e5, e6])
print(f"The dobot has {ets.n} joints")
#sample initial joing angles
q = np.array([45, 45, 45])

# Allocate the resulting forward kinematics array
fk = np.eye(4) 

# Now we must loop over the ETs in the Panda
for et in ets:
    if et.isjoint:
        # This ET is a variable joint
        # Use the q array to specify the joint angle for the variable ET
        fk = fk @ et.A(q[et.jindex])
    else:
        # This ET is static
        fk = fk @ et.A()

# Pretty print our resulting forward kinematics using an SE3 object
print(sm.SE3(fk))
