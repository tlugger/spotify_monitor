import json

from nio import TerminatorBlock
from nio.command import command
from nio.command.params.string import StringParameter
from nio.properties import SelectProperty, BoolProperty, VersionProperty
from nio.util.logging.levels import LogLevel


@command("log", StringParameter("phrase", default='Default phrase'))
class Logger(TerminatorBlock):

    """ Logger block.

    A NIO block for logging arbitrary signals.

    """

    # this is overidden here to change the default log_level from the base
    # block
    log_level = SelectProperty(LogLevel, title="Log Level", default="INFO")
    log_at = SelectProperty(LogLevel, title="Log At", default="INFO")
    log_as_list = BoolProperty(title="Log as a list",
                               default=False, visible=False)
    log_hidden_attributes = BoolProperty(title="Log Hidden Attributes",
                                         default=False)
    version = VersionProperty("1.1.0")

    def process_signals(self, signals):
        """ Overridden from the block interface.

        When an instance of Logger is in the receivers list for some
        other block, this method allows the sending block to deliver its
        outgoing signal object to the logger, which logs them individually.

        Args:
            signals (list of Signal): a list of signals to be logged.

        Returns:
            None
        """
        log_func = self._get_logger()

        if self.log_as_list():
            self._log_signals_as_list(log_func, signals)
        else:
            self._log_signals_sequentially(log_func, signals)

    def _log_signals_as_list(self, log_func, signals):
        try:
            log_func([
                json.dumps(signal.to_dict(self.log_hidden_attributes()), default=str, sort_keys=True)
                for signal in signals])
        except:
            self.logger.exception(
                "Failed to log {} signals".format(len(signals)))

    def _log_signals_sequentially(self, log_func, signals):
        for s in signals:
            try:
                log_func(json.dumps(s.to_dict(self.log_hidden_attributes()), default=str, sort_keys=True))
            except:
                self.logger.exception("Failed to log signal")

    def _get_logger(self):
        """ Returns a function that can log, based on the current config.

        This will return a different log level function based on what this
        block is configured to log at.
        """
        if isinstance(self.log_at(), LogLevel):
            log_str = self.log_at().name.lower()
        else:
            log_str = str(self.log_at()).lower()

        return getattr(self.logger, log_str, self.logger.error)

    def log(self, phrase="None provided"):
        self._get_logger()("Command log called with phrase: {0}".format(phrase))
