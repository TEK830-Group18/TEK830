import tkinter as tk

class ScheduleList(tk.Frame):
    def __init__(self, parent):
        super().__init__(master=parent)
        
        self._list_box = tk.Listbox(self)
        self._list_box.pack()
        
        self.grid(row=0, column=2, sticky="W",padx=20)
        
        