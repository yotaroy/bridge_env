import argparse
import logging

from bridge_env import Player
from bridge_env.network_bridge.bidding_system import WeakBid
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
    parser.add_argument('-l', '--location',
                        default='N',
                        type=str,
                        help='Player (N, E, S or W)')

    args = parser.parse_args()
    player = Player[args.location]
    with Client(player=player,
                team_name=str(player.pair),
                bidding_system=WeakBid(),
                playing_system=RandomPlay(),
                ip_address=args.ip_address,
                port=args.port) as client:
        print(client)
        client.run()
        print('end')
