# SmartThings-WeeWxWeatherStation
WeeWx Gateway for SmartThings

weeWX is a Linux (also macOS, BSD, Solaris) application that interfaces with weather stations and produces reports, publishes to weather station networks, and other neat things.  More details at http://www.weewx.com/.

This SmartApp polls a weeWX weather station and provides temperature, relative humidity, wind speed/direction and gusts, rain stats to SmartThings.  Polling frequency is configurable.  I assume you're working with your own weather station.  If not, be nice with the polling frequency.

An extension is required for weeWX to produce JSON formatted reports.  This is based on the currentweatherxml.py extension published here: https://www.mail-archive.com/weewx-user@googlegroups.com/msg02106.html, but has been adjusted to produce JSON output and removes the abstraction around attribute names.  See currentweatherjson.py in this repository.

On Debian/Ubuntu the file should be placed in /usr/share/weewx/weewx.  On other systems ... put it where the rest of the python scripts are for weeWX.  You could probably find it by doing a find on 'wxmanager.py' (find / -name 'wxmanager.py').

Additionally, the following configuration is needed in weewx.conf (/etc/weewx/weewx.conf on my system).  The base directory should be where your weeWX reports are published to, which should be accessible to a web server, such as Apache httpd or nginx.  weeWX will need permissions to write to this file.

```
[CurrentWeatherJSON]
filename=/var/www/html/weewx/current.json
```
Also, append this to Engine -> Services -> report_services: `weewx.currentweather.CurrentWeatherJSON`

It might look something like this:
```
[Engine]
    
    [[Services]]
        ...
        report_services = weewx.engine.StdPrint, weewx.engine.StdReport, weewx.currentweatherjson.CurrentWeatherJSON

```

Lastly, I've tested this on my local LAN, but I don't publish my weeWX reports on the Internet.  Internet based reporting *should* work ... but we all know how that goes.

Use at your own risk. It works for me.
