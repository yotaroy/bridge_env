import pytest
from pytest_mock import MockFixture

from bridge_env import Card, Player, Suit
from bridge_env.network_bridge.server import PlayerThread, Server


class TestThreadHandler:

    @pytest.fixture(scope='function')
    def thread_handler(self, mocker: MockFixture):
        return PlayerThread(connection=mocker.MagicMock(),
                            event_sync=mocker.MagicMock(),
                            event_thread=mocker.MagicMock(),
                            sent_message_queues=mocker.MagicMock(),
                            received_message_queues=mocker.MagicMock(),
                            players_event=mocker.MagicMock(),
                            team_names=mocker.MagicMock())

    @pytest.mark.parametrize(
        ('expected_message', 'received_message', 'expected'), [
            ('Test message', 'test Message', True),
            ('Space number is not same', 'Space  Number is   not Same', True),
            ('North plays a card', 'North plays acard', False),
        ])
    def test_check_message(self,
                           expected_message,
                           received_message,
                           expected,
                           thread_handler,
                           mocker: MockFixture):
        mock_receive_message = mocker.patch(
            'bridge_env.network_bridge.socket_interface.MessageInterface.'
            'receive_message')
        mock_receive_message.return_value = received_message

        mock_handle_error_func = mocker.patch(
            'bridge_env.network_bridge.server.PlayerThread._handle_error')
        actual = thread_handler._check_message(expected_message)
        if not expected:
            mock_handle_error_func.assert_called_once()
        assert actual == expected

    @pytest.mark.parametrize(
        ('content', 'expected_team_name', 'expected_player',
         'expected_protocol_version'),
        [('Connecting "team_example" as North using protocol version 18',
          'team_example', Player.N, 18),
         ('Connecting "directory/file.ext" as East using protocol version 1',
          'directory/file.ext', Player.E, 1),
         ('Connecting "Dir/File_test.ext" as SOUTH Using Protocol Version 123',
          'Dir/File_test.ext', Player.S, 123)
         ])
    def test_parse_connection_info(self,
                                   content,
                                   expected_team_name,
                                   expected_player,
                                   expected_protocol_version):
        assert PlayerThread.parse_connection_info(content) == (
            expected_team_name, expected_player, expected_protocol_version)


class TestServer:

    @pytest.mark.parametrize(('hand_set', 'expected'), [
        ({Card(12, Suit.C), Card(9, Suit.C), Card(10, Suit.C), Card(11, Suit.H),
          Card(2, Suit.C), Card(2, Suit.H), Card(4, Suit.S), Card(9, Suit.H),
          Card(11, Suit.C), Card(14, Suit.H), Card(3, Suit.H), Card(13, Suit.S),
          Card(10, Suit.S)}, 'S K T 4. H A J 9 3 2. D -. C Q J T 9 2.')
    ])
    def test_hand_to_str(self, hand_set, expected):
        assert Server.hand_to_str(hand_set) == expected

    @pytest.mark.parametrize(('message', 'expected'), [
        ('North bids 1D Alert.', 'North bids 1D'),
        ('East bids 2D alert. ', 'East bids 2D'),
        ('South bids 3S  Alert. ', 'South bids 3S'),
    ])
    def test_remove_alert_word(self, message, expected):
        assert Server.remove_alert_word(message) == expected
