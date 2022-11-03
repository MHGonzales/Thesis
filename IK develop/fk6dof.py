import numpy as np
import roboticstoolbox as rtb
import spatialmath as sm


#change value to actual dobot link lengths
l0 = 1
#joint 1
e1 = rtb.ET.tz(l0)
e2 = rtb.ET.Rz()

#joint 2
e3 = rtb.ET.Ry()

#joint 3
e4 = rtb.ET.tz(l0)
e5 = rtb.ET.Ry()

#joint 4
e6 = rtb.ET.tz(l0)
e7 = rtb.ET.Rz()

#joint 5
e8 = rtb.ET.Ry()

#joint 6
e9 = rtb.ET.tz(l0)
e10 = rtb.ET.Ry()


#forward kinematics
ets = rtb.ETS([e1, e2, e3, e4, e5, e6, e7, e8, e9, e10])
print(f"The dobot has {ets.n} joints")