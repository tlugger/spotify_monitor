# Spotify Monitor

This nio project can be run from a Raspberry Pi to monitor the playback status of a users Spotify account. The color of a blink(1) dongle can be canged depending on which device is currently streaming music. "Unauthorized" devices will have their playback stopeed every 10 seconds, change the dongle red, and send a slack message to the account holder about the unauthorized device

## How to Use

### Clone Using the nio CLI

You can create a new project directory with the nio-cli

  ```
    pip3 install nio-cli
    nio new <new_project_name> --template https://github.com/tlugger/spotify_monitor.git
  ```

### Obtain API Credentials

* Visit the [Spotify Developer](https://developer.spotify.com/web-api/) page to create your spotify app and get your API credentials

* Visit the [Slack API](https://api.slack.com) console to create your Slack app and get your API token

### Configure User Variables

* Modify nio.env and replace all '<>' placeholders with your credentials obtained above for 'CLIENT_ID', 'CLIENT_SECRET', and 'SLACK_API_TOKEN'. 

* Replace '<YOUR LIST OF AUTHOREZED DEVICE NAME STRINGS>' with a list of device names (as Spotify knows them) that you want to be "Authorized"

  * Note: The Spotify API returns some odd unicode for apostrophes. Something like 'Tyler's MacBook Pro' would become 'Tyler\u2019s MacBook Pro'.

* Replace '<YOUR SPOTIFY USERNAME>' with the username assigned to your profile at Spotifys [Account overview](https://www.spotify.com/us/account/overview/) page.

* Repalce '<SLACK_USERNAME>' with your slack username for direct messages. 

### Setup Spotify Authorization Script

An additional step requred for the Spotify block is to set up 'blocks/spotify/spotify.py' with your Spotify credentials. This script is automatically run once by nio with instructions to vistit a redirect url in your browser to authorize your app and cache your initial auth token. See Spotipy description for authentication below:
```
	User authentication requires interaction with your
        web browser. Once you enter your credentials and
        give authorization, you will be redirected to
        a url.  Paste that url you were directed to to
        complete the authorization.
``` 

### Configure the `SetColor` Block

This block is what sets the RGB color code for the blink(1) dongle. To add colors for you device. Open this block within the _DeviceIndicator_ service of your instance in the [System Designer](http://designer.n.io). 

Currently each RGB (red, green, blue) field has two lookups. One for a device name equal to `<Device Name>` setting that color to a maximum level and one default that does not set a color. The default should be hit for any device assigned to the name "nothing" but all of your other devices should have a custom lookup for their device name and a unique RGB code assigned to them. 

Note: Be sure to keep the defaut (`{{True}}`) formula at the bottom of the look ups so it is only hit if no other device names match your custom lookups. 

## File Reference

**blocks**<br>A directory that contains block types, as submodules. The project template comes with a few of the most commonly used block types. Block types can be added and removed. Additional block types can be found in the block library and added through the System Designer, or, you can add your own custom block types here.

**etc**
<br>A folder containing project configurations and scripts.

**service_tests**<br>A submodule for service tests that includes `NioServiceTestCase` and other tools for service testing.

**tests**<br>A folder for your tests with an example set up for a service test.

**Dockerfile**<br>An optional script to create a Docker image of the project. Docker can be used as a tool in deployments.

**docker-compose.yml**<br>A file optionally used in conjunction with Docker to configure your application so that all its dependencies can be started with a single command.

**nio.conf**<br>A file that contains the nio project configuration. Default values are shown.

**nio.env**<br>A file containing environment variables for the project. If this file contains secrets, you will want to add it to the `.gitignore` file.

