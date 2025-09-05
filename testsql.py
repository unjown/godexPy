import tkinter as tk
from module1_page import Module1Page
from module2_page import Module2Page
from module3_page import Module3Page
from main_menu import MainMenuPage
import sys
import sqlite3
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Inventory & Assembly System")
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry(f"{screen_width}x{screen_height}")
        container = tk.Frame(self)
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for F in (MainMenuPage, Module1Page, Module2Page, Module3Page):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")  

        self.show_frame("MainMenuPage")

    def show_frame(self, page_name):
        self.frames[page_name].tkraise()
        if page_name == "Module3Page":
            self.frames[page_name].loadCustomers()

if __name__ == "__main__":
    app = App()
    app.mainloop()
    print(f"Python version: {sys.version}")
    print(f"Tkinter version (Tcl/Tk): {tk.TclVersion}")
    with sqlite3.connect("inventory.db", timeout=5) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM packingListTemp")
            conn.commit()
    print("cleared packingListTemp")
