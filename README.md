# HydroSoil hydrOS Operating System
[![GitHub release](https://img.shields.io/github/release/BlaT2512/HydroSoil.svg)](https://gitHub.com/BlaT2512/HydroSoil/releases/)
[![GitHub license](https://img.shields.io/github/license/BlaT2512/HydroSoil.svg)](https://github.com/BlaT2512/HydroSoil/blob/master/LICENSE)
[![GitHub issues](https://img.shields.io/github/issues/BlaT2512/HydroSoil.svg)](https://gitHub.com/BlaT2512/HydroSoil/issues/)
[![Build Status](https://travis-ci.com/BlaT2512/HydroSoil.svg?branch=master)](https://travis-ci.com/BlaT2512/HydroSoil)
[![GitHub stars](https://img.shields.io/github/stars/BlaT2512/HydroSoil.svg?style=social&label=Star&maxAge=2592000)](https://gitHub.com/BlaT2512/HydroSoil/stargazers/)

![HydroSoil Logo](extras/Icon-256.png)
![hydrOS Logo](extras/hydrOS.png)

Official Repository for the hydrOS, the operating system behind HydroSoil: Smart Irrigation Solutions products.

# FYI: hydrOS is still in beta and unsuitable for stable use. Ensure you back up your data or run this in a safe environment if testing.

# Installing, running and building hydrOS
The latest version of hydrOS comes standard with all official HydroSoil products, including [HydroCore and HydroUnit products](https://hydrosoil.tk/products.html). The operating system can also be built from source code.
To build from source, install all dependencies for what you need as listed below.

## Dependencies
### hydrOS on HydroCore Linux package dependencies:
- Python 3 (python3) [latest version]
- Python GTK3 (libgtk-3-dev)
- Python GTK WebKit 3
- Mosquitto MQTT (mosquitto)
- Mosquitto MQTT Client (mosquitto-clients)
### hydrOS on HydroCore Python package dependencies:
- wireless
- wifi
- packaging
- paho-mqtt
### HydroUnit Standard C++ (Arduino) library dependencies:
- PubSubClient
- ESP8266WiFi (standard with the ESP8266 board package)

## Configuring HydroCore device for running hydrOS
First, connect the device to your desired WiFi network.
After this, configure the device by editing the Mosquitto configuration file with this command:

`sudo nano /etc/mosquitto/mosquitto.conf`

Remove this line from the bottom of the file:

`include_dir /etc/mosquitto/conf.d`

And then insert this at the bottom of the file:
```
allow_anonymous false
password_file /etc/mosquitto/pwfile
listener 1883
```
You can then exit out of Nano and save the file. In the Linux terminal, enter the following:

`sudo mosquitto_passwd -c /etc/mosquitto/pwfile SoilMeasurer`

When prompted for password, enter `HydroSoil123`

Once this is set up, change the device's hostname to `hydrosoilmainunit`

Reboot the device.

# Changelog
### v0.2-beta [LATEST PRE-RELEASE]
This second major pre-release of hydrOS brings huge performance & feature updates as well as bug fixes
Includes source code for hydrOS (Python), HydroLauncher (Python) and HydroUnit Standard (C++)
### New Features:
- Settings WiFi list showing available networks and disconnect functionality
- Settings page for changing weather location
- Radio buttons for changing the weather units (metric or imperial)
- Auto update refined and fixed for an even smoother experience
- Settings page for changing the time/date timezone and ability to sync the clock with NTP server
- New fluent, minimal dropdown notifications to replace bulky dialogs
- New red droplet icons for zones when critically low
- New fluent dropdown power menu
- Settings page to search for HydroUnit sensors and add them
- New plant/crop selection process with fluent dropdown
- Unregistered zones are now greyed-out on the Irrigation Zones page
- Initial setup process refined and fixed
- HydroSoil eManual reading capability in settings
- HydroCore factory reset capability
- Settings page GUI updated with sidebar
- HydroLauncher updated and refined
- HydroUnit Standard code heavily updated
- Tons of other bug fixes and small refinements
#### Known Issues:
- The zone/sensor config settings page is currently being worked on and not completed, a sample is included showcasing what it might look like
- Connection with the HydroSoil iOS app is not yet esatblished, but coming in the near future...
- HydroUnit Standard blue zone indicator light does not currently work

### v0.1-alpha
Initial pre-release of hydrOS
Includes source code for hydrOS (Python), HydroLauncher (Python) and HydroUnit Standard (C++)
#### New Features:
- Calendar page showing basic weather forecast for next 6 days and number of routines scheduled for each day
- Weather page showing detailed weather forecast for the current day and next 5 days
- Home page showing connected devices and status, simple weather forecast down the side and simple calendar at the bottom
- Zones page showing detail about each zone and allowing user to change mode, set Program mode schedule, change plant/crop and turn manual zone on/off
- Basic layout of most settings pages and the main settings page
- Header bar showing current local time in top-left corner and zone/WiFi status in top-right corner
- Menu bar allowing easy navigation between pages
- Automatic Updates - Detection of new release of hydrOS from Github and downloading required files and installing them
#### Known Issues:
- Settings pages currently do not work, the UI has only been created at the moment
- Multiple fatal errors occur when WiFi network is not connected
- HydroUnit Standard blue zone indicator light does not currently work
- Connection with the HydroSoil iOS app is not yet established

# Planned upcoming changes
### v0.3-beta
hydrOS v0.3-beta is nearly ready for release and will be coming out in the next few weeks.
This will most likely be the final beta before the first proper release, v1.0.0.
Will include source code for hydrOS (Python), HydroLauncher (Python) and HydroUnit Standard (C++)
#### New Features:
 - WiFi Network List on settings page allowing you to see networks and connect
 - Select weather location in settings page by postcode or city and country
 - Add new zone or sensor in settings with IconView and ability to select zone
 - Sync date and time with internet ability
 - Timezone changing ability with list downloaded for specified country
 - New fluent UI notifications dropdown - WiFi connection details, soil moisture level warning and new sensor detected
 - New fluent UI dropdown power menu
 - Refined initial setup process with ability to add new HydroUnits and connect to WiFi
 - Reset to factory default settings page
 - Zone and sensor configuration settings page allowing sensors to be reordered, deleted and renamed
 - Calendar week start setting in settings general page ability
 - Various big fixes
 
 ### v1.0.0
 This will be the first proper release of hydrOS and will have great stability and performance.
 Will include source code for hydrOS (Python), HydroLauncher (Python) and HydroUnit Standard (C++). HydroUnit Premium (C++) source code may also be released.
 #### New Features:
 - 2-Way Phone app connectivity through MQTT server
 - Settings page in GUI listing connected devices and ability to revoke devices and authorise them
 
 ### Other planned new features (could be added to v1.0.0 or future updates):
 - Offline splash screen at startup (HydroLauncher) showing available networks with start to offline mode option at the bottom
 - Offline mode with limited functionality and persistent notification asking to connect
 - JSON settings and livedata with zones.json file including all zone data and settings.json file with everything else (replacing current text files)
 - macOS theme for GUI application and support for other custom themes, and a light/dark mode
 - New settings page allowing support for custom plant/crops and editing to the list, also ability to reset to default list and download latest list
 - More new HydroLauncher features
 - Support for user to view raw moisture percentage and pH values for zones
 - System log in settings showing zone watering changes, programs running/stopping, wifi connectivity, tracebacks and much more
 - Support for run-once program for a specific zone
 - Support for a rain sensor to be connected so irrigation is stopped live when rain occurs and a rain delay setting
 - New support for integrations with support for sending specific events to IFTTT (with key) and MQTT (with host name/ip, port, username and password)
 - STDOUT and STDIN communication between 3 scripts instead of text files (HydroLauncher, hydrOS and MQTT scripts)
 - Most likely various bug fixes
