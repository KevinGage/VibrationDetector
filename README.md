# VibrationDetector
python raspberry pi vibration detection project

# Components
https://components101.com/sensors/sw-420-vibration-sensor-module

# Libraries
pip3 install RPi.GPIO
pip3 install pip install paho-mqtt

# Instructions
Download mqtt-vibration.py script to /usr/local/bin/. Edit the address and credentials for the broker. If needed add the path to the brokers CA (For self signed certs), otherwise remove tls parameter from publish.single tls={"ca_certs":""}) so it looks like tls={}

Create /etc/systemd/system/mqtt-vibration.service

start service and enable it for auto on boot systemctl start mqtt-vibration systemctl enable mqtt-vibration