import customtkinter
import requests


class AcceptPassenger(customtkinter.CTkToplevel):
    def __init__(self,passenger_info, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.passenger_info = passenger_info
        self.geometry("500x200")
        self.title("Passenger Requests")
        self.columnconfigure(0,weight=1)
        self.rowconfigure(0,weight=1)


        self.passenger_requests_frame = customtkinter.CTkScrollableFrame(master=self,label_text="Incoming Passenger Request",)
        self.passenger_requests_frame.grid(row=0, column=0,sticky = "nsew")

        self.passenger_label = customtkinter.CTkLabel(master = self.passenger_requests_frame,text=f"Passenger Name: {self.passenger_info['passenger_name']}, Age: {self.passenger_info['passenger_age']}, Final Destination: {self.passenger_info.get('passenger_finaldest')}")
        self.passenger_label.grid(pady=(20, 0), padx=(20, 20), row=0, column=0,sticky = "ew")

        self.accept_button = customtkinter.CTkButton(master=self.passenger_requests_frame, text="Accept", command=self.accept_incoming_passenger)
        self.accept_button.grid(row=0, column=1,pady=(20, 0), padx=(20, 20),sticky = "ew")

        self.decline_button = customtkinter.CTkButton(master = self.passenger_requests_frame,text="Decline")
        self.decline_button.grid(row=0, column=3,pady=(20, 0), padx=(20, 20),sticky = "ew")

    def accept_incoming_passenger(self):
        self.accepted_passenger_info = {
            'passenger_name': self.passenger_info['passenger_name'],
            'passengers_age': self.passenger_info['passenger_age'],
            'driver_name': self.passenger_info['driver_name'],
            'driver_age' : self.passenger_info['driver_age'],
            'driver_numplate': self.passenger_info['driver_numplate']
        }
        self.accepted_passengers = requests.post(f"http://surveyer.pythonanywhere.com/passenger_accepted",json = self.accepted_passenger_info)
        print(self.accepted_passengers.content)
    
    def decline_incoming_passenger(self):
        return
        


def accept_passenger(passenger_info):
    toplevel_window = None
    if toplevel_window is None or not toplevel_window.winfo_exists():
        toplevel_window = AcceptPassenger(passenger_info)
        
    else:
        toplevel_window.focus()  # if window exists focus it
