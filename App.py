from View.activation_button import ActivationButton
from View.schedule_list import ScheduleList
from View.time_slider import TimeSlider
from View.AppFrame import AppFrame
from View.clock_widget import ClockWidget
from View.AptLayout import AptLayout as Apt
from model.model import Model
from model.algorithm.random_malg import RandomMAlg
from model.algorithm.abstract_mimicking_algorithm import Schedule
from model.AptModel import AptModel
from controller.AptController import AptController
import threading

class Application:
    def __init__(self):
        self.model = Model("tools/mock_user_data.json", Schedule)
        self.app = AppFrame()
        self.setup_ui()

    def setup_ui(self):
        # Slider and clock widget
        slider = TimeSlider(self.app)
        clock_widget = ClockWidget(self.app, slider)
        slider.add_observer(clock_widget)
        clock_widget.start_timer()
        
        # Actitvation button and schedule list
        activation_btn = ActivationButton(self.app)
        schedule_list = ScheduleList(self.app, activation_btn)
        activation_btn.add_observer(schedule_list)

        # Apt layout
        model = AptModel(self.model.schedule)
        controller = AptController(model, slider)
        apt = Apt(self.app, controller, model)
        slider.add_observer(apt)

        self.app.mainloop()

    def run_model(self):
        self.model.mainloop()
        

if __name__ == "__main__":
    application = Application()

    model_thread: threading.Thread = threading.Thread(application.run_model())
    model_thread.start()
