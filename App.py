from View.AppFrame import AppFrame
from View.time_widget import TimeWidget

if __name__ == "__main__":
    app = AppFrame()
    time_widget = TimeWidget(app)
    time_widget.update_time()
    
    app.mainloop()
    