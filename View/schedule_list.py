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

        self._build_list()

        
    #TODO This method should probably get all events and generate ScheduleListElements to put in the list.
    def _build_list(self):
        """
        Fills the frame with entries from a list of scheduled activites.
        """
        nr_of_elements = 10
        for i in range(0, nr_of_elements):
            e = ScheduleListElement(self, str(i))
            e.grid(row=i, column=0,pady=5)

    
    #TODO maybe this should trigger when schedule in model updates? This class could observe the model?
    def update_list(self):
        """Should update the list in the list box with entries from a schedule
        """
        pass