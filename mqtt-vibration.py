#!/usr/bin/python3
import RPi.GPIO as GPIO
import time
import paho.mqtt.publish as publish

### Change These ###
# Io for vibration sensors
washer_channel = 3
dryer_channel = 4

# How ofter to check status
check_time = 10

#MQTT broker address and credentials
Broker = ''
auth = {
    'username': '',
    'password': '',
}
mqtt_port = 8883
#MQTT topic
washer_pub_topic = 'home/washer/running'
dryer_pub_topic = 'home/dryer/running'

### Dont change after this line ###

# variables to track state
washer_running = False
washer_counter = 0
washer_last_count = 0
washer_minutes_running = 0

dryer_running = False
dryer_counter = 0
dryer_last_count = 0
dryer_minutes_running = 0

GPIO.setmode(GPIO.BCM)
GPIO.setup(washer_channel, GPIO.IN)
GPIO.setup(dryer_channel, GPIO.IN)

def washer_callback(channel):
  global washer_counter
  if GPIO.input(channel):
    washer_counter += 1
  else:
    washer_counter += 1

def dryer_callback(channel):
  global dryer_counter
  if GPIO.input(channel):
    dryer_counter += 1
  else:
    dryer_counter += 1

GPIO.add_event_detect(washer_channel, GPIO.BOTH, bouncetime=300) # notifiy if going high or low
GPIO.add_event_callback(washer_channel, washer_callback)

GPIO.add_event_detect(dryer_channel, GPIO.BOTH, bouncetime=300) # notifiy if going high or low
GPIO.add_event_callback(dryer_channel, dryer_callback)

def check_washer():
  global washer_counter
  global washer_last_count
  global washer_running
  global washer_minutes_running

  if washer_counter > washer_last_count:
    if not washer_running:
      if washer_minutes_running > 5:
        washer_running = True
        # send mqtt started
        try:
          publish.single(washer_pub_topic, 'ON', hostname=Broker, port=mqtt_port, auth=auth, tls={})
        except:
          print("Error posting info to mqqt")
      else:
       washer_minutes_running += 1
  else:
    # not running anymore so reset
    washer_counter = 0
    if washer_running:
      washer_running = False
      # send mqtt washer stopped
      try:
        publish.single(washer_pub_topic, 'OFF', hostname=Broker, port=mqtt_port, auth=auth, tls={})
      except:
        print("Error posting info to mqqt")

  washer_last_count = washer_counter


def check_dryer():
  global dryer_counter
  global dryer_last_count
  global dryer_running
  global dryer_minutes_running

  if dryer_counter > dryer_last_count:
    if not dryer_running:
      if dryer_minutes_running > 5:
        dryer_running = True
        # send mqtt started
        try:
          publish.single(dryer_pub_topic, 'ON', hostname=Broker, port=mqtt_port, auth=auth, tls={})
        except:
          print("Error posting info to mqqt")
      else:
       dryer_minutes_running += 1
  else:
    # not running anymore so reset
    dryer_counter = 0
    if dryer_running:
      dryer_running = False
      # send mqtt dryer stopped
      try:
        publish.single(dryer_pub_topic, 'OFF', hostname=Broker, port=mqtt_port, auth=auth, tls={})
      except:
        print("Error posting info to mqqt")
  dryer_last_count = dryer_counter

# startup
# set running to false to reset logic
try:
  publish.single(washer_pub_topic, 'OFF', hostname=Broker, port=mqtt_port, auth=auth, tls={})
  publish.single(dryer_pub_topic, 'OFF', hostname=Broker, port=mqtt_port, auth=auth, tls={})
except:
  print("Error posting info to mqqt")

# main loop
while True:
  check_washer()
  check_dryer()
  time.sleep(check_time)