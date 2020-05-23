#  update.py
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
# This is the code which runs to install latest hydrOS update
# It is run when user requests update

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
mqttScript_command = "python3 /home/pi/HydroSoil/mqtt.py"
mainScript_command = "python3 /home/pi/HydroSoil/main.py"

# Import sleep to delay
from time import sleep

# Start main code for class HydroLauncherMain

class HydroLauncherMain:
  
  def check_install_update(self):
    # Check if a hydrOS update is ready for installation
    try: # Check for update file
      with open('/home/pi/HydroLauncher/updatenow') as file:
        updateData = file.readlines()
    except:
      pass
    else:
      # Install update to hydrOS
      print("Installing hydrOS Update")
      self.builder.get_object("Title Update").set_text("Installing hydrOS " + updateData[0][:-1] + "...")
      self.builder.get_object("New Features Text").set_text(''.join(map(str, updateData[1:])))
      self.builder.get_object("Main Container").set_current_page(1)
      self.builder.get_object("Progress").set_fraction(0)
      self.mainScript.kill()
      self.mqttScript.kill()
      # Start the hydrOS Update Installation
      # Copy all new & required files to HydroSoil folder
      os.system("sudo cp -f /home/pi/HydroSoilNew/HydroSoil/main.py /home/pi/HydroSoil/main.py")
      self.builder.get_object("Progress").set_fraction(0.09)
      os.system("sudo cp -f /home/pi/HydroSoilNew/HydroSoil/mqtt.py /home/pi/HydroSoil/mqtt.py")
      self.builder.get_object("Progress").set_fraction(0.18)
      os.system("sudo cp -f /home/pi/HydroSoilNew/HydroSoil/version /home/pi/HydroSoil/version")
      self.builder.get_object("Progress").set_fraction(0.27)
      os.system("sudo cp -f /home/pi/HydroSoilNew/HydroSoil/plant-crop-list.csv /home/pi/HydroSoil/plant-crop-list.csv")
      self.builder.get_object("Progress").set_fraction(0.36)
      os.system("sudo cp -fr /home/pi/HydroSoilNew/HydroSoil/assets /home/pi/HydroSoil/assets")
      self.builder.get_object("Progress").set_fraction(0.45)
      os.system("sudo cp -fr /home/pi/HydroSoilNew/HydroSoil/icons /home/pi/HydroSoil/icons")
      self.builder.get_object("Progress").set_fraction(0.54)
      os.system("sudo cp -f /home/pi/HydroSoilNew/HydroSoil/background.jpg /home/pi/HydroSoil/background.jpg")
      self.builder.get_object("Progress").set_fraction(0.63)
      os.system("sudo cp -f /home/pi/HydroSoilNew/HydroSoil/splash.png /home/pi/HydroSoil/splash.png")
      self.builder.get_object("Progress").set_fraction(0.72)
      os.system("sudo cp -f /home/pi/HydroSoilNew/newupdate /home/pi/HydroSoil/newupdate")
      self.builder.get_object("Progress").set_fraction(0.81)
      # Clean up after installation
      os.system("sudo rm -fr /home/pi/HydroSoilNew")
      self.builder.get_object("Progress").set_fraction(0.9)
      os.system("sudo rm -f /home/pi/HydroLauncher/updatenow")
      self.builder.get_object("Progress").set_fraction(1)
      # Reboot into new hydrOS version
      time.sleep(1)
      os.system("sudo reboot")
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
    self.builder.get_object("Main Container").set_current_page(2)
    # Run hydrOS and MQTT Server
    self.mqttScript = subprocess.Popen(mqttScript_command.split())
    self.mainScript = subprocess.Popen(mainScript_command.split())
    # Set timed interupts for update checking
    self.updateroutine = GLib.timeout_add(10000, self.check_install_update) # 10 seconds

if __name__ == "__main__":
  main = HydroLauncherMain()
  Gtk.main()
