#!/bin/bash
# This script sets up a Raspberry Pi 3B+ ready for deploying and development of HydroSoil

# First, update software to latest version
echo "Upgrading the Raspberry Pi software..."
sudo apt-get update
sudo apt-get upgrade

# Now install dependencies needed to run, and Glade and Geany for development
echo "Installing dependencies..."
sudo apt-get install python3 -y
sudo apt-get install libgtk-gtk-3 glade geany -y
pip3 install wireless
pip3 install wifi
pip3 install paho-mqtt
pip3 install packaging

# Setup the MQTT server for communication
echo "Setting up MQTT Server..."
sudo apt-get install mosquitto -y
sudo apt-get install mosquitto-clients -y
