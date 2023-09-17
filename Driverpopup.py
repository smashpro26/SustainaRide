import customtkinter
import requests

class DriverPopup(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("400x300")    
        self.passenger_refreshbtn = customtkinter.CTkButton(master=self, text='Refresh', command=self.FindPassenger)
        self.passenger_refreshbtn.grid(row=1, column=0, sticky='nsew')     


        self.passengerlist_scrollable = customtkinter.CTkScrollableFrame(master=self, label_text='Passenger_list')
        self.passengerlist_scrollable.grid(row=0, column=0, sticky='nsew')
        self.columnconfigure(0, weight=1)


        self.passenger_list = customtkinter.CTkLabel(master = self, text="No one at the momenent",wraplength=380)
        self.passenger_list.grid(row=0, column=0, sticky='nsew')
        
        self.FindPassenger()
        
    def FindPassenger(self):
        self.passengers = {}
        self.counter = 0
        self.passengers = requests.get(f"http://surveyer.pythonanywhere.com/get_passengers")  
        if self.passengers.status_code == 200:
            self.client_info = self.passengers.json()
            print(self.client_info)
            for passenger in self.client_info:
                self.name = passenger.get('name')
                self.age = str(passenger.get('age'))
                print(self.name + " " + self.age )
                driver = customtkinter.CTkLabel(master=self.passengerlist_scrollable,text="Name: " + self.name + " Age: " + self.age)
                driver.grid(row = self.counter, column = 0,pady=(20, 0), padx=(20, 20), sticky='nsew')
                self.counter += 1
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