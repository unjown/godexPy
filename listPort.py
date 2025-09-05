import ctypes
import os

# Load the correct DLL (32-bit or 64-bit depending on your Python)
GodexPrinter = ctypes.windll.LoadLibrary(os.getcwd() + "\\EZio64.dll")

# Map IDs to human-readable names (non-USB)
PORTS = {
    "0 - LPT1": "0",
    "1 - COM1": "1",
    "2 - COM2": "2",
    "3 - COM3": "3",
    "4 - COM4": "4",
    "5 - LPT2": "5",
    # "6 - USB" will be handled by FindNextUSB instead of here
}

def test_port(port_id: str) -> bool:
    """
    Try to open a port and close it immediately.
    Return True if successful, False otherwise.
    """
    try:
        result = GodexPrinter.openport(port_id.encode("ascii"))
        if result == 1:
            GodexPrinter.closeport()
            return True
    except Exception:
        pass
    return False

def get_usb_printers():
    """
    Enumerate connected GoDEX USB printers using FindNextUSB.
    Returns list like ["USB: USB001 - GODEX XYZ"] or empty list.
    """
    printers = []
    buf = ctypes.create_string_buffer(256)

    while True:
        result = GodexPrinter.FindNextUSB(buf)
        if result == 1:  # OK, found one
            usb_id = buf.value.decode("ascii", errors="ignore").strip()
            if usb_id:
                printers.append(f"6 - USB ({usb_id})")
        else:
            break

    return printers

def get_connected_ports():
    """
    Return a list of connected printer ports with labels.
    Includes COM/LPT (tested) and USB (via FindNextUSB).
    """
    connected = []

    # --- Check LPT/COM ---
    for label, pid in PORTS.items():
        if test_port(pid):
            try:
                buf = ctypes.create_string_buffer(256)
                GodexPrinter.getprintername(buf)
                printer_name = buf.value.decode("ascii", errors="ignore")
                connected.append(f"{label} ({printer_name})")
            except Exception:
                connected.append(label)

    # --- Check USB ---
    usb_list = get_usb_printers()
    connected.extend(usb_list)

    if not connected:
        return ["No printer connected"]

    return connected


# --- Debug Run ---
if __name__ == "__main__":
    print("Connected Ports:")
    for port in get_connected_ports():
        print(" -", port)
