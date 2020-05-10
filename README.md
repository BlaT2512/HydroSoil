# HydroSoil hydrOS Operating System
[![GitHub release](https://img.shields.io/github/release/BlaT2512/hydrOS.svg)](https://GitHub.com/BlaT2512/hydrOS/releases/)
[![GitHub license](https://img.shields.io/github/license/BlaT2512/hydrOS.svg)](https://github.com/BlaT2512/hydrOS/blob/master/LICENSE)
[![GitHub issues](https://img.shields.io/github/issues/BlaT2512/hydrOS.svg)](https://GitHub.com/BlaT2512/hydrOS/issues/)
[![GitHub stars](https://img.shields.io/github/stars/BlaT2512/hydrOS.svg?style=social&label=Star&maxAge=2592000)](https://GitHub.com/BlaT2512/hydrOS/stargazers/)

![HydroSoil Logo](logos/Icon-256.png)
![hydrOS Logo](logos/hydrOS.png)

Official Repository for the hydrOS, the operating system behind HydroSoil: Smart Irrigation Solutions.

# Installing, running and building hydrOS
The latest version of hydrOS comes standard with all official HydroSoil products, including HydroCore and HydroUnit products. The operating system can also be built from source code.
To build from source, install all dependencies for what you need as listed below.

## Dependencies
### hydrOS on HydroCore Linux package dependencies:
- python3 (latest version)
- libgtk-3-dev
- mosquitto
- mosquitto-clients
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

Once this is set up, change the device's hostname to `soilsystemmainunit`
Reboot the device.

# Changelog & planned upcoming changes
### v0.1 [LATEST PRE-RELEASE]
Initial release of hydrOS
Includes source code for HydroUnit Standard.
#### New Features:
- Calendar page showing basic weather forecast for next 6 days and number of routines scheduled for each day
- Weather page showing detailed weather forecast for the current day and next 5 days
- Home page showing connected devices and status, simple weather forecast down the side and simple calendar at the bottom
- Zones page showing detail about each zone and allowing user to change mode, set Program mode schedule, change plant/crop and turn manual zone on/off
- Basic layout of most settings pages and the main settings page
- Header bar showing current local time in top-left corner and zone/WiFi status in top-right corner
- Menu bar allowing easy navigation between pages
#### Known Issues:
- Settings pages currently do not work, the UI has only been created at the moment
- Multiple fatal errors occur when WiFi network is not connected
- HydroUnit Standard blue zone indicator light does not currently work
- Connection with the HydroSoil iOS app is not yet established

### v0.2 [PLANNED]
#### Planned Features:
- Automatic Updates - Detection of new release of hydrOS from Github and downloading required files and installing them
- Updates for HydroUnit's over-air when detected
