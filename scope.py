from device_interface import DeviceInterface
from enum import Enum


class Channel:
    def __init__(self, scope, channel):
        self.scope = scope
        self.channel = channel

    def set_vertical_range(self, lower, upper):
        self.scope.device.SetVerticalRange(self.channel, lower, upper)

    def set_y_offset(self, offset):
        self.scope.device.SetYOffset(self.channel, offset)

    def set_coupling(self, coupling):
        if type(coupling) != self.scope.Coupling:
            raise ValueError("Invalid coupling")
        self.scope.device.SetCoupling(self.channel, coupling.value)

    def set_default_probe(self, probe):
        if type(probe) != self.scope.DefaultProbes:
            raise ValueError("Invalid default probe")
        self.channel.SetProbe(probe.value)

    def get_data(self):
        return list(self.scope.device.DataSourceScope.LatestDataPackage.GetData(
            self.scope.ChannelDataSourceScope.VIEWPORT.value, self.channel
        ).array)


class Generator:
    def __init__(self, scope):
        self.scope = scope

    def stop(self):
        self.scope.device.GeneratorToDigitalEnabled = 0
        self.scope.device.GeneratorToAnalogEnabled = 0

    def start_analog(self):
        self.scope.device.GeneratorToAnalogEnabled = 1

    def start_digital(self):
        self.scope.device.GeneratorToDigitalEnabled = 1

    def set_wave(self, points, period=1e-7):
        self.scope.device.GeneratorSamplePeriod = period
        self.scope.device.GeneratorDataDouble = points
        self.scope.commit_settings()



class SmartScope:
    def __init__(self, device_interface=DeviceInterface()):
        self.device_interface = device_interface

        self.chA = None
        self.chB = None
        self.generator = None

        self.device = None

        class Coupling(Enum):
            DC = device_interface.Devices.Coupling.DC
            AC = device_interface.Devices.Coupling.AC
        self.Coupling = Coupling

        class AnalogChannel(Enum):
            ChA = device_interface.Devices.AnalogChannel.ChA
            ChB = device_interface.Devices.AnalogChannel.ChB
        self.AnalogChannel = AnalogChannel

        class AcquisitionMode(Enum):
            AUTO = device_interface.Devices.AcquisitionMode.AUTO
            NORMAL = device_interface.Devices.AcquisitionMode.NORMAL
            SINGLE = device_interface.Devices.AcquisitionMode.SINGLE
        self.AcquisitionMode = AcquisitionMode

        class DefaultProbes(Enum):
            X1 = device_interface.Devices.Probe.DefaultX1Probe
            X10 = device_interface.Devices.Probe.DefaultX10Probe
        self.DefaultProbes = DefaultProbes

        class TriggerSource(Enum):
            CHANNEL = device_interface.Devices.TriggerSource.Channel
            EXTERNAL = device_interface.Devices.TriggerSource.External
        self.TriggerSource = TriggerSource

        class TriggerEdge(Enum):
            RISING = device_interface.Devices.TriggerEdge.RISING
            FALLING = device_interface.Devices.TriggerEdge.FALLING
            ANY = device_interface.Devices.TriggerEdge.ANY
        self.TriggerEdge = TriggerEdge

        class TriggerMode(Enum):
            EDGE = device_interface.Devices.TriggerMode.Edge
            TIMEOUT = device_interface.Devices.TriggerMode.Timeout
            PULSE = device_interface.Devices.TriggerMode.Pulse
            DIGITAL = device_interface.Devices.TriggerMode.Digital
        self.TriggerMode = TriggerMode

        class ChannelDataSourceScope(Enum):
            ACQUISITION = device_interface.DataSources.ChannelDataSourceScope.Acquisition
            VIEWPORT = device_interface.DataSources.ChannelDataSourceScope.Viewport
            OVERVIEW = device_interface.DataSources.ChannelDataSourceScope.Overview
        self.ChannelDataSourceScope = ChannelDataSourceScope

    def use_main_device(self):
        self._use_device(self.device_interface.device_manager.MainDevice)

    def use_physical_device(self):
        self.device_interface.wait_for_real_device()
        self._use_device(self.device_interface.device_manager.MainDevice)

    def _use_device(self, device):
        self.device = device
        self.chA = Channel(self, self.AnalogChannel.ChA.value)
        self.chB = Channel(self, self.AnalogChannel.ChB.value)
        self.generator = Generator(self)

        self.generator.stop()
        self.stop()
        self.device.DataSourceScope.Start()

    def start(self):
        self.device.Running = True
        self.commit_settings()

    def stop(self):
        self.device.Running = False
        self.commit_settings()

    def commit_settings(self):
        self.device.CommitSettings()

    def set_acquisition_length(self, length):
        self.device.AcquisitionLength = length

    def set_trigger_hold_off(self, offset):
        self.device.TriggerHoldOff = offset

    def set_rolling(self, rolling):
        self.device.Rolling = rolling

    def set_send_overview_buffer(self, send_buffer):
        self.device.SendOverviewBuffer = send_buffer

    def set_acquisition_mode(self, mode):
        if type(mode) != self.AcquisitionMode:
            raise ValueError("Invalid acquisition mode")
        self.device.AcquisitionMode = mode.value

    def set_prefer_partial(self, prefer_partial):
        self.device.PreferPartial = prefer_partial

    def set_view_port(self, start, end):
        self.device.SetViewPort(start, end)

    def set_trigger(self, channel, edge, level):
        if type(edge) != self.TriggerEdge:
            raise ValueError("Invalid trigger edge")
        if not isinstance(channel, Channel):
            raise ValueError("Invalid trigger channel")

        tv = self.device_interface.Devices.TriggerValue()
        tv.source = self.TriggerSource.CHANNEL.value
        tv.channel = channel.channel
        tv.edge = edge.value
        tv.level = level
        self.device.TriggerValue = tv
