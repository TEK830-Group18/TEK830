from View.AppFrame import AppFrame
from View.AptLayout import AptLayout as Apt

if __name__ == "__main__":
    app = AppFrame()
    apt = Apt(app)
    app.mainloop()
