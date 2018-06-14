from scope import SmartScope
from matplotlib import pyplot as plt

scope = SmartScope()
scope.use_main_device()

scope.set_acquisition_length(0.002)
# scope.set_trigger_hold_off(0.0005)

scope.set_rolling(False)
scope.set_send_overview_buffer(False)
scope.set_acquisition_mode(scope.AcquisitionMode.NORMAL)
scope.set_prefer_partial(False)
scope.set_view_port(0, 0.001)

scope.chA.set_vertical_range(-1, 1)
scope.chA.set_y_offset(0)
scope.chA.set_coupling(scope.Coupling.DC)
scope.chA.set_default_probe(scope.DefaultProbes.X1)

# scope.chB.set_vertical_range(-1, 1)
# scope.chB.set_y_offset(0)
# scope.chB.set_coupling(scope.Coupling.DC)
# scope.chB.set_default_probe(scope.DefaultProbes.X1)

scope.set_trigger(scope.chA, scope.TriggerEdge.RISING, 0.5)

scope.commit_settings()
scope.start()

from time import sleep
sleep(1)

data = scope.chA.get_data()
# data2 = scope.chB.get_data()
plt.plot(data)
# plt.plot(data2)

plt.show()
