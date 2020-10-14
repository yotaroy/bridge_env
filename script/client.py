import argparse
import logging

from bridge_env import Player
from bridge_env.network_bridge.bidding_system import AlwaysPass
from bridge_env.network_bridge.client import Client
from bridge_env.network_bridge.playing_system import RandomPlay

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port',
                        default=2000,
                        type=int,
                        help='Port number for TensorBoard. (default=2000)')
    parser.add_argument('-i', '--ip_address',
                        default='localhost',
                        type=str,
                        help='')

    args = parser.parse_args()
    with Client(player=Player.N,
                team_name='teamNS',
                bidding_system=AlwaysPass(),
                playing_system=RandomPlay(),
                ip_address=args.ip_address,
                port=args.port) as client:
        print(client)
        client.run()
        print('end')
