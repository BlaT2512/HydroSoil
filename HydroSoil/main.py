#  main.py
#  
#  Copyright 2020  <pi@hydrosoilmainunit>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
# This is the main code, for handling and loading the GUI
# It is run on boot of the Raspberry Pi

# Ensure that the unit has a unique ID code
import random # For generating ID code
uniqueID = "" # This main unit's unique ID code
try: # Returns exception if the file doesn't exist
  with open('/home/pi/HydroSoil/ID.txt') as file:
    uniqueID = file.readlines()
except: # Unique ID doesn't exist, generate one
  uniqueID = 'M' + str(random.randint(0,10)) + str(random.randint(0,10)) + str(random.randint(0,10)) + str(random.randint(0,10)) + str(random.randint(0,10))
  with open('/home/pi/HydroSoil/ID.txt', 'w') as file:
    file.writelines(uniqueID)
else: # Unique ID file exists, check for the code in it
  if len(uniqueID[0]) != 6 or uniqueID[0].startswith("M") == False: # If ID code is invalid generate one
    uniqueID = 'M' + str(random.randint(0,10)) + str(random.randint(0,10)) + str(random.randint(0,10)) + str(random.randint(0,10)) + str(random.randint(0,10))
    with open('/home/pi/HydroSoil/ID.txt', 'w') as file:
      file.writelines(uniqueID)
finally:
  uniqueID = uniqueID[0]

# Import OS & Subprocess for terminal commands
import subprocess
import os

# Import libraries
# Import GTK and dependencies for making/handling GUI
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, Gdk, GLib
from gi.repository.GdkPixbuf import Pixbuf

# Import wifi libraries for controlling the pi's WiFi and listing available networks
from wireless import Wireless # For connecting and connection status
wireless = Wireless()
from wifi import Cell, Scheme # For listing available networks
#print(Cell.all('wlan0'))

# Import time libraries to get and parse time
import datetime
import ntplib
client = ntplib.NTPClient()

#  Import requests and json to parse the weather forecast
import requests
import json
api_key = 'b0fbd0c6dfd34924a0266d204e4a5d14'
api_location = 'postal_code=5159'
api_call = 'https://api.weatherbit.io/v2.0/forecast/daily?' + api_location + '&days=6&key=' + api_key

# Import CSV for parsing csv data for the plant/crop types
import csv
from operator import itemgetter

# Import GPIO Zero for controlling solenoids
from gpiozero import LED
solenoid = LED(14)

# Set the working directory
os.chdir("/home/pi/HydroSoil")

# Variables and settings
Page = 1 # What page the GUI is on
nZones = 6 # The number of zones (6 without expansion kit)
curNewZone = 0 # The new zone that the user has currently selected on various dialogs
curPlantCrop= -1 # The current plant or crop the user has selected in the change plant/crop dialog
warningOpen = 0 # Whether the warning dialog is currently open
dateToday = 0 # The date today, used for updating the calendar when the day changes
sensBlacklist = "" # List of sensors that the user pressed "Cancel" when being asked to set it up
# Stored weather data for next 7 days
forecastData = [
    (0, 0, 0, 0, 0, 0, 0, 0, "", "", 0), # Layout:  date (date obj), max temp (int), min temp (int), humidity (int), rain (int), rain prob (int), gust speed (int), wind dir (str), uv index (int), description (str), weather code (int)
    (0, 0, 0, 0, 0, 0, 0, 0, "", "", 0),
    (0, 0, 0, 0, 0, 0, 0, 0, "", "", 0),
    (0, 0, 0, 0, 0, 0, 0, 0, "", "", 0),
    (0, 0, 0, 0, 0, 0, 0, 0, "", "", 0),
    (0, 0, 0, 0, 0, 0, 0, 0, "", "", 0)
]

# Start main code for class SoilSystemMain

