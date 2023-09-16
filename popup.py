import customtkinter 

class PickOthers(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x300")

        self.label = customtkinter.CTkLabel(self, text="PickUpOthersWindow")
        self.label.pack(padx=20, pady=20)
        


def PickUpOthers():
    toplevel_window = None
    if toplevel_window is None or not toplevel_window.winfo_exists():
        toplevel_window = PickOthers()
    else:
        toplevel_window.focus()  # if window exists focus it




class GetPicked(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x300")

        self.label = customtkinter.CTkLabel(self, text="GetPickedUpWindow")
        self.label.pack(padx=20, pady=20)

def GetPickedUp():
    toplevel_window = None
    if toplevel_window is None or not toplevel_window.winfo_exists():
        toplevel_window = GetPicked()  # create window if its None or destroyed
    else:
        toplevel_window.focus()  # if window exists focus it










'''
class App(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("500x400")

        self.button_1 = customtkinter.CTkButton(self, text="open toplevel", command=self.open_toplevel)
        self.button_1.pack(side="top", padx=20, pady=20)

        self.toplevel_window = None
'''




'''
app = App()
app.mainloop()
'''