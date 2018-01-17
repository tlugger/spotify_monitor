from time import sleep
from unittest.mock import MagicMock

from nio.block.terminals import DEFAULT_TERMINAL
from nio.signal.base import Signal
from nio.testing.block_test_case import NIOBlockTestCase

from ..debounce_block import Debounce


class TestDebounce(NIOBlockTestCase):

    def test_debounce(self):
        """Test that signals are properly debounce for configured interval."""
        block = Debounce()
        block._backup = MagicMock()
        self.configure_block(block, {
            "interval": {
                "milliseconds": 200
            }
        })
        block.start()
        block.process_signals([Signal(), Signal()])
        block.process_signals([Signal()])
        self.assert_num_signals_notified(1, block)
        sleep(.3)
        block.process_signals([Signal()])
        self.assert_num_signals_notified(2, block)
        block.stop()

    def test_debounce_group(self):
        """Test that the group by mixin is properly used."""
        block = Debounce()
        block._backup = MagicMock()
        self.configure_block(block, {
            "interval": {
                "milliseconds": 200
            },
            "group_by": "{{ $group }}"
        })
        block.start()
        block.process_signals([
            Signal({'group': 'bar'}),
        ])
        self.assert_num_signals_notified(1, block)
        block.process_signals([
            Signal({'group': 'bar'}),
            Signal({'group': 'foo'})
        ])
        self.assert_num_signals_notified(2, block)
        sleep(.3)
        block.process_signals([Signal({'group': 'bar'})])
        self.assert_num_signals_notified(3, block)
        block.stop()
        self.assertTrue(self.last_notified[DEFAULT_TERMINAL][0].group == 'bar')
        self.assertTrue(self.last_notified[DEFAULT_TERMINAL][1].group == 'foo')
        self.assertTrue(self.last_notified[DEFAULT_TERMINAL][2].group == 'bar')

    def test_debounce_signal_interval(self):
        """Signals are properly debounce for dynamically set interval."""
        block = Debounce()
        block._backup = MagicMock()
        self.configure_block(block, {
            "interval": "{{ datetime.timedelta(milliseconds=$interval) }}"
        })
        block.start()
        block.process_signals(
            [Signal({'interval': 200}), Signal({'interval': 200})])
        block.process_signals([Signal({'interval': 200})])
        self.assert_num_signals_notified(1, block)
        sleep(.3)
        block.process_signals([Signal({'interval': 200})])
        self.assert_num_signals_notified(2, block)
        block.stop()
