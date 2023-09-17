import customtkinter
import requests

class DriverPopup(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x300")    
        self.passenger_refreshbtn = customtkinter.CTkButton(master=self, text='Refresh', command=self.FindPassenger)
        self.passenger_refreshbtn.grid(row=1, column=0, sticky='nsew')     

        self.passenger_list = customtkinter.CTkLabel(master = self, text="No one at the momenent")
        self.passenger_list.grid(row=0, column=0, sticky='nsew', wraptext=100)
        
        self.passengers = requests.get(f"http://surveyer.pythonanywhere.com/get_passengers")  
        if self.passengers.status_code == 200:
            client_info = self.passengers.json()
            print(client_info)
            self.passenger_list.configure(text=self.passengers.content)
        
    def FindPassenger(self):
        self.passengers = requests.get(f"http://surveyer.pythonanywhere.com/get_passengers")  
        if self.passengers.status_code == 200:
            client_info = self.passengers.json()
            print(client_info)
        else:
            print(f"Failed to get passenger information. Status code: {self.passengers.status_code}")
            print("Press the refresh button: ")
        
        
        #self.all_passengers = [self.all_passengers.append(passenger['name']) for passenger in self.passenger_list]
        #self.passenger_list.configure(text="\n".join(self.all_passengers))
        print(self.passengers)
        self.passenger_list.configure(text=self.passengers.content)

def DriverPanel():
    toplevel_window = None
    if toplevel_window is None or not toplevel_window.winfo_exists():
        toplevel_window = DriverPopup()
    else:
        toplevel_window.focus()  # if window exists focus it