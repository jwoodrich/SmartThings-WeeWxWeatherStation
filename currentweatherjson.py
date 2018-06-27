# Based on currentweatherxml.py, Copyright 2016 HiljoLodewijk, extended by Jason Woodrich (@jwoodrich on github)

import os
import os.path
import time
import json

import weewx
import weewx.engine
import weeutil.weeutil

class CurrentWeatherJSON(weewx.engine.StdService):
        def __init__(self, engine, config_dict):
                super(CurrentWeatherJSON, self).__init__(engine, config_dict)
                d = config_dict.get('CurrentWeatherJSON', {})
                self.filename   = d.get('filename', '/var/tmp/current.json')
                self.binding    = d.get('binding', 'loop')
                self.nonevalue  = d.get('nonevalue', 'None')

                if self.binding == 'loop':
                        self.bind(weewx.NEW_LOOP_PACKET, self.handle_new_loop)
                else:
                        self.bind(weewx.NEW_ARCHIVE_RECORD, self.handle_new_archive)

        def handle_new_loop(self, event):
                self.write_data(event.packet)

        def handle_new_archive(self, event):
                delta = time.time() - event.record['dateTime']
                if delta > event.record['interval'] * 60:
                        return
                self.write_data(event.record)

        def write_data(self, data):
                with open(self.filename, "w") as f:
                        json.dump(data,f)

        def sort_keys(self, record):
                fields = ['local_time']
                for k in sorted(record):
                        if k != 'local_time':
                                fields.append(k)
                return fields

        def sort_data(self, record):
                fields = [str(record['local_time'])]
                for k in sorted(record):
                        if k != 'local_time':
                                fields.append(str(record[k]))
                return fields

        def format(self, data, label, places=None):
                value = data.get(label)
                if value is None:
                        value = self.nonevalue
                elif places is not None:
                        try:
                                v = float(value)
                                fmt = "%%.%df" % places
                                value = fmt % v
                        except ValueError:
                                pass
                return str(value)

