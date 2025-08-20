import tkinter as tk

class MainMenuPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="🗂️ Inventory & Assembly Main Menu", font=("Arial", 18, "bold")).pack(pady=30)

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="📦 Module 1: Inventory & Labeling", width=30,
                  command=lambda: controller.show_frame("Module1Page")).pack(pady=10)

        tk.Button(btn_frame, text="📃 Module 2: Packing List", width=30,
                  command=lambda: controller.show_frame("Module2Page")).pack(pady=10)

        tk.Button(btn_frame, text="🛠️ Module 3: Assembly Validation", width=30,
                  command=lambda: controller.show_frame("Module3Page")).pack(pady=10)

        tk.Button(self, text="Exit", width=15, command=controller.quit).pack(pady=30)
