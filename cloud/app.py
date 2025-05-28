
# app.py

#- Configs -----------------------------------------------------------------------------------------

SYSTEM_PORT = "/dev/tty.usbmodem21401"


#- Imports -----------------------------------------------------------------------------------------

import threading

from scripts.system  import system_run, update_temperature
from scripts.board   import thingsboard_setup
from scripts.control import mqtt_setup


#- Main entry point --------------------------------------------------------------------------------

def main():
    thread_mqtt = threading.Thread(target=mqtt_setup, args=())
    thread_sys = threading.Thread(target=system_run, args=(SYSTEM_PORT,))
    thread_temp_api = threading.Thread(target=update_temperature, args=())

    thread_mqtt.start()
    thread_sys.start()
    thread_temp_api.start()

    thread_mqtt.join()
    thread_sys.join()
    thread_temp_api.join()

#---------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    print("[main] Starting the system")
    main()

