from View.AppFrame import AppFrame
from View.Lamp import Lamp

if __name__ == "__main__":
    app = AppFrame()
    lamp = Lamp(app)
    app.mainloop()
    