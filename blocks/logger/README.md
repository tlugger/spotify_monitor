LoggerBlock
===========

Logs each incoming signal to the configured log level.

From the [python logging howto,](https://docs.python.org/3.5/howto/logging.html) log
levels are defined in the following way, in order of increasing severity:

- DEBUG
- INFO
- WARNING
- ERROR
- CRITICAL

There are two configurable options for the logger block: log_level and
log_at. Both are set using the above hierarchy. If log_level is NOTSET,
the logger block inherits the log level of the service.

log_at is used to log messages at different severity levels. As long as
it is greater or equal to log_level it will log messages at the configured
level.

Properties
--------------
- **log_level**(select): Sets the log level for the block. Default is INFO.
- **log_at**(select): The log level to log outgoing messages at. Default is INFO.
- **log_as_list**(hidden, bool): Whether to log incoming signals as lists. The default
behavior is to log lists of incoming signals one at a time. Setting this to True
allows one to see if the block received multiple signals at once or multiple
signals sequentially.

Dependencies
----------------
None

Commands
----------------

-   **log** (phrase="Default phrase"): Logs a DEBUG message `"Command log called with phrase: {0}".format(phrase)`.

Input
-------
Any list of signals.

Output
---------
None
