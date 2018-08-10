# SmartThings-WeeWxWeatherStation
WeeWx Gateway for SmartThings

weeWX is a Linux (also macOS, BSD, Solaris) application that interfaces with weather stations and produces reports, publishes to weather station networks, and other neat things.  More details at http://www.weewx.com/.

This SmartApp polls a weeWX weather station and provides temperature, relative humidity, wind speed/direction and gusts, rain stats to SmartThings.  Polling frequency is configurable.  I assume you're working with your own weather station.  If not, be nice with the polling frequency.

The SmartApp and Device Handlers must be installed on SmartThings via the Groovy API.  This can be done by logging into https://graph.api.smartthings.com/, selecting your location, then:
1. Click "My Device Handlers", then "Create Device Handler"
2. Select the "From Code" tab
3. Copy and paste the device handler code from the repository at /devicetypes/jwoodrich/weewx-weather-station.src/weewx-weather-station.groovy into the window, then click Create.  
4. Click "Publish", then "For Me" from the dropdown.
5. Click "My SmartApps", then "New SmartApp"
6. Select the "From Code" tab
7. Copy and paste the SmartApp code from the repository at /smartapps/jwoodrich/weewx-json-gateway.src/weewx-json-gateway.groovy into the window, then click Create.
8. Click "Publish", then "For Me" from the dropdown.

At this point the SmartApp and Device Handlers should be available in the SmartThings app.  They can be configured from Automation -> SmartApps by clicking "+ Add a SmartApp", "+ My Apps", then "WeeWX JSON Gateway".  You will be prompted for the IP address of the weather station.  Local LAN should be enabled if WeeWX is on the same network (behind a router) as the SmartThings hub.  This has been tested on Android.  I'm not familiar with the iOS app, but I assume it's similar.

An extension is required for weeWX to produce JSON formatted reports.  This is based on the currentweatherxml.py extension published here: https://www.mail-archive.com/weewx-user@googlegroups.com/msg02106.html, but has been adjusted to produce JSON output and removes the abstraction around attribute names.  See /currentweatherjson.py in this repository.

On Debian/Ubuntu the file should be placed in /usr/share/weewx/weewx.  On other systems ... put it where the rest of the python scripts are for weeWX.  You could probably find it by doing a find on 'wxmanager.py' (find / -name 'wxmanager.py').

Additionally, the following configuration is needed in weewx.conf (/etc/weewx/weewx.conf on my system).  The base directory should be where your weeWX reports are published to, which should be accessible to a web server, such as Apache httpd or nginx.  weeWX will need permissions to write to this file.

```
[CurrentWeatherJSON]
filename=/var/www/html/weewx/current.json
```
Also, append this to Engine -> Services -> report_services: `weewx.currentweatherjson.CurrentWeatherJSON`

It might look something like this:
```
[Engine]
    
    [[Services]]
        ...
        report_services = weewx.engine.StdPrint, weewx.engine.StdReport, weewx.currentweatherjson.CurrentWeatherJSON

```

Lastly, I've tested this on my local LAN, but I don't publish my weeWX reports on the Internet.  Internet based reporting *should* work ... but we all know how that goes.

Use at your own risk. It works for me.
