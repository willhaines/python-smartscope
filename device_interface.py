import clr
from time import sleep

class DeviceInterface:
    Devices = None
    DataSources = None
    enums = None
    device_manager = None

    def __init__(self, dll_path="/opt/smartscope/DeviceInterface.dll"):
        clr.AddReference(dll_path)
        from LabNation.DeviceInterface import Devices
        from LabNation.DeviceInterface import DataSources

        self.Devices = Devices
        self.DataSources = DataSources

        self.device_manager = self.Devices.DeviceManager()
        self.device_manager.Start()

    def __del__(self):
        self.device_manager.Stop()

    def wait_for_real_device(self):
        while not self.device_manager.SmartScopeConnected:
            sleep(0.1)

