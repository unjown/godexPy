import tkinter as tk
from tkinter import ttk, messagebox
import listPort as lp
import printCommand as pc
def choose_port_popup():
    """Popup dialog with dropdown to choose printer"""
    result = {"choice": None}

    def on_ok():
        result["choice"] = port_var.get()
        print(result["choice"])
        pc.printCommand()
        popup.destroy()

    def on_cancel():
        print( "Cancelled" )
        popup.destroy()

    popup = tk.Toplevel()
    popup.title("Select Printer")
    popup.geometry("300x150")
    popup.transient()
    popup.grab_set()

    tk.Label(popup, text="Select Printer:").pack(pady=5)

    connected = lp.get_connected_ports()
    port_var = tk.StringVar(value=connected[0] if connected else "")

    dropdown = ttk.Combobox(
        popup, textvariable=port_var,
        values=connected,
        state="readonly"
    )
    dropdown.pack(pady=5, padx=10, fill="x")

    btn_frame = tk.Frame(popup)
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="OK", width=10, command=on_ok).pack(side="left", padx=5)
    tk.Button(btn_frame, text="Cancel", width=10, command=on_cancel).pack(side="left", padx=5)

    popup.wait_window()
    return result["choice"]