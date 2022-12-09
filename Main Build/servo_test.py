
import DobotDllType as dType
import math

CON_STR = {
    dType.DobotConnect.DobotConnect_NoError:  "DobotConnect_NoError",
    dType.DobotConnect.DobotConnect_NotFound: "DobotConnect_NotFound",
    dType.DobotConnect.DobotConnect_Occupied: "DobotConnect_Occupied"}
    
api = dType.load()
state = dType.ConnectDobot(api, "", 115200)[0]
print("Connect status:",CON_STR[state])

x = float(input('Input Radians Value: '))
deg = math.degrees(x)
print(deg)
pwm = (deg/18.0) + 2.5
print(pwm)

addr = 4
frequency = 50

dType.SetIOMultiplexing(api, addr, 2, 1)
dType.dSleep(1000)
dutyCycle = pwm
print(dutyCycle)    
dType.SetIOPWM(api, addr, frequency, dutyCycle,1)
dType.dSleep(5000)
print(dType.GetIOPWM(api, addr))
dType.dSleep(5000)
dType.DisconnectDobot(api)



