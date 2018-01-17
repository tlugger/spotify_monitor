import logging
import json
from unittest.mock import MagicMock, call

from nio.testing.block_test_case import NIOBlockTestCase
from nio import Signal

from ..logger_block import Logger


class TestLogger(NIOBlockTestCase):

    def test_logger_not_enabled(self):
        blk = Logger()
        self.configure_block(blk, {
            'name': 'loggerblock',
            'log_level': 'INFO',
            'log_at': 'DEBUG',
        })
        self.assertFalse(blk.logger.isEnabledFor(
            getattr(logging, blk.log_at().name)))

    def test_logger_enabled(self):
        blk = Logger()
        self.configure_block(blk, {
            'name': 'loggerblock',
            'log_level': 'DEBUG',
            'log_at': 'INFO',
        })
        self.assertTrue(blk.logger.isEnabledFor(
            getattr(logging, blk.log_at().name)))

    def test_logger_equal(self):
        blk = Logger()
        self.configure_block(blk, {
            'name': 'loggerblock',
            'log_level': 'DEBUG',
            'log_at': 'DEBUG',
        })
        self.assertTrue(blk.logger.isEnabledFor(
            getattr(logging, blk.log_at().name)))

    def test_default_process_signals(self):
        blk = Logger()
        self.configure_block(blk, {})
        blk.logger = MagicMock()
        signal = Signal({"I <3": "n.io"})
        blk.process_signals([signal])
        blk.logger.info.assert_called_once_with(json.dumps(signal.to_dict()))
        self.assertEqual(blk.logger.error.call_count, 0)

    def test_list_process_signals(self):
        blk = Logger()
        self.configure_block(blk, {})
        blk.logger = MagicMock()
        signal = Signal({"I <3": "n.io"})
        blk.process_signals([signal, signal])
        blk.logger.info.assert_has_calls([
            call(json.dumps(signal.to_dict())),
            call(json.dumps(signal.to_dict())),
        ])
        self.assertEqual(blk.logger.error.call_count, 0)

    def test_exception_on_logging(self):
        blk = Logger()
        self.configure_block(blk, {})
        blk.logger = MagicMock()
        blk.logger.info.side_effect = Exception()
        signal = Signal({"I <3": "n.io"})
        blk.process_signals([signal])
        blk.logger.info.assert_called_once_with(json.dumps(signal.to_dict()))
        blk.logger.exception.assert_called_once_with("Failed to log signal")

    def test_list_logging(self):
        blk = Logger()
        self.configure_block(blk, {"log_as_list": True})
        blk.logger = MagicMock()
        signal = Signal({"I <3": "n.io"})
        blk.process_signals([signal, signal])
        blk.logger.info.assert_called_once_with([json.dumps(signal.to_dict()),
                                                 json.dumps(signal.to_dict())])
        self.assertEqual(blk.logger.error.call_count, 0)

    def test_log_sorting(self):
        blk = Logger()
        self.configure_block(blk, {})
        blk.logger = MagicMock()
        signal1 = Signal({"I <3": "n.io",
                          "You <3": "n.io",
                          "We All <3": "n.io"})
        signal2 = Signal({"You <3": "n.io",
                          "I <3": "n.io",
                          "We All <3": "n.io"})
        blk.process_signals([signal1, signal2])
        blk.logger.info.assert_has_calls([
            call(json.dumps(signal1.to_dict(), sort_keys=True)),
            call(json.dumps(signal2.to_dict(), sort_keys=True)),
        ])
        self.assertEqual(blk.logger.error.call_count, 0)

    def test_log_hidden_attributes(self):
        blk = Logger()
        self.configure_block(blk, {"log_hidden_attributes": True})
        blk.logger = MagicMock()
        signal = Signal({"_hidden": "hidden!", "not_hidden": "not hidden!"})
        blk.process_signals([signal])
        blk.logger.info.assert_called_once_with(json.dumps(signal.to_dict(True),
                                                           sort_keys=True))
        self.assertEqual(blk.logger.error.call_count, 0)
        self.assertEqual(len(signal.to_dict(True)), 2)
