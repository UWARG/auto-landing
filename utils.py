from dronekit import connect

# fetches from who knows where the dimensions of the bounding box

def FetchBoudingBoxDimension():
    return x1, x2, y1, y2


class Controller:
    def __init__(self, ConnectionEndpoint):
        self.vehicle = connect(ConnectionEndpoint, wait_ready=True)
        self.x1, self.x2, self.y1, self.y2 = FetchBoudingBoxDimension()
    
    def Halt(self):
        # Might want the code to be more sophisticated 
        # My work is done !!
        self.vehicle.airspeed = 0

    def RotateX(degrees):
        return

    def RotateY(degrees):
        return

    def RotateZ(degrees):
        return
