import dronekit_sitl
from dronekit import connect, VehicleMode, LocationGlobal, Command
from pymavlink import mavutil
import argparse
import time

# high level interface for sending commands to drone.
class SimulationRunner:
    """
    High level interface for sending commands to drone.
    """
    def __init__(self):
        self._sitl = dronekit_sitl.start_default()
        self._connection_string = "udp:127.0.0.1:14550"
        # connect to vehicle
        print(f"Connecting to vehicle on {self._connection_string}")
        self._vehicle = connect(self._connection_string, wait_ready=True)
        self._cmds = self._vehicle.commands
        # download current mission
        self._cmds.download()
        self._cmds.wait_ready()
    
    def Takeoff(self, altitude: float):
        """
        Armms vehicle and flies to altitude
        """
        while not self._vehicle.is_armable:
            print("Waiting for vehicle to init...")
            time.sleep(1)

        self._vehicle.mode = VehicleMode("GUIDED")
        self._vehicle.armed = True
        while not self._vehicle.armed:
            print("Waiting for arming...")
            time.sleep(1)

        # takeoff
        self._vehicle.simple_takeoff(altitude)
        self._vehicle.groundspeed=5  # 5m/s groundspeed

        # reach safe height before moving on
        while True:
            print("Altitude: ", self._vehicle.location.global_relative_frame.alt)
            if self._vehicle.location.global_relative_frame.alt >= altitude * 0.95: # trigger just below target
                print("Reached target altitude")
                break
            time.sleep(1)
        
    def Move(self, speed: float):
        self._vehicle_mode = VehicleMode("GUIDED")
        self._vehicle.airspeed = 5


    def Rotate(self, degrees: int, relative=True):
        self._vehicle.mode = VehicleMode("GUIDED")
        is_relative = 0
        if relative:
            is_relative=1
        msg = self._vehicle.message_factory.command_long_encode(
            0,0, # target system, target component,
            mavutil.mavlink.MAV_CMD_CONDITION_YAW, #command
            0, # confirmation,
            degrees, # param 1 - yaw in degrees
            10, # param 2 - yaw speed deg/s
            1, # param 3 - 1 - cw, -1 - ccw
            is_relative, # relative vs absolute (0)
            0, 0, 0)
        self._vehicle.send_mavlink(msg)
    
    def Stabilize(self):
        self._vehicle.mode = VehicleMode("GUIDED")

    def Descend(self):
        self._vehicle.mode = VehicleMode("GUIDED")

    def Land(self, boxLatLeft: float, boxLongLeft: float, boxLatRight: float, boxLongRight: float):
        """
        Use bounding box coordinates from geolocation to land
        """
        self._vehicle.mode = VehicleMode("GUIDED")
    
    @property
    def vehicle_attributes(self) -> dict:
        return dict(
            GPS = str(self._vehicle.gps_0),
            Battery = str(self._vehicle.battery),
            LastHeartbeat = self._vehicle.last_heartbeat,
            IsArmable = self._vehicle.is_armable,
            SystemStatus = self._vehicle.system_status.state,
            Mode = self._vehicle.mode.name
        )

    def StopSim(self):
        self._vehicle.close()
        self._sitl.stop()
        print("Simulation stopped.")
