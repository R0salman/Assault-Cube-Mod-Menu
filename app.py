from mod import *
import customtkinter as ctk
import sys


ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self, mod):
        super().__init__()
        self.mod = mod
        self.title("EatherBird's Mod Menu")
        self.geometry("700x500")
        
        self.log_frame = ctk.CTkFrame(self)
        self.log_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.log_text = ctk.CTkTextbox(self.log_frame, wrap="word", state="disabled")
        self.log_text.pack(fill="both", expand=True, padx=10, pady=10)
        
        sys.stdout = self
        
        print(self.mod.id_and_address)
        
        self.control_frame = ctk.CTkFrame(self)
        self.control_frame.pack(fill="x", padx=10, pady=10)

        self.health_entry = ctk.CTkEntry(self.control_frame, placeholder_text="Enter Health Value")
        self.health_entry.pack(side="left", padx=5, pady=5)

        self.set_health_button = ctk.CTkButton(self.control_frame, text="Set Health", command=self.set_health)
        self.set_health_button.pack(side="left", padx=5, pady=5)

        self.god_mode_switch = ctk.CTkSwitch(self.control_frame, text="God Mode", command=self.toggle_god_mode)
        self.god_mode_switch.pack(side="left", padx=5, pady=5)
        
        self.theme_toggle = ctk.CTkButton(self.control_frame, text="Toggle Theme", command=self.toggle_theme)
        self.theme_toggle.pack(side="left", padx=5, pady=5)

        self.exit_button = ctk.CTkButton(self.control_frame, text="Exit", command=self.destroy)
        self.exit_button.pack(side="right", padx=5, pady=5)
        

    def write(self, message):
        self.log_text.configure(state="normal")
        self.log_text.insert("end", message)
        self.log_text.configure(state="disabled")
        self.log_text.see("end")

    def flush(self):
        pass
    
    def toggle_theme(self, *args):
        current_mode = ctk.get_appearance_mode()
        if current_mode == "Dark":
            ctk.set_appearance_mode("Light")
        else:
            ctk.set_appearance_mode("Dark")
    
    def set_health(self):
        try:
            health = int(self.health_entry.get())
            self.mod.set_health(health)
        except ValueError:
            print("Please enter a valid value!")

    def toggle_god_mode(self):
        self.mod.toggle_god_mode()
