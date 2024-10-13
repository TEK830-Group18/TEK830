from View.time_slider import TimeSlider
from View.AppFrame import AppFrame
from View.clock_widget import ClockWidget
from View.AptLayout import AptLayout as Apt
from model.model import Model
from model.scheduler import RandomScheduler
import threading

class Application:
    def __init__(self):
        self.model = Model("tools/mock_user_data.json", RandomScheduler())
        self.app = AppFrame()
        self.setup_ui()

    def setup_ui(self):
        # Slider and clock widget
        slider = TimeSlider(self.app)
        clock_widget = ClockWidget(self.app, slider)
        slider.add_observer(clock_widget)
        clock_widget.start_timer()
        
        # Schedule
        schedule = self.model.schedule

        # Apt layout
        apt = Apt(self.app, slider, schedule)
        slider.add_observer(apt)
        
        # Main loop
        self.app.mainloop()

    def run_model(self):
        self.model.mainloop()


if __name__ == "__main__":
    application = Application()

    model_thread: threading.Thread = threading.Thread(application.run_model())
    model_thread.start()