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
#### New Features:
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
- Most likely various bug fixes
  
### Overview of other planned new features (could be added to v1.0.0 or future updates):
#### New Settings Pages
- Personalisation - Change theme/accent colour and choose between light/dark mode
- Plant/crop List - Edit the plant/crop list for zones and add your own entries, also download the latest list and reset to default
- System Log - Shows all event that have occured including irrigation related and WiFi, MQTT, tracebacks and more
- Rain Sensing - Enable rain sensor connection and set parameters such as what percent rain should trigger it and rain delay
- Intergrations - Allows integration with user's IFTTT recipes and user's own MQTT server with a specific topic
- Extensions - Allows extensions to be added to hydrOS which bring more functionality or features, and can be installed from a database or custom github URL

#### Performance Updates
- JSON Settings - Allows quicker and much easier writing and reading to settings files
- STDOUT and STDIN communication - Allows much faster internal communication between the processes

#### Extensions
- A hydrOS Extension Market will be released allowing developer's custom extensions to be easily found (hosted on Github)
- Extension protocol allows developers to make their own extensions and add them to market or give custom link to user's
- One-time codes can be given to user's who have purchased a product so that only they have access to the extension
- A custom verification process can be made to run when extension is installed (e.g. check verification code) or on every startup (e.g. check if verification code is still valid or being used elsewhere)
##### A draft of the extension protocol can be found below

#### Other New Features
- Offline Mode - Allows hydrOS to be used with limited functionality when WiFi is disconnected
- Irrigation Zones - Irrigation Zones page now shows you the moisture percentage and pH level for each zone
- Irrigation Zones - Run-once programs can now be created for zones to irrigate for a specific time just once
- HydroLauncher - New and more working features are being added including debugging

# Extensions
## What are hydrOS Extensions?
hydrOS Extensions allow developers to write their own code snippets to add functionality to the HydroSoil system, e.g. an extension allowing connectivity to a custom sensor or integration with a product. There are many different triggers or ways your code can run, e.g. run a function every second, when a certain condition is met, at a certain time etc. An extension can also simply add a theme to hydrOS and contain no code. This is a personalisation theme. Note that extensions can not currently add to the GUI, apart from having their own settings page. This may be allowed in the future.

## How are extensions installed?
Extensions can be installed in hydrOS via Settings > Extensions. There are 2 ways an extensions can be installed, although for both methods the extension must be hosted as a GitHub repo. It can either be installed from the extension marketplace or via a custom URL to the code in a GitHub repo. The extensions marketplace allows developers to have their extension easily found and displayed in the hydrOS extension list. You can get your extension added by following the extension marketplace addition process, detailed below. You can also get your extension installed via direct link to your GitHub repo.

## How do I get my extension added to the marketplace?
To get your extension added to the marketplace, you will need to open an issue on this GitHub repository. When asked what issue type to create, select the extension marketplace addition template.

## Extension Protocol [DRAFT]
The protocol guide below will help you develop a hydrOS extension. Functionality is not yet available in hydrOS, it will be coming in a future update with the beta coming out soon.

### Code extension folder/file structure
Code extensions add functionality to hydrOS.

Extensions will have their own folder in the [hydrOS Root]\extensions directory, with the following structure:
```
ExampleExtension/
ExampleExtension/extension.json
ExampleExtension/settingsGUI.json
ExampleExtension/src/
ExampleExtension/src/main.py
ExampleExtension/src/mqtt.py*
ExampleExtension/src/launcher.py*
ExampleExtension/src/settings.json*
ExampleExtension/src/assets/*
```
File/folder names with an asterix at the end are not compulsory to the folder structure.

#### extension.json
The `extension.json` file contains information about the extension and what it does. Details of how to structure this file will be added soon.

#### settingsGUI.json
The `settingsGUI.json` file contains the data for what settings there are for this extension, e.g. a dropdown box for the user to select the sensor model. It can be blank if there are no settings but must exist. The user will be able to access the settings page for your extension built from this file via Settings > Extensions > [Extension Name]. Details of how to structure this file will be added soon.

#### src/main.py
This file contains the main code for your extension which will be run by main.py. Details of how to structure this file and it's class will be added soon.

#### src/mqtt.py
This file contains any code which you would like to add functionality to the MQTT server, e.g. recieving messages from a certain topic for your custom sensor. Details of how to structure this file and it's class will be added soon.

#### src/launcher.py
This file contains any code which you would like to add functionality to the HydroLauncher, e.g. an extra button to the HydroLauncher menu or task to run on startup before the launch of GUI and/or MQTT server. Details of how to structure this file and it's class will be added soon.

#### src/settings.json
This file contains any settings that your script needs to function, e.g. the sensor model and ID. It can be written to and accessed by your extension's GUI settings page (defined by `settingsGUI.json`).

#### src/assets/ folder
The `src/assets` folder can contain any extra assets that your script needs. It is not accessible by the user.

### Personalisation extension folder/file structure
Personalisation extensions add theme(s) to hydrOS.

Extensions will have their own folder in the [hydrOS Root]\extensions directory, with the following structure:
```
ExampleExtension/
ExampleExtension/extension.json
ExampleExtension/theme/
ExampleExtension/theme/index.theme
ExampleExtension/theme/themeName/
ExampleExtension/theme/themeName/gtk.css
ExampleExtension/theme/themeName/gtk-dark.css*
ExampleExtension/theme/themeName/settings.ini
ExampleExtension/theme/themeName/thumbnail.png
ExampleExtension/theme/themeName/assets/
```
File/folder names with an asterix at the end are not compulsory to the folder structure.

#### extension.json
The `extension.json` file contains information about the extension and what it does. Details of how to structure this file will be added soon.

#### theme/ folder
The theme folder contains the actual GTK theme

#### theme/index.theme
This is a standard GTK theme file which contains information about the theme. It is not used by hydrOS but by the internal system when loading the theme.

#### theme/themeName/ folder
This folder contains a GTK 3 theme. The theme must be a GTK 3 theme as this is what hydrOS is based on. You can have multiple themes which are installed with your extension, for this you should have a folder like this in the `theme` folder for each one.

#### theme/themeName/gtk.css
`gtk.css` is the main theme file which contains the actual theme data and how to display the theme for the system, such as which files are used in the assets folder.

#### theme/themeName/gtk-dark.css
`gtk-dark.css` is very similar to `gtk.css` but is the information for the dark version of your theme, if it has one.

#### theme/themeName/settings.ini
`settings.ini` is a standard theme file which contains information about the theme settings.

#### theme/themeName/thumbnail.png
This image is a thumbnail image of the theme.

#### theme/themeName/assets/ folder
This folder contains the image assets for your theme, generally in PNG or SVG format. The assets are used by `gtk.css` and `gtk.dark.css` if your theme has a dark mode.