class SoilSystemMain:

  # These first functions are called when a main menu item is clicked
  # They load up a whole different page
  
  def on_home_button(self, object, data=None):
    # Home button (third button on bottom menu)
    # This function loads up the home page
    global Page
    Page = 1
    PageTabs = self.builder.get_object("Content Tabs")
    PageTabs.set_current_page(0)
    self.builder.get_object('Title').set_title('Home')
    self.select_menu_icon("Home")
    
  def on_calendar_button(self, object, data=None):
    # Calendar button (first button on bottom menu)
    # This function loads up the calendar page
    global Page
    Page = 2
    PageTabs = self.builder.get_object("Content Tabs")
    PageTabs.set_current_page(1)
    self.builder.get_object('Title').set_title('Calendar')
    self.select_menu_icon("Calendar")
    
  def on_weather_button(self, object, data=None):
    # Weather forecast button (second button on bottom menu)
    # This function loads up the weather forecast page
    global Page
    Page = 3
    PageTabs = self.builder.get_object("Content Tabs")
    PageTabs.set_current_page(2)
    self.select_menu_icon("Weather")
    self.builder.get_object('Title').set_title('Weather Forecast')
    self.update_weather_page()
    
  def on_zones_button(self, object, data=None):
    # Irrigation zones button (fourth button on bottom menu)
    # This function loads up the irrigation zones page
    global Page
    Page = 4
    PageTabs = self.builder.get_object("Content Tabs")
    PageTabs.set_current_page(3)
    self.select_menu_icon("Zones")
    self.builder.get_object('Title').set_title('Irrigation Zones')
    self.update_zones()
    
  def on_settings_button(self, object, data=None):
    # Settings button (last button on bottom menu)
    # This function loads up the settings page
    global Page
    Page = 5
    self.builder.get_object("Settings Layout").set_current_page(0) # Go to main settings page
    PageTabs = self.builder.get_object("Content Tabs")
    PageTabs.set_current_page(4)
    self.builder.get_object('Title').set_title('Settings')
    self.select_menu_icon("Settings")
    
  def select_menu_icon(self, iconName="Home"):
    # Sets an icon (makes it blue) and deselects the others
    iconObject = iconName + " Icon"
    Icon = self.builder.get_object(iconObject)
    iconPath = "assets/" + iconName + " Sel.png"
    Icon.set_from_file(iconPath)
    if iconName != "Home":
      Icon = self.builder.get_object("Home Icon")
      Icon.set_from_file("assets/Home.png")
    if iconName != "Calendar":
      Icon = self.builder.get_object("Calendar Icon")
      Icon.set_from_file("assets/Calendar.png")
    if iconName != "Weather":
      Icon = self.builder.get_object("Weather Icon")
      Icon.set_from_file("assets/Weather.png")
    if iconName != "Zones":
      Icon = self.builder.get_object("Zones Icon")
      Icon.set_from_file("assets/Zones.png")
    if iconName != "Settings":
      Icon = self.builder.get_object("Settings Icon")
      Icon.set_from_file("assets/Settings.png")
  
  def on_setting(self, btn):
    # When one of the settings buttons are clicked on the settings page
    self.builder.get_object("Settings Layout").set_current_page(int(btn.get_name()))
    # Some pages also have special things that need to be done when opened e.g. start searching for WiFi networks
    curSettingsPage = int(btn.get_name())
    if curSettingsPage == 1:
      # Disable new sensor found message as it is already searching for new units
      # Start searching for new HydroUnits
      pass
    elif curSettingsPage == 2:
      # Set up GUI and add all info for zone configuration
      pass
    elif curSettingsPage == 3:
      # Start searching for WiFi networks
      pass
    elif curSettingsPage == 4:
      # Load in current location information
      pass
    elif curSettingsPage == 5:
      # Load in list of registered devices
      pass
    elif curSettingsPage == 7:
      # Load in device information
      pass
    elif curSettingsPage == 8:
      # Check for available updates
      self.builder.get_object('Update Text').set_text("Checking for updates...")
      latestData = requests.get('https://api.github.com/repos/BlaT2512/hydrOS/releases/latest').json()
      latestVersion = latestData['tag_name']
      latestNotes = latestData['body'].split('\r\n')
      latestType = latestData['body'].split('\r\n')[2]
      latestSize = latestData['body'].split('\r\n')[3][13:]
      with open('/home/pi/HydroSoil/version') as file:
        currentVersion = file.readlines()
      currentVersion = currentVersion[0]
      if currentVersion != latestVersion:
        self.builder.get_object('Update Text').set_text("hydrOS " + latestVersion + " is available!")
        self.builder.get_object('Update Desc').set_text("hydrOS " + latestVersion + " is ready to download. Click the button below to begin the download.\nDownload size: " + latestSize + "\n" + latestType)
        self.builder.get_object('Status Text Update').show()
        self.builder.get_object('Update Action').show()
        self.builder.get_object('Status Text Update').set_text("Status: Ready to download")
        self.builder.get_object('Update Action').set_label("Download Update")
        self.builder.get_object('Release Notes').set_text(latestNotes[0] + '\n\n' + '\n'.join(map(str, latestNotes[5:])))
        
      else:
        self.builder.get_object('Update Text').set_text("You have the latest release")
        self.builder.get_object('Update Desc').set_text("hydrOS " + currentVersion + " is the latest version.")
        self.builder.get_object('Status Text Update').hide()
        self.builder.get_object('Update Action').hide()
        self.builder.get_object('Release Notes').set_text(latestNotes[0] + '\n\n' + '\n'.join(map(str, latestNotes[5:])))
  
  def on_update_action(self, btn):
    # Called when install/download update button is pressed
    btn.set_sensitive(False)
    if btn.get_label() == "Download Update":
      # Download the new available update
      latestData = requests.get('https://api.github.com/repos/BlaT2512/hydrOS/releases/latest').json()
      latestVersion = latestData['tag_name']
      latestType = latestData['body'].split('\r\n')[2]
      latestSize = latestData['body'].split('\r\n')[3][13:]
      self.builder.get_object('Update Text').set_text("Downloading hydrOS " + latestVersion)
      self.builder.get_object('Update Desc').set_text("hydrOS " + latestVersion + " is downloading...\nDownload size: " + latestSize + "\n" + latestType)
      self.builder.get_object('Status Text Update').set_text("Status: Downloading...")
      self.builder.get_object('Update Action').set_sensitive(False)
      os.system("git clone -b '" + latestVersion + "' --single-branch --depth 1 https://github.com/BlaT2512/hydros.git /home/pi/HydroSoilNew")
      self.builder.get_object('Update Text').set_text("Ready to Install")
      self.builder.get_object('Update Desc').set_text("hydrOS " + latestVersion + " has been downloaded and is ready to install.\nThe HydroLauncher will be opened to install the update, and then a restart will automatically occur.")
      self.builder.get_object('Status Text Update').set_text("Status: Ready to install")
      self.builder.get_object('Update Action').set_label("Install Update & Restart")
      self.builder.get_object('Update Action').set_sensitive(True)
    else:
      # Install new available
      latestData = requests.get('https://api.github.com/repos/BlaT2512/hydrOS/releases/latest').json()
      latestVersion = latestData['tag_name']
      latestNotes = latestData['body'].split('\r\n')
      self.builder.get_object('Update Text').set_text("Preparing Installation...")
      self.builder.get_object('Update Desc').set_text("hydrOS " + latestVersion + " is about to be installed.\nPreparing this update will take up to 10 seconds...")
      self.builder.get_object('Status Text Update').set_text("Status: Preparing install...")
      self.builder.get_object('Update Action').set_sensitive(False)
      with open('/home/pi/HydroSoilNew/newupdate', 'w') as file:
        file.writelines(latestVersion + '\n' + latestNotes[0] + '\n\n' + '\n'.join(map(str, latestNotes[5:])))
      # Prepare for hydrOS to be terminated
      # Communicate with HydroLauncher and make it install update
      with open('/home/pi/HydroLauncher/updatenow', 'w') as file:
        file.writelines(latestVersion + '\n' + latestNotes[0] + '\n\n' + '\n'.join(map(str, latestNotes[5:])))
  
  def on_setup_next(self, btn):
    # When next button is clicked on intial setup on one of the pages
    print(int(btn.get_name()))
    if int(btn.get_name()) < 6:
      self.builder.get_object("Setup container").set_current_page(int(btn.get_name()))
    # Some pages also have special things that need to be done when opened e.g. start searching for WiFi networks
    curSetupPage = int(btn.get_name())
    if curSetupPage == 1:
      # Start searching for WiFi networks
      pass
    elif curSetupPage == 2:
      # Start searching for HydroUnit sensors
      pass
    elif curSetupPage == 6:
      # Finish setup and restart
      with open('/home/pi/HydroSoil/setupvalid', 'w') as file:
        file.writelines("\n")
      
      try: # Returns exception if the file doesn't exist
        with open('/home/pi/HydroSoil/settings.txt') as file:
          settingsData = file.readlines()
      except: # Settings doesn't exist, generate blank settings
        settingsData = '''lastclocksync=never
zone1setup=0
zone2setup=0
zone3setup=0
zone4setup=0
zone5setup=0
zone6setup=0
zone1=Automatic
zone2=Automatic
zone3=Automatic
zone4=Automatic
zone5=Automatic
zone6=Automatic
zone1program=
zone2program=
zone3program=
zone4program=
zone5program=
zone6program=
zone1cropf=
zone2cropf=
zone3cropf=
zone4cropf=
zone5cropf=
zone6cropf=
zone1crop=
zone2crop=
zone3crop=
zone4crop=
zone5crop=
zone6crop=
zone1rmoisture=0
zone2rmoisture=0
zone3rmoisture=0
zone4rmoisture=0
zone5rmoisture=0
zone6rmoisture=0
zone1lmoisture=0
zone2lmoisture=0
zone3lmoisture=0
zone4lmoisture=0
zone5lmoisture=0
zone6lmoisture=0
calweekstart=

        '''
        with open('/home/pi/HydroSoil/settings.txt', 'w') as file:
          file.writelines(settingsData)
      
      os.system('sudo reboot')
  
  def on_settings_radio(self, btn):
    # Runs when a radio button in settings state was changed
    if btn.get_active():
      if btn.get_name() == "Metric":
        # Set units to metrics
        pass
      elif btn.get_name() == "Imperial":
        # Set units to imperial
        pass
      elif btn.get_name() == "Sunday":
        # Set calendar week start to Sunday
        pass
      elif btn.get_name() == "Monday":
        # Set calendar week start to Monday
        pass
  
  def on_newupdate_close(self, btn):
    # Runs when the close button is pressed in the new features after update window
    self.builder.get_object("Toplevel").set_current_page(0)
    os.system('sudo rm /home/pi/HydroSoil/newupdate')
        
  def wifisig(self):
    # This function runs every second when and sets the WiFi Icon
    WifiIcon = self.builder.get_object("WiFi Status")
    wifistatus = wireless.current()
    if str(wifistatus) == "None":
      icon = Gio.ThemedIcon(name="network-wireless-offline-symbolic")
      WifiIcon.set_from_gicon(icon, Gtk.IconSize.BUTTON)
    else:
      icon = Gio.ThemedIcon(name="network-wireless-symbolic")
      WifiIcon.set_from_gicon(icon, Gtk.IconSize.BUTTON)
    return True
    
  def counter(self):
    global dateToday
    # This functions runs every second and sets the time in the top-left corner
    Time = self.builder.get_object("Time")
    #response = client.request('pool.ntp.org')
    #Time.set_text(time.strftime('%R',time.localtime(response.tx_time)))
    timeNow = datetime.datetime.now()
    if timeNow.hour > 12:
        nowHour = timeNow.hour - 12
        meridian = "pm"
    else:
        nowHour = timeNow.hour
        meridian = "am"
    Time.set_text(str(nowHour) + ":" + str(timeNow.minute) + " " + meridian)
    if dateToday != datetime.date.today():
      # Update the calendar if the day has changed
      dateToday = datetime.date.today()
      self.builder.get_object('Main Calendar').select_month(dateToday.month-1, dateToday.year)
      self.builder.get_object('Home Calendar').select_month(dateToday.month-1, dateToday.year)
      self.builder.get_object('Main Calendar').select_day(dateToday.day)
      self.builder.get_object('Home Calendar').select_day(dateToday.day)
      self.builder.get_object('Main Calendar').clear_marks()
      self.builder.get_object('Home Calendar').clear_marks()
      self.builder.get_object('Main Calendar').mark_day(dateToday.day)
      self.builder.get_object('Home Calendar').mark_day(dateToday.day)
      self.builder.get_object('Home Cal Text').set_text(self.generate_calendar_text(dateToday.year, dateToday.month-1, dateToday.day, False))
    # Return true for the function to continue
    return True
    
  def on_wifistatus_clicked(self, btn):
    #self.builder.get_object('WiFi Status Dialog').set_property('secondary_text','WiFi network \"Tourneur\" is connected.\nWeather data is successfully being recieved.\nTime server is connected for syncing.')
    #self.builder.get_object('WiFi Status Dialog').run()
    #self.builder.get_object('WiFi Status Dialog').hide()
    exit(0)
  
  def on_plantcrop_change(self, btn):
    global curPlantCrop, curNewZone
    # Get current settings data
    with open('/home/pi/HydroSoil/settings.txt') as file:
      settingsData = file.readlines()
    # If the zone has a current plant, select that
    plantCropCombo = self.builder.get_object('PlantCropDropdown')
    if settingsData[24+int(btn.get_name())][9:-1] != '=':
      # Plant has been set before, so select that plant and display it at the top
      self.builder.get_object('Current crop title').show()
      self.builder.get_object('Current crop text').show()
      self.builder.get_object('New crop text').show()
      self.builder.get_object('Current crop text').set_text(settingsData[18+int(btn.get_name())][11:-1])
      plantCropCombo.set_active(int(settingsData[24+int(btn.get_name())][10:-1]))
      self.builder.get_object('New crop title').set_text(settingsData[18+int(btn.get_name())][11:-1])
      curPlantCrop = int(settingsData[24+int(btn.get_name())][10:-1])
      with open("plant-crop-list.csv", newline='') as csvfile:
        csvparser = csv.reader(csvfile, delimiter=',')
        Tup1 = ()
        i = 0
        for Tup1 in csvparser:
          if i == curPlantCrop:
            self.builder.get_object('New crop title').set_text(str(Tup1[0]))
            self.builder.get_object('New crop text').set_text("Irrigation required moisture level (" + str(Tup1[1]) + "): " + str(Tup1[2]) + "%\nCritically low moisture level (" + str(Tup1[1]) + "): " + str(Tup1[3]) + "%")
          i += 1
        csvfile.closed
    else:
      # This is the first time setting the plant/crop type
      self.builder.get_object('Current crop title').hide()
      self.builder.get_object('Current crop text').hide()
      plantCropCombo.set_active(-1) # Set no plant to currently active
      self.builder.get_object('New crop title').set_text("No plant or crop selected")
      self.builder.get_object('New crop text').hide()
      curPlantCrop = -1
    # Set zone icon for the GUI
    self.builder.get_object('Plant Crop Icon').set_from_file("assets/Zone " + btn.get_name() + ".png")
    self.builder.get_object('Plant Crop Icon').set_name(btn.get_name())
    curNewZone = int(btn.get_name())
    # Show plant/crop chooser GUI
    self.builder.get_object('Plant or Crop Selector').resize(200, 200) # 200x200 pixels
    self.builder.get_object('Plant or Crop Selector').run()
  
  def on_plantcrop_combo(self, btn):
    global curPlantCrop, curNewZone
    curPlantCrop = btn.get_active()
    self.builder.get_object('New crop text').show()
    with open("plant-crop-list.csv", newline='') as csvfile:
      csvparser = csv.reader(csvfile, delimiter=',')
      Tup1 = ()
      i = 0
      for Tup1 in csvparser:
        if i == curPlantCrop:
          self.builder.get_object('New crop title').set_text(str(Tup1[0]))
          self.builder.get_object('New crop text').set_text("Irrigation required moisture level (" + str(Tup1[1]) + "): " + str(Tup1[2]) + "%\nCritically low moisture level (" + str(Tup1[1]) + "): " + str(Tup1[3]) + "%")
        i += 1
      csvfile.closed
  
  def on_changecrop_cancel(self, btn):
    self.builder.get_object('Plant or Crop Selector').hide()
    # Ignore all user input as they cancelled their edits
  
  def on_changecrop_save(self, btn):
    global curPlantCrop, curNewZone
    self.builder.get_object('Plant or Crop Selector').hide()
    # Save changes made by the user
    # First, read the current settings file into variable
    with open('/home/pi/HydroSoil/settings.txt') as file:
      settingsData = file.readlines()
    # Then make all modifications needed
    with open("plant-crop-list.csv", newline='') as csvfile:
      csvparser = csv.reader(csvfile, delimiter=',')
      Tup1 = ()
      i = 0
      for Tup1 in csvparser:
        if i == curPlantCrop:
          settingsData[18+curNewZone] = "zone" + str(curNewZone) + "cropf=" + str(Tup1[0]) + "\n"
          settingsData[24+curNewZone] = "zone" + str(curNewZone) + "crop=" + str(curPlantCrop) + "\n"
          settingsData[30+curNewZone] = "zone" + str(curNewZone) + "rmoisture=" + str(Tup1[2]) + "\n"
          settingsData[36+curNewZone] = "zone" + str(curNewZone) + "lmoisture=" + str(Tup1[3]) + "\n"
          self.builder.get_object('Crop Name Zone' + str(curNewZone)).set_text("Plant/crop: " + str(Tup1[0]))
          self.builder.get_object('New crop text').set_text("Irrigation required moisture level (" + str(Tup1[1]) + "): " + str(Tup1[2]) + "%\nCritically low moisture level (" + str(Tup1[1]) + "): " + str(Tup1[3]) + "%")
          break
        i += 1
      csvfile.closed
    # Finally, write the new settings
    with open('/home/pi/HydroSoil/settings.txt', 'w') as file:
      file.writelines(settingsData)
  
  def on_zone_edit(self, btn):
    # Get current settings data
    with open('/home/pi/HydroSoil/settings.txt') as file:
      settingsData = file.readlines()
    # Set up GUI for chosen zone
    self.builder.get_object('Program Edit Icon').set_from_file("assets/Zone " + btn.get_name() + ".png")
    self.builder.get_object('Program Edit Icon').set_name(btn.get_name())
    i = 1
    while i < 8:
      self.builder.get_object('Time Slider 1-' + str(i)).hide()
      i += 1
    i = 1
    while i < 8:
      self.builder.get_object('Time Slider 2-' + str(i)).hide()
      i += 1
    self.builder.get_object('Check Day 1').set_active(False)
    self.builder.get_object('Check Day 2').set_active(False)
    self.builder.get_object('Check Day 3').set_active(False)
    self.builder.get_object('Check Day 4').set_active(False)
    self.builder.get_object('Check Day 5').set_active(False)
    self.builder.get_object('Check Day 6').set_active(False)
    self.builder.get_object('Check Day 7').set_active(False)
    # Load up previous program if one has been set before
    if settingsData[12+int(btn.get_name())][12:-1] == "=":
      # Program has never been set before.
      self.builder.get_object('Current program title').hide()
      self.builder.get_object('Current program text').hide()
      self.builder.get_object('New program text').set_text("No days currently selected")
      self.builder.get_object('Save edit program').set_sensitive(False)
    else:
      # A previous program exists, load it
      self.builder.get_object('Current program title').show()
      self.builder.get_object('Current program text').show()
      i = 1
      while i < (len(settingsData[12+int(btn.get_name())][13:-1])-3)/14 + 1:
        curDay = settingsData[12+int(btn.get_name())][14+(i-1)*14]
        self.builder.get_object('Check Day ' + curDay).set_active(True)
        self.builder.get_object('Time 1-' + curDay).set_text(settingsData[12+int(btn.get_name())][16+(i-1)*14:21+(i-1)*14].replace(':',' : '))
        self.builder.get_object('Time 2-' + curDay).set_text(settingsData[12+int(btn.get_name())][22+(i-1)*14:27+(i-1)*14].replace(':',' : '))
        i += 1
      self.builder.get_object('Program Setting 1').set_active(int(settingsData[12+int(btn.get_name())][28+(i-2)*14:29+(i-2)*14]))
      self.builder.get_object('Program Setting 2').set_active(int(settingsData[12+int(btn.get_name())][29+(i-2)*14:30+(i-2)*14]))
      # Update the text for the preview of new schedule
      # Put the commonly used objects into variables (makes it much more readable and shorter)
      chkMonday = self.builder.get_object('Check Day 1')
      chkTuesday = self.builder.get_object('Check Day 2')
      chkWednesday = self.builder.get_object('Check Day 3')
      chkThursday = self.builder.get_object('Check Day 4')
      chkFriday = self.builder.get_object('Check Day 5')
      chkSaturday = self.builder.get_object('Check Day 6')
      chkSunday = self.builder.get_object('Check Day 7')
      newText = self.builder.get_object('New program text')
      # Generate description of this new program for the user
      genText = self.generate_program_description(chkMonday.get_active(), chkTuesday.get_active(), chkWednesday.get_active(), chkThursday.get_active(), chkFriday.get_active(), chkSaturday.get_active(), chkSunday.get_active(), self.builder.get_object('Time 1-1').get_text(), self.builder.get_object('Time 1-2').get_text(), \
      self.builder.get_object('Time 1-3').get_text(), self.builder.get_object('Time 1-4').get_text(), self.builder.get_object('Time 1-5').get_text(), self.builder.get_object('Time 1-6').get_text(), self.builder.get_object('Time 1-7').get_text(), \
      self.builder.get_object('Time 2-1').get_text(), self.builder.get_object('Time 2-2').get_text(), self.builder.get_object('Time 2-3').get_text(), self.builder.get_object('Time 2-4').get_text(), self.builder.get_object('Time 2-5').get_text(), \
      self.builder.get_object('Time 2-6').get_text(), self.builder.get_object('Time 2-7').get_text())
      self.builder.get_object('New program text').set_text(genText)
      self.builder.get_object('Current program text').set_text(genText)
      newText.set_line_wrap(True)
    
    self.builder.get_object('Edit Program Dialog').resize(430, 1) # 430px width, default height
    self.builder.get_object('Edit Program Dialog').run()

  def on_programedit_cancel(self, btn):
    self.builder.get_object('Edit Program Dialog').hide()
    # Ignore all user input as they cancelled their edits
  
  def on_programedit_save(self, btn):
    self.builder.get_object('Edit Program Dialog').hide()
    # Save the settings that the user chose
    # First, get the settings text file
    with open('/home/pi/HydroSoil/settings.txt') as file:
      settingsData = file.readlines()
    curZone = int(self.builder.get_object('Program Edit Icon').get_name())
    # Next, clear the current schedule for the zone we are editing
    settingsData[12+curZone] = "zone" + str(curZone) + "program="
    # Now check if each day was selected and if it was, add that day's data to the program
    i = 1
    while i < 8:
      if self.builder.get_object('Check Day ' + str(i)).get_active():
        settingsData[12+curZone] += "D" + str(i) + "S" + self.builder.get_object('Time 1-' + str(i)).get_text().replace(' : ', ':') + "L" + self.builder.get_object('Time 2-' + str(i)).get_text().replace(' : ', ':')
      i += 1
    settingsData[12+curZone] += "S"
    settingsData[12+curZone] += str(int(self.builder.get_object('Program Setting 1').get_active()))
    settingsData[12+curZone] += str(int(self.builder.get_object('Program Setting 2').get_active()))
    settingsData[12+curZone] += "\n"
    # Finally, write the new data to the settings file
    with open('/home/pi/HydroSoil/settings.txt', 'w') as file:
      file.writelines(settingsData)

  def on_programtime_updown(self, btn):
    hour, min = self.builder.get_object('Time ' + btn.get_name()[:3]).get_text().split(' : ')
    hour = int(hour)
    min = int(min)
    if btn.get_name()[4:] == "Up": # Up button
      if min == 45:
        min = 0
        hour += 1
      else:
        min += 15
      if hour == 24:
        hour = 0
      if hour == 0 and min == 0 and btn.get_name()[:1] == "2":
        hour = 0
        min = 15
    else: # Down button
      if min == 0:
        min = 45
        hour -= 1
      else:
        min -= 15
    if hour == -1:
      hour = 23
    if hour == 0 and min == 0 and btn.get_name()[:1] == "2":
      hour = 23
      min = 45
    min = "0" + str(min) if min < 10 else str(min)
    hour = "0" + str(hour) if hour < 10 else str(hour)
    self.builder.get_object('Time ' + btn.get_name()[:3]).set_text(hour + " : " + min)
    # Update the text for the preview of new schedule
    # Put the commonly used objects into variables (makes it much more readable and shorter)
    chkMonday = self.builder.get_object('Check Day 1')
    chkTuesday = self.builder.get_object('Check Day 2')
    chkWednesday = self.builder.get_object('Check Day 3')
    chkThursday = self.builder.get_object('Check Day 4')
    chkFriday = self.builder.get_object('Check Day 5')
    chkSaturday = self.builder.get_object('Check Day 6')
    chkSunday = self.builder.get_object('Check Day 7')
    newText = self.builder.get_object('New program text')
    # Generate description of this new program for the user
    newText.set_text(self.generate_program_description(chkMonday.get_active(), chkTuesday.get_active(), chkWednesday.get_active(), chkThursday.get_active(), chkFriday.get_active(), chkSaturday.get_active(), chkSunday.get_active(), self.builder.get_object('Time 1-1').get_text(), self.builder.get_object('Time 1-2').get_text(), \
    self.builder.get_object('Time 1-3').get_text(), self.builder.get_object('Time 1-4').get_text(), self.builder.get_object('Time 1-5').get_text(), self.builder.get_object('Time 1-6').get_text(), self.builder.get_object('Time 1-7').get_text(), \
    self.builder.get_object('Time 2-1').get_text(), self.builder.get_object('Time 2-2').get_text(), self.builder.get_object('Time 2-3').get_text(), self.builder.get_object('Time 2-4').get_text(), self.builder.get_object('Time 2-5').get_text(), \
    self.builder.get_object('Time 2-6').get_text(), self.builder.get_object('Time 2-7').get_text()))
    newText.set_line_wrap(True)
    self.builder.get_object('Edit Program Dialog').resize(430, 1)

  def on_programday_toggle(self, chkbox):
    if chkbox.get_active():
      self.builder.get_object('Time Slider 1-' + chkbox.get_name()).show()
      self.builder.get_object('Time Slider 2-' + chkbox.get_name()).show()
    else:
      self.builder.get_object('Time Slider 1-' + chkbox.get_name()).hide()
      self.builder.get_object('Time Slider 2-' + chkbox.get_name()).hide()
    # Update the text for the preview of new schedule
    # Put the commonly used objects into variables (makes it much more readable and shorter)
    chkMonday = self.builder.get_object('Check Day 1')
    chkTuesday = self.builder.get_object('Check Day 2')
    chkWednesday = self.builder.get_object('Check Day 3')
    chkThursday = self.builder.get_object('Check Day 4')
    chkFriday = self.builder.get_object('Check Day 5')
    chkSaturday = self.builder.get_object('Check Day 6')
    chkSunday = self.builder.get_object('Check Day 7')
    newText = self.builder.get_object('New program text')
    # Generate description of this new program for the user
    newText.set_text(self.generate_program_description(chkMonday.get_active(), chkTuesday.get_active(), chkWednesday.get_active(), chkThursday.get_active(), chkFriday.get_active(), chkSaturday.get_active(), chkSunday.get_active(), self.builder.get_object('Time 1-1').get_text(), self.builder.get_object('Time 1-2').get_text(), \
    self.builder.get_object('Time 1-3').get_text(), self.builder.get_object('Time 1-4').get_text(), self.builder.get_object('Time 1-5').get_text(), self.builder.get_object('Time 1-6').get_text(), self.builder.get_object('Time 1-7').get_text(), \
    self.builder.get_object('Time 2-1').get_text(), self.builder.get_object('Time 2-2').get_text(), self.builder.get_object('Time 2-3').get_text(), self.builder.get_object('Time 2-4').get_text(), self.builder.get_object('Time 2-5').get_text(), \
    self.builder.get_object('Time 2-6').get_text(), self.builder.get_object('Time 2-7').get_text()))
    newText.set_line_wrap(True)
    self.builder.get_object('Edit Program Dialog').resize(430, 1)
  
  def generate_program_description(self, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, Start1, Start2, Start3, Start4, Start5, Start6, Start7, Dur1, Dur2, Dur3, Dur4, Dur5, Dur6, Dur7):
    if Monday == False and Tuesday == False and Wednesday == False and Thursday == False and Friday == False and Saturday == False and Sunday == False: # No days are selected
      genText = "No days currently selected"
      self.builder.get_object('Save edit program').set_sensitive(False)
    else:
      genText = "Every week on "
      self.builder.get_object('Save edit program').set_sensitive(True)
      if Monday:
        endTime = self.add_times(Start1, Dur1)
        genText += "Monday (from " + Start1.replace(' : ', ':') + " to " + endTime + "), "
      if Tuesday:
        endTime = self.add_times(Start2, Dur2)
        genText += "Tuesday (from " + Start2.replace(' : ', ':') + " to " + endTime + "), "
      if Wednesday:
        endTime = self.add_times(Start3, Dur3)
        genText += "Wednesday (from " + Start3.replace(' : ', ':') + " to " + endTime + "), "
      if Thursday:
        endTime = self.add_times(Start4, Dur4)
        genText += "Thursday (from " + Start4.replace(' : ', ':') + " to " + endTime + "), "
      if Friday:
        endTime = self.add_times(Start5, Dur5)
        genText += "Friday (from " + Start5.replace(' : ', ':') + " to " + endTime + "), "
      if Saturday:
        endTime = self.add_times(Start6, Dur6)
        genText += "Saturday (from " + Start6.replace(' : ', ':') + " to " + endTime + "), "
      if Sunday:
        endTime = self.add_times(Start7, Dur7)
        genText += "Sunday (from " + Start7.replace(' : ', ':') + " to " + endTime + "), "
      genText = '.'.join(genText.rsplit(', ', 1)) # Replace last ', ' with a full stop
      genText = ' and '.join(genText.rsplit(', ', 1)) # Replace the new last ', ' with the word 'and'
    return genText
  
  def add_times(self, time1, time2):
    h1, m1 = time1.split(' : ')
    h2, m2 = time2.split(' : ')
    h1 = int(h1)
    m1 = int(m1)
    h2 = int(h2)
    m2 = int(m2)
    h3 = h1 + h2
    m3 = m1 + m2
    if m3 > 60:
      m3 -= 60
      h3 += 1
    if h3 > 23:
      h3 -= 24
      m3 = "0" + str(m3) if m3 < 10 else str(m3)
      h3 = "0" + str(h3) if h3 < 10 else str(h3)
      return h3 + ":" + m3 + " next day"
    else:
      m3 = "0" + str(m3) if m3 < 10 else str(m3)
      h3 = "0" + str(h3) if h3 < 10 else str(h3)
      return h3 + ":" + m3

  def on_zonemode_change(self, btn):
    if btn.get_active():
      with open('/home/pi/HydroSoil/settings.txt') as file:
        settingsData = file.readlines()
      if btn.get_label() == "Automatic - recommended":
        settingsData[6+int(btn.get_name())] = "zone" + btn.get_name() + "=Automatic\n"
      elif btn.get_label() == "Program":
        settingsData[6+int(btn.get_name())] = "zone" + btn.get_name() + "=Program\n"
      else:
        settingsData[6+int(btn.get_name())] = "zone" + btn.get_name() + "=Manual\n"
        with open('/home/pi/HydroSoil/livedata.txt') as file:
          liveData = file.readlines()
        liveData[-1+int(btn.get_name())] = "zone" + btn.get_name() + "onf=\n"
        with open('/home/pi/HydroSoil/livedata.txt', 'w') as file:
          file.writelines(liveData)
        self.builder.get_object('Manual Switch Zone' + btn.get_name()).set_active(False)
      with open('/home/pi/HydroSoil/settings.txt', 'w') as file:
        file.writelines(settingsData)
      self.update_zone_controls()
  
  def on_zone_manual(self, switch, state):
    with open('/home/pi/HydroSoil/livedata.txt') as file:
      liveData = file.readlines()
    if state: # If the button is now active
      liveData[-1+int(switch.get_name())] = "zone" + switch.get_name() + "onf=, running\n"
    else:
      liveData[-1+int(switch.get_name())] = "zone" + switch.get_name() + "onf=\n"
    with open('/home/pi/HydroSoil/livedata.txt', 'w') as file:
      file.writelines(liveData)
  
  def update_zone_controls(self):
    with open('/home/pi/HydroSoil/settings.txt') as file:
      settingsData = file.readlines()
    # Disable (grey out) controls for modes that aren't enabled on zones page
    i = 1
    while i < nZones+1:
      if settingsData[6+i][6:-1] == "Automatic":
        self.builder.get_object('Manual Switch Zone' + str(i)).set_sensitive(False)
        self.builder.get_object('Edit Routine Zone' + str(i)).set_sensitive(False)
      elif settingsData[6+i][6:-1] == "Program":
        self.builder.get_object('Manual Switch Zone' + str(i)).set_sensitive(False)
        self.builder.get_object('Edit Routine Zone' + str(i)).set_sensitive(True)
      else:
        self.builder.get_object('Manual Switch Zone' + str(i)).set_sensitive(True)
        self.builder.get_object('Edit Routine Zone' + str(i)).set_sensitive(False)
      i += 1

  def on_calendar_day(self, cal):
    # Called when the user changes day on the home screen calendar
    calYear, calMonth, calDay = cal.get_date()
    self.builder.get_object('Home Cal Text').set_text(self.generate_calendar_text(calYear, calMonth, calDay, False))

  def generate_calendar_text(self, year, month, day, routines):
    with open('/home/pi/HydroSoil/settings.txt') as file:
      settingsData = file.readlines()
    # Creates description of the provided day for the calendar
    procDate = datetime.date(year, month+1, day)
    procWeekno = procDate.isoweekday()
    procWeekday = procDate.strftime('%A')
    procMonth = procDate.strftime('%B')

    description = procWeekday + ", " + str(day) + " " + procMonth + " " + str(year) + "\n"

    if (procDate - datetime.date.today()).days < 6 and (procDate - datetime.date.today()).days > -1:
      # Weather data is available
      description += "Forecast: " + str(forecastData[(procDate - datetime.date.today()).days][1]) + "°C (" + str(forecastData[(procDate - datetime.date.today()).days][4]) + "mm Rain)"
    else:
      description += "Weather data not available"
    
    return description
  
  def calendarDetail(self, cal, year, month, day):
    with open('/home/pi/HydroSoil/settings.txt') as file:
      settingsData = file.readlines()
    # Creates mini description of provided day for main calendar details underneath numbers
    procDate = datetime.date(year, month+1, day)
    procWeekno = procDate.isoweekday()
    procWeekday = procDate.strftime('%A')
    procMonth = procDate.strftime('%B')
    description = ""
    
    zoneNo = 1
    todayRoutineNo = 0
    while zoneNo < nZones+1:
      i = 1
      while i < (len(settingsData[12+zoneNo][13:-1])-3)/14 + 1:
        curDay = settingsData[12+zoneNo][14+(i-1)*14]
        if int(curDay) == procWeekno and settingsData[6+zoneNo][6:-1] == "Program": # If this day in the schedule is the calendar day selected and the zone is on program mode
          curDayStart = settingsData[12+zoneNo][16+(i-1)*14:21+(i-1)*14].replace(':',' : ')
          curDayLen = settingsData[12+zoneNo][22+(i-1)*14:27+(i-1)*14].replace(':',' : ')
          curDayEnd = self.add_times(curDayStart, curDayLen)
          curDayStart = curDayStart.replace(' : ', ':')
          todayRoutineNo += 1
          
        i += 1
      zoneNo += 1
    
    if todayRoutineNo == 1:
      description += "1 Routine"
    elif todayRoutineNo > 1:
      description += str(todayRoutineNo) + " Routines"

    if (procDate - datetime.date.today()).days < 6 and (procDate - datetime.date.today()).days > -1:
      # Weather data is available
      description += "\n" + str(forecastData[(procDate - datetime.date.today()).days][1]) + "°C (" + str(forecastData[(procDate - datetime.date.today()).days][4]) + "mm Rain)"
    
    return description
  
  def on_calendar_month(self, cal):
    calYear, calMonth, calDay = cal.get_date()
    calMonth = calMonth+1
    if calYear != datetime.date.today().year or calMonth != datetime.date.today().month:
      cal.clear_marks()
    else:
      cal.mark_day(datetime.date.today().day)
  
  def forecast(self):
    # This function runs every half an hour and collect/parses weather data from the internet
    # Make the JSON Call to the Weatherbit server
    json_data = requests.get(api_call).json()
    
    # Iterates through each item in json_data (each of the 6 days)
    for item in json_data['data']:
      # Get the date of this item
      date = item['valid_date']

      itemDate = datetime.date(int(date[:4]), int(date[5:7]), int(date[8:10]))
      todayDate = datetime.date.today()
      diff = str(itemDate - todayDate)
      # Get different required values from JSON to fill array
      forecastData[int(diff[0])] = (itemDate, "%.0f" % item['max_temp'], "%.0f" % item['min_temp'], item['rh'], "%.1f" % item['precip'], item['pop'], "%.0f" % item['wind_gust_spd'], item['wind_cdir'], "%.0f" % item['uv'], item['weather']['description'], item['weather']['code'])
    return True
  
  def check_program_due(self, zoneNo):
    # Checks whether a zone's program needs to run right now
    with open('/home/pi/HydroSoil/settings.txt') as file:
      settingsData = file.readlines()
    
    i = 1
    while i < (len(settingsData[12+zoneNo][13:-1])-3)/14 + 1:
      curDay = settingsData[12+zoneNo][14+(i-1)*14]

      if int(curDay) == int(datetime.datetime.today().isoweekday()): # If this day in the schedule is today
        curDayStart = settingsData[12+zoneNo][16+(i-1)*14:21+(i-1)*14].replace(':',' : ')
        curDayLen = settingsData[12+zoneNo][22+(i-1)*14:27+(i-1)*14].replace(':',' : ')
        curDayEnd = self.add_times(curDayStart, curDayLen)
        curDayStart = curDayStart.replace(' : ', ':')
        curDayNow = datetime.datetime.now().time()

        if curDayNow >= datetime.time(int(curDayStart[0:2]), int(curDayStart[4:6])) and curDayNow < datetime.time(int(curDayStart[0:2]), int(curDayStart[4:6])):
          return True
        
      i += 1
    return False
  
  def critical_warning(self, onoff, zoneNo):
    global warningOpen
    # Turns warning notification on or off for a zone
    with open('/home/pi/HydroSoil/settings.txt') as file:
      settingsData = file.readlines()
    
    if onoff: # Turns warning notification on
      if warningOpen: # If warning dialog is already open
        warnText = self.builder.get_object('Warning Text').get_text()
        if ("Zone " + str(zoneNo) in warnText) and ("Zone " + str(zoneNo) + " (" + settingsData[18+zoneNo][11:-1] + ")" not in warnText): # If the crop or plant has changed for this zone
          warnText == "The soil moisture level of the plant's in\nsome zone's is critically low:\n"
          warnText += ", Zone " + str(zoneNo) + " (" + settingsData[18+zoneNo][11:-1] + ")"
          self.builder.get_object('Warning Text').set_text(warnText)
        elif "Zone " + str(zoneNo) + " (" + settingsData[18+zoneNo][11:-1] + ")" not in warnText: # The zone is not currently in the warning dialog
          warnText += ", Zone " + str(zoneNo) + " (" + settingsData[18+zoneNo][11:-1] + ")"
          self.builder.get_object('Warning Text').set_text(warnText)
      
      else: # If warning dialog if not open at the moment
        warnText = "The soil moisture level of the plant's in\nsome zone's is critically low:\n"
        warnText += "Zone " + str(zoneNo) + " (" + settingsData[18+zoneNo][11:-1] + ")"
        self.builder.get_object('Warning Text').set_text(warnText)
        self.builder.get_object('Warning Dialog').show()
        self.builder.get_object('Warning Dialog').set_modal(False)
        warningOpen = 1
    
    else: # Turn warning notification off
      if warningOpen: # The warning is currently open
        self.builder.get_object('Warning Dialog').hide()
        warningOpen = 0
        warnText = "The soil moisture level of the plant's in\nsome zone's is critically low:\n"
        self.builder.get_object('Warning Text').set_text(warnText)

  def sensor_update(self):
    global nZones, curNewZone, sensBlacklist
    # This function runs every second and turn on required irrigation, also checks if a new sensor was detected
    # Gather soil moisture data from sensors and plant/crop data
    with open('/home/pi/HydroSoil/livedata.txt') as file:
      liveData = file.readlines()
    with open('/home/pi/HydroSoil/settings.txt') as file:
      settingsData = file.readlines()
    
    # HydroIrrigate Logic v2 brings more stability and smarter logic for your irrigation than ever before. It fixes multiple bugs from v1 and brinds a more intuitive and smart dessign then before.
    # How the logic for each of the modes work:
    # Automatic mode - If the soil value is 5% or more under what it should be, it will be watered until it is 5% over what it should be (the minimum) unless there will be more than 10mm of rain tomorrow.
    # Program mode - The user schedules when the plant should be watered (e.g. Every Tuesday & Thursday from 15:00 to 15:30). They can also choose to only carry out the program if the plant needs water (semi-automatic)
    # Manual - The user can switch each zone on or off whenever they like with a simple slider.
    # There is a critically low water level for each plant/crop. This is a dangerously low amount of water for the plant.
    # How this is handled - In Automatic mode - It will water the plant even if there is going to be more than 10mm rain tomorrow.
    # In program mode - The user can set whether the plant should be watered or if they just recieve a warning notification.
    # In manual mode - The user receives a warning notification.
    
    # Start of the HydroIrrigate Logic v2 Code
    # Create the repeat loop that runs for every zone
    i = 1
    while i < nZones+1:
      if settingsData[i][11:-1] != '0': # Only run this if the zone is actually set up

        # SECTION 1: VARIABLE DECLARATION
        zoneMode = settingsData[6+i][6:-1] # The mode of the current zone
        zoneSetup = settingsData[i][11:-1] # Used to decide whether the current zone's sensor is set up
        zoneMoisture = int(liveData[17+i][14:-1]) # Moisture level of current zone
        zoneRequired = int(settingsData[30+i][15:-1]) # Required moisture level of current zone
        zoneLow = int(settingsData[36+i][15:-1]) # Critically low moisture level of current zone
        rainTomorrow = int(round(float(forecastData[1][4]))) # Rain in mm from the forecast for tomorrow
        zoneRunning = liveData[-1+i][9:-1] # Used to decide whether the current zone's irrigation is running
        zoneConnected = liveData[5+i][10:-1] # Whether the current zone is connected
        try: # Raises ValueError if there is no program
          zoneAlwaysRun = int(settingsData[12+i][-3:-2]) # Whether the zone's program should always run or only when needed
          zoneWarning = 1-int(settingsData[12+i][-2:-1]) # Whether the zone's program is set to give warning notification or automatically water at critical level
          zoneProgram = settingsData[12+i][13:-1] # The zone's program schedule
        except:
          pass # This doesn't matter as obviously the zone isn't set to program mode
        zoneLastActivity = liveData[23+i][17:-1] # Last time that data was receieved from the zone's sensor
        zoneProgramDue = self.check_program_due(i) # Whether the zone's program needs to run right now

        # SECTION 2a: AUTOMATIC MODE LOGIC. This section decides whether to irrigate was the zone is set to automatic
        if zoneMode == "Automatic": # If this zone is automatic

          self.critical_warning(0, i) # Turn warning notification off

          if zoneMoisture > zoneLow+7: # If the zone is at normal level
            if zoneMoisture < zoneRequired-7 and zoneRunning != ", running" and zoneConnected == "Connected" and rainTomorrow < 10: # If the zone needs watering, isn't being watered, is connected and there will be less than 10mm rain tomorrow
              # Water plant, it needs watering
              zoneRunning = ", running"
              solenoid.on()
            
            elif (zoneMoisture >= zoneRequired+5 and zoneRunning == ", running") or zoneConnected != "Connected" or rainTomorrow >= 10: # If the zone doesn't need watering, isn't connected, or there will be over 10mm rain tomorrow
              # Stop watering plant, it doesn't need it
              zoneRunning = ""
              solenoid.off()
            
          elif zoneMoisture > zoneLow: # If the zone has just come to normal level
            if zoneRunning != ", running" and zoneConnected == "Connected": # If zone isn't running and is connected
              # Water plant, it needs watering
              zoneRunning = ", running"
              solenoid.on()

            elif zoneRunning == ", running" and zoneConnected != "Connected": # If zone is running but not connected
              # Stop watering plant, it doesn't need it
              zoneRunning = ""
              solenoid.off()
          
          elif zoneMoisture <= zoneLow: # If the zone is at critical level
            if zoneRunning != ", running" and zoneConnected == "Connected": # If zone isn't running and is connected
              # Water plant, it needs watering
              zoneRunning = ", running"
              solenoid.on()

            elif zoneRunning == ", running" and zoneConnected != "Connected": # If zone is running but not connected
              # Stop watering plant, it doesn't need it
              zoneRunning = ""
              solenoid.off()
        
        # SECTION 2b: PROGRAM MODE LOGIC. This section decides whether to irrigate when the zone is set to program mode.
        elif zoneMode == "Program": # If this zone is program

          if zoneMoisture > zoneLow: # If the zone is at normal level
            self.critical_warning(0, i) # Turn warning notification off

            if zoneProgramDue and zoneRunning != ", running" and zoneConnected == "Connected" and (zoneAlwaysRun or zoneMoisture < zoneRequired): # If zone program is due, isn't running, is connected and is set to always run or needs to run
              # Water plant, it needs watering
              zoneRunning = ", running"
              solenoid.on()
            
            elif zoneRunning == ", running" and (zoneProgramDue == 0 or zoneConnected != "Connected"): # If zone is running and doesn't need to or isn't connected
              # Stop watering plant, it doesn't need it
              zoneRunning = ""
              solenoid.off()
          
          else: # If the zone is at critically low level

            if zoneWarning == 0 and zoneRunning != ", running" and zoneConnected == "Connected": # If the zone is set to automatically run at critically low level, connected and not running
              # Water plant, it needs watering
              zoneRunning = ", running"
              self.critical_warning(0, i) # Turn warning notification off
              solenoid.on()
            
            elif zoneProgramDue and zoneRunning != ", running" and zoneConnected == "Connected": # If the zone program is due ant is is not running and connected
              # Water plant, it needs watering
              zoneRunning = ", running"
              self.critical_warning(0, i) # Turn warning notification off
              solenoid.on()
            
            elif zoneWarning and zoneRunning != ", running" and zoneConnected == "Connected": # If the zone is connected and not running, and user requested critical level warning notification
              # Give the user a warning notification
              self.critical_warning(1, i)
            
            elif zoneRunning == ", running" and (zoneProgramDue == 0 or zoneConnected != "Connected") and zoneWarning: # If the zone program has finished and it is being watered, or not connected
              # Stop watering plant, it doesn't need it
              zoneRunning = ""
              self.critical_warning(0, i) # Turn warning notification off
              solenoid.off()
            
            else:
              self.critical_warning(0, i) # Turn warning notification off
        
        # SECTION 2c: MANUAL MODE LOGIC. This section turns off irrigation when manual sensor is disconnected, and sends warning at critical level for manual mode.
        else: # If this zone is manual mode
          
          if zoneMoisture > zoneLow: # If the zone is at normal level
            self.critical_warning(0, i) # Turn warning notification off

            if zoneRunning == ", running" and zoneConnected != "Connected": # If the zone is running but not connected
              # Stop watering plant, it doesn't need it
              zoneRunning = ""
              solenoid.off()
          
          else: # If the zone is at critically low level
            
            if zoneRunning != ", running" and zoneConnected == "Connected": # If the zone isn't running and connected
              # Give the user a warning notification
              self.critical_warning(1, i)
              
            elif zoneRunning == ", running" and zoneConnected != "Connected": # If the zone is running but not connected
              # Stop watering plant, it doesn't need it
              zoneRunning = ""
              self.critical_warning(0, i) # Turn warning notification off
              solenoid.off()
            
            else:
              self.critical_warning(0, i) # Turn warning notification off
        
        # SECTION 3: FINISH UP. Write changed values back to the settings file
        liveData[-1+i] = "zone" + str(i) + "onf=" + str(zoneRunning) + "\n"
        with open('/home/pi/HydroSoil/livedata.txt', 'w') as file:
          file.writelines(liveData)
      i += 1
    
    # This functions also checks for new sensors, and dispalys GUI if one was detected
    if liveData[30][12:-1] != '0':
      newCode = liveData[30][13:-1]
      newType = liveData[30][12:13]
      if newType == 'S':
        newType = "standard"
      else:
        newType = "premium"
      # Set up the dropdown box for the chosen zone
      i = 1
      s = 0
      while i < nZones+1:
        if settingsData[i][11:-1] == '0':
          # Zone is not setup so this is an option for registering
          self.builder.get_object('NewZone'+ str(i)).set_sensitive(True)
          s += 1
          if s == 1:
            # This is the first available zone, so select it
            self.builder.get_object('NewZone' + str(i)).set_active(True)
            self.builder.get_object('Register Confirm Text').set_text("This sensor will be registered as Zone " + str(i))
            curNewZone = i
        else:
          self.builder.get_object('NewZone'+ str(i)).set_sensitive(False)
        i += 1
        # Change text to correct information
        self.builder.get_object('Register Info Text').set_text("A new " + newType + " soil measure sensor has been detected (ID code " + newCode + ").\nTo set it up and connect it, choose a zone below to associate it with, and then choose it's program settings on the Zones page.\nIf you don't want to set up this sensor, press Cancel.")
        self.builder.get_object('Register Info Text').set_line_wrap(True)
        # Show the dialog GUI
        self.builder.get_object('Connect New Sensor').resize(1, 1)
        self.builder.get_object('Connect New Sensor').run()
  
  def on_newzone_toggle(self, btn):
    global curNewZone
    # Called when a different zone radio button is clicked for the new sensor detected dialog
    if btn.get_active():
      self.builder.get_object('Register Confirm Text').set_text("The sensor will be registered as Zone " + btn.get_name())
      self.builder.get_object('New Zone Icon').set_from_file("assets/Zone " + btn.get_name() + ".png")
      curNewZone = int(btn.get_name())
  
  def on_newsensor_cancel(self, btn):
    # User didn't want to register the new selected zone
    with open('/home/pi/HydroSoil/livedata.txt') as file:
      liveData = file.readlines()
    liveData[30] = "newdetected=0\n"
    with open('/home/pi/HydroSoil/livedata.txt', 'w') as file:
      file.writelines(liveData)
    self.builder.get_object('Connect New Sensor').hide()
  
  def on_newsensor_connect(self, btn):
    global curNewZone
    # User wants to connect the new sensor
    with open('/home/pi/HydroSoil/settings.txt') as file:
      settingsData = file.readlines()
    with open('/home/pi/HydroSoil/livedata.txt') as file:
      liveData = file.readlines()
    print(curNewZone)
    settingsData[curNewZone] = "zone" + str(curNewZone) + "setup=" + liveData[30][12:13] + liveData[30][13:-1] + "\n"
    liveData[30] = "newdetected=0\n"
    self.builder.get_object('Connect New Sensor').hide()
    with open('/home/pi/HydroSoil/livedata.txt', 'w') as file:
      file.writelines(liveData)
    with open('/home/pi/HydroSoil/settings.txt', 'w') as file:
      file.writelines(settingsData)
    
  def second_routine(self):
    # This routine runs every second and does tasks required
    self.wifisig() # Updates the WiFi icon depending if the unit has icon or not
    self.counter() # Updates the clock every second
    self.update_zones() # Collect live data incoming from the sensors and update zones information
    self.sensor_update() # Collect soil moisture data and turn import paho.mqtt.client as mqtton irrigation accordingly, also looks for new sensors
    return True
  
  def update_zones(self):
    global nZones
    # This function runs every second and updates the information about all the zones & zone icons
    # Get all the settings and live data
    with open('/home/pi/HydroSoil/settings.txt') as file:
      settingsData = file.readlines()
    with open('/home/pi/HydroSoil/livedata.txt') as file:
      liveData = file.readlines()
    
    # Update all the info - modular
    i = 1
    while i < nZones+1:
      try: # The command below gives an exception when the file is being written to at the same time
        self.builder.get_object("Status Zone" + str(i)).set_text("Zone " + str(i) + " - " + liveData[5+i][10:-1])
      except: # The error is OK because this command runs every second, so it will get updated the next second
          pass
      
      if liveData[5+i][10:-1] == "Connected":
        self.builder.get_object("Home Status Zone" + str(i)).set_from_icon_name("bluetooth-online", Gtk.IconSize.LARGE_TOOLBAR)
      else:
        self.builder.get_object("Home Status Zone" + str(i)).set_from_icon_name("bluetooth-offline", Gtk.IconSize.LARGE_TOOLBAR)
        self.builder.get_object("Manual Switch Zone" + str(i)).set_active(False)
        self.builder.get_object("Manual Switch Zone" + str(i)).set_sensitive(False)

      self.builder.get_object("Home Overview Zone" + str(i)).set_text("— " + liveData[5+i][10:-1] + liveData[-1+i][9:-1] + ". " + settingsData[6+i][6:-1] + " mode.")

      if settingsData[6+i][6:-1] == "Automatic":
        self.builder.get_object("Button1 Zone" + str(i)).set_active(True)
        self.builder.get_object("Button2 Zone" + str(i)).set_active(False)
        self.builder.get_object("Button3 Zone" + str(i)).set_active(False)
      elif settingsData[6+i][6:-1] == "Program":
        self.builder.get_object("Button1 Zone" + str(i)).set_active(False)
        self.builder.get_object("Button2 Zone" + str(i)).set_active(True)
        self.builder.get_object("Button3 Zone" + str(i)).set_active(False)
      else:
        self.builder.get_object("Button1 Zone" + str(i)).set_active(False)
        self.builder.get_object("Button2 Zone" + str(i)).set_active(False)
        self.builder.get_object("Button3 Zone" + str(i)).set_active(True)
      if int(liveData[12][9:-1]) + int(liveData[13][9:-1]) + int(liveData[14][9:-1]) + int(liveData[15][9:-1]) + int(liveData[16][9:-1]) + int(liveData[17][9:-1]) == 1:
        self.builder.get_object("Home Text").set_text("— All systems OK, " + str(int(liveData[12][9:-1]) + int(liveData[13][9:-1]) + int(liveData[14][9:-1]) + int(liveData[15][9:-1]) + int(liveData[16][9:-1]) + int(liveData[17][9:-1])) + " sensor connected.")
      else:
        self.builder.get_object("Home Text").set_text("— All systems OK, " + str(int(liveData[12][9:-1]) + int(liveData[13][9:-1]) + int(liveData[14][9:-1]) + int(liveData[15][9:-1]) + int(liveData[16][9:-1]) + int(liveData[17][9:-1])) + " sensors connected.")
          
      # Set zone status icons in the top-right corner - modular
      if settingsData[6+i][6:-1] != "Automatic":
        if liveData[-1+i][9:-1] == ", running":
          self.builder.get_object("Icon Zone" + str(i)).set_from_file("assets/Zone "  + str(i) + " - Manual On.png")
          self.builder.get_object("Home Icon Zone" + str(i)).set_from_file("assets/Zone "  + str(i) + " - Manual On.png")
          self.builder.get_object("Zone"  + str(i) + " Status").set_from_file("assets/Zone "  + str(i) + " - Manual On.png")
        else:
          self.builder.get_object("Icon Zone" + str(i)).set_from_file("assets/Zone "  + str(i) + " - Manual.png")
          self.builder.get_object("Home Icon Zone" + str(i)).set_from_file("assets/Zone "  + str(i) + " - Manual.png")
          self.builder.get_object("Zone"  + str(i) + " Status").set_from_file("assets/Zone "  + str(i) + " - Manual.png")
      else:
        if liveData[-1+i][9:-1] == ", running":
          self.builder.get_object("Icon Zone" + str(i)).set_from_file("assets/Zone "  + str(i) + " On.png")
          self.builder.get_object("Home Icon Zone" + str(i)).set_from_file("assets/Zone "  + str(i) + " On.png")
          self.builder.get_object("Zone"  + str(i) + " Status").set_from_file("assets/Zone "  + str(i) + " On.png")
        else:
          self.builder.get_object("Icon Zone" + str(i)).set_from_file("assets/Zone "  + str(i) + ".png")
          self.builder.get_object("Home Icon Zone" + str(i)).set_from_file("assets/Zone "  + str(i) + ".png")
          self.builder.get_object("Zone"  + str(i) + " Status").set_from_file("assets/Zone "  + str(i) + ".png")
    
      i += 1
  
  def update_weather_page(self):
    # This function updates the weather information on the weather page and home page - modular
    i = 1
    while i < 7: # Repeat 6 times
      if (i == 1):
        if forecastData[i-1][10] == 900:
          self.builder.get_object("Overview Day" + str(i)).set_text("Today - Rain")
          self.builder.get_object("Home2 Day" + str(i)).set_text("Today - " + str(forecastData[i-1][1]) + "°C")
        elif forecastData[i-1][10] < 300:
          self.builder.get_object("Overview Day" + str(i)).set_text("Today - Thunderstorm")
          self.builder.get_object("Home2 Day" + str(i)).set_text("Today - " + str(forecastData[i-1][1]) + "°C")
        else:
          self.builder.get_object("Overview Day" + str(i)).set_text("Today - " + forecastData[i-1][9])
          self.builder.get_object("Home2 Day" + str(i)).set_text("Today - " + str(forecastData[i-1][1]) + "°C")
      elif (i == 2):
        if forecastData[i-1][10] == 900:
          self.builder.get_object("Overview Day" + str(i)).set_text("Tomorrow - Rain")
          self.builder.get_object("Home2 Day" + str(i)).set_text("Tomorrow - " + str(forecastData[i-1][1]) + "°C")
        elif forecastData[i-1][10] < 300:
          self.builder.get_object("Overview Day" + str(i)).set_text("Tomorrow - Thunderstorm")
          self.builder.get_object("Home2 Day" + str(i)).set_text("Tomorrow - " + str(forecastData[i-1][1]) + "°C")
        else:
          self.builder.get_object("Overview Day" + str(i)).set_text("Tomorrow - " + forecastData[i-1][9])
          self.builder.get_object("Home2 Day" + str(i)).set_text("Tomorrow - " + str(forecastData[i-1][1]) + "°C")
      else:
        if forecastData[i-1][10] == 900:
          self.builder.get_object("Overview Day" + str(i)).set_text(forecastData[i-1][0].strftime('%A') + " - Rain")
          self.builder.get_object("Home2 Day" + str(i)).set_text(forecastData[i-1][0].strftime('%A') + " - " + str(forecastData[i-1][1]) + "°C")
        elif forecastData[i-1][10] < 300:
          self.builder.get_object("Overview Day" + str(i)).set_text(forecastData[i-1][0].strftime('%A') + " - Thunderstorm")
          self.builder.get_object("Home2 Day" + str(i)).set_text(forecastData[i-1][0].strftime('%A') + " - " + str(forecastData[i-1][1]) + "°C")
        else:
          self.builder.get_object("Overview Day" + str(i)).set_text(forecastData[i-1][0].strftime('%A') + " - " + forecastData[i-1][9])
          self.builder.get_object("Home2 Day" + str(i)).set_text(forecastData[i-1][0].strftime('%A') + " - " + str(forecastData[i-1][1]) + "°C")
      self.builder.get_object("Max Day" + str(i)).set_text(str(forecastData[i-1][1]) + "°C")
      self.builder.get_object("Min Day" + str(i)).set_text("Minimum " + str(forecastData[i-1][2]) + "°C")
      self.builder.get_object("Humidity Day" + str(i)).set_text("Humidity - " + str(forecastData[i-1][3]) + "%")
      self.builder.get_object("Rain Day" + str(i)).set_text("Rain - " + str(forecastData[i-1][4]) + "mm (" + str(forecastData[i-1][5]) + "% chance)")
      self.builder.get_object("Wind Day" + str(i)).set_text("Wind - " + str(forecastData[i-1][6]) + "km/h (" + forecastData[i-1][7] + ")")
      self.builder.get_object("UV Day" + str(i)).set_text("UV Index - " + str(forecastData[i-1][8]))
      self.builder.get_object("Home3 Day" + str(i)).set_text(str(forecastData[i-1][4]) + "mm rain (" + str(forecastData[i-1][5]) + "% chance)")
      self.builder.get_object("Home4 Day" + str(i)).set_text(str(forecastData[i-1][3]) + "% Humidity")
      
      e = 1
      eText = "Icon"
      while e < 3: # Repeat 2 times
        if (forecastData[i-1][10] < 300): # Thunderstorm
          self.builder.get_object(eText + " Day" + str(i)).set_from_icon_name("weather-storm", Gtk.IconSize.DIALOG)
        elif (forecastData[i-1][10] < 400): # L + str(i)ight rain / drizzle
          self.builder.get_object(eText + " Day").set_from_icon_name("weather-showers-scattered", Gtk.IconSize.DIALOG)
        elif (forecastData[i-1][10] < 600 or forecastData[i-1][10] == 900): # Rain / shower
          self.builder.get_object(eText + " Day" + str(i)).set_from_icon_name("weather-showers", Gtk.IconSize.DIALOG)
        elif (forecastData[i-1][10] < 700): # Snow
          self.builder.get_object(eText + " Day" + str(i)).set_from_icon_name("weather-snow", Gtk.IconSize.DIALOG)
        elif (forecastData[i-1][10] < 800): # Fog / haze
          self.builder.get_object(eText + " Day" + str(i)).set_from_icon_name("weather-fog", Gtk.IconSize.DIALOG)
        elif (forecastData[i-1][10] == 800): # Clear
          self.builder.get_object(eText + " Day" + str(i)).set_from_icon_name("weather-clear", Gtk.IconSize.DIALOG)
        elif (forecastData[i-1][10] < 804): # Few clouds
          self.builder.get_object(eText + " Day" + str(i)).set_from_icon_name("weather-few-clouds", Gtk.IconSize.DIALOG)
        elif (forecastData[i-1][10] == 804): # Overcast
          self.builder.get_object(eText + " Day" + str(i)).set_from_icon_name("weather-overcast", Gtk.IconSize.DIALOG)
        eText = "Home1"
        e += 1
      i += 1

  def __init__(self):
    global dateToday
    # This is the first function called, when the code is started
    # Set the Glade GUI file being used
    self.gladefile = "HydroSoil.glade"
    # Set up the GUI Builder
    self.builder = Gtk.Builder()
    # Add the Glade GUI file to the GUI Builder
    self.builder.add_from_file(self.gladefile)
    # Connect all the signals and functions to this code
    self.builder.connect_signals(self)
    # Get the window object (called HydroSoil)
    self.window = self.builder.get_object("HydroSoil")
    # Show the home screen
    self.window.show()
    # Make the window fullscreen
    #self.window.fullscreen()
    
    # CHECK IF MAIN UNIT IS SETUP
    startupMode = 1
    
    try: # Returns exception if the file doesn't exist
      with open('/home/pi/HydroSoil/newupdate') as file:
        startupMode = 2
        updateData = file.readlines()
    except:
      pass # Startup Mode stays as 1
    
    try: # Returns exception if the file doesn't exist
      with open('/home/pi/HydroSoil/setupvalid') as file:
        pass
    except:
      startupMode = 3
    
    if startupMode == 3:
      # SET UP THE HYDROCORE
      self.builder.get_object("Toplevel").set_current_page(1)
      print("Setting up HydroCore")
      return
    elif startupMode == 2:
      # SHOW FEATURES OF NEW UPDATE
      self.builder.get_object("Toplevel").set_current_page(2)
      self.builder.get_object('New Features Title').set_text("What's New: hydrOS v" + updateData[0][:-1])
      self.builder.get_object('New Features Text').set_text(''.join(map(str, updateData[1:])))
      print("Showing new update features")
    else:
      # CONTINUE AS NORMAL
      self.builder.get_object("Toplevel").set_current_page(0)
    
    # Set current page to Home (first tab)
    self.builder.get_object("Content Tabs").set_current_page(0)
    self.builder.get_object("Home Icon").set_from_file("assets/Home Sel.png")
    # Configure some more properties of the GUI than cannot be set in Glade
    self.builder.get_object("Main Calendar").set_detail_func(self.calendarDetail)
    self.builder.get_object("Main Calendar").set_detail_height_rows(2)
    self.builder.get_object("Humidity Day1").set_xalign(1)
    self.builder.get_object("Rain Day1").set_xalign(1)
    self.builder.get_object("Wind Day1").set_xalign(1)
    self.builder.get_object("UV Day1").set_xalign(1)
    self.builder.get_object("Humidity Day2").set_xalign(1)
    self.builder.get_object("Rain Day2").set_xalign(1)
    self.builder.get_object("Wind Day2").set_xalign(1)
    self.builder.get_object("UV Day2").set_xalign(1)
    self.builder.get_object("Humidity Day3").set_xalign(1)
    self.builder.get_object("Rain Day3").set_xalign(1)
    self.builder.get_object("Wind Day3").set_xalign(1)
    self.builder.get_object("UV Day3").set_xalign(1)
    self.builder.get_object("Humidity Day4").set_xalign(1)
    self.builder.get_object("Rain Day4").set_xalign(1)
    self.builder.get_object("Wind Day4").set_xalign(1)
    self.builder.get_object("UV Day4").set_xalign(1)
    self.builder.get_object("Humidity Day5").set_xalign(1)
    self.builder.get_object("Rain Day5").set_xalign(1)
    self.builder.get_object("Wind Day5").set_xalign(1)
    self.builder.get_object("UV Day5").set_xalign(1)
    self.builder.get_object("Humidity Day6").set_xalign(1)
    self.builder.get_object("Rain Day6").set_xalign(1)
    self.builder.get_object("Wind Day6").set_xalign(1)
    self.builder.get_object("UV Day6").set_xalign(1)
    self.builder.get_object("Home Text").set_xalign(0)
    self.builder.get_object("Setting Label 1").set_xalign(0)
    self.builder.get_object("Setting Label 2").set_xalign(0)
    self.builder.get_object("Setting Label 3").set_xalign(0)
    self.builder.get_object("Setting Label 4").set_xalign(0)
    self.builder.get_object("Setting Label 5").set_xalign(0)
    self.builder.get_object("Setting Label 6").set_xalign(0)
    self.builder.get_object("Setting Label 7").set_xalign(0)
    self.builder.get_object("Setting Label 8").set_xalign(0)
    self.builder.get_object("Setting Label 9").set_xalign(0)
    self.builder.get_object("Setting Label 10").set_xalign(0)
    self.builder.get_object("Status Text Update").set_xalign(1)
    self.builder.get_object("Button1 Zone1").set_name("1")
    self.builder.get_object("Button2 Zone1").set_name("1")
    self.builder.get_object("Button3 Zone1").set_name("1")
    self.builder.get_object("Button1 Zone2").set_name("2")
    self.builder.get_object("Button2 Zone2").set_name("2")
    self.builder.get_object("Button3 Zone2").set_name("2")
    self.builder.get_object("Button1 Zone3").set_name("3")
    self.builder.get_object("Button2 Zone3").set_name("3")
    self.builder.get_object("Button3 Zone3").set_name("3")
    self.builder.get_object("Button1 Zone4").set_name("4")
    self.builder.get_object("Button2 Zone4").set_name("4")
    self.builder.get_object("Button3 Zone4").set_name("4")
    self.builder.get_object("Button1 Zone5").set_name("5")
    self.builder.get_object("Button2 Zone5").set_name("5")
    self.builder.get_object("Button3 Zone5").set_name("5")
    self.builder.get_object("Button1 Zone6").set_name("6")
    self.builder.get_object("Button2 Zone6").set_name("6")
    self.builder.get_object("Button3 Zone6").set_name("6")
    # Parse crop/plant list & soil data for choose plant GUI
    plant_list = self.builder.get_object('Crops & Plants')
    with open("plant-crop-list.csv", newline='') as csvfile:
      csvparser = csv.reader(csvfile, delimiter=',')
      Tup1 = ()
      i = 0
      for Tup1 in csvparser:
        plant_list.insert(-1, [str(Tup1[0])])
        i += 1
      csvfile.closed
    # Add values to dropdown selection box (GtkComboBox)
    plantCropCombo = self.builder.get_object('PlantCropDropdown')
    renderer_combo = Gtk.CellRendererText()
    plantCropCombo.pack_start(renderer_combo, True)
    plantCropCombo.add_attribute(renderer_combo, "text", 0)
    # Update the zones page (disable controls for disabled modes)
    self.update_zone_controls()
    # Set timed interupts for clock & wifi status
    self.secondroutine = GLib.timeout_add(1000, self.second_routine) # 1 second
    self.weatherroutine = GLib.timeout_add(1800000, self.forecast) # 30 minutes
    self.forecast()
    self.update_weather_page()
    self.update_zones()
    # Select today on the calendar, and mark it for the user
    dateToday = datetime.date.today()
    self.builder.get_object('Main Calendar').select_month(dateToday.month-1, dateToday.year)
    self.builder.get_object('Home Calendar').select_month(dateToday.month-1, dateToday.year)
    self.builder.get_object('Main Calendar').select_day(dateToday.day)
    self.builder.get_object('Home Calendar').select_day(dateToday.day)
    self.builder.get_object('Main Calendar').mark_day(dateToday.day)
    self.builder.get_object('Home Calendar').mark_day(dateToday.day)
    self.builder.get_object('Home Cal Text').set_text(self.generate_calendar_text(dateToday.year, dateToday.month-1, dateToday.day, False))

if __name__ == "__main__":
  main = SoilSystemMain()
  Gtk.main()
