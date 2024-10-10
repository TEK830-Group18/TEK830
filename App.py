from View.time_slider import TimeSlider
from View.AppFrame import AppFrame
from View.clock_widget import ClockWidget
from View.AptLayout import AptLayout as Apt
from model.model import Model
from model.nn_model.nn_scheduler import NNScheduler
from model.scheduler import Scheduler, RandomScheduler
import threading


def model():
    model = Model("tools/mock_user_data.json", NNScheduler())
    model.mainloop()

def view():
    app = AppFrame()
    
    slider = TimeSlider(app)
    
    clock_widget = ClockWidget(app, slider)
    slider.add_observer(clock_widget)
    # Starts the clock
    clock_widget.start_timer()
    apt = Apt(app)
    
    # TODO probably need to override this mainloop method as it blocks any following code.
    app.mainloop()


if __name__ == "__main__":
    model_thread: threading.Thread = threading.Thread(target=model())
    view_thread: threading.Thread = threading.Thread(target=view())
