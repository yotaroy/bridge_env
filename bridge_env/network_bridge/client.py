from logging import getLogger

from .socket_interface import SocketInterface
from .. import Player

logger = getLogger(__file__)


class Client(SocketInterface):
    """Client of network computer bridge programs.
    Four clients play each hand.

    Protocol version == 18 (1 August 2005)
    http://www.bluechipbridge.co.uk/protocol.htm
    """
    PROTOCOL_VERSION = 18

    def __init__(self,
                 player: Player,
                 team_name: str,
                 ip_address: str,
                 port: int):
        self.player = player
        self.team_name = team_name

        self.ip_address = ip_address
        self.port = port

        self.player_name: str
        if player is Player.N:
            self.player_name = 'North'
        elif player is Player.E:
            self.player_name = 'East'
        elif player is Player.S:
            self.player_name = 'South'
        elif player is Player.W:
            self.player_name = 'West'
        else:
            raise ValueError('player must be Player object.')

    def _connect(self):
        self._socket.connect((self.ip_address, self.port))
        message = f'Connecting "{self.team_name}" as {self.player_name} ' \
                  f'using protocol version {self.PROTOCOL_VERSION}'
        self._send_message(message)

    def run(self):
        self._connect()
