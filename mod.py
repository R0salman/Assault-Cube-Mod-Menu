import time
import threading
from pymem import Pymem
from pymem.process import module_from_name
import psutil

def is_process_running(process_name):
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == process_name:
            return True
    return False

class AssultCubeMod:
    def __init__(self):
        if not is_process_running("ac_client.exe"):
            print("Assault Cube is not running. Please start the game first.")
            exit()
        try:
            self.pm = Pymem("ac_client.exe")
            self.module = module_from_name(self.pm.process_handle, "ac_client.exe").lpBaseOfDll
            self.id_and_address = f"Process ID: {self.pm.process_id} , Base Address: {hex(self.module)}"
            self.health_address = self.module + 0x0017E0A8 # health ptr chain,, 0xEC
            self.ammo_address = self.module + 0x0018AC00 # ammo ptr chain,, 0x140
            self.health_offset = 0xEC
            self.ammo_offset = 0x140
            self.god_mode = False
            self.god_mode_thread = None
        except Exception as e:
            print(f"Error initializing Pymem:: {e}")
            exit()

    def GetHealthPTR(self):
        try:
            base_pointer = self.pm.read_int(self.health_address)
            if not base_pointer:
                print("Health Base pointer is null.")
                return None
            health_address = base_pointer + self.health_offset
            return health_address
        except Exception as e:
            print(f"Error reading health memory: {e}")
            return None
        
    def GetAmmoPTR(self):
        try:
            base_pointer = self.pm.read_int(self.ammo_address)
            if not base_pointer:
                print("Ammo base pointer is null.")
                return None
            ammo_address = base_pointer + self.ammo_offset
            return ammo_address
        except Exception as e:
            print(f"Error reading ammo memory: {e}")
            return None

    def set_health(self, value, log=True):
        health_address = self.GetHealthPTR()
        if health_address:
            try:
                self.pm.write_int(health_address, value)
                if log:
                    print(f"Health set to {value}")
            except Exception as e:
                if log:
                    print(f"Failed to set health: {e}")
    
    def set_ammo(self, value, log=True):
        ammo_address = self.GetAmmoPTR()
        if ammo_address:
            try:
                self.pm.write_int(ammo_address, value)
                if log:
                    print(f"Ammo set to {value}")
            except Exception as e:
                if log:
                    print(f"Failed to set ammo: {e}")

    def toggle_god_mode(self):
        self.god_mode = not self.god_mode
        print(f"God Mode: {'ON' if self.god_mode else 'OFF'}")

        if self.god_mode:
            self.god_mode_thread = threading.Thread(target=self.god_mode_loop, daemon=True)
            self.god_mode_thread.start()
        else:
            if self.god_mode_thread:
                self.god_mode_thread.join()

    def god_mode_loop(self):
        while self.god_mode:
            self.set_health(9999, log=False) #"log=False" is used to prevent logging repeated messages.
            self.set_ammo(999, log=False)
            time.sleep(0.1)