from datetime import datetime
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
from model.algorithm.nn_model.nn_alg import NNAlg
from model.timer import Timer

class Application:
    def __init__(self, model, start_time : datetime):
        self.model = model
        self.model.set_time(start_time)
        self.app = AppFrame()
        self.setup_ui(model)

    def setup_ui(self, model):
        # Demo model
        model = self.model
        # Slider and clock widget
        slider = TimeSlider(self.app, model)
        clock_widget = ClockWidget(self.app, self.model)
        
        # Actitvation button and schedule list
        activation_btn = ActivationButton(self.app, self.model)
        schedule_list = ScheduleList(self.app, activation_btn, self.model)
        activation_btn.add_observer(schedule_list)

        apt = Apt(self.app, self.model)
        
        model.add_observer(apt)
        #TODO add mqtt_light_service as observer of model
        
    def run_model(self):
        self.model.mainloop()
        
    def run_ui(self):
        self.app.mainloop()
    
        
if __name__ == "__main__":
    start_time = datetime.now().replace(hour=0,minute=0,second=0)
    timer = Timer()
    schduler = NNAlg()
    model = DemoModel(schduler, timer, start_time)
    app = Application(model, start_time)
    # view_thread: threading.Thread = threading.Thread(target=app.run_ui)
    model_thread: threading.Thread = threading.Thread(target=app.run_model)
    
    model_thread.daemon = True
    
    model_thread.start()
    app.run_ui()
    
    
