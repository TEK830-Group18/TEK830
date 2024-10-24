from datetime import datetime
import customtkinter as ctk


class ScheduleListElement(ctk.CTkFrame):
    """A class that represents the elements that will populate the schedule list

    Args:
        ctk (CTkFrame)
    """
    def __init__(self, master, lamp_name : str, time_stamp : datetime, action: str):
        super().__init__(master)
        
        self.text = f"{lamp_name.capitalize()} will turn {action.upper()} \n at {time_stamp.time()}"
        
        self._lbl = ctk.CTkLabel(self,
                                 text = self.text,
                                 width = 140,
                                 height=40,
                                 corner_radius=10,
                                 fg_color="#ebe8e8",
                                 font=("Helvetica", 12),
                                 text_color="black"
                                 )
        
        self._lbl.grid(row=0, column=0, padx=2)
 
        self.configure(fg_color = "white")
        