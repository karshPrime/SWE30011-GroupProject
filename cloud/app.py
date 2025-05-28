
# app.py

#- Configs -----------------------------------------------------------------------------------------

SYSTEM_PORT = "/dev/tty.usbmodem21401"


#- Imports -----------------------------------------------------------------------------------------

import threading

from scripts.web     import run_webserver
from scripts.system  import system_run, update_temperature, system_terminate
from scripts.board   import thingsboard_setup, thingsboard_terminate
from scripts.control import mqtt_setup, mqtt_terminate


#- Main entry point --------------------------------------------------------------------------------

def main():
    try:
        thread_mqtt = threading.Thread(target=mqtt_setup, args=())
        thread_sys = threading.Thread(target=system_run, args=(SYSTEM_PORT,))
        thread_temp_api = threading.Thread(target=update_temperature, args=())
        thread_board = threading.Thread(target=thingsboard_setup, args=())

        thread_mqtt.start()
        thread_sys.start()
        thread_temp_api.start()
        thread_board.start()

        run_webserver()

    except KeyboardInterrupt:
        system_terminate()
        thingsboard_terminate()
        mqtt_terminate()

        thread_mqtt.join()
        thread_sys.join()
        thread_temp_api.join()
        thread_board.join()

#---------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    print("[main] Starting the system")
    main()

