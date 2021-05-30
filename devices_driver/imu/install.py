
import os
import shutil

print("Configuring imu_measure app...")
path_to_app = "/etc/capsule/imu_measure"
path_to_log = "/var/log/capsule/imu_measure"
path_to_conf = "/etc/capsule/imu_measure/config.yaml"
if not os.path.exists(path_to_app):
    print("Create folder", path_to_app)
    os.makedirs(path_to_app, 0o775)
    os.chown(path_to_app, 1000, 0) # Rudloff id and group Root
    os.chmod(path_to_app, 0o775) # Give all read access but Rudloff write access
if not os.path.exists(path_to_log):
    print("Create folder", path_to_log)
    os.makedirs(path_to_log, 0o644)
    os.chown(path_to_log, 1000, 0) # Rudloff id and group Root
    os.chmod(path_to_log, 0o775) # Give all read access but Rudloff write access
if not os.path.exists(path_to_conf):
    print("Create imu_measure configuration")
    shutil.copy2(os.path.join(os.path.dirname(__file__), "default_config.yaml"), path_to_conf)
    os.chown(path_to_conf, 1000, 0) # Rudloff id and group Root
    os.chmod(path_to_conf, 0o775) # Give all read access but Rudloff write access
else:
    print("IMU measure configuration file already installed")