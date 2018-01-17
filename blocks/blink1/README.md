Blink1
======

Control a [blink(1) dongle](http://blink1.thingm.com/).

Note: The blink1 python module has a dependency on pyusb. On some machines it may be that pyusb from pypi is not a recent enough version. If your block connects to the Blink1 device but is unable to fade the colors, try installing from [source](https://github.com/walac/pyusb). In addition to this, you can also try a [newer version](https://github.com/todbot/blink1) of blink1. This todbot repo is the official repo for thingm, yet it is not the one on pypi.

Properties
----------
- **color**: (colors= red|green|blue): RGB color to fade to.
- **fade_milliseconds**: Time it takes to fade to new color.

Inputs
------
- **default**: Any list of signals.

Outputs
-------
None

Commands
--------
None

Dependencies
------------
-   [**blink1**](https://pypi.python.org/pypi/blink1/0.0.12)
