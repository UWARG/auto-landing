from simulation.runner import SimulationRunner
import time

if __name__ == "__main__":
    simRunner = SimulationRunner()
    simRunner.Takeoff(10)
    while True:
        simRunner.Rotate(100, False)
        simRunner.Move(10)
        print("rotating")