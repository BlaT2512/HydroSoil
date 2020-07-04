#  launcher.py
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
# The HydroLauncher runs at boot of the HydroCore
# It can update, control and repair hydrOS and triggers it to run

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

# Import libraries
# Import GTK and dependencies for making/handling GUI
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, Gdk, GLib
from gi.repository.GdkPixbuf import Pixbuf

# Import requests and json to get latest update data
import requests
import json

# Import OS & subprocess for terminal commands, and set the working directory
import os
import subprocess
os.chdir("/home/pi/HydroLauncher")
mqttScript_command = "python3 /home/pi/HydroSoil/mqtt.py &"
mainScript_command = "python3 /home/pi/HydroSoil/main.py &"

# Import sleep to delay
from time import sleep

# Start main code for class HydroLauncherMain

class HydroLauncherMain:
  
  def check_routine(self):
    # Check if anything needs to be done
    # First, check if a hydrOS update is ready
    try: # Check for update file
      with open('/home/pi/HydroLauncher/updatenow') as file:
        updateData = file.readlines()
    except:
      pass
    else:
      # Install update to hydrOS
      self.mainScript.terminate()
      self.mqttScript.terminate()
      print("Installing hydrOS Update")
      self.builder.get_object('Title Update').set_text("Installing hydrOS " + updateData[0][:-1] + "...")
      self.builder.get_object('New Features Text').set_text(''.join(map(str, updateData[1:])))
      self.builder.get_object('Main Tabs').set_current_page(1)
      self.builder.get_object('Progress').set_fraction(0)
      while Gtk.events_pending(): Gtk.main_iteration() # Update GUI
      # Start the hydrOS Update Installation
      # Copy all new & required files to HydroSoil folder
      #os.system("sudo cp -f /home/pi/HydroSoilNew/HydroSoil/main.py /home/pi/HydroSoil/main.py")
      self.builder.get_object("Progress").set_fraction(0.09)
      while Gtk.events_pending(): Gtk.main_iteration() # Update GUI
      sleep(1)
      #os.system("sudo cp -f /home/pi/HydroSoilNew/HydroSoil/mqtt.py /home/pi/HydroSoil/mqtt.py")
      self.builder.get_object("Progress").set_fraction(0.18)
      while Gtk.events_pending(): Gtk.main_iteration() # Update GUI
      sleep(1)
      os.system("sudo cp -f /home/pi/HydroSoilNew/HydroSoil/version /home/pi/HydroSoil/version")
      self.builder.get_object("Progress").set_fraction(0.27)
      while Gtk.events_pending(): Gtk.main_iteration() # Update GUI
      sleep(1)
      os.system("sudo cp -f /home/pi/HydroSoilNew/HydroSoil/plant-crop-list.csv /home/pi/HydroSoil/plant-crop-list.csv")
      self.builder.get_object("Progress").set_fraction(0.36)
      while Gtk.events_pending(): Gtk.main_iteration() # Update GUI
      sleep(1)
      os.system("sudo cp -fr /home/pi/HydroSoilNew/HydroSoil/assets /home/pi/HydroSoil/assets")
      self.builder.get_object("Progress").set_fraction(0.45)
      while Gtk.events_pending(): Gtk.main_iteration() # Update GUI
      sleep(1)
      os.system("sudo cp -fr /home/pi/HydroSoilNew/HydroSoil/icons /home/pi/HydroSoil/icons")
      self.builder.get_object("Progress").set_fraction(0.54)
      while Gtk.events_pending(): Gtk.main_iteration() # Update GUI
      sleep(1)
      os.system("sudo cp -f /home/pi/HydroSoilNew/HydroSoil/background.jpg /home/pi/HydroSoil/background.jpg")
      self.builder.get_object("Progress").set_fraction(0.63)
      while Gtk.events_pending(): Gtk.main_iteration() # Update GUI
      sleep(1)
      os.system("sudo cp -f /home/pi/HydroSoilNew/HydroSoil/splash.png /home/pi/HydroSoil/splash.png")
      self.builder.get_object("Progress").set_fraction(0.72)
      while Gtk.events_pending(): Gtk.main_iteration() # Update GUI
      sleep(1)
      os.system("sudo cp -f /home/pi/HydroSoilNew/newupdate /home/pi/HydroSoil/newupdate")
      self.builder.get_object("Progress").set_fraction(0.81)
      while Gtk.events_pending(): Gtk.main_iteration() # Update GUI
      sleep(1)
      # Clean up after installation
      os.system("sudo rm -fr /home/pi/HydroSoilNew")
      self.builder.get_object("Progress").set_fraction(0.9)
      while Gtk.events_pending(): Gtk.main_iteration() # Update GUI
      sleep(1)
      os.system("sudo rm -f /home/pi/HydroLauncher/updatenow")
      self.builder.get_object("Progress").set_fraction(1)
      while Gtk.events_pending(): Gtk.main_iteration() # Update GUI
      # Check if reset needs to be done as well, and then reboot into new hydrOS version
      try: # Check for utility file
        with open('/home/pi/HydroLauncher/reset') as file:
          resetData = file.readlines()
      except:
        sleep(1)
        os.system("sudo reboot")
      else:
        # Reset HydroCore then reboot
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
zone1rmoisture=
zone2rmoisture=
zone3rmoisture=
zone4rmoisture=
zone5rmoisture=
zone6rmoisture=
zone1lmoisture=
zone2lmoisture=
zone3lmoisture=
zone4lmoisture=
zone5lmoisture=
zone6lmoisture=
calweekstart=
locationtype=citystate
location=Adelaide
locationcountry=AU
weatherunits=M
tzcountry=AU
timezone=Australia/Adelaide
tzoffset=34200

