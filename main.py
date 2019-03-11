
import argparse

from agents.random_walker import RandomWalker
from client.drone_client import DroneClient


if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument('--interval', default=1, type=int)
    args.add_argument('--move-type', default='velocity', type=str)
    config = args.parse_args()

    client = DroneClient(config.interval)
    walker = RandomWalker(client, config.move_type, (-2, 2))
    walker.run(50)
    client.destroy()
