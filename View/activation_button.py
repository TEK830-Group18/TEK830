import tkinter as tk
import customtkinter as ctk

from model.observable import Observable
from model.observer import Observer

class ActivationButton(ctk.CTkFrame, Observable):
    def __init__(self, parent):
        super().__init__(master=parent)
        
        self._obeservers = []
        
        self._activated = False
        
        self._btn = ctk.CTkButton(self,
                                  text="Activate HÄRMAPA", 
                                  fg_color="#2C2C2C", 
                                  text_color="white", 
                                  font=("Inter", 16, "bold"), 
                                  command=self.toggle_modes, 
                                  width=300, 
                                  height=40,
                                  hover_color="#757575"
                                  )
        self._btn.pack(pady=10)
        
        self.grid(row=5, column=1, columnspan=2)
        self.configure(fg_color="#0057AD")
        
    def toggle_modes(self):
        """Method that triggers when button is pressed. Switches between HÄRMAPA schedule and regluar schedule
        """
        if(self._activated == False):
            self._btn.configure(text="Deactivate HÄRMAPA")
            self._activated = True
        else:
            self._btn.configure(text="Activate HÄRMAPA")
            self._activated = False
        self.notify_observers()
            
    def is_activated(self) -> bool:
        return self._activated
    
    def add_observer(self, observer: Observer):
        self._obeservers.append(observer)
        
    def remove_observer(self, observer: Observer) -> None:
        self._obeservers.remove(observer)
        
    def notify_observers(self) -> None:
        for ob in self._obeservers:
            ob.notified_update()