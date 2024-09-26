from View.AppFrame import AppFrame
from View.time_widget import TimeWidget
from model.model import Model
import threading

def model():
    model = Model()
    model.mainloop()

def view():
    app = AppFrame()
    time_widget = TimeWidget(app)
    time_widget.update_time()
    
    app.mainloop()

if __name__ == "__main__":
    model_thread: threading.Thread = threading.Thread(target=model())
    view_thread: threading.Thread = threading.Thread(target=view())
    