import tkinter as tk
import customtkinter as ctk

from View.activation_button import ActivationButton
from View.observer import Observer
from View.schedule_list_element import ScheduleListElement

class ScheduleList(ctk.CTkFrame, Observer):
    def __init__(self, master, controller : ActivationButton):
        super().__init__(master)
        self._width = 150
        self._height = 230
        self._controller : ActivationButton = controller
        
        self._deactivated_str = "Schedule without HÄRMAPA"
        self._activated_str = "Schedule with HÄRMAPA"
        
        self.configure(height=self._height, width=self._width, fg_color="#0057AD")
        
        # create variable for frame title
        self._title_lbl_text_var : tk.StringVar = tk.StringVar()
        self._title_lbl_text_var.set(self._deactivated_str)
        
        #Init title label for scrollable frame
        self._title_lbl_frame = ctk.CTkFrame(self, 
                                             width=self._width, 
                                             height=30,
                                             fg_color = "#ebe8e8",
                                             )
        self._title_lbl_frame.grid(row=0,column=0,sticky="nswe")
        
        # create title label
        self._title_lbl = ctk.CTkLabel(self._title_lbl_frame, textvariable = self._title_lbl_text_var, text_color="black", font=("Helvetica",12))
        self._title_lbl.pack()
        
        # Init scrollable frame, representing list
        self._list_frame = ctk.CTkScrollableFrame(self, height=200, 
                       width=self._width, 
                       fg_color = "white", 
                       scrollbar_fg_color = "#ebe8e8"
                       )
        self._list_frame.grid(row=1,column=0,sticky="nswe")
        
        self.grid(row=1, column=2, sticky="W",padx=20)

        self._build_list()

        
    #TODO This method should probably get all events and generate ScheduleListElements to put in the list.
    def _build_list(self):
        """
        Fills the frame with entries from a list of scheduled activites in order, from first to last.
        """
        
        #example code for filling the list
        nr_of_elements = 10
        for i in range(0, nr_of_elements):
            e = ScheduleListElement(self._list_frame, f"Room {i}, Event {i}")
            e.grid(row=i, column=0,pady=5)
        

    
    #TODO maybe this should trigger when schedule in model updates? This class could observe the model?
    def update_list(self):
        """Should update the list in the list box with new entries from a schedule
        """
        pass
    
    def notified_update(self):
        if self._controller.is_activated() == True:
            self._title_lbl_text_var.set(self._activated_str)
        else:
            self._title_lbl_text_var.set(self._deactivated_str)