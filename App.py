from View.appFrame import appFrame
from model.model import Model
import threading

def model():
    model = Model("data")
    model.mainloop()

def view():
    app = appFrame()
    app.mainloop()

if __name__ == "__main__":
    model_thread: threading.Thread = threading.Thread(target=model())
    view_thread: threading.Thread = threading.Thread(target=view())
    