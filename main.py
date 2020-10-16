#!/usr/bin/python3                                                                                                                                                                            
import RPi.GPIO as GPIO                                                                                                                                                                       
import time                                                                                                                                                                                   
                                                                                                                                                                                              
# Change These                                                                                                                                                                                
washer_channel = 3                                                                                                                                                                            
check_time = 30                                                                                                                                                                               
                                                                                                                                                                                              
# variables to track state
washer_running = False
washer_counter = 0
washer_last_count = 0
washer_minutes_running = 0

GPIO.setmode(GPIO.BCM)
GPIO.setup(washer_channel, GPIO.IN)

def callback(channel):
  global washer_counter
  if GPIO.input(channel):
    washer_counter += 1
  else:
    washer_counter += 1

GPIO.add_event_detect(washer_channel, GPIO.BOTH, bouncetime=300) # notifiy if going high or low                                                                                               
GPIO.add_event_callback(washer_channel, callback)

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
        print("washer started")
      else:
       washer_minutes_running += 1
  else:
    # not running anymore so reset
    washer_counter = 0
    if washer_running:
      washer_running = False
      # send mqtt washer stopped
      print("washer stopped")

  washer_last_count = washer_counter


# main loop
while True:
  check_washer()
  time.sleep(check_time)
