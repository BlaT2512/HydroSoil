# Import Paho MQTT to subscribe to MQTT Broker
import paho.mqtt.client as mqtt

# Import datetime for recording timestamps of messages
import datetime
from datetime import timedelta

# Get unique ID code (main.py generates one if needed before this script is run)
with open('/home/pi/HydroSoil/ID.txt') as file:
  uniqueID = file.readlines()
uniqueID = uniqueID[0]

# Import threading for timed function
import threading

# Settings and variables for the MQTT Broker
mqtt_username = "SoilMeasurer"
mqtt_password = "HydroSoil123"
mqtt_sensor_topic = "HydroSoil Data"
mqtt_app_topic = "HydroSoil App"
mqtt_broker_ip = "hydrosoilmainunit.local"
client = mqtt.Client()
client.username_pw_set(mqtt_username, mqtt_password)

# Other variables and settings
nZones = 6 # The number of zones (6 without expansion kit)

def on_connect(client, userdata, flags, rc):
  print ("Connected to MQTT Server") # Debugging
  client.subscribe(mqtt_sensor_topic)
  client.subscribe(mqtt_app_topic)
    
def on_message(client, userdata, msg):
  rawPayload = str(msg.payload)
  
  if str(msg.topic) == "HydroSoil Data":
    # Data Recieved from HydroUnit
    # Process & parse payload
    rawPayload = rawPayload[2:-1]
    rawPayload = rawPayload.lstrip("0")
    payloadSensor = rawPayload[:7]
    payloadData = rawPayload[9:]
    print ("Topic: " + msg.topic + "\nSoil sensor sender: " + payloadSensor + "\nSensor value: " + payloadData + "\n") # Debugging
    # Write values to appropriate lines in file /home/pi/HydroSoil/livedata.txt
    with open('/home/pi/HydroSoil/settings.txt') as file:
      settingsData = file.readlines()
    with open('/home/pi/HydroSoil/livedata.txt') as file:
      liveData = file.readlines()
    
    i = 1
    s = 0
    while i < nZones+1:
      if settingsData[i][11:-1] == payloadSensor:
        d = datetime.datetime.today()
        s += 1
        liveData[5+i] = "zone" + str(i) + "conf=Connected\n"
        liveData[11+i] = "zone" + str(i) + "con=1\n"
        liveData[17+i] = "zone" + str(i) + "moisture=" + str(payloadData) + "\n"
        liveData[23+i] = "zone" + str(i) + "lastactivity=" + str(d) + "\n"
        with open('/home/pi/HydroSoil/livedata.txt', 'w') as file:
          file.writelines(liveData)
      i += 1
    
    if s == 0: # This sensor is not registered as a zone, report a new sensor was detected
      liveData[30] = "newdetected=" + payloadSensor + "\n"
      with open('/home/pi/HydroSoil/livedata.txt', 'w') as file:
          file.writelines(liveData)
  elif str(msg.topic) == "HydroSoil App":
    # Data Recieved from HydroSoil App
    # Process & parse payload
    pass

def check_disconnect():
  # This function runs every 2 seconds and sets sensors to disconnected that haven't sent data in over 5 seconds
  with open('/home/pi/HydroSoil/settings.txt') as file:
    settingsData = file.readlines()
  with open('/home/pi/HydroSoil/livedata.txt') as file:
    liveData = file.readlines()
  d = datetime.datetime.today()
  
  i = 1
  while i < nZones+1:
    try: # Returns exception if file is being written to at the same time
      if settingsData[i][11:-1] != "0" and liveData[23+i][17:-1] != "=" and liveData[5+i][10:-1] == "Connected":
        old_d = datetime.datetime(int(liveData[23+i][18:22]), int(liveData[23+i][23:25]), int(liveData[23+i][26:28]), int(liveData[23+i][29:31]), int(liveData[23+i][32:34]), int(liveData[23+i][35:37]))
        diff = d-old_d
        diff = diff.seconds
        if diff > 5:
          liveData[5+i] = "zone" + str(i) + "conf=Disconnected\n"
          liveData[11+i] = "zone" + str(i) + "con=0\n"
          with open('/home/pi/HydroSoil/livedata.txt', 'w') as file:
            file.writelines(liveData)
    except:
      pass # This doesn't matter as routine is run every 2 seconds
    i += 1
  threading.Timer(2.0, check_disconnect).start()

check_disconnect()
threading.Timer(2.0, check_disconnect).start()
client.publish(mqtt_sensor_topic, "HydroSoil Main Unit " + uniqueID + " Connected")
client.publish(mqtt_app_topic, "HydroSoil Main Unit " + uniqueID + " Connected")
client.on_connect = on_connect
client.on_message = on_message
client.connect(mqtt_broker_ip, 1883)
client.loop_forever()
client.disconnect()
