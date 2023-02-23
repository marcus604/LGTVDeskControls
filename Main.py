import sys
import RPi.GPIO as GPIO
from time import sleep
from configparser import ConfigParser
import requests


#Custom
from log import getLogger, logging

PROGRAM_NAME = "LG TV Desk Controls"

logger = getLogger(__name__, "logs/{}.log".format(PROGRAM_NAME))

BASE_URL = ''
HEADERS = ''

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
    endpoint = BASE_URL + 'switch_to_laptop'
    logger.debug(endpoint)
    response = requests.post(endpoint, headers=HEADERS)
    logger.debug(response)
    sleep(0.25)

def turnOnPC(channel):
    logger.info("Turning on pc")
    endpoint = BASE_URL + 'switch_to_pc'
    logger.debug(endpoint)
    response = requests.post(endpoint, headers=HEADERS)
    logger.debug(response)
    sleep(0.25)

def turnOff(channel):
    logger.info("Turning off")
    endpoint = BASE_URL + 'monitor_off'
    logger.debug(endpoint)
    response = requests.post(endpoint, headers=HEADERS)
    logger.debug(response)
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
    gpioConfig = config["GPIO_PINS"]
    haConfig = config["HOME_ASSISTANT"]

    GPIO_PC = int(gpioConfig["PC_INPUT"])
    GPIO_LAPTOP = int(gpioConfig["LAPTOP_INPUT"])
    GPIO_OFF = int(gpioConfig["OFF"])

    HA_IP = haConfig["IP"]
    HA_PORT = haConfig["PORT"]
    HA_TOKEN = haConfig["TOKEN"]

    global BASE_URL 
    global HEADERS 

    BASE_URL = f'http://{HA_IP}:{HA_PORT}/api/services/script/'
    HEADERS = {'Authorization': f'Bearer {HA_TOKEN}'}

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