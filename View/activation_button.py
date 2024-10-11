import tkinter as tk
import customtkinter as ctk

class ActivationButton(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent)
        
        self._activated = False
        
        self._btn = ctk.CTkButton(self,
                                  text="Activate HÄRMAPA", 
                                  fg_color="#2C2C2C", 
                                  text_color="white", 
                                  font=("Inter", 16, "bold"), 
                                  command=self.toggle_modes, 
                                  width=300, 
                                  height=40,
                                  )
        self._btn.pack(pady=10)
        
        self.grid(row=4, column=1, columnspan=2)
        self.configure(fg_color="#0057AD")
        
    def toggle_modes(self):
        if(self._activated == False):
            self._btn.configure(text="Deactivate HÄRMAPA")
            self._activated = True
        else:
            self._btn.configure(text="Activate HÄRMAPA")
            self._activated = False