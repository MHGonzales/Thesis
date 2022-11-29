import DobotDllType as dType

CON_STR = {
    dType.DobotConnect.DobotConnect_NoError:  "DobotConnect_NoError",
    dType.DobotConnect.DobotConnect_NotFound: "DobotConnect_NotFound",
    dType.DobotConnect.DobotConnect_Occupied: "DobotConnect_Occupied"}
    
api = dType.load()
state = dType.ConnectDobot(api, "", 115200)[0]
print("Connect status:",CON_STR[state])

addr = 4
frequency = 50

dType.SetIOMultiplexing(api, addr, 2, 1)
dType.dSleep(5000)

for ii in range(3,13,1):
    dutyCycle = float(ii)
    print(dutyCycle)
    dType.SetIOPWM(api, addr, frequency, dutyCycle,1)
    dType.dSleep(5000)
    print(dType.GetIOPWM(api, addr))
    dType.dSleep(5000)
    
dType.DisconnectDobot(api)