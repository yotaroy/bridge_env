import argparse
import logging

from bridge_env.network_bridge.server import Server

if __name__ == '__main__':
    FORMAT = '%(asctime)s - %(threadName)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.DEBUG, format=FORMAT)
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
    with Server(ip_address=args.ip_address, port=args.port) as server:
        server.run()
