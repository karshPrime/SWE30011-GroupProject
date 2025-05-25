
# app.py

#- Configs -----------------------------------------------------------------------------------------

SYSTEM1_PORT = "/dev/ttyACM0"


#- Imports -----------------------------------------------------------------------------------------

import threading
from scripts.system1 import Run as System1Run


#- Main entry point --------------------------------------------------------------------------------

def main():
    thread1 = threading.Thread(target=System1Run, args=(SYSTEM1_PORT,))
    thread1.start()
    thread1.join()
#---------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    print("[main] starting the system")
    main()

