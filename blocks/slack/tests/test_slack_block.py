from unittest import skipUnless
from unittest.mock import MagicMock

from nio.block.terminals import DEFAULT_TERMINAL
from nio.signal.base import Signal
from nio.testing.block_test_case import NIOBlockTestCase

slacker_available = True
try:
    from slacker import Slacker
except:
    slacker_available = False

try:
    from ..slack_block import Slack
except:
    # Allow tests to fail if the block cannot be imported
    pass


@skipUnless(slacker_available, 'slacker is not available!!')
class TestSlack(NIOBlockTestCase):

    def test_send_message(self):
        """ Tests that messages get sent under the default conditions """
        blk = Slack()
        self.configure_block(blk, {
            'message': '{{ $message }}',
            'channel': '{{ $channel }}',
            'api_token': 'FAKE TOKEN',
            'bot_info': {
                'name': 'Bot Name',
                'icon': ':bot_emoji:'
            }
        })
        mock = blk._slacker.chat.post_message = MagicMock()
        blk.start()
        blk.process_signals([Signal({
            'message': 'This is my message',
            'channel': 'This is my channel'
        })])
        blk.stop()
        mock.assert_called_once_with(
            'This is my channel', 'This is my message',
            icon_emoji=':bot_emoji:', username='Bot Name')
        self.assertEqual(1, len(self.last_notified[DEFAULT_TERMINAL]))

    def test_send_message_icon_url(self):
        """ Tests that messages get sent when a URL is supplied for an icon """
        blk = Slack()
        self.configure_block(blk, {
            'message': '{{ $message }}',
            'channel': '{{ $channel }}',
            'api_token': 'FAKE TOKEN',
            'bot_info': {
                'name': 'Bot Name',
                'icon': 'http://ICONURL'
            }
        })
        mock = blk._slacker.chat.post_message = MagicMock()
        blk.start()
        blk.process_signals([Signal({
            'message': 'This is my message',
            'channel': 'This is my channel'
        })])
        blk.stop()
        mock.assert_called_once_with(
            'This is my channel', 'This is my message',
            icon_url='http://ICONURL', username='Bot Name')
        self.assertEqual(1, len(self.last_notified[DEFAULT_TERMINAL]))

    def test_send_message_notified_signal(self):
        """ Tests that signals are notified with response """
        blk = Slack()
        self.configure_block(blk, {
            'message': 'message',
            'channel': 'channel',
        })
        blk._slacker = MagicMock()
        blk._send_message = MagicMock()
        resp = {'raw': 'raw response', 'body': 'and a body'}
        blk._send_message.return_value.__dict__ = resp
        blk.start()
        blk.process_signals([Signal({'i <3': 'n.io'})])
        blk.stop()
        self.assertEqual(1, len(self.last_notified[DEFAULT_TERMINAL]))
        self.assertDictEqual(
            self.last_notified[DEFAULT_TERMINAL][0].to_dict(), resp)

    def test_no_message(self):
        """ Tests message is not sent if it can't be found on the signal """
        blk = Slack()
        self.configure_block(blk, {
            'message': '{{$message}}',
            'channel': '{{$channel}}',
            'api_token': 'FAKE TOKEN',
            'bot_info': {}
        })
        mock = blk._slacker.chat.post_message = MagicMock()
        blk.start()
        blk.process_signals([Signal({
            'not_a_message': 'This is my message',
            'channel': 'This is my channel'
        })])
        blk.stop()
        self.assertEqual(mock.call_count, 0)
        # No signals are notified if the Slack messages is not successful
        self.assertEqual(0, len(self.last_notified[DEFAULT_TERMINAL]))

    def test_no_channel(self):
        """ Tests message is not sent if channel can't be found """
        blk = Slack()
        self.configure_block(blk, {
            'message': '{{ $message }}',
            'channel': '{{ $channel }}',
            'api_token': 'FAKE TOKEN',
            'bot_info': {}
        })
        mock = blk._slacker.chat.post_message = MagicMock()
        blk.start()
        blk.process_signals([Signal({
            'message': 'This is my message',
            'not_a_channel': 'This is my channel'
        })])
        blk.stop()
        self.assertEqual(mock.call_count, 0)
        # No signals are notified if the Slack messages is not successful
        self.assertEqual(0, len(self.last_notified[DEFAULT_TERMINAL]))

    def test_bad_expression(self):
        """ Tests message is not sent if there is an invalid expression """
        blk = Slack()
        self.configure_block(blk, {
            'message': '{{ message }}',  # this is a bad expression
            'channel': '{{ $channel }}',
            'api_token': 'FAKE TOKEN',
            'bot_info': {}
        })
        mock = blk._slacker.chat.post_message = MagicMock()
        blk.start()
        blk.process_signals([Signal({
            'message': 'This is my message',
            'channel': 'This is my channel'
        })])
        blk.stop()
        self.assertEqual(mock.call_count, 0)
        # No signals are notified if the Slack messages is not successful
        self.assertEqual(0, len(self.last_notified[DEFAULT_TERMINAL]))

    def test_invalid_channel(self):
        """ Tests that a channel with a potentially malformed name will
            gets flagged. """

        # Instantiate the slack block.
        blk = Slack()

        # Option 1: The channel does not begin with "#" or "@".
        self.assertFalse(blk._valid_channel_name("I_dont_start_with_@_or_#"))

        # Option 2: The channel begins with "#" (a slack channel).
        self.assertTrue(blk._valid_channel_name("#Im_a_slack_channel"))

        # Option 3: The channel begins with "@" (a slack direct message).
        self.assertTrue(blk._valid_channel_name("@Im_a_user_handle"))
