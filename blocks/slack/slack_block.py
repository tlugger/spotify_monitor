from slacker import Slacker

from nio.block.base import Block
from nio.util.discovery import discoverable
from nio.properties import VersionProperty, StringProperty, \
    ObjectProperty, PropertyHolder
from nio.block.mixins.enrich.enrich_signals import EnrichSignals


class BotInformation(PropertyHolder):

    name = StringProperty(title='Name', default='')
    icon = StringProperty(title='Icon (URL or emoji)', default=':smiley_cat:')

    def get_bot_details(self, signal):
        """ Returns a dictionary of kwargs for the bot details.

        Given a signal, this method will construct a dictionary of kwargs
        for the Slack API call with the correct parameters. Mainly, it will
        figure out whether an icon is a URL or an emoji and use the correct
        parameter name
        """
        param_dict = dict()

        # Put the bot's name in the username field
        param_dict['username'] = self.name(signal)

        # If it starts and ends with a colon, it's an emoji code
        icon = self.icon(signal).strip()
        if icon.startswith(':') and icon.endswith(':'):
            param_dict['icon_emoji'] = icon
        else:
            param_dict['icon_url'] = icon

        return param_dict


@discoverable
class Slack(EnrichSignals, Block):

    """ Send messages to a slack channel as a bot """

    api_token = StringProperty(
        title='Slack API Token', default='[[SLACK_API_TOKEN]]')
    channel = StringProperty(title='Slack Channel', default='{{ $channel }}')
    message = StringProperty(title='Message', default='{{ $message }}')
    bot_info = ObjectProperty(
        BotInformation, title='Bot Details', default=BotInformation())
    version = VersionProperty('0.1.0')

    def __init__(self):
        super().__init__()
        self._slacker = None

    def configure(self, context):
        super().configure(context)
        self._slacker = Slacker(self.api_token())

    def process_signals(self, signals, input_id='default'):
        signals_to_notify = []
        for signal in signals:
            # If the channel name is potentially invalid, attempt to send the
            # message anyways. If no channel or DM identifier is specified, the
            # subject is assumed to be a channel.
            try:
                if not self._valid_channel_name(self.channel(signal)):
                    self.logger.warning(
                        "Channel '{}' may be invalid. "
                        "Channel names should start with '#' and "
                        "Direct Messages should start with '@'.".format(
                                                         self.channel(signal)))
                resp = self._send_message(
                    self.channel(signal),
                    self.message(signal),
                    **(self.bot_info().get_bot_details(signal)))
                signals_to_notify.append(
                    self.get_output_signal(resp.__dict__, signal))
            except:
                self.logger.exception(
                    "Unable to send message for signal {}".format(signal))
        if signals_to_notify:
            self.notify_signals(signals_to_notify)

    def _send_message(self, to_channel, message, **kwargs):
        """ Send a message to a Slack channel

        Pass additional kwargs for additional parameters to be sent to the
        Slack API call. These parameters can be found here:
        https://api.slack.com/methods/chat.postMessage
        """
        self.logger.debug("Sending message {} to channel {}".format(
            message, to_channel))
        resp = self._slacker.chat.post_message(to_channel, message, **kwargs)
        if resp.body.get('ok'):
            self.logger.debug("Message {} sent successfully".format(message))
        return resp

    def _valid_channel_name(self, channel):
        """ Determine if channel syntax looks off. """
        return channel.startswith('#') or channel.startswith('@')
