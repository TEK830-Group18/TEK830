from View.activation_button import ActivationButton
from View.schedule_list import ScheduleList
from View.time_slider import TimeSlider
from View.AppFrame import AppFrame
from View.clock_widget import ClockWidget
from View.AptLayout import AptLayout as Apt
from model.model import Model
from model.algorithm.random_malg import RandomMAlg
import threading


def model():
    model = Model("tools/mock_user_data.json", RandomMAlg())
    model.mainloop()

def view():
    app = AppFrame()
    
    slider = TimeSlider(app)
    
    clock_widget = ClockWidget(app, slider)
    slider.add_observer(clock_widget)
    # Starts the clock
    clock_widget.start_timer()
    apt = Apt(app)
    activation_btn = ActivationButton(app)
    schedule_list = ScheduleList(app, activation_btn)
    activation_btn.add_observer(schedule_list)
    
    # TODO probably need to override this mainloop method as it blocks any following code.
    app.mainloop()


if __name__ == "__main__":
    model_thread: threading.Thread = threading.Thread(target=model())
    view_thread: threading.Thread = threading.Thread(target=view())
