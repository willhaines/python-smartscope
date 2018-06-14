import numpy as np
from matplotlib import pyplot as plt
from time import sleep

from scope import SmartScope

scope = SmartScope()
scope.use_physical_device()

scope.set_acquisition_length(100e-6)
# scope.set_trigger_hold_off(0.0005)

scope.set_rolling(False)
scope.set_send_overview_buffer(False)
scope.set_acquisition_mode(scope.AcquisitionMode.AUTO)
scope.set_prefer_partial(False)
scope.set_view_port(0, 100e-6)

scope.chA.set_vertical_range(-0.5, 2.5)
scope.chA.set_y_offset(0)
scope.chA.set_coupling(scope.Coupling.DC)
scope.chA.set_default_probe(scope.DefaultProbes.X1)

# scope.chB.set_vertical_range(-1, 1)
# scope.chB.set_y_offset(0)
# scope.chB.set_coupling(scope.Coupling.DC)
# scope.chB.set_default_probe(scope.DefaultProbes.X1)

scope.set_trigger(scope.chA, scope.TriggerEdge.RISING, 0.5)

# set up generator
sample_freq = 10e6
sample_period = 1/sample_freq

wave_freq = 1000e3
wave_period = 1/wave_freq
wave_amplitude = 1
wave_dc_offset = 1

t = np.arange(0, 10*wave_period, sample_period)
wave = wave_dc_offset + wave_amplitude*np.sin(2*np.pi*wave_freq*t)

scope.generator.set_wave(wave, sample_period)
scope.generator.start_analog()

scope.commit_settings()
scope.start()

sleep(5)

data = scope.chA.get_data()
# data2 = scope.chB.get_data()
plt.plot(data)
plt.plot(wave)
# plt.plot(data2)

del scope.device_interface
plt.show()
