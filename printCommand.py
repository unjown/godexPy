import os
import ctypes
def printCommand():
    # Use EZio32.dll
    GodexPrinter = ctypes.windll.LoadLibrary(os.getcwd() + "\\EZio64.dll")  

    # Open USB Port (6)
    GodexPrinter.openport("6")

    # Set Command ( Print Detail Information in Printer )
    Cmd = ctypes.create_string_buffer(b"~V\r\n")

    # Send Command
    GodexPrinter.sendcommand(Cmd)

    # Close Port
    GodexPrinter.closeport()
