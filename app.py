
# app.py

#- Configs -----------------------------------------------------------------------------------------

SYSTEM1_PORT = "/dev/ttyACM0"
SYSTEM2_PORT = "/dev/ttyACM1"
SYSTEM3_PORT = "/dev/ttyACM2"


#- Imports -----------------------------------------------------------------------------------------

import threading
from scripts.system1 import Run as System1Run
from scripts.system2 import Run as System2Run
from scripts.system3 import Run as System3Run


#- Main entry point --------------------------------------------------------------------------------

def main():
    thread1 = threading.Thread(target=System1Run, args=(SYSTEM1_PORT,))
    thread2 = threading.Thread(target=System2Run, args=(SYSTEM2_PORT,))
    thread3 = threading.Thread(target=System3Run, args=(SYSTEM3_PORT,))

    thread1.start()
    thread2.start()
    thread3.start()

    thread1.join()
    thread2.join()
    thread3.join()

#---------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    print("[main] starting the system")
    main()

