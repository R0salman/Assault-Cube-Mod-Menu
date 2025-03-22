# Made By: R0Salman
from app import App
from mod import AssultCubeMod

if __name__ == "__main__":
    try:
        mod = AssultCubeMod()
        app = App(mod)
        app.mainloop()
    except Exception as e:
        print(f"ERR:: Something happened! {e}")
        input("Press Enter to continue...")