import tkinter as tk
from module1_page import Module1Page
from module2_page import Module2Page
from module3_page import Module3Page
from main_menu import MainMenuPage
import sys

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Inventory & Assembly System")
        self.geometry("1000x600")

        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        self.frames = {}
        for F in (MainMenuPage, Module1Page, Module2Page, Module3Page):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("MainMenuPage")

    def show_frame(self, page_name):
        self.frames[page_name].tkraise()

if __name__ == "__main__":
    app = App()
    app.mainloop()
    print(f"Python version: {sys.version}")
    print(f"Tkinter version (Tcl/Tk): {tk.TclVersion}")
