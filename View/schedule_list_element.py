import customtkinter as ctk


class ScheduleListElement(ctk.CTkFrame):
    """A class that represents the elements that will populate the schedule list

    Args:
        ctk (CTkFrame)
    """
    def __init__(self, master, text : str):
        super().__init__(master)
        
        
        self._lbl = ctk.CTkLabel(self,
                                 text = text,
                                 width = 140,
                                 height=30,
                                 corner_radius=10,
                                 fg_color="#4c4c4c",
                                 font=("Helvetica", 12),
                                 )
        
        self._lbl.grid(row=0, column=0, padx=2)
 
        self.configure(fg_color = "white")
        