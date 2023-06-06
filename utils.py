from dronekit import connect

# fetches from who knows where the dimensions of the bounding box


def FetchBoudingBoxDimension() -> tuple[int, int, int, int]:
    return x1, x2, y1, y2


class Controller:
    def __init__(self, ConnectionEndpoint: str):
        self.vehicle = connect(ConnectionEndpoint, wait_ready=True)
        self.x1, self.x2, self.y1, self.y2 = FetchBoudingBoxDimension()

    def Halt(self) -> None:
        # Might want the code to be more sophisticated
        # My work is done !!
        self.vehicle.airspeed = 0

    def RotateX(degrees: float) -> None:
        return

    def RotateY(degrees: float) -> None:
        return

    def RotateZ(degrees: float) -> None:
        return
