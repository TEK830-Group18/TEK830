import customtkinter as ctk

from View.schedule_list_element import ScheduleListElement

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
        
        self.elem = ScheduleListElement(self)
        self.elem.grid(row=0, column=0,pady=5)
        self.elem2 = ScheduleListElement(self)
        self.elem2.grid(row=1, column=0,pady=5)

        
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