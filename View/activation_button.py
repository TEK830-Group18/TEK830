import tkinter as tk

class ActivationButton(tk.Frame):
    def __init__(self, parent):
        super().__init__(master=parent)
        
        self._activated = False
        
        self._btn = tk.Button(self, text="Activate HÄRMAPA", bg="#2C2C2C", fg="white", font=("Inter", 16, "bold"), command=self.toggle_modes, width=40)
        self._btn.pack(pady=10)
        
        self.grid(row=4, column=1, columnspan=2)
        self.configure(bg="#0057AD")
        
    def toggle_modes(self):
        if(self._activated == False):
            self._btn.config(text="Deactivate HÄRMAPA")
            self._activated = True
        else:
            self._btn.config(text="Activate HÄRMAPA")
            self._activated = False