'''
        with open('/home/pi/HydroSoil/settings.txt', 'w') as file:
          file.writelines(settingsData)
        liveData = '''zone1onf=
zone2onf=
zone3onf=
zone4onf=
zone5onf=
zone6onf=
zone1conf=Disconnected
zone2conf=Disconnected
zone3conf=Disconnected
zone4conf=Disconnected
zone5conf=Disconnected
zone6conf=Disconnected
zone1con=0
zone2con=0
zone3con=0
zone4con=0
zone5con=0
zone6con=0
zone1moisture=
zone2moisture=
zone3moisture=
zone4moisture=
zone5moisture=
zone6moisture=
zone1lastactivity=
zone2lastactivity=
zone3lastactivity=
zone4lastactivity=
zone5lastactivity=
zone6lastactivity=
newdetected=0
nsenslastactivity=0

'''
        with open('/home/pi/HydroSoil/livedata.txt', 'w') as file:
          file.writelines(liveData)
        os.system("sudo rm -f /home/pi/HydroLauncher/reset")
        os.system("sudo rm -f /home/pi/HydroSoil/setupvalid")
        sleep(1)
        os.system("sudo reboot")
    
    # Check for HydroCore reset
    try: # Check for utility file
      with open('/home/pi/HydroLauncher/reset') as file:
        resetData = file.readlines()
    except:
      pass
    else:
      # Reset HydroCore then reboot
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
zone1rmoisture=
zone2rmoisture=
zone3rmoisture=
zone4rmoisture=
zone5rmoisture=
zone6rmoisture=
zone1lmoisture=
zone2lmoisture=
zone3lmoisture=
zone4lmoisture=
zone5lmoisture=
zone6lmoisture=
calweekstart=
locationtype=citystate
location=Adelaide
locationcountry=AU
weatherunits=M
tzcountry=AU
timezone=Australia/Adelaide
tzoffset=34200

'''
      with open('/home/pi/HydroSoil/settings.txt', 'w') as file:
        file.writelines(settingsData)
      liveData = '''zone1onf=
zone2onf=
zone3onf=
zone4onf=
zone5onf=
zone6onf=
zone1conf=Disconnected
zone2conf=Disconnected
zone3conf=Disconnected
zone4conf=Disconnected
zone5conf=Disconnected
zone6conf=Disconnected
zone1con=0
zone2con=0
zone3con=0
zone4con=0
zone5con=0
zone6con=0
zone1moisture=
zone2moisture=
zone3moisture=
zone4moisture=
zone5moisture=
zone6moisture=
zone1lastactivity=
zone2lastactivity=
zone3lastactivity=
zone4lastactivity=
zone5lastactivity=
zone6lastactivity=
newdetected=0
nsenslastactivity=0

'''
      with open('/home/pi/HydroSoil/livedata.txt', 'w') as file:
        file.writelines(liveData)
      os.system("sudo rm -f /home/pi/HydroLauncher/reset")
      os.system("sudo rm -f /home/pi/HydroSoil/setupvalid")
      sleep(1)
      os.system("sudo reboot")
    
    # Then check if the HydroLauncher utility menu needs to be opened
    try: # Check for utility file
      with open('/home/pi/HydroLauncher/utilities') as file:
        updateData = file.readlines()
    except:
      pass
    else:
      self.builder.get_object('Main Tabs').set_current_page(0)
      os.system("sudo rm -f /home/pi/HydroLauncher/utilities")
    return True
      
  def __init__(self):
    # This is the first function called, when the code is started
    # Set the Glade GUI file being used
    self.gladefile = "HydroLauncher.glade"
    # Set up the GUI Builder
    self.builder = Gtk.Builder()
    # Add the Glade GUI file to the GUI Builder
    self.builder.add_from_file(self.gladefile)
    # Connect all the signals and functions to this code
    self.builder.connect_signals(self)
    # Get the window object (called HydroLauncher)
    self.window = self.builder.get_object("HydroLauncher")
    # Show the home screen
    self.window.show()
    # Make the window fullscreen
    #self.window.fullscreen()
    # Set current page to Loading (third tab)
    self.builder.get_object('Main Tabs').set_current_page(2)
    # Run hydrOS and MQTT Server
    self.mqttScript = subprocess.Popen(mqttScript_command.split())
    self.mainScript = subprocess.Popen(mainScript_command.split())
    # Set timed interupts for update checking
    self.checkingroutine = GLib.timeout_add(10000, self.check_routine) # 10 seconds
    # Check validity of the settings and livedata files
    try: # Returns exception if the file doesn't exist
      with open('/home/pi/HydroSoil/settings.txt') as file:
        settingsData = file.readlines()
    except: # Settings doesn't exist
      settingsRequired = True
    else:
      if settingsData != []:
        settingsRequired = False
      else:
        settingsRequired = True
    
    try: # Returns exception if the file doesn't exist
      with open('/home/pi/HydroSoil/livedata.txt') as file:
        liveData = file.readlines()
    except: # Livedata doesn't exist
      livedataRequired = True
    else:
      if liveData != []:
        livedataRequired = False
      else:
        livedataRequired = True
    
    if settingsRequired:
      # Settings doesn't exist, generate blank settings
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
zone1rmoisture=
zone2rmoisture=
zone3rmoisture=
zone4rmoisture=
zone5rmoisture=
zone6rmoisture=
zone1lmoisture=
zone2lmoisture=
zone3lmoisture=
zone4lmoisture=
zone5lmoisture=
zone6lmoisture=
calweekstart=
locationtype=citystate
location=Adelaide
locationcountry=AU
weatherunits=M
tzcountry=AU
timezone=Australia/Adelaide
tzoffset=34200

'''
      with open('/home/pi/HydroSoil/settings.txt', 'w') as file:
        file.writelines(settingsData)
    
    if livedataRequired:
      # Livedata doesn't exist, generate blank livedata
      liveData = '''zone1onf=
zone2onf=
zone3onf=
zone4onf=
zone5onf=
zone6onf=
zone1conf=Disconnected
zone2conf=Disconnected
zone3conf=Disconnected
zone4conf=Disconnected
zone5conf=Disconnected
zone6conf=Disconnected
zone1con=0
zone2con=0
zone3con=0
zone4con=0
zone5con=0
zone6con=0
zone1moisture=
zone2moisture=
zone3moisture=
zone4moisture=
zone5moisture=
zone6moisture=
zone1lastactivity=
zone2lastactivity=
zone3lastactivity=
zone4lastactivity=
zone5lastactivity=
zone6lastactivity=
newdetected=0
nsenslastactivity=0

'''
      with open('/home/pi/HydroSoil/livedata.txt', 'w') as file:
        file.writelines(liveData)

if __name__ == "__main__":
  main = HydroLauncherMain()
  Gtk.main()
