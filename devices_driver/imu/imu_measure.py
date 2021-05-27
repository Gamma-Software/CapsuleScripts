import vnpy
import time

vs = vnpy.VnSensor()
if True:
#if vs.verify_sensor_connectivity():
    vs.response_timeout_ms = 1000

    vs.connect("/dev/ttyUSB0", 921600)

    while vs.is_connected:
        print(vs.read_magnetic_measurements())
        ypr = vs.read_yaw_pitch_roll()
        print(ypr)
        time.sleep(1/20)
else:
    print("not connected")
vs.disconnect()