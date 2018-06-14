### SmartScopeConnect.m
import clr

clr.AddReference("/opt/smartscope/DeviceInterface.dll")
from LabNation.DeviceInterface import Devices
from LabNation.DeviceInterface import DataSources

def connection_handler(x, y):
    print("connection_handler")
    print(x)
    print(y)

device_manager = Devices.DeviceManager(connection_handler)
print(device_manager)
#Devices.DeviceConnectHandler(device_manager.fallbackDevice, True)
device_manager.Start(True)

scope = device_manager.MainDevice
print(scope)

scope.Running = False
scope.CommitSettings()

scope.DataSourceScope.Start()

# define timebase and trigger position
scope.AcquisitionLength = 0.001
scope.TriggerHoldOff = 0.0005

# set optimal configuration for analog scoping
scope.Rolling = False
scope.SendOverviewBuffer = False
scope.AcquisitionMode = Devices.AcquisitionMode.AUTO
scope.PreferPartial = False
scope.SetViewPort(0, scope.AcquisitionLength)

# define ChannelA input
scope.SetVerticalRange(Devices.AnalogChannel.ChA, -3, 3)
scope.SetYOffset(Devices.AnalogChannel.ChA, 0)
scope.SetCoupling(Devices.AnalogChannel.ChA, Devices.Coupling.DC)
Devices.AnalogChannel.ChA.SetProbe(Devices.Probe.DefaultX1Probe)

# define ChannelB input
scope.SetVerticalRange(Devices.AnalogChannel.ChB, -3, 3)
scope.SetYOffset(Devices.AnalogChannel.ChB, 0)
scope.SetCoupling(Devices.AnalogChannel.ChB, Devices.Coupling.DC)
Devices.AnalogChannel.ChB.SetProbe(Devices.Probe.DefaultX1Probe)

# define trigger
tv = Devices.TriggerValue()
tv.source = Devices.TriggerSource.Channel
tv.channel = Devices.AnalogChannel.ChA
tv.edge = Devices.TriggerEdge.RISING
tv.level = 0.5
scope.TriggerValue = tv

# go!
scope.CommitSettings()
scope.Running = True
scope.CommitSettings()

print(scope.DataSourceScope.IsRunning)

### SmartScopePlot.m
import numpy as np

def data_handler(data, args):
    print(np.asarray(data.GetData(DataSources.ChannelDataSourceScope.Viewport, Devices.AnalogChannel.ChA).array))

scope.DataSourceScope.OnNewDataAvailable += data_handler
scope.DataSourceScope.Start()

from time import sleep
sleep(10)

print("finished")
