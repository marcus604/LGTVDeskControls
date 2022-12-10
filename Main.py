#Libraries
from configparser import ConfigParser
import sys
import RPi.GPIO as GPIO 
from time import sleep
import subprocess


#Custom
from log import getLogger, logging

##########CHANGE ME#################
PROGRAM_NAME = "LG TV Desk Controls"

logger = getLogger(__name__, "logs/{}.log".format(PROGRAM_NAME))

MODE_READ_ONLY = False
MODE_VERBOSE = False


def logLaunch():
    logger.info("Starting {}".center(40, "=").format(PROGRAM_NAME))
    if MODE_READ_ONLY:
        logger.info("Read Only Mode".center(40, "="))
    if MODE_VERBOSE:
        logger.info("Verbose Logging".center(40, "="))

def turnOnMac(channel):
    logger.info("Turning on mac")
    p = subprocess.Popen("lgtv Monitor on", stdout=subprocess.PIPE, shell=True)
    p2 = subprocess.Popen("lgtv Monitor setInput HDMI_1", stdout=subprocess.PIPE, shell=True)
    sleep(0.25)

def turnOnPC(channel):
    logger.info("Turning on pc")
    p = subprocess.Popen("lgtv Monitor on", stdout=subprocess.PIPE, shell=True)
    p2 = subprocess.Popen("lgtv Monitor setInput HDMI_3", stdout=subprocess.PIPE, shell=True)
    sleep(0.25)

def turnOff(channel):
    logger.info("Turning off")
    p = subprocess.Popen("lgtv Monitor off", stdout=subprocess.PIPE, shell=True)
    sleep(0.25)
    


##################################################
#################Main Application#################
##################################################
def main():
    #Log startup
    logLaunch()

    #Get config file
    config = ConfigParser()

    config.read("config.ini")
    userConfig = config["GPIO_PINS"]

    GPIO_PC = int(userConfig["PC_INPUT"])
    GPIO_LAPTOP = int(userConfig["LAPTOP_INPUT"])
    GPIO_OFF = int(userConfig["OFF"])
    

    GPIO.setwarnings(False) 
    GPIO.setmode(GPIO.BOARD) 
    GPIO.setup(GPIO_LAPTOP, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(GPIO_LAPTOP,GPIO.RISING,callback=turnOnMac, bouncetime=300) 

    GPIO.setup(GPIO_PC, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(GPIO_PC,GPIO.RISING,callback=turnOnPC, bouncetime=300) 

    GPIO.setup(GPIO_OFF, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(GPIO_OFF,GPIO.RISING,callback=turnOff, bouncetime=300) 

    while True:
        sleep(0.5)

    GPIO.cleanup()
    
    logger.info("Finished {}".center(40, "=").format(PROGRAM_NAME))

    
    
##################################################
#####################Launcher#####################
##################################################
if __name__ == "__main__":

    VERBOSE_FLAG = "-v"             
    

    logLevel = logging.INFO
    if len(sys.argv) != 1:
        for arg in sys.argv[1:]:
            if arg == VERBOSE_FLAG:
                logLevel = logging.DEBUG
                MODE_VERBOSE = True
    
    logger.setLevel(logLevel)
    main()