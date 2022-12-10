import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
from time import sleep
import subprocess


def turnOnMac(channel):
    print("turn on mac!")
    p = subprocess.Popen("lgtv Monitor on", stdout=subprocess.PIPE, shell=True)
    p2 = subprocess.Popen("lgtv Monitor setInput HDMI_1", stdout=subprocess.PIPE, shell=True)
    sleep(0.25)

def turnOnPC(channel):
    print("turn on pc!")
    p = subprocess.Popen("lgtv Monitor on", stdout=subprocess.PIPE, shell=True)
    p2 = subprocess.Popen("lgtv Monitor setInput HDMI_3", stdout=subprocess.PIPE, shell=True)
    sleep(0.25)

def turnOff(channel):
    print("turn off!")
    p = subprocess.Popen("lgtv Monitor off", stdout=subprocess.PIPE, shell=True)
    sleep(0.25)

print("starting!")
GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(7,GPIO.RISING,callback=turnOnMac, bouncetime=300) # Setup event on pin 10 rising edge

GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(10,GPIO.RISING,callback=turnOnPC, bouncetime=300) # Setup event on pin 10 rising edge

GPIO.setup(8, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(8,GPIO.RISING,callback=turnOff, bouncetime=300) # Setup event on pin 10 rising edge

while True:
    sleep(0.5)

GPIO.cleanup() # Clean up