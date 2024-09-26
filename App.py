from View.AppFrame import AppFrame
from model.model import Model
import threading

def model():
    model = Model()
    model.mainloop()

def view():
    app = AppFrame()
    app.mainloop()

if __name__ == "__main__":
    modelThread: threading.Thread = threading.Thread(target=model())
    viewThread: threading.Thread = threading.Thread(target=view())
    