
# app.py

#- Configs -----------------------------------------------------------------------------------------

SYSTEM1_PORT = "/dev/ttyACM0"
SYSTEM2_PORT = "/dev/ttyACM1"


#- Imports -----------------------------------------------------------------------------------------

import threading
from scripts.system1 import Run as System1Run
from scripts.system2 import Run as System2Run


#- Main entry point --------------------------------------------------------------------------------

def main():
    thread1 = threading.Thread(target=System1Run, args=(SYSTEM1_PORT,))
    thread2 = threading.Thread(target=System2Run, args=(SYSTEM2_PORT,))
    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()
#---------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    print("[main] starting the system")
    main()

