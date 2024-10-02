import time
from View.AppFrame import AppFrame
from View.time_widget import TimeWidget
from View.AptLayout import AptLayout as Apt
from model.model import Model
import threading

def model():
    model = Model("tools/mock_user_data.json")
    model.mainloop()

def view():
    app = AppFrame()
    time_widget = TimeWidget(app, time.strftime('%H:%M:%S'))
    # Starts the clock
    time_widget.start_timer()
    apt = Apt(app)
    # TODO probably need to override this mainloop method as it blocks any following code.
    app.mainloop()


if __name__ == "__main__":
    model_thread: threading.Thread = threading.Thread(target=model())
    view_thread: threading.Thread = threading.Thread(target=view())
