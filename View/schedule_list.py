import tkinter as tk

class ScheduleList(tk.Frame):
    def __init__(self, parent):
        super().__init__(master=parent)
        
        self._lbl = tk.Label(self,text="SCHEDULE")
        self._lbl.pack()
        
        self._list_box = tk.Listbox(self)
        self._list_box.pack()
        
        self._insert_schedule()
        
        self.grid(row=0, column=2, sticky="W",padx=20)
        
    #TODO Implement this
    def _insert_schedule(self):
        """
        Fills the listbox with entries from a list of scheduled activites.
        """
        pass
    
    #TODO
    def update_list(self):
        """Should update the list in the list box
        """
        pass