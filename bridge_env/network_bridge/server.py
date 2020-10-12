from logging import getLogger
from typing import Optional

from .socket_interface import SocketInterface

logger = getLogger(__file__)


class Server(SocketInterface):
    """Server of network computer bridge programs.
    A server acts as the table manager.

    Protocol version == 18 (1 August 2005)
    http://www.bluechipbridge.co.uk/protocol.htm
    """
    PROTOCOL_VERSION = 18

    def __init__(self, ip_address: str, port: int):
        """

        :param ip_address:
        :param port: The port numbers should be within the standard range of
            1024 to 5000.
        """
        super().__init__(ip_address=ip_address, port=port)

    def _deal_cards(self, seed: Optional[int] = None):
        pass

    def run(self):
        """Runs the server."""
        super()._socket.bind((super().ip_address, super().port))
        super()._socket.listen(4)

        while True:
            connection, address = super()._socket.accept()
            with connection:
                while True:
                    data = connection.recv(1024)
                    if not data:
                        break
                    logger.info(f'data: {data}, address: {address}')
