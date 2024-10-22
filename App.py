from View.activation_button import ActivationButton
from View.schedule_list import ScheduleList
from View.time_slider import TimeSlider
from View.AppFrame import AppFrame
from View.clock_widget import ClockWidget
from View.AptLayout import AptLayout as Apt
from model.algorithm.motn_malg import MoreOftenThanNotMAlg
from model.model import Model
from model.algorithm.random_malg import RandomMAlg
from model.algorithm.abstract_mimicking_algorithm import Schedule
from model.demo_model import DemoModel
import threading

from model.timer import Timer

class Application:
    def __init__(self):
        self.model = DemoModel(MoreOftenThanNotMAlg(), Timer())
        self.app = AppFrame()
        self.setup_ui()

    def setup_ui(self):
        # Demo model
        model = self.model
        # Slider and clock widget
        slider = TimeSlider(self.app, model)
        clock_widget = ClockWidget(self.app, model)
        
        # Actitvation button and schedule list
        activation_btn = ActivationButton(self.app)
        schedule_list = ScheduleList(self.app, activation_btn)
        activation_btn.add_observer(schedule_list)

        apt = Apt(self.app, model)
        
        model.add_observer(apt)
        
    def run_model(self):
        self.model.mainloop()
        
    def run_ui(self):
        self.app.mainloop()
    
        
if __name__ == "__main__":
    app = Application()
    # view_thread: threading.Thread = threading.Thread(target=app.run_ui)
    model_thread: threading.Thread = threading.Thread(target=app.run_model)
    
    model_thread.daemon = True
    
    model_thread.start()
    app.run_ui()
    # view_thread.start()
    
    
