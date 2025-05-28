
# app.py

#- Configs -----------------------------------------------------------------------------------------

SYSTEM1_PORT = "/dev/ttyACM0"
SYSTEM2_PORT = "/dev/ttyACM1"


#- Imports -----------------------------------------------------------------------------------------

import threading
from scripts.system1 import system_run as s1_run
from scripts.system2 import system_run as s2_run
from scripts.system3 import system_run as s3_run
from scripts.control import mqtt_setup


#- Main entry point --------------------------------------------------------------------------------

def main():
    thread_mqtt = threading.Thread(target=mqtt_setup, args=())
    thread1 = threading.Thread(target=s1_run, args=(SYSTEM1_PORT,))
    thread2 = threading.Thread(target=s2_run, args=(SYSTEM2_PORT,))
    thread3 = threading.Thread(target=s3_run, args=())

    thread_mqtt.start()
    thread1.start()
    thread2.start()
    thread3.start()

    thread_mqtt.join()
    thread1.join()
    thread2.join()
    thread3.join()

#---------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    print("[main] Starting the system")
    main()

