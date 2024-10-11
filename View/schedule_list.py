import customtkinter as ctk

class ScheduleList(ctk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        self._width = 150
        self._height = 230
        super().__init__(master, **kwargs)
        
        self.configure(height=self._height, 
                       width=self._width, 
                       fg_color = "white", 
                       label_text = "SCHEDULE", 
                       label_font = ("Helvetica",16), 
                       label_text_color = "black",
                       label_fg_color = "#D3D3D3")
        
        self.grid(row=0, column=2, sticky="W",padx=20)

    
    
    
    # def __init__(self, parent):
    #     super().__init__(master=parent)
        
    #     self._lbl = tk.Label(self,text="SCHEDULE", font=("Helvetica",10,"bold"))
    #     self._lbl.pack()
        
    #     self._list_box = tk.Listbox(self, height=15)
    #     self._list_box.pack()
        
    #     self._insert_schedule()
        
    #     self.grid(row=0, column=2, sticky="W",padx=20)
        
    #TODO Implement this
    def _insert_schedule(self):
        """
        Fills the listbox with entries from a list of scheduled activites.
        """
        pass
    
    #TODO
    def update_list(self):
        """Should update the list in the list box with entries from a schedule
        """
        pass