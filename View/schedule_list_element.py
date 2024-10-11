import customtkinter as ctk


class ScheduleListElement(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        
        self.configure(width = 130, height=50 ,fg_color = "gray")