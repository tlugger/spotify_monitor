Slack
=====
Send messages to a Slack channel as a bot.

Properties
----------
- **api_token**: The API Token for your bot. Get a test token at the Slack Web API page.
- **bot_info**: Information about the bot that will be sending the message.
- **channel**: The channel to send your message to. You can use the channel name (prefixed with a hashtag) or you can use the channel ID returned from the API. Direct messages are supported as well (prefixed with @).
- **enrich**: If true, the original incoming signal will be included in the output signal.
- **message**: The message to send to the channel.

Inputs
------
- **default**: Any list of signals.

Outputs
-------
- **default**: The response of the slack request.

Commands
--------

Dependencies
------------
 * [slacker](https://github.com/os/slacker)

Output Example
--------------
EnrichSignals mixin is used to pass through input signals and enrich them with the [response](https://api.slack.com/methods/chat.postMessage) from the Slack request.
```python
{
  "successful": True,
  "error": None,
  "body": {
    "ok": True,
    "ts": "1405895017.000506",
    "channel": "C024BE91L",
    "message": {
      "type": "message",
      "username": "hansmosh",
      "text": "i <3 n.io",
      "ts": "1405895017.000506",
        …
    }
  },
  "raw": '{"ok":true,"chanel":"C024BE91L",...}'
}
```

