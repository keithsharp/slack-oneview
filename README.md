# HP OneView integrated with Slack
HP OneView[1] is an infrastructure management application that provides a rich HTTP/JSON 
RESTful API and a State Change Message Bus (SCMB) implemented using AMQP/RabbitMQ.  This
provides the opportunity to integrate OneView with other systems.  Slack[2] is a group 
messaging system that is increasingly used by IT infrastructure teams.  Slack provides 
many integration points that allow messages to be published into chat channels from other
applications.

This example Python application listens on the OneView SCMB for messages relating power 
status changes in the servers OneView is managing and publishes them into a Slack 
channel.

## Installation and Setup
As described below there is some SSL setup required.  This uses the python-hpOneView[3]
library which has a minimum requirement of Python 3.4.  The main application only
requires the AMQP library, so should run on earlier versions of Python (not tested).

### SSL Configuration
The SCMB is encrypted using SSL so it is necessary to generate (if not done previously)
and download the relevant certificates and keys.  To make this simpler there is a small
application called keys.py to generate and download the certificates and keys.  Running 
the command:

    keys.py -s <oneview server> -u <username> -p <password>

will download the client certificate, key, and CA root bundle to the current working 
directory.  Options to place the files in a particular directory and to generate keys 
are available - run keys.py with the -h flag for full help.

### Configuring the Application
The application uses a single configuration file to define the following parameters.  In
the [slack] section:

* **webhook** is the URL of the incoming web hook that you configure within the Slack web 
interface.
* **channel** is the name of the Slack channel that you want to send messages to.  I
think this needs to be prefixed with a #.
* **botname** is the name of the bot that will be associated with the published messages.
You could set this to the name of you OneView server if you were running multiple
instances.

In the [oneview] section:

* **server** is the name or IP address of your OneView server.
* **username** is the username that the application will use to authenticate to OneView.
* **password** is the password that the application will use to authenticate to OneView.
* **certfile** is the path to the certificate file you downloaded with keys.py.
* **keyfile** is the path to the key file you downloaded with keys.py.
* **caroot** is the path to the CA root file you downloaded with keys.py.

## Running the Application
Once you have created the configuration, running the application is as simple as:

    server.py -f /path/to/your/configuration/file

If you power off one of your servers using the OneView GUI you should see two messages
published in your Slack channel: one stating that the server is powering off and 
second once the server has completed the power off.  A similar pattern will occur if 
you power on a server.

## References
[1] http://www.hp.com/go/oneview
[2] https://slack.com
[3] https://github.com/HewlettPackard/python-hpOneView