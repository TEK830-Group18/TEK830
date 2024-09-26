
class Model():
    def __init__(self, data) -> None:
        self.user_data = self.read_data(data)
        self.schedule = self.update_schedule(self.user_data)

    def mainloop(self):
        #self.user_data = self.update_data()
        self.schedule = self.update_schedule(self.user_data)

    def read_data(self, data):
        pass

    def update_schedule(self, data):
        pass