# coding=utf-8
from __future__ import absolute_import
import serial
from octoprint.util import RepeatedTimer
import octoprint.plugin

### (Don't forget to remove me)
# This is a basic skeleton for your plugin's __init__.py. You probably want to adjust the class name of your plugin
# as well as the plugin mixins it's subclassing from. This is really just a basic skeleton to get you started,
# defining your plugin as a template plugin, settings and asset plugin. Feel free to add or remove mixins
# as necessary.
#
# Take a look at the documentation on what other plugin mixins are available.

import octoprint.plugin

class Bme_monitorPlugin(
    octoprint.plugin.StartupPlugin,
    octoprint.plugin.SettingsPlugin,
    octoprint.plugin.AssetPlugin,
    octoprint.plugin.TemplatePlugin
):

    def on_after_startup(self):
        self._logger.info("Bme_monitor Plugin startuje...")
        self.sensors_data = {
            "bme1": {"temp": "--", "hum": "--", "pres": "--"},
            "bme2": {"temp": "--", "hum": "--", "pres": "--"}
        }
        # initialization of serial com
        try:
            self.ser = serial.Serial('/dev/serial/by-id/usb-Arduino__www.arduino.cc__0043_24230303637351411141-if00', 9600, timeout=1)
            # periodically read serial every 2.0 secconds
            self._timer = RepeatedTimer(2.0, self.read_serial_data)
            self._timer.start()
        except Exception as e:
            self._logger.error(f"Cant open serial com: {e}")

    def read_serial_data(self):
        if self.ser.in_waiting > 0:
            try:
                line = self.ser.readline().decode('utf-8').strip()
                parts = line.split()

                # modifyng raw pressure to display in hPa 
                raw_pressure = float(parts[3])
                hpa_pressure = raw_pressure / 100.0

                if not parts: return

                key = parts[0].replace(":", "").lower() # bme1 or bme2
                if key in self.sensors_data and len(parts) >= 4:
                    self.sensors_data[key] = {
                        "temp": parts[1],
                        "hum": parts[2],
                        "pres": f"{hpa_pressure:.2f}"
                    }
                    # This is supposed to send the data to the js
                    self._logger.info(f"sending sensor data to js: {self.sensors_data}") 
                    self._plugin_manager.send_plugin_message(self._identifier, self.sensors_data)

            except Exception as e:
                self._logger.error(f"error somewhere on serial com: {e}")
                self._logger.info(parts)
# this will create huge spam in logs---           self._logger.info(parts)



    ##~~ SettingsPlugin mixin

    def get_settings_defaults(self):
        return {
            # put your plugin's default settings here
        }

    ##~~ AssetPlugin mixin

    def get_assets(self):
        # Define your plugin's asset files to automatically include in the
        # core UI here.
        return {
            "js": ["js/bme_monitor.js"],
            "css": ["css/bme_monitor.css"],
            "less": ["less/bme_monitor.less"]
        }

    ##~~ Softwareupdate hook

    def get_update_information(self):
        # Define the configuration for your plugin to use with the Software Update
        # Plugin here. See https://docs.octoprint.org/en/main/bundledplugins/softwareupdate.html
        # for details.
        return {
            "bme_monitor": {
                "displayName": "Bme_monitor Plugin",
                "displayVersion": self._plugin_version,

                # version check: github repository
                "type": "github_release",
                "user": "G6seven",
                "repo": "OctoPrint-Bme_monitor",
                "current": self._plugin_version,

                # update method: pip
                "pip": "https://github.com/G6seven/OctoPrint-Bme_monitor/archive/{target_version}.zip",
            }
        }


# If you want your plugin to be registered within OctoPrint under a different name than what you defined in setup.py
# ("OctoPrint-PluginSkeleton"), you may define that here. Same goes for the other metadata derived from setup.py that
# can be overwritten via __plugin_xyz__ control properties. See the documentation for that.
__plugin_name__ = "Bme_monitor Plugin"


# Set the Python version your plugin is compatible with below. Recommended is Python 3 only for all new plugins.
# OctoPrint 1.4.0 - 1.7.x run under both Python 3 and the end-of-life Python 2.
# OctoPrint 1.8.0 onwards only supports Python 3.
__plugin_pythoncompat__ = ">=3,<4"  # Only Python 3

def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = Bme_monitorPlugin()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
    }